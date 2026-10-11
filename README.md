# AI Verification & Regression Assistant

A beginner-friendly project that scans simulator-style verification logs, detects common failures, runs a small regression over multiple logs, and generates JSON and Markdown reports.

> Current version: rule-based log analysis. It does not yet call an LLM, run a real hardware simulator, or verify a PCIe controller. Those are planned extensions.

## Features

- Classifies log files as PASS, FAIL, or UNKNOWN.
- Detects assertion failures, timeouts, compile errors, protocol errors, and warnings.
- Runs a regression across all `.log` files in `sample_logs/`.
- Generates JSON and Markdown reports.
- Provides rule-based debugging suggestions.
- Includes unit tests.

## Requirements

- Python 3.10 or newer
- Git (for publishing to GitHub)

No third-party Python packages are required for the first version.

## Run on Windows PowerShell

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python run_assistant.py
```

If PowerShell blocks activation, run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` in that terminal, then activate the environment again.

## Run tests

```powershell
python -m unittest discover -s tests -v
```

## Output

After running the assistant, open:

- `reports/regression_report.json`
- `reports/regression_report.md`

The reports are generated locally and are excluded from Git by default.

## Project roadmap

1. Improve log parsing and add more unit tests.
2. Add an optional LLM API for evidence-based explanations.
3. Add a FastAPI endpoint and simple dashboard.
4. Add real Verilator/SystemVerilog example tests.
5. Add Linux shell automation and optional Slurm integration.

## Safety and reliability

- Treat AI explanations as hypotheses, not confirmed root causes.
- Keep API keys in environment variables; never commit secrets.
- Use only synthetic or authorized logs. Do not upload confidential company logs.
- Validate every output against the original log evidence.

## License

MIT (add a `LICENSE` file before distributing if you want to use this license formally).
