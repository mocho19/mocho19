# Reproduce the demo

## Offline

Clone the portfolio branch, then enter this directory:

```bash
git clone --branch portfolio/azure-agentic-security-triage https://github.com/mocho19/mocho19.git
cd mocho19/projects/azure-agentic-security-triage
python3 --version
python3 agent.py --alert ALERT-001
python3 agent.py --alert ALERT-002
python3 -m unittest discover -s tests -v
```

Python 3.10+ is required. Offline mode requires no credentials, downloads or pip packages.
The vendored upstream reference has separate dependencies and is not executed.

## Optional live Azure inference

Use an existing Azure OpenAI resource with a deployed model that supports Chat
Completions and function tools. Do not use a Foundry project `/api/projects/...`
endpoint. The resource must permit network access from your machine.

1. Install [Azure CLI](https://learn.microsoft.com/cli/azure/install-azure-cli).
2. Use the [Azure OpenAI setup guide](https://learn.microsoft.com/azure/ai-foundry/openai/how-to/create-resource)
   to create a resource and model deployment if you do not have one. This incurs
   Azure charges and is a manual prerequisite, not an action performed by this project.
3. Have your administrator grant the identity appropriate inference access on that
   resource. See [Azure OpenAI RBAC roles](https://learn.microsoft.com/azure/ai-foundry/openai/how-to/role-based-access-control).
4. Sign in and export your resource root and actual deployment name:

```bash
az login
export AZURE_OPENAI_ENDPOINT='https://YOUR-RESOURCE.openai.azure.com'
export AZURE_OPENAI_DEPLOYMENT='YOUR-CHAT-MODEL-DEPLOYMENT'
python3 agent.py --live --alert ALERT-001
```

The `.env.example` file is documentation only; `.env` is not loaded. No API keys are
needed. Requests target `/openai/v1/chat/completions` and use an Azure CLI bearer token
for `https://cognitiveservices.azure.com/`, consistent with the
[official REST authentication and endpoint reference](https://learn.microsoft.com/en-us/azure/foundry/openai/latest).
Choose a tool-capable model that accepts `max_completion_tokens` and the `system` role.

## Check results and troubleshoot

- Confirm `mode` is `azure-live`, evidence IDs match the selected fixture and all
  proposals remain `approval_required` with `executed: false`.
- Authentication failures: check Azure CLI sign-in, tenant and resource role assignments.
- Not found: check the resource root and deployment name, which may differ from model name.
- Throttling: inspect quota in the portal, wait, then retry manually.
- Incomplete response: the app fails the handoff. Review the model's token needs before
  changing the token budget. No claim of a successful live run should be recorded.
- Network errors: check permitted network access and DNS through your administrator.

The live demo creates no agents, threads, storage or Azure infrastructure. Each run
can incur inference charges. Stop running it to stop its requests. If you manually
created Azure resources, review their billing and remove only the dedicated resources
you no longer need through the portal. No deletion script is included.
