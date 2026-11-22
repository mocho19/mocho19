# Validation record

Date: 22 November 2026. Runner: Codex in the local workspace, Python 3.13.12.
This records automated preparation checks, not a personal execution claim by Sayeem.

| Check | Result |
| --- | --- |
| `python3 -m unittest discover -s tests -v` | 15 tests passed |
| `python3 agent.py --alert ALERT-001` | Completed scripted read/propose/handoff; evidence E-101/E-102; zero actions |
| `python3 agent.py --alert ALERT-002` | Completed scripted read/propose/handoff; evidence E-201/E-202; zero actions |
| Azure request construction | Mocked HTTP/token test passed; no real credentials used |
| Live Azure inference | Not run |
| Infrastructure deployment | Not performed; not included in this demo |
| Vendored course reference | Preserved for comparison; not imported or executed |

Tests cover unknown tools, malformed/extra arguments, cross-alert access, missing
alerts, evidence-before-proposal, inappropriate actions, duplicate proposals,
round/tool budgets, truncated responses, handoffs without evidence and endpoint
validation. An injection fixture verifies that tool dispatch cannot execute an
unauthorized function; it does not measure model resistance to injected text.

To extend this record, run the live checklist in SETUP.md and record your actual
observations, model version, failures and limitations. Do not mark cloud checks as
passed based on the offline simulation or mocked transport.
