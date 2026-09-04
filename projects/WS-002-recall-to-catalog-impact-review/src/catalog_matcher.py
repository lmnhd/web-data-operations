"""Deterministic recall-to-catalog matching for the WS-002 vertical proof."""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from typing import Any


TOKEN_RE = re.compile(r"[a-z0-9]+")
STRENGTH_RE = re.compile(r"\b(\d+(?:\.\d+)?)\s*(mcg|mg|ml|%)(?![a-z0-9])", re.IGNORECASE)
STOP_WORDS = {
    "and", "by", "capsule", "capsules", "company", "distributed", "for",
    "inc", "injection", "llc", "manufactured", "only", "pack", "packaged",
    "pharmaceuticals", "rx", "solution", "tablet", "tablets", "the", "usp",
}
ALLOWED_RECALL_FIELDS = {
    "recall_number", "event_id", "report_date", "recalling_firm",
    "product_description", "code_info", "product_type", "upc", "brand_name",
    "generic_name", "manufacturer_name", "product_ndc",
}


def canonical_identifier(value: str | None) -> str:
    digits = "".join(char for char in str(value or "") if char.isdigit())
    return digits.lstrip("0") or digits


def normalized_tokens(*values: Any) -> set[str]:
    tokens: set[str] = set()
    for value in values:
        items = value if isinstance(value, list) else [value]
        for item in items:
            for token in TOKEN_RE.findall(str(item or "").lower()):
                if len(token) > 1 and token not in STOP_WORDS:
                    tokens.add(token)
    return tokens


def token_overlap(left: set[str], right: set[str]) -> float:
    if not left or not right:
        return 0.0
    return len(left & right) / min(len(left), len(right))


def strengths(*values: Any) -> dict[str, set[str]]:
    found: dict[str, set[str]] = {}
    for value in values:
        items = value if isinstance(value, list) else [value]
        for item in items:
            for amount, unit in STRENGTH_RE.findall(str(item or "")):
                found.setdefault(unit.lower(), set()).add(amount.lower())
    return found


def fingerprint(record: dict[str, Any]) -> str:
    selected = {key: record.get(key) for key in sorted(ALLOWED_RECALL_FIELDS)}
    payload = json.dumps(selected, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class PairEvidence:
    recall_number: str
    score: int
    decision: str
    reasons: tuple[str, ...]

    def as_dict(self) -> dict[str, Any]:
        return {
            "recall_number": self.recall_number,
            "score": self.score,
            "decision": self.decision,
            "reasons": list(self.reasons),
        }


def compare_pair(catalog: dict[str, Any], recall: dict[str, Any]) -> PairEvidence:
    catalog_upc = canonical_identifier(catalog.get("upc"))
    catalog_ndc = canonical_identifier(catalog.get("ndc"))
    recall_upcs = {canonical_identifier(value) for value in recall.get("upc", [])}
    recall_ndcs = {canonical_identifier(value) for value in recall.get("product_ndc", [])}

    exact_upc = bool(catalog_upc and catalog_upc in recall_upcs)
    exact_ndc = bool(catalog_ndc and catalog_ndc in recall_ndcs)
    lot = str(catalog.get("lot_code") or "").lower().strip()
    exact_lot = bool(lot and lot in str(recall.get("code_info") or "").lower())

    catalog_product = normalized_tokens(catalog.get("product_name"))
    recall_product = normalized_tokens(
        recall.get("product_description"), recall.get("brand_name"), recall.get("generic_name")
    )
    product_similarity = token_overlap(catalog_product, recall_product)

    catalog_maker = normalized_tokens(catalog.get("manufacturer"))
    recall_maker = normalized_tokens(recall.get("recalling_firm"), recall.get("manufacturer_name"))
    maker_similarity = token_overlap(catalog_maker, recall_maker)

    catalog_strengths = strengths(catalog.get("product_name"))
    recall_strengths = strengths(recall.get("product_description"), recall.get("brand_name"))
    common_units = set(catalog_strengths) & set(recall_strengths)
    strength_match = any(
        catalog_strengths[unit] & recall_strengths[unit] for unit in common_units
    )
    strength_conflict = any(
        not catalog_strengths[unit] & recall_strengths[unit] for unit in common_units
    )

    score = 0
    reasons: list[str] = []
    if exact_upc:
        score += 70
        reasons.append("exact_upc")
    if exact_ndc:
        score += 50
        reasons.append("exact_ndc_family")
    if exact_lot:
        score += 35
        reasons.append("exact_lot_code")
    if maker_similarity >= 0.6:
        score += 15
        reasons.append("manufacturer_overlap")
    if product_similarity >= 0.35:
        score += 20
        reasons.append("strong_product_text_overlap")
    elif product_similarity >= 0.2:
        score += 10
        reasons.append("partial_product_text_overlap")
    if strength_match:
        score += 10
        reasons.append("strength_match")
    if strength_conflict:
        score -= 80
        reasons.append("strength_conflict")
        if exact_upc or exact_ndc:
            score = max(score, 50)

    if strength_conflict and (exact_upc or exact_ndc):
        decision = "review_needed"
    elif exact_lot and (exact_upc or exact_ndc):
        decision = "match"
    elif exact_upc and exact_ndc and product_similarity >= 0.2:
        decision = "match"
    elif exact_upc and product_similarity >= 0.35:
        decision = "match"
    elif exact_ndc and product_similarity >= 0.35 and maker_similarity >= 0.6:
        decision = "match"
    elif score >= 30 or (product_similarity >= 0.5 and strength_match):
        decision = "review_needed"
    else:
        decision = "no_match"

    return PairEvidence(
        recall_number=str(recall["recall_number"]),
        score=score,
        decision=decision,
        reasons=tuple(reasons),
    )


def match_catalog(
    catalog_rows: list[dict[str, Any]],
    recall_rows: list[dict[str, Any]],
    provenance: dict[str, str],
) -> list[dict[str, Any]]:
    recall_by_number = {str(row["recall_number"]): row for row in recall_rows}
    results: list[dict[str, Any]] = []

    for catalog in sorted(catalog_rows, key=lambda row: str(row["catalog_id"])):
        evidence = sorted(
            (compare_pair(catalog, recall) for recall in recall_rows),
            key=lambda item: (-item.score, item.recall_number),
        )
        viable = [item for item in evidence if item.decision != "no_match"]
        match_candidates = [item for item in viable if item.decision == "match"]
        best = evidence[0] if evidence else None
        runner_score = evidence[1].score if len(evidence) > 1 else -999

        if match_candidates and best and best.decision == "match" and best.score - runner_score >= 15:
            classification = "match"
            matched_number: str | None = best.recall_number
            candidates = [best.recall_number]
            reasons = list(best.reasons)
        elif viable:
            classification = "review_needed"
            matched_number = None
            candidates = [item.recall_number for item in viable]
            reasons = sorted({reason for item in viable for reason in item.reasons})
        else:
            classification = "no_match"
            matched_number = None
            candidates = []
            reasons = ["no_candidate_reached_review_threshold"]

        selected = recall_by_number.get(matched_number) if matched_number else None
        candidate_provenance = [
            {
                "recall_number": number,
                "source_url": provenance["source_url"],
                "retrieved_at": provenance["retrieved_at"],
                "content_fingerprint": fingerprint(recall_by_number[number]),
            }
            for number in candidates
        ]
        results.append({
            "catalog_id": catalog["catalog_id"],
            "classification": classification,
            "matched_recall_number": matched_number,
            "candidate_recall_numbers": candidates,
            "reasons": reasons,
            "top_score": best.score if best else 0,
            "source_url": provenance["source_url"] if candidates else None,
            "retrieved_at": provenance["retrieved_at"] if candidates else None,
            "content_fingerprint": fingerprint(selected) if selected else None,
            "candidate_provenance": candidate_provenance,
            "pair_evidence": [item.as_dict() for item in evidence[:3]],
        })

    return results


def evaluate(results: list[dict[str, Any]], expected: list[dict[str, Any]]) -> dict[str, Any]:
    expected_by_id = {row["catalog_id"]: row for row in expected}
    comparisons = []
    for result in results:
        label = expected_by_id[result["catalog_id"]]
        passed = (
            result["classification"] == label["classification"]
            and result["matched_recall_number"] == label.get("matched_recall_number")
        )
        comparisons.append({"catalog_id": result["catalog_id"], "passed": passed})
    passed_count = sum(item["passed"] for item in comparisons)
    return {
        "labels_total": len(comparisons),
        "labels_passed": passed_count,
        "labels_failed": len(comparisons) - passed_count,
        "exact_label_rate": passed_count / len(comparisons) if comparisons else None,
        "comparisons": comparisons,
    }
