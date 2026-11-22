import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location("meeting_app", Path(__file__).parents[1] / "app.py")
app = importlib.util.module_from_spec(spec)
spec.loader.exec_module(app)


class Offline:
    live = False


class MeetingTests(unittest.TestCase):
    def parse(self, text=app.EXAMPLE):
        return app.run({"text": text}, Offline())["data"]

    def test_explicit_actions_and_commitments(self):
        result = self.parse()
        self.assertEqual(len(result["tasks"]), 3)
        omar = next(t for t in result["tasks"] if t["owner"] == "Omar")
        self.assertEqual(omar["due_date"], "2026-12-03")
        self.assertEqual(omar["task"], "review the access policy")
        self.assertEqual(result["external_tasks_created"], 0)

    def test_unassigned_task_stays_unassigned(self):
        task = self.parse("ACTION: Unassigned | Review scope | not set")["tasks"][0]
        self.assertIsNone(task["owner"])
        self.assertIsNone(task["due_date"])
        self.assertIn("owner_unassigned", task["review_flags"])

    def test_discussion_is_not_a_task(self):
        self.assertEqual(self.parse("Maya: We might build a dashboard.")["tasks"], [])

    def test_decisions_and_blockers_have_source(self):
        result = self.parse()
        self.assertEqual(result["decisions"][0]["source_line"], 2)
        self.assertEqual(result["blockers"][0]["source_line"], 5)

    def test_bad_date_preserved_but_flagged(self):
        result = self.parse("ACTION: Maya | Update report | 2026-02-30")
        self.assertIn("invalid_due_date", result["tasks"][0]["review_flags"])

    def test_csv_formula_is_escaped(self):
        result = self.parse("ACTION: Maya | =HYPERLINK(attack) | not set")
        self.assertIn("'=HYPERLINK", result["csv_export"])

    def test_duplicate_commitments_are_deduplicated(self):
        row = "ACTION: Maya | Review scope | not set"
        self.assertEqual(len(self.parse(row + "\n" + row)["tasks"]), 1)

    def test_invented_owner_rejected_in_live_mode(self):
        class Bad:
            live = True
            def json(self, *args):
                return {"tasks": [{"task": "Review scope", "owner": "Invented", "due_date": None, "source_line": 1}],
                        "decisions": [], "blockers": []}
        with self.assertRaises(ValueError):
            app.run({"text": "ACTION: Unassigned | Review scope | not set"}, Bad())


if __name__ == "__main__":
    unittest.main()
