# Security and Truthfulness Audit

**Reviewed:** 2026-08-10
**Classification:** static source inventory; not production-ready

## Decision

The former command-center presentation was not an operational security product. It contained simulated alerts and randomized operational metrics, while another page described source-derived values as real or live. Those surfaces were removed rather than retained as a demo.

The repository is repositioned as a small, reusable portfolio-inventory component. It reports only static observations with collection methods, Git revisions, dirty-worktree state, and explicit limitations.

## Resolved findings

- Removed randomized scans, alerts, uptime, detection rates, and blocked-threat counts.
- Removed historical baseline performance values without adequate provenance.
- Replaced `live` source labels with `repository_source_snapshot`.
- Renamed the displayed test metric to test function declarations; the collector does not claim the tests passed.
- Removed unsupported ATT&CK coverage and operational health claims.
- Removed the external Three.js runtime dependency and legacy simulated dashboard.
- Added tests that reject baseline and effectiveness fields.

## Residual risks

- Static analysis can miss dynamically generated tests and non-Python suites.
- A repository's source may contain incorrect or misleading content; this collector does not validate behavior.
- A dirty sibling worktree may not match its recorded commit. The condition is surfaced, not resolved automatically.
- The local HTTP serving command is not hardened for network exposure.
- There is no authentication because there is no deployed service. Adding network deployment would require a new threat model and access controls.

## Readiness

The repository is **not production-ready** and must not be represented as security monitoring, prevention, or benchmark evidence. Its defensible use is a local, point-in-time source inventory.
