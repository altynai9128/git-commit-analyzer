# Git Commit History Analyzer

CLI tool for analyzing git repository commit history with JSON output and HTML reports.

## Features

- ✅ Analyze last N commits (configurable, default 500)
- 📊 Metrics: commits per day/week, top contributors, conventional commit compliance
- 🔥 Code churn hotspots (last 30 days)
- 📄 JSON output mode
- 📈 HTML report with 3+ interactive charts
- 🧪 8+ unit tests with fixture repos
- ⚡ Handles 10,000+ commits without hanging

## Installation

git clone https://github.com/YOUR_USERNAME/git-commit-analyzer
cd git-commit-analyzer
python -m venv venv

## Activate virtual environment:

Windows:

venv\Scripts\activate

Linux/Mac:

source venv/bin/activate

## Install dependencies:

pip install -r requirements.txt

## Usage

Basic syntax:

python cli.py <repo-path> [--max-commits N] [--output FORMAT] [--report-file FILENAME]

## Parameters
| Parameter | Description | Default |
|-----------|-------------|---------|
| `repo-path` | Path to git repository | Required |
| `--max-commits` | Number of commits to analyze | 500 |
| `--output` | Output format: `json` or `html` | json |
| `--report-file` | HTML report filename (for html output) | report.html |

## Examples
JSON output:

python cli.py /path/to/git/repo --max-commits 500 --output json

HTML report:

python cli.py /path/to/git/repo --max-commits 1000 --output html --report-file my_report.html

Default values:

python cli.py /path/to/git/repo

JSON Output Example

{
  "total_commits_analyzed": 100,
  "commits_per_day": {
    "2026-04-01": 15,
    "2026-04-02": 22
  },
  "commits_per_week": {
    "2026-W13": 45,
    "2026-W14": 67
  },
  "top_contributors_commits": [
    ["Alice Smith", 45],
    ["Bob Johnson", 32]
  ],
  "top_contributors_lines": [
    ["Alice Smith", 12500],
    ["Bob Johnson", 8900]
  ],
  "conventional_commit_percent": 85.5,
  "avg_pr_size_files": 2.3,
  "avg_pr_size_lines": 145.7,
  "code_churn_hotspots": [
    {
      "file": "src/main.py",
      "change_count": 12,
      "total_lines_changed": 345
    }
  ]
}

HTML Report

Creates an interactive HTML file with 4 charts:

- Commit frequency over time (line chart)

- Contributor distribution (pie chart)

- File churn heatmap (bar chart)

- Commits per week (histogram)

- Open HTML report in browser:

python cli.py /path/to/repo --output html --report-file reports/my_report.html
The reports folder will be created automatically.

## Running Tests

pytest tests/ -v

## Requirements
Python 3.8+
Git (installed and available in PATH)

## Dependencies
gitpython==3.1.41
pandas==2.2.1
matplotlib==3.8.3
seaborn==0.13.2
plotly==5.19.0
click==8.1.7
pytest==8.0.2

## xample Output
See sample_output/example_report.html for a complete HTML report example.

## Notes
- Works with repositories containing 10,000+ commits (streaming processing)

- "Average PR size" is calculated as average changes per commit (for repositories without pull requests)

- Code churn hotspots only consider commits from the last 30 days

- Conventional commits format: type(scope): description (feat, fix, docs, style, refactor, perf, test, chore)