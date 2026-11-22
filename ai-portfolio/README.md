# Sayeem Chowdhury · AI Application Portfolio

Seven working application prototypes for clients who need practical AI workflows
with clear evidence, validation and human review. The collection connects cloud
security experience with document intelligence, customer operations and business automation.

**Python · Microsoft Foundry SDK · Responses API · retrieval · function tools · structured outputs**

[Discuss a freelance project](mailto:msayeem.secops@gmail.com) ·
[LinkedIn](https://www.linkedin.com/in/msayeemchow/) ·
[GitHub](https://github.com/mocho19)

## Explore the seven projects

| Application | What it does | Engineering focus |
| --- | --- | --- |
| [Evidence Desk](projects/knowledge-assistant/) | Finds policy passages, cites sources and abstains when no evidence matches | BM25 retrieval, grounded generation, citation validation |
| [CaseFlow](projects/support-agent/) | Looks up an order, checks policy and prepares an escalation draft | Scoped function tools, return-date arithmetic, evidence checks |
| [Invoice Check](projects/invoice-validator/) | Extracts invoice fields and flags inconsistent totals | Structured extraction, Decimal reconciliation, exception handling |
| [Security Investigation Copilot](projects/security-investigator/) | Correlates sign-in and storage events into an analyst handoff | Local investigation tools, timelines, bounded agent execution |
| [Contract Radar](projects/contract-review/) | Finds clause evidence and calculates renewal notice deadlines | Source-linked extraction, date arithmetic, review queues |
| [Freelance AI Proposal Studio](projects/proposal-studio/) | Produces requirements, a solution design and critical review | Three-stage AI workflow, discovery questions, explicit assumptions |
| [Meeting to Momentum](projects/meeting-actions/) | Converts transcript commitments into tasks and CSV data | Structured extraction, source validation, missing-owner handling |

Each project has its own code, sample input, tests, architecture and limitations.
They share a browser workbench and Foundry client so authentication and model-call
handling can be reviewed in one place. These are seven applications in one portfolio
collection, rather than seven separate repositories.

## Run the browser workbench

```bash
git clone https://github.com/mocho19/mocho19.git
cd mocho19/ai-portfolio
python3 server.py
```

Open **http://127.0.0.1:8765**. Choose an application, edit the sample and run it.
Results include evidence and a workflow trace; JSON can be downloaded. The application
runs on your computer and is not a public hosted service. Python 3.10+ is required.
Offline demos need no package installation and make no model calls.

For a command-line demo or the complete test suite:

```bash
python3 run.py invoice-validator
python3 run.py knowledge-assistant --text 'How often is privileged access reviewed?'
python3 -m unittest discover -s tests -v
```

## Microsoft Foundry integration

The optional live mode uses `AIProjectClient`, Entra authentication and the Responses
API through `get_openai_client()`. The support and security apps implement bounded
client-side tool-calling agents. Other apps use structured model outputs or a staged
workflow, with business calculations in application code.

[Follow the setup guide](docs/SETUP.md) to connect an existing project and compatible
deployment. Live model calls incur Azure usage charges. This collection does not
provision hosted Foundry agents or claim that cloud deployment has been completed.

## Verification and ownership

**69 automated tests passed**, and all seven workflows were exercised in the browser
in offline mode. [Validation record](docs/VALIDATION.md) ·
[Architecture](docs/ARCHITECTURE.md) · [Portfolio walkthrough](docs/PORTFOLIO.md)

These projects were prepared for Sayeem Chowdhury with Codex assistance. They are new
AI-assisted implementations, not copied course projects. Synthetic sample data is
included; the CV and private client material are not included. Live Foundry inference,
production deployment, business outcomes and client acceptance remain unverified.
See [PROVENANCE.md](PROVENANCE.md).

For client work, a sensible next step is a short discovery session to agree on data
access, desired workflow, evaluation examples, budget and deployment requirements.
These demos illustrate implementation approaches; they do not promise production
readiness or measured commercial results.

MIT license. See [LICENSE](LICENSE).
