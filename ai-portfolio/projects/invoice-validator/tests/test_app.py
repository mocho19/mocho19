import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location("invoice_app", Path(__file__).parents[1] / "app.py")
app = importlib.util.module_from_spec(spec)
spec.loader.exec_module(app)


class Offline:
    live = False


class InvoiceTests(unittest.TestCase):
    def run_text(self, text):
        return app.run({"text": text}, Offline())["data"]

    def test_valid_invoice_reconciles(self):
        result = self.run_text(app.EXAMPLE)
        self.assertEqual(result["status"], "checks_passed")
        self.assertEqual(result["calculated_subtotal"], "380.00")
        self.assertFalse(result["payment_executed"])

    def test_total_mismatch_is_flagged(self):
        result = self.run_text(app.EXAMPLE.replace("Total: 467.40", "Total: 400.00"))
        self.assertTrue(any("Subtotal plus tax" in issue for issue in result["issues"]))

    def test_line_item_mismatch_is_flagged(self):
        result = self.run_text(app.EXAMPLE.replace("2 | 150.00", "3 | 150.00"))
        self.assertTrue(any("Line items total" in issue for issue in result["issues"]))

    def test_missing_fields_and_bad_rows_need_review(self):
        result = self.run_text("Invoice: X\nItem: invalid")
        self.assertEqual(result["status"], "review_required")
        self.assertTrue(any("Missing field: total" in issue for issue in result["issues"]))

    def test_duplicate_total_is_ambiguous(self):
        result = self.run_text(app.EXAMPLE + "\nTotal: 467.40")
        self.assertTrue(any("Duplicate field" in issue for issue in result["issues"]))

    def test_decimal_rounding(self):
        result = self.run_text("Invoice: X\nCurrency: EUR\nItem: A | 0.125 | 1.00\nSubtotal: 0.13\nTax: 0\nTotal: 0.13")
        self.assertEqual(result["calculated_subtotal"], "0.13")
        self.assertEqual(result["status"], "checks_passed")

    def test_hallucinated_live_evidence_is_rejected(self):
        class Bad:
            live = True
            def json(self, *args):
                return {"fields": [{"name": "total", "value": "999", "source_line": 1}], "items": []}
        with self.assertRaises(ValueError):
            app.run({"text": app.EXAMPLE}, Bad())

    def test_empty_input_rejected(self):
        with self.assertRaises(ValueError):
            self.run_text("")


if __name__ == "__main__":
    unittest.main()
