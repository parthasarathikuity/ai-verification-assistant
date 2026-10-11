"""Parse simple simulator-style logs into structured findings."""
from __future__ import annotations
import re
from pathlib import Path

ERROR_PATTERNS = [
    ("ASSERTION_FAILURE", re.compile(r"\b(assertion failed|assert failed|assertion error)\b", re.I)),
    ("TIMEOUT", re.compile(r"\b(timeout|timed out)\b", re.I)),
    ("COMPILE_ERROR", re.compile(r"\b(compile error|syntax error|undefined module)\b", re.I)),
    ("PROTOCOL_ERROR", re.compile(r"\b(protocol error|unexpected packet|invalid sequence)\b", re.I)),
    ("GENERAL_ERROR", re.compile(r"\b(error|fatal)\b", re.I)),
]
WARNING_PATTERN = re.compile(r"\bwarning\b", re.I)
PASS_PATTERN = re.compile(r"\b(TEST PASS|PASS|PASSED)\b", re.I)
FAIL_PATTERN = re.compile(r"\b(TEST FAIL|FAIL|FAILED|FATAL|ERROR)\b", re.I)

def analyze_log_text(text: str) -> dict:
    lines = text.splitlines()
    findings = []
    warnings = []
    passed_marker = False
    failed_marker = False

    for line_number, line in enumerate(lines, start=1):
        stripped = line.strip()
        if not stripped:
            continue
        if PASS_PATTERN.search(stripped):
            passed_marker = True
        if FAIL_PATTERN.search(stripped):
            failed_marker = True
        if WARNING_PATTERN.search(stripped):
            warnings.append({"line": line_number, "text": stripped})
        for category, pattern in ERROR_PATTERNS:
            if pattern.search(stripped):
                findings.append({
                    "line": line_number,
                    "category": category,
                    "text": stripped,
                })
                break

    if findings or failed_marker:
        status = "FAIL"
    elif passed_marker:
        status = "PASS"
    else:
        status = "UNKNOWN"

    return {
        "status": status,
        "total_lines": len(lines),
        "error_count": len(findings),
        "warning_count": len(warnings),
        "errors": findings,
        "warnings": warnings,
    }

def analyze_log_file(path: str | Path) -> dict:
    log_path = Path(path)
    text = log_path.read_text(encoding="utf-8", errors="replace")
    result = analyze_log_text(text)
    result["file"] = str(log_path)
    return result
