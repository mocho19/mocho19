# Verification record

Prepared on 22 November 2026 by Codex, Python 3.13.12 on macOS.

| Check | Observed result |
| --- | --- |
| Full unittest suite | 69 tests passed |
| Shared registry and CLI | All seven editable example workflows returned labeled JSON |
| Browser execution | All seven examples completed through the workbench in offline mode |
| Knowledge retrieval | Offboarding policy ranked first; unrelated-topic query abstains |
| Customer support | Delayed-order escalation remains an unsent draft; scoped reads enforced |
| Invoice calculation | Example subtotal 380.00; totals validated; mismatches flagged |
| Security correlation | Five events produced two synthetic signals; no containment executed |
| Contract timeline | Example notice deadline 2026-12-30, 38 days after the reference date |
| Proposal workflow | Requirements, architecture and review emitted; price arithmetic uses input assumptions |
| Meeting extraction | Three tasks, one decision and one blocker; CSV prepared without external writes |
| Foundry runtime contracts | Mocked schema output, tool call IDs, invalid tools, loop limits and incomplete responses tested |
| Live SDK installation/inference | Not tested |
| Hosted cloud deployment | Not performed |
| Business impact or client acceptance | Not measured |

The tests include source/quote rejection, cross-record access denial, malformed
input, arithmetic mismatches, duplicate records, missing evidence, dates and draft
state behavior. Model-quality or cloud-availability claims cannot be derived from
offline tests. Add dated live observations only after performing them.

Reproduce: `python3 -m unittest discover -s tests -v` from the portfolio root.
