from types import SimpleNamespace
import unittest
from portfolio.ai import AIError, FoundryAI, OfflineAI, validate


class Item:
    def __init__(self, name="lookup", arguments='{"record":"demo"}', call_id="call_1"):
        self.type, self.name, self.arguments, self.call_id = "function_call", name, arguments, call_id
    def model_dump(self, **kwargs):
        return vars(self)


def response(items=None, text="done", status="completed"):
    return SimpleNamespace(output=items or [], output_text=text, status=status, usage=None)


class FakeClient:
    def __init__(self, replies):
        self.responses = self
        self.replies = iter(replies)
        self.requests = []
    def create(self, **kwargs):
        self.requests.append(kwargs)
        return next(self.replies)


class RuntimeTests(unittest.TestCase):
    def tool(self, handler):
        return {"lookup": {"description": "read fixture", "parameters": {
            "type": "object", "properties": {"record": {"type": "string", "enum": ["demo"]}},
            "required": ["record"], "additionalProperties": False}, "handler": handler}}

    def test_call_result_ids_and_history_are_preserved(self):
        seen = []
        client = FakeClient([response([Item()]), response()])
        ai = FoundryAI(client, "test")
        result = ai.agent("test", "test", self.tool(lambda record: seen.append(record) or {"record": record}))
        self.assertEqual(seen, ["demo"])
        self.assertEqual(result["answer"], "done")
        item = client.requests[1]["input"][-1]
        self.assertEqual(item["call_id"], "call_1")
        self.assertEqual(item["type"], "function_call_output")
        self.assertFalse(client.requests[0]["store"])

    def test_unauthorized_and_malformed_tools_do_not_dispatch(self):
        for item in (Item("delete"), Item(arguments="{"), Item(arguments='{"record":"other"}'), Item(arguments='{"record":"demo","extra":1}')):
            called = []
            ai = FoundryAI(FakeClient([response([item]), response()]), "test")
            result = ai.agent("test", "test", self.tool(lambda **args: called.append(args)))
            self.assertEqual(called, [])
            self.assertIn(result["trace"][0]["status"], ("tool_not_allowed", "invalid_arguments"))

    def test_tool_loop_is_bounded(self):
        ai = FoundryAI(FakeClient([response([Item()])] * 6), "test")
        with self.assertRaises(AIError):
            ai.agent("test", "test", self.tool(lambda **args: {}))

    def test_parallel_tool_budget_is_checked_before_execution(self):
        seen = []
        ai = FoundryAI(FakeClient([response([Item()] * 11)]), "test")
        with self.assertRaises(AIError):
            ai.agent("test", "test", self.tool(lambda **args: seen.append(args)))
        self.assertEqual(seen, [])

    def test_incomplete_responses_are_rejected(self):
        ai = FoundryAI(FakeClient([response(status="incomplete")]), "test")
        with self.assertRaises(AIError):
            ai.json("test", {}, {"type": "object"})

    def test_structured_response_contract(self):
        schema = {"type": "object", "properties": {"answer": {"type": "string"}},
                  "required": ["answer"], "additionalProperties": False}
        client = FakeClient([response(text='{"answer":"supported"}')])
        self.assertEqual(FoundryAI(client, "test").json("test", {}, schema), {"answer": "supported"})
        self.assertEqual(client.requests[0]["text"]["format"]["schema"], schema)
        for text in ('{"invented":true}', '{"answer":10}', 'not json'):
            with self.assertRaises(AIError):
                FoundryAI(FakeClient([response(text=text)]), "test").json("test", {}, schema)

    def test_schema_unsupported_rules_fail_closed(self):
        with self.assertRaises(ValueError):
            validate("text", {"type": "string", "pattern": "[a-z]"})
        with self.assertRaises(ValueError):
            validate(True, {"type": "integer"})
        validate(None, {"type": ["string", "null"]})

    def test_offline_cannot_silently_call_model(self):
        with self.assertRaises(AIError):
            OfflineAI().json("test", {}, {})

    def test_endpoint_rejects_non_azure_and_missing_config(self):
        from unittest.mock import patch
        with patch.dict("os.environ", {"FOUNDRY_PROJECT_ENDPOINT": "https://evil.example/api/projects/demo"}):
            with self.assertRaises(AIError):
                FoundryAI().__enter__()
