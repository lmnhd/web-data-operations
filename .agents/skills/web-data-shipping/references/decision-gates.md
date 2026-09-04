# Bounded decision gates

## Why this replaces the legacy gate

The first workflow treated provisional candidate-register suggestions as mandatory feature requirements, compared new concepts with rejected concepts as though they were released products, and used several reviewers instructed to refute when uncertain. This produced useful research but systematic rejection and repeated context growth.

## Concept decision record

For each candidate, record only:

1. target buyer and operational decision;
2. dated demand evidence and its confidence;
3. permitted source/access path;
4. central testable claim;
5. difference from released projects;
6. smallest vertical proof;
7. fatal blockers, repairable conditions, and limitations.

## Severity classification

### Fatal

A finding is fatal only when it prevents an honest bounded proof:

- prohibited access or required circumvention;
- no usable data source;
- no identifiable buyer outcome;
- no way to test the central claim;
- duplication of an already released project without material added value.

Reject the candidate and record a reconsideration condition.

### Repairable

The candidate may proceed after a scoped correction:

- metric definition is wrong but a valid denominator exists;
- the source lacks a numeric rate ceiling but a conservative, non-probing acquisition path exists;
- personal or restricted fields can be excluded through an ingest allowlist;
- buyer value needs a bounded qualification or delivery step;
- an optional capability belongs in a later project.

Apply one repair pass, then seek human approval.

### Limitation

The vertical proof can proceed if the Manifest discloses the condition:

- small benchmark sample;
- manual review required for ambiguous records;
- no production-scale or real-time claim;
- source fragility or incomplete field coverage;
- demand evidence is indirect and must be strengthened before marketing.

## Novelty test

Compare against `RELEASED` projects only. Rejected and unbuilt concepts are research history, not occupied portfolio territory.

A new project passes when it provides a materially different buyer outcome or demonstrates one new technical capability plus a meaningful difference in source, data-quality problem, monitoring behavior, delivery workflow, or proof method.

A candidate register may suggest useful features; it cannot silently become a mandatory checklist.

## Critic output

Use one consolidated critic response:

```json
{
  "decision": "proceed|repair|reject",
  "fatal": [],
  "repairable": [],
  "limitations": [],
  "required_vertical_proof": [],
  "claims_to_avoid": []
}
```

Uncertainty belongs under `limitations` unless it meets the fatal definition.
