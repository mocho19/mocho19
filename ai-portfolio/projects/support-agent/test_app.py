import importlib.util
from pathlib import Path
from datetime import date
import unittest

spec = importlib.util.spec_from_file_location("support_app", Path(__file__).with_name("app.py"))
app = importlib.util.module_from_spec(spec)
spec.loader.exec_module(app)


class Offline:
    live = False


class SupportTests(unittest.TestCase):
    def test_delayed_order_creates_unsent_draft(self):
        result = app.run({"text": "ORD-1001 is late, please escalate"}, Offline())
        self.assertIn("delayed", result["summary"])
        self.assertFalse(result["data"]["drafts"][0]["submitted"])
        self.assertEqual(result["data"]["actions_executed"], 0)

    def test_return_window_uses_dates(self):
        within = app.run({"text": "return ORD-1002"}, Offline())
        outside = app.run({"text": "return ORD-1003"}, Offline())
        self.assertEqual(within["data"]["order"]["days_since_delivery"], 12)
        self.assertEqual(within["data"]["order"]["return_review_window"], "within_window")
        self.assertEqual(outside["data"]["order"]["return_review_window"], "outside_window")

    def test_reference_date_is_editable(self):
        result = app.run({"text": "return ORD-1002", "as_of": "2027-01-01"}, Offline())
        self.assertEqual(result["data"]["order"]["return_review_window"], "outside_window")

    def test_missing_or_multiple_id_requires_clarification(self):
        for text in ("where is my order", "compare ORD-1001 and ORD-1002"):
            with self.assertRaises(ValueError):
                app.run({"text": text}, Offline())

    def test_unknown_record_does_not_guess(self):
        result = app.run({"text": "status ORD-9999"}, Offline())
        self.assertEqual(result["data"]["status"], "not_found")
        self.assertEqual(result["sources"], [])

    def test_scope_enforced_even_for_tool_calls(self):
        tools = app.SupportTools("ORD-1001", date(2026, 11, 22))
        self.assertEqual(tools.get_order("ORD-1002")["error"], "order_out_of_scope")
        self.assertEqual(tools.draft_escalation("ORD-1002", "Please investigate")["error"], "order_out_of_scope")

    def test_lookup_required_and_duplicate_drafts_deduplicated(self):
        tools = app.SupportTools("ORD-1001", date(2026, 11, 22))
        self.assertEqual(tools.draft_escalation("ORD-1001", "Please investigate")["error"], "lookup_required")
        tools.get_order("ORD-1001")
        tools.draft_escalation("ORD-1001", "Please investigate")
        tools.draft_escalation("ORD-1001", "Another reason")
        self.assertEqual(len(tools.drafts), 1)

    def test_live_agent_gets_scoped_tools(self):
        class FakeAgent:
            live = True
            def agent(self, instructions, prompt, tools):
                self_outer.assertEqual(tools["get_order"]["handler"](order_id="ORD-1002")["error"], "order_out_of_scope")
                tools["get_order"]["handler"](order_id="ORD-1001")
                tools["get_policy"]["handler"](topic="delivery")
                tools["draft_escalation"]["handler"](order_id="ORD-1001", reason="Investigate delay")
                return {"answer": "An unsent escalation draft requires review.", "trace": []}
        self_outer = self
        result = app.run({"text": "escalate ORD-1001"}, FakeAgent())
        self.assertFalse(result["data"]["drafts"][0]["refund_issued"])

    def test_live_reply_without_evidence_tools_rejected(self):
        class FakeAgent:
            live = True
            def agent(self, *args):
                return {"answer": "I guessed the order status", "trace": []}
        with self.assertRaises(ValueError):
            app.run({"text": "where is ORD-1001"}, FakeAgent())


if __name__ == "__main__":
    unittest.main()
