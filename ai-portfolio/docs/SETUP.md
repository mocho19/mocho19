# Setup and reproducible runs

## Offline application demos

Use Python 3.10 or newer. From `ai-portfolio/`:

```bash
python3 server.py
```

Open http://127.0.0.1:8765. All seven apps accept editable synthetic text. The
reference date is explicit for date-based workflows. The server binds only to your
computer, handles one application run at a time and does not retain input on disk.
Browser downloads are saved only when you choose Download result JSON.

Use `python3 run.py <project-slug>` to run an example. Override it with
`--text 'your input'` or `--input /path/to/input.txt`. Use `--as-of 2026-11-22`
to make date-based examples reproducible. The knowledge corpus and synthetic order
catalog can be edited in their respective project directories.

## Optional live Microsoft Foundry mode

Prerequisites: an existing Microsoft Foundry project, an appropriate Entra role,
network access and a deployed model supporting Responses, function tools and
structured JSON outputs. Model capability varies; select a deployment supporting
all three features for the full collection. This repository does not create Azure
resources or change role assignments.

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements-live.txt
az login
export FOUNDRY_PROJECT_ENDPOINT='https://YOUR-RESOURCE.services.ai.azure.com/api/projects/YOUR-PROJECT'
export FOUNDRY_MODEL_NAME='YOUR-DEPLOYMENT-NAME'
python3 run.py knowledge-assistant --live
python3 server.py --enable-live
```

Then select Microsoft Foundry in the browser's processing menu. The endpoint is a
**project endpoint**, not an Azure OpenAI resource root. `.env.example` is a reference;
the app reads exported variables and does not automatically load `.env` files.
The model value is your deployment name, not necessarily the model family name.

The optional SDK requirement pins `azure-ai-projects` to 2.11.0; other direct dependencies
have major-version bounds. This is not a fully resolved transitive lockfile. The
offline suite has no third-party dependencies. SDK installation and real inference
have not been tested in this preparation environment; validate them in your own project.

Official references, checked 22 November 2026:

- [Foundry Python SDK and project endpoints](https://learn.microsoft.com/python/api/overview/azure/ai-projects-readme)
- [AIProjectClient and authenticated OpenAI client](https://learn.microsoft.com/python/api/azure-ai-projects/azure.ai.projects.aiprojectclient)
- [Structured outputs](https://learn.microsoft.com/azure/foundry/openai/how-to/structured-outputs)
- [Function calling](https://learn.microsoft.com/azure/foundry/agents/how-to/tools/function-calling)
- [Foundry role-based access](https://learn.microsoft.com/azure/ai-foundry/concepts/rbac-azure-ai-foundry)

## Verify the live behavior before claiming it

Run each app with its synthetic example. Record the project commit, model version,
date, result, observed usage, latency and failures. Check citations, tool traces,
rejected inputs and all zero-execution/draft state fields. Use a second input to
establish that responses change with evidence. Run the tests before recording a
successful demonstration. A mocked response or offline run does not verify Azure.

Failure checks: missing dependency → install the optional requirements; authentication
error → check sign-in/tenant and project role; missing deployment → check its actual
name and model features; incomplete output → inspect token requirements; throttling
→ check quota and retry manually. Service error bodies and tokens are not displayed.

Each model response is capped at 2,400 output tokens; a run permits at most ten
responses. Tool agents additionally cap themselves at six responses and ten tool
calls. These are workload bounds, not a monetary spending cap. Stop the server with
Ctrl+C when finished. No cleanup of cloud resources is needed for the application
itself, because it does not provision any.
