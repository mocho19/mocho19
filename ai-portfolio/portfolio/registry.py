import importlib.util
import json
from pathlib import Path
from portfolio.ai import OfflineAI, FoundryAI

ROOT = Path(__file__).resolve().parents[1]
SLUGS = ["knowledge-assistant", "support-agent", "invoice-validator",
         "security-investigator", "contract-review", "proposal-studio", "meeting-actions"]


def load(slug):
    if slug not in SLUGS:
        raise ValueError("Unknown application")
    spec = importlib.util.spec_from_file_location(slug.replace("-", "_"), ROOT / "projects" / slug / "app.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def catalog():
    return [load(slug).SPEC for slug in SLUGS]


def execute(slug, payload, live=False):
    if not isinstance(payload, dict) or not isinstance(payload.get("text"), str):
        raise ValueError("Provide text input")
    if not payload["text"].strip() or len(payload["text"]) > 16000:
        raise ValueError("Enter between 1 and 16,000 characters")
    if set(payload) - {"text", "as_of"}:
        raise ValueError("Unsupported input fields")
    app = load(slug)
    if live:
        with FoundryAI() as ai:
            result = app.run(payload, ai)
            result["model_calls"] = ai.calls
            result["usage"] = ai.usage
    else:
        result = app.run(payload, OfflineAI())
    result["mode"] = "foundry-live" if live else "offline-deterministic"
    result["project"] = slug
    result["ai_assisted_project"] = True
    json.dumps(result, allow_nan=False)
    return result
