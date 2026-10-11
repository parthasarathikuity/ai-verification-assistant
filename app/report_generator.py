# """Generate a readable Markdown report from the regression JSON data."""
# from pathlib import Path
# from app.ai_analyzer import suggest_debugging_steps

# def write_markdown_report(report: dict, output_path: str | Path) -> Path:
#     output_path = Path(output_path)
#     output_path.parent.mkdir(parents=True, exist_ok=True)
#     lines = [
#         "# Regression Report",
#         "",
#         f"- Total log files: **{report['total_tests']}**",
#         f"- Passed: **{report['summary']['PASS']}**",
#         f"- Failed: **{report['summary']['FAIL']}**",
#         f"- Unknown: **{report['summary']['UNKNOWN']}**",
#         "",
#     ]
#     for result in report["results"]:
#         lines.extend([
#             f"## {Path(result['file']).name}: {result['status']}",
#             "",
#             f"- Errors detected: {result['error_count']}",
#             f"- Warnings detected: {result['warning_count']}",
#             "",
#         ])
#         for error in result["errors"]:
#             lines.append(f"- **{error['category']}**, line {error['line']}: `{error['text']}`")
#         for step in suggest_debugging_steps(result):
#             lines.append(f"- Suggested next step: {step}")
#         lines.append("")
#     output_path.write_text("\n".join(lines), encoding="utf-8")
#     return output_path

"""Generate a Markdown report with optional LLM explanations."""
import os
from pathlib import Path

from app.ai_analyzer import (
    analyze_with_llm,
    suggest_debugging_steps,
)


def write_markdown_report(report: dict, output_path: str | Path) -> Path:
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    lines = [
        "# AI Verification Assistant — Regression Report",
        "",
        f"- Total log files: **{report['total_tests']}**",
        f"- Passed: **{report['summary']['PASS']}**",
        f"- Failed: **{report['summary']['FAIL']}**",
        f"- Unknown: **{report['summary']['UNKNOWN']}**",
        "",
    ]

    for result in report["results"]:
        lines.extend([
            f"## {Path(result['file']).name}: {result['status']}",
            "",
            f"- Errors detected: {result['error_count']}",
            f"- Warnings detected: {result['warning_count']}",
            "",
            "### Detected errors",
            "",
        ])

        for error in result["errors"]:
            lines.append(
                f"- **{error['category']}**, line {error['line']}: "
                f"`{error['text']}`"
            )

        lines.extend(["", "### Rule-based suggestions", ""])
        for step in suggest_debugging_steps(result):
            lines.append(f"- {step}")

        lines.extend(["", "### LLM analysis", ""])

        if result["status"] == "FAIL" and os.getenv("OPENAI_API_KEY"):
            try:
                explanation = analyze_with_llm(result)
            except Exception as exc:
                # Print the full error in the terminal for debugging.
                print(
                    f"LLM error for {Path(result['file']).name}: "
                    f"{type(exc).__name__}: {exc}"
                )

                # Keep the report useful even when the API fails.
                explanation = (
                    "LLM analysis failed.\n\n"
                    f"- Error type: `{type(exc).__name__}`\n"
                    f"- Error details: `{exc}`\n"
                    "- Check API quota, rate limits, model access, "
                    "and API configuration."
                )

        elif result["status"] != "FAIL":
            explanation = "LLM analysis not needed for this result."

        else:
            explanation = (
                "Skipped because OPENAI_API_KEY is not configured."
            )

        lines.extend([explanation, ""])

    output_path.write_text("\n".join(lines), encoding="utf-8")
    return output_path

