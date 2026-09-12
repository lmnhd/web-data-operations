"use strict";

let currentRunData = null;

document.addEventListener("DOMContentLoaded", async () => {
  await loadCodeExcerpt();

  document.getElementById("rules-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    await runEngine();
  });

  document.getElementById("preset-default").addEventListener("click", async () => {
    document.getElementById("rule_pothole").value = 5;
    document.getElementById("rule_streetlight").value = 3;
    document.getElementById("rule_tree").value = 10;
    document.getElementById("rule_garbage").value = 2;
    await runEngine();
  });

  document.getElementById("preset-strict").addEventListener("click", async () => {
    document.getElementById("rule_pothole").value = 3;
    document.getElementById("rule_streetlight").value = 2;
    document.getElementById("rule_tree").value = 5;
    document.getElementById("rule_garbage").value = 1;
    await runEngine();
  });

  document.getElementById("download-json").addEventListener("click", () => {
    if (!currentRunData) return;
    downloadFile(JSON.stringify(currentRunData, null, 2), "sla_evaluation_run.json", "application/json");
  });

  document.getElementById("download-csv").addEventListener("click", () => {
    if (!currentRunData || !currentRunData.csv) return;
    downloadFile(currentRunData.csv, "sla_evaluation_queue.csv", "text/csv");
  });

  // Automatically execute run on initial load
  await runEngine();
});

async function loadCodeExcerpt() {
  try {
    const res = await fetch("/api/code");
    if (res.ok) {
      const data = await res.json();
      document.getElementById("code").textContent = data.excerpt || "";
    }
  } catch (err) {
    console.error("Failed to load code excerpt", err);
  }
}

async function runEngine() {
  const btn = document.getElementById("run");
  const errorEl = document.getElementById("error");
  const runlineEl = document.getElementById("runline");
  errorEl.hidden = true;
  btn.disabled = true;

  const rules = {
    "Pothole Repair": parseInt(document.getElementById("rule_pothole").value, 10),
    "Streetlight Maintenance": parseInt(document.getElementById("rule_streetlight").value, 10),
    "Tree Trimming": parseInt(document.getElementById("rule_tree").value, 10),
    "Garbage Collection": parseInt(document.getElementById("rule_garbage").value, 10),
  };

  try {
    const res = await fetch("/api/run", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ rules }),
    });

    if (!res.ok) {
      const errData = await res.json();
      throw new Error(errData.error || "Execution failed");
    }

    const data = await res.json();
    currentRunData = data;
    renderResults(data);

    runlineEl.textContent = `Executed python sla_engine.evaluate_dataset in ${data.elapsed_ms} ms. Reference now: ${data.reference_now}`;
  } catch (err) {
    errorEl.textContent = err.message;
    errorEl.hidden = false;
  } finally {
    btn.disabled = false;
  }
}

function renderResults(data) {
  document.getElementById("result").hidden = false;
  document.getElementById("decision-title").textContent = `${data.total_records} Records Evaluated`;

  const pill = document.getElementById("decision-pill");
  pill.textContent = `${data.status_summary.SLA_BREACHED} Breached`;
  pill.className = "pill pill-SLA_BREACHED";

  // Summary counts
  const summaryEl = document.getElementById("summary-cards");
  summaryEl.innerHTML = `
    <div class="count-card">
      <strong style="color:var(--green)">${data.status_summary.COMPLIANT || 0}</strong>
      <span>COMPLIANT</span>
    </div>
    <div class="count-card">
      <strong style="color:var(--orange)">${data.status_summary.AT_RISK || 0}</strong>
      <span>AT RISK</span>
    </div>
    <div class="count-card">
      <strong style="color:var(--red)">${data.status_summary.SLA_BREACHED || 0}</strong>
      <span>SLA BREACHED</span>
    </div>
    <div class="count-card">
      <strong style="color:var(--blue)">${data.status_summary.INCOMPLETE_DATA_REVIEW || 0}</strong>
      <span>DATA REVIEW</span>
    </div>
  `;

  // Ward Table
  const wardContainer = document.getElementById("ward-table-container");
  let wardHtml = `
    <table>
      <thead>
        <tr>
          <th>Ward Name</th>
          <th>Total Requests</th>
          <th>Compliant</th>
          <th>At Risk</th>
          <th>Breached</th>
          <th>Compliance Rate</th>
        </tr>
      </thead>
      <tbody>
  `;

  const wardEntries = Object.entries(data.ward_analytics || {});
  wardEntries.sort((a, b) => a[1].compliance_rate_pct - b[1].compliance_rate_pct); // Lowest compliance first

  for (const [wardName, stats] of wardEntries) {
    const isBottleneck = stats.compliance_rate_pct < 50.0;
    const rowClass = isBottleneck ? "bottleneck-highlight" : "";
    wardHtml += `
      <tr class="${rowClass}">
        <td><strong>${escapeHtml(wardName)}</strong>${isBottleneck ? " (Bottleneck)" : ""}</td>
        <td>${stats.total_requests}</td>
        <td>${stats.compliant}</td>
        <td>${stats.at_risk}</td>
        <td>${stats.breached}</td>
        <td><strong>${stats.compliance_rate_pct}%</strong></td>
      </tr>
    `;
  }
  wardHtml += `</tbody></table>`;
  wardContainer.innerHTML = wardHtml;

  // Records list
  const listEl = document.getElementById("records-list");
  listEl.innerHTML = "";

  for (const rec of data.evaluated_records) {
    const card = document.createElement("div");
    card.className = "record-card";

    const statusPillClass = `pill-${rec.sla_status}`;
    card.innerHTML = `
      <div>
        <h3>${escapeHtml(rec.service_request_id)} - ${escapeHtml(rec.service_name)}</h3>
        <div class="record-meta">
          <span><strong>Ward:</strong> ${escapeHtml(rec.ward)}</span>
          <span><strong>Created:</strong> ${escapeHtml(rec.created_date || "N/A")}</span>
          <span><strong>Target SLA:</strong> ${rec.sla_target_days} days (${escapeHtml(rec.target_date || "N/A")})</span>
          <span><strong>Closed:</strong> ${escapeHtml(rec.closed_date || "Still Open")}</span>
          <span><strong>Duration:</strong> ${rec.duration_days !== null ? rec.duration_days + " days" : "N/A"}</span>
          <span><strong>Margin:</strong> ${rec.margin_days !== null ? rec.margin_days + " days" : "N/A"}</span>
        </div>
        <div class="record-reason">
          Reason Code: <code>${escapeHtml(rec.reason_code)}</code> | Lifecycle: <code>${escapeHtml(rec.lifecycle_state)}</code>
        </div>
      </div>
      <div>
        <span class="pill ${statusPillClass}">${escapeHtml(rec.sla_status)}</span>
      </div>
    `;
    listEl.appendChild(card);
  }
}

function escapeHtml(str) {
  if (str === null || str === undefined) return "";
  return String(str)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

function downloadFile(content, fileName, mimeType) {
  const blob = new Blob([content], { type: mimeType });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = fileName;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
}
