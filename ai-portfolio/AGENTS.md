# Development guidance

This project was built with the microsoft-foundry skill. Before working on or answering questions about foundry agents, read the microsoft-foundry skill first.

Keep offline processing distinct from model inference. Never mark an Azure check
as passed without a real run. Do not publish private user documents or credentials.
Run `python3 -m unittest discover -s tests -v` after behavioral changes. The shared
runtime is in `portfolio/`; each application owns its scenario under `projects/`.
