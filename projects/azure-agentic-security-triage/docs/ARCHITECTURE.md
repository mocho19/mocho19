# Architecture and limits

The model suggests tool calls. Only `ToolBoundary.execute` can dispatch them.
It checks the tool name, JSON object keys, value types, requested alert ID, allowed
action and whether evidence has been read. A schema alone is not authorization.
Only the selected synthetic alert is accessible. There is no shell tool, remote
retrieval, Azure resource client, approval endpoint or remediation executor.

The live model sees the request, tool schema and selected synthetic evidence.
Model responses remain untrusted. The application preserves call IDs when returning
results, caps a run at six model responses and eight tool calls, uses a 1,200-token
completion limit per response and refuses incomplete/filtered responses. An HTTP
timeout or quota error terminates the run; automatic retries are intentionally absent.
These bounds limit work, but do not constitute a monetary spending cap.

Tool proposals are session-local and deduplicated. `approval_required` is a state
label, not an implemented approval workflow. A real integration would need authenticated
reviewers, durable audit records, idempotency and separate execution credentials.

The Azure transport accepts public commercial Azure resource hostnames only. It
obtains an Entra token through the user's Azure CLI session and does not persist it.
Use an identity with inference permissions only. Sovereign clouds and project-path
endpoints are outside this demo. Local proxies retain normal Python behavior.

## Residual limitations

- The prompt asks the model to treat evidence as data and cite evidence IDs. Those
  natural-language properties are not mechanically guaranteed or evaluated here.
- Tests establish application controls, not immunity to prompt injection or model hallucinations.
- A model could still produce misleading final text. Review the actual proposal objects
  and trace; do not infer execution from generated prose.
- Alerts are fabricated. There is no Sentinel, Defender, Graph or Resource Graph connection.
- Local output may contain model text and synthetic evidence. Never substitute private
  incident data without reviewing its handling and your organization's requirements.
- Live quality, latency, cost and Azure availability have not been measured.
