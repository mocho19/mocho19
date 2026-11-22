"""Collect each isolated project's behavioral suite without module-name collisions."""
import importlib.util
from pathlib import Path
import unittest
from portfolio.registry import ROOT, SLUGS, execute, load


class IntegrationTests(unittest.TestCase):
    def test_all_seven_examples_are_serializable_and_labeled(self):
        for slug in SLUGS:
            with self.subTest(project=slug):
                result = execute(slug, {"text": load(slug).SPEC["example_input"], "as_of": "2026-11-22"})
                self.assertEqual(result["mode"], "offline-deterministic")
                for field in ("summary", "data", "sources", "trace"):
                    self.assertIn(field, result)

    def test_global_input_boundary(self):
        for payload in ({"text": ""}, {"text": "x" * 16001}, {"text": 5}, {"text": "test", "command": "delete"}):
            with self.assertRaises(ValueError):
                execute("knowledge-assistant", payload)
        with self.assertRaises(ValueError):
            load("../../secret")


def load_tests(loader, tests, pattern):
    suite = unittest.TestSuite([tests])
    for slug in SLUGS:
        for index, path in enumerate(sorted((ROOT / "projects" / slug).rglob("test_*.py"))):
            name = "test_" + slug.replace("-", "_") + str(index)
            spec = importlib.util.spec_from_file_location(name, path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            suite.addTests(loader.loadTestsFromModule(module))
    return suite
