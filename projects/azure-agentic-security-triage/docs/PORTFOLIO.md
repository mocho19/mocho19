# Portfolio walkthrough for Sayeem Chowdhury

## Current framing

"An AI-assisted Azure security-triage learning project inspired by Tim Warner's
AI-103 examples. It demonstrates a bounded tool-calling loop, application-enforced
tool validation and a proposal-only analyst handoff using synthetic alerts."

Describe the offline mode as simulation. Only describe Azure execution after
performing and recording a real run. This project does not establish course
completion, certification or production operations experience.

## Five-minute demonstration

1. Acknowledge the upstream reference and explain the new security scenario.
2. Run both offline fixtures and point out the tool trace and approval-required proposal.
3. Show tests denying a cross-alert request, malformed arguments and an unauthorized tool.
4. Explain why authorization checks belong in code even when the prompt asks for safe behavior.
5. Show the Azure backend and its configuration. If available, perform a live run;
   otherwise identify it as an integration path awaiting cloud verification.

## Add your own evidence

Record a dated note after reviewing the implementation and running it yourself:

| Evidence | Record after completing |
| --- | --- |
| Environment | Python version, project commit, model deployment/version, region; omit secrets |
| Live behavior | Selected alert, expected versus observed tool calls and evidence citations |
| Quality | Whether the model acknowledges uncertainty and avoids claiming execution |
| Operations | Usage, approximate cost, latency, errors and how you investigated them |
| Original learning | One design decision you can explain and one change you made yourself |

Suggested next contribution: add a new synthetic scenario with an independently
written test and explain the tradeoff in a short decision record. A later real
telemetry integration should use a separately authorized read-only identity and
an explicit data-handling design.
