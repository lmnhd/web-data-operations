# Independent export inspection

The validator executed the CLI into validator-owned paths. The generated default JSON/CSV and changed-input JSON/CSV are byte-identical to the committed evidence:

- default JSON SHA-256: `b66859a2171639e8027275580849ae8eaa0cfa4be428531177f0d2724895baa5`;
- default CSV SHA-256: `c4d4fcc284484e8947a9ed68ff1d26a4a1eb64877e339d88bc3910dd50f027a9`;
- changed JSON SHA-256: `8f6d013fc6d53adcb4d8665cb1e1316223821199e6f65806ea55185317d44408`;
- changed CSV SHA-256: `ac242308cf923bcc0a583a1c6fa1c231218dfb8d80b0d37d7ad8bef2b03b489f`.

The default files contain six cases and agree on 2 RECONCILED, 1 MISMATCH, and 3 REVIEW_REQUIRED. Decisions, reason codes, values, tolerance, locator, factor set/year, and input/source/factor/engine hashes agree. No company names, personal names, signatures, addresses, contacts, credentials, or full filing bodies were found.

The frozen check nevertheless fails: JSON identifies run `ws004-1984fbedb2ae05ca`, but CSV has no `runId` column. The exact CSV headers begin with `caseId` and contain the per-result trace fields only. Therefore the run ID cannot be compared across both formats as required by `check_exports`.
