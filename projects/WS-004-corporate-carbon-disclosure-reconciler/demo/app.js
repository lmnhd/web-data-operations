"use strict";

let currentRun = null;

document.addEventListener("DOMContentLoaded", async () => {
  const caseSelect = document.getElementById("case-select");
  const unitSelect = document.getElementById("unit-select");

  caseSelect.addEventListener("change", () => {
    const controlled = caseSelect.value === "CASE-02-CONTROLLED-MWH-RECONCILED";
    unitSelect.disabled = !controlled;
    if (!controlled) unitSelect.value = "MWh";
  });

  document.getElementById("review-form").addEventListener("submit", async (event) => {
    event.preventDefault();
    await runEngine();
  });

  document.getElementById("preset-default").addEventListener("click", async () => {
    caseSelect.value = "";
    unitSelect.value = "MWh";
    unitSelect.disabled = true;
    await runEngine();
  });

  document.getElementById("preset-unit-change").addEventListener("click", async () => {
    caseSelect.value = "CASE-02-CONTROLLED-MWH-RECONCILED";
    unitSelect.disabled = false;
    unitSelect.value = "kWh";
    await runEngine();
  });

  document.getElementById("download-json").addEventListener("click", () => {
    if (!currentRun) return;
    const copy = { ...currentRun };
    delete copy.csv;
    downloadFile(JSON.stringify(copy, null, 2), "carbon_reconciliation_run.json", "application/json");
  });

  document.getElementById("download-csv").addEventListener("click", () => {
    if (!currentRun) return;
    downloadFile(currentRun.csv, "carbon_reconciliation_results.csv", "text/csv");
  });

  await loadCodeExcerpt();
  await runEngine();
});

async function loadCodeExcerpt() {
  try {
    const response = await fetch("/api/code");
    if (!response.ok) return;
    const data = await response.json();
    document.getElementById("code").textContent = data.excerpt || "";
  } catch (error) {
    console.error("Code excerpt unavailable", error);
  }
}

async function runEngine() {
  const button = document.getElementById("run");
  const errorElement = document.getElementById("error");
  const caseId = document.getElementById("case-select").value || null;
  const activityUnit = caseId ? document.getElementById("unit-select").value : null;
  button.disabled = true;
  errorElement.hidden = true;

  try {
    const response = await fetch("/api/run", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ caseId, activityUnit }),
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || "Evidence run failed.");
    currentRun = data;
    renderRun(data);
  } catch (error) {
    errorElement.textContent = error.message;
    errorElement.hidden = false;
  } finally {
    button.disabled = false;
  }
}

function renderRun(data) {
  const summary = data.summary;
  const isBenchmark = summary.totalCases === 6;
  document.getElementById("result").hidden = false;
  document.getElementById("decision-title").textContent = isBenchmark
    ? "Six evidence cases evaluated"
    : "Controlled unit case evaluated";

  const pill = document.getElementById("decision-pill");
  if (isBenchmark) {
    pill.textContent = "Oracle reproduced";
    pill.className = "pill reconciled";
  } else {
    pill.textContent = data.results[0].decision.replaceAll("_", " ");
    pill.className = `pill ${decisionClass(data.results[0].decision)}`;
  }

  document.getElementById("runline").textContent = `Run ${data.runId} / Python engine ${shortHash(data.engineSha256)} / ${summary.totalCases} case${summary.totalCases === 1 ? "" : "s"}`;
  document.getElementById("summary-cards").innerHTML = `
    ${summaryCard(summary.RECONCILED, "RECONCILED", "reconciled")}
    ${summaryCard(summary.MISMATCH, "MISMATCH", "mismatch")}
    ${summaryCard(summary.REVIEW_REQUIRED, "REVIEW REQUIRED", "review")}
  `;

  document.getElementById("results-list").innerHTML = data.results.map(resultCard).join("");
}

function summaryCard(value, label, className) {
  return `<div class="count-card ${className}"><strong>${value}</strong><span>${label}</span></div>`;
}

function resultCard(result) {
  const computed = result.computedEmissionsTco2e === null
    ? "Not computed"
    : `${formatNumber(result.computedEmissionsTco2e)} tCO2e`;
  const disclosed = result.disclosedEmissionsValue === null
    ? "Not supplied"
    : `${formatNumber(result.disclosedEmissionsValue)} ${escapeHtml(result.disclosedEmissionsUnit)}`;
  const activity = result.activityValue === null
    ? "Not extractable"
    : `${formatNumber(result.activityValue)} ${escapeHtml(result.activityUnit)}`;
  return `
    <article class="result-card">
      <div class="result-main">
        <div class="result-title">
          <span class="pill ${decisionClass(result.decision)}">${escapeHtml(result.decision.replaceAll("_", " "))}</span>
          <div>
            <h3>${escapeHtml(friendlyCase(result.caseId))}</h3>
            <p>${escapeHtml(result.fixtureKind.replaceAll("_", " "))}</p>
          </div>
        </div>
        <div class="calculation-grid">
          <div><span>ACTIVITY</span><strong>${activity}</strong></div>
          <div><span>DISCLOSED</span><strong>${disclosed}</strong></div>
          <div><span>RECOMPUTED</span><strong>${computed}</strong></div>
          <div><span>REASON</span><strong>${escapeHtml(result.reasonCode.replaceAll("_", " "))}</strong></div>
        </div>
      </div>
      <div class="trace">
        <span>${escapeHtml(result.sourceId)}</span>
        <span title="${escapeHtml(result.sourceLocator)}">${escapeHtml(result.sourceLocator)}</span>
        <code>${shortHash(result.sourceSha256)}</code>
      </div>
    </article>
  `;
}

function decisionClass(decision) {
  return {
    RECONCILED: "reconciled",
    MISMATCH: "mismatch",
    REVIEW_REQUIRED: "review",
  }[decision] || "neutral";
}

function friendlyCase(caseId) {
  return caseId
    .replace(/^CASE-0?/, "Case ")
    .replaceAll("-", " ")
    .toLowerCase()
    .replace(/\b\w/g, (character) => character.toUpperCase());
}

function formatNumber(value) {
  const parsed = Number(value);
  return Number.isFinite(parsed)
    ? parsed.toLocaleString(undefined, { maximumFractionDigits: 6 })
    : escapeHtml(value);
}

function shortHash(value) {
  return value ? `${value.slice(0, 10)}...${value.slice(-6)}` : "not available";
}

function escapeHtml(value) {
  return String(value ?? "")
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}

function downloadFile(content, fileName, mimeType) {
  const blob = new Blob([content], { type: mimeType });
  const url = URL.createObjectURL(blob);
  const anchor = document.createElement("a");
  anchor.href = url;
  anchor.download = fileName;
  document.body.appendChild(anchor);
  anchor.click();
  anchor.remove();
  URL.revokeObjectURL(url);
}
