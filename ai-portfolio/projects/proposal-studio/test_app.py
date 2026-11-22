import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location("proposal_app", Path(__file__).with_name("app.py"))
app = importlib.util.module_from_spec(spec)
spec.loader.exec_module(app)

class Offline:
    live = False

class ProposalTests(unittest.TestCase):
    def test_complete_pipeline_and_decimal_arithmetic(self):
        result = app.run({"text": app.SPEC["example_input"]}, Offline())
        self.assertEqual(result["data"]["estimate_from_user_assumptions"]["subtotal_eur"], "4200.00")
        self.assertIn("Retrieval", result["data"]["solution_design"]["pattern"])
        self.assertEqual(len(result["trace"]), 3)
        self.assertEqual(result["data"]["external_actions"], 0)

    def test_no_price_without_user_assumptions(self):
        result = app.run({"text": "Problem: Classify incoming support requests for our small business."}, Offline())
        self.assertEqual(result["data"]["estimate_from_user_assumptions"]["status"], "discovery_required")

    def test_partial_assumptions_not_a_price(self):
        self.assertEqual(app.estimate({"estimate hours": "40"})["status"], "incomplete_assumptions")

    def test_nonfinite_or_negative_estimates_rejected(self):
        for hours in ("NaN", "Infinity", "-2", "10001", "abc"):
            with self.assertRaises(ValueError): app.estimate({"estimate hours": hours, "hourly rate eur": "50"})

    def test_changed_input_changes_solution(self):
        result = app.run({"text": "Problem: Extract invoice fields and validate totals for our accounting team."}, Offline())
        self.assertEqual(result["data"]["solution_design"]["pattern"], "Structured document extraction workflow")

    def test_short_brief_and_duplicate_fields_rejected(self):
        with self.assertRaises(ValueError): app.parse_brief("short")
        with self.assertRaises(ValueError): app.parse_brief("Problem: A reasonably long client problem.\nProblem: another")

    def test_sources_preserve_line_numbers(self):
        _, sources = app.parse_brief("Client: A synthetic organization\n\nProblem: Make document search easier.")
        self.assertEqual([s["id"] for s in sources], ["L1", "L3"])

    def test_live_stages_and_pricing_is_mechanical(self):
        class Live:
            live = True
            calls = []
            def json(self, instructions, data, schema):
                self.calls.append(data)
                if len(self.calls) == 1:
                    return {"problem": "Find policies", "users": "Analysts", "requirements": ["Citations"], "unknowns": ["Access"], "source_ids": ["L2"]}
                if len(self.calls) == 2:
                    return {"pattern": "Grounded assistant", "components": [], "phases": [], "integrations_to_confirm": "Teams", "out_of_scope": [], "acceptance_checks": []}
                return {"status": "discovery_draft", "risks": ["Confirm access"], "questions": ["Who approves?"], "review_result": "Draft", "next_step": "Discovery"}
        live = Live()
        result = app.run({"text": app.SPEC["example_input"]}, live)
        self.assertEqual(len(live.calls), 3)
        self.assertNotIn("Hourly rate", str(live.calls[0]))
        self.assertEqual(result["data"]["estimate_from_user_assumptions"]["subtotal_eur"], "4200.00")

    def test_live_unknown_source_rejected(self):
        class Live:
            live = True
            def json(self, *args): return {"source_ids": ["L999"]}
        with self.assertRaises(ValueError): app.run({"text": app.SPEC["example_input"]}, Live())

if __name__ == "__main__": unittest.main()
