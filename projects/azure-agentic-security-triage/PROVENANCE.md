# Provenance and contribution boundaries

Prepared for Sayeem Chowdhury on 22 November 2026 with Codex assistance.

Source: https://github.com/timothywarner-org/ai103

Inspected revision: `55aca6dca5dde232e277d7076082ca59bd30963c`.

The source identifies Tim Warner as author and carries an MIT license with
`Copyright (c) 2025 Tim Warner`. That notice and full permission text are retained
in `vendor/ai103/LICENSE`. Reuse is based on the license found at the inspected
revision; no external course videos, books or proprietary materials were copied.

| Local path | Origin | Changes |
| --- | --- | --- |
| `vendor/ai103/function_calling.py` | Upstream `lessons/10-build-agents-foundry/function_calling.py` | None; reference only, not imported or tested here |
| `vendor/ai103/LICENSE` | Upstream `LICENSE` | None |
| `agent.py`, `tests/`, `data/`, documentation and configuration | Newly prepared for this project with AI assistance | New code and prose; inspired by the upstream request/execute/continue teaching pattern |

The upstream reference uses Microsoft Agent Framework and `FoundryChatClient`.
The portfolio implementation deliberately exposes the orchestration boundary using
Python standard-library code and optional Azure OpenAI REST calls. It does not claim
to reproduce the course's full functionality or security posture. The source README
labels its repository educational and intentionally vulnerable; the reference file
is included for attribution and comparison, not as production-ready code.

The full upstream repository was not copied. This is a focused learning derivative
with an independently prepared security use case. Sayeem is the portfolio owner;
upstream authorship remains with Tim Warner. AI-generated additions should be
reviewed, understood and exercised before being represented as personal experience.
