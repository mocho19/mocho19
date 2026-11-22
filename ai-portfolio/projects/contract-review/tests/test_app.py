from pathlib import Path
import importlib.util
import unittest

spec = importlib.util.spec_from_file_location("contract_app", Path(__file__).parents[1] / "app.py")
app = importlib.util.module_from_spec(spec)
spec.loader.exec_module(app)


class Offline:
    live = False


class ContractTests(unittest.TestCase):
    def review(self, text=app.EXAMPLE, as_of="2026-11-22"):
        return app.run({"text": text, "as_of": as_of}, Offline())["data"]

    def test_renewal_calendar_arithmetic(self):
        result = self.review()
        self.assertEqual(result["timeline"]["notice_deadline"], "2026-12-30")
        self.assertEqual(result["timeline"]["days_until_notice"], 38)
        self.assertFalse(result["notice_sent"])

    def test_expired_deadline_is_explicit(self):
        self.assertEqual(self.review(as_of="2027-01-01")["timeline"]["state"], "deadline_passed")

    def test_due_today(self):
        self.assertEqual(self.review(as_of="2026-12-30")["timeline"]["state"], "due_today")

    def test_missing_clauses_are_excerpt_questions(self):
        result = self.review("End date: 2027-02-28\nNotice period: 60 days")
        self.assertIn("security", result["not_found_in_excerpt"])
        self.assertTrue(any("excerpt" in question for question in result["review_questions"]))

    def test_conflicting_dates_do_not_guess(self):
        result = self.review(app.EXAMPLE + "\nEnd date: 2027-03-31")
        self.assertIsNone(result["timeline"]["notice_deadline"])
        self.assertTrue(any("Multiple end dates" in issue for issue in result["issues"]))

    def test_invalid_date_is_flagged(self):
        result = self.review(app.EXAMPLE.replace("2027-02-28", "2027-02-30"))
        self.assertEqual(result["timeline"]["state"], "incomplete")

    def test_hallucinated_quote_is_rejected(self):
        class Bad:
            live = True
            def json(self, *args):
                return {"clauses": [{"category": "security", "source_line": 1, "quote": "Military grade encryption"}]}
        with self.assertRaises(ValueError):
            app.run({"text": app.EXAMPLE}, Bad())

    def test_bad_as_of_is_rejected(self):
        with self.assertRaises(ValueError):
            self.review(as_of="tomorrow")


if __name__ == "__main__":
    unittest.main()
