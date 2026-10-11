import unittest
from app.log_parser import analyze_log_text

class TestLogParser(unittest.TestCase):
    def test_pass_log(self):
        result = analyze_log_text("Starting test\nTEST PASS\n")
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["error_count"], 0)

    def test_assertion_failure(self):
        result = analyze_log_text("Starting test\nASSERTION FAILED: ready was low\nTEST FAIL\n")
        self.assertEqual(result["status"], "FAIL")
        self.assertEqual(result["errors"][0]["category"], "ASSERTION_FAILURE")

    def test_unknown_log(self):
        result = analyze_log_text("Simulator started\nStill running\n")
        self.assertEqual(result["status"], "UNKNOWN")

if __name__ == "__main__":
    unittest.main()
