from pathlib import Path
from app.regression_runner import run_regression, REPORT_DIR
from app.report_generator import write_markdown_report

def main():
    report = run_regression()
    markdown_path = write_markdown_report(report, REPORT_DIR / "regression_report.md")
    print("\nDetailed report created:")
    print(markdown_path.resolve())

if __name__ == "__main__":
    main()
