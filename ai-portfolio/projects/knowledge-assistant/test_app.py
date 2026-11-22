import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location("knowledge_app", Path(__file__).with_name("app.py"))
app = importlib.util.module_from_spec(spec)
spec.loader.exec_module(app)


class Offline:
    live = False


class KnowledgeTests(unittest.TestCase):
    def test_offboarding_ranks_access_policy_first(self):
        hits = app.retrieve("departing employee access removal offboarding")
        self.assertEqual(hits[0]["id"], "KB-01")
        self.assertGreater(hits[0]["score"], 0)

    def test_different_query_changes_retrieved_evidence(self):
        self.assertEqual(app.retrieve("travel receipt reimbursement")[0]["id"], "KB-06")
        self.assertEqual(app.retrieve("customer retention ninety days")[0]["id"], "KB-04")

    def test_unknown_topic_abstains(self):
        result = app.run({"text": "quantum banana spaceship"}, Offline())
        self.assertEqual(result["data"]["status"], "insufficient_evidence")
        self.assertEqual(result["sources"], [])

    def test_offline_returns_real_excerpts_with_ids(self):
        result = app.run({"text": "privileged administrator access review"}, Offline())
        self.assertIn("KB-02", result["data"]["citation_ids"])
        self.assertIn("every month", result["summary"])

    def test_blank_question_rejected(self):
        with self.assertRaises(ValueError):
            app.run({"text": " "}, Offline())

    def test_model_invented_citation_rejected(self):
        class BadModel:
            live = True
            def json(self, *args):
                return {"answer": "I invented an answer", "citation_ids": ["KB-999"]}
        with self.assertRaises(ValueError):
            app.run({"text": "travel reimbursement"}, BadModel())

    def test_valid_live_response_contract(self):
        class Model:
            live = True
            def json(self, *args):
                return {"answer": "Submit within thirty days [KB-06].", "citation_ids": ["KB-06"]}
        result = app.run({"text": "travel reimbursement"}, Model())
        self.assertEqual(result["data"]["status"], "generated_answer_requires_review")


if __name__ == "__main__":
    unittest.main()
