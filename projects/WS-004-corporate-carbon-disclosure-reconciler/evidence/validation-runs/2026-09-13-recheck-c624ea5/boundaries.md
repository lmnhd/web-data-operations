# WS-004 independent repair recheck - source, privacy, and release boundaries

The official source archive and factor workbook remain only under ignored `tmp/ws004_source/` and are absent from tracked project/history paths. No full filing, ZIP, XLSX, extracted HTML/XML body, credential, arbitrary URL/file access, or live write path is exposed by the project.

Independent source verification:

- archive: 54,357,249 bytes; SHA-256 `cd8733ad05cbb3eeaca514f6b2044d16c6b6098d72535a90354d1863bd5077e5`;
- factor workbook: 505,634 bytes; SHA-256 `8bfdb45b81ec4a88e3bdf4584637330f62e6bd09ce1940e654c5d7b7f736de94`;
- selected entry 09904577: 697,457 bytes; SHA-256 `af67a7e7290d925386229997479a7835289fb79398cb5b588e4377b37ee0ecfd`;
- selected entry 12976528: 384,195 bytes; SHA-256 `532cfd04ed088021a847577ef6f56e74eb5dcbc4f82f300509860f7041d65d33`;
- selected entry 00376891: 572,888 bytes; SHA-256 `d1769b95779aebeeab88245b5ed24b2e3b83229c4305d00a112eba8cebab4b1d`.

The workbook front sheet independently shows year 2025, version 1, status Final, updated 2025-06-10. Rows 79, 83, and 3066 match the minimized natural-gas net/gross and UK-electricity factor records, including factor IDs, units, and values 0.2027, 0.18296, and 0.177 kg CO2e/kWh.

The minimized fixtures/outputs retain permitted company numbers and narrow public metrics but no company names, personal names, signatures, addresses, contact details, credentials, or full filing bodies. The Flask adapter accepts only bounded known-case operations, enforces a 4 KB JSON cap and same-origin POSTs, and offers no arbitrary source URL/path or server-side write operation. The category-conflict and malformed-digest repairs now enforce the source contract in both engine and API paths.

The validator identity `/root/ws004_independent_validator` differs from the plan's builder identity `/root`. The complete normalized hash map covers 31 project/shared artifacts under the protocol exclusions. No hosting, deployment, release, or publication action was performed or authorized. The executable gate is simulated against a copy of state set to `RELEASE_READY`; actual iteration state remains unchanged.
