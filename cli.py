import click
import json
from pathlib import Path
from analyzer import GitCommitAnalyzer
from html_report import generate_html_report

@click.command()
@click.argument("repo_path", type=click.Path(exists=True))
@click.option("--max-commits", default=500, help="Maximum commits to analyze")
@click.option("--output", type=click.Choice(["json", "html"]), default="json")
@click.option("--report-file", default="report.html", help="HTML report filename")
def analyze_repo(repo_path, max_commits, output, report_file):
    """Analyze git repository and generate insights"""
    
    click.echo(f"📊 Analyzing repository: {repo_path}")
    click.echo(f"📝 Analyzing last {max_commits} commits...")
    
    analyzer = GitCommitAnalyzer(repo_path, max_commits)
    metrics = analyzer.analyze()
    
    if output == "json":
        print(json.dumps(metrics, indent=2, default=str))
        
    elif output == "html":
        generate_html_report(metrics, report_file)
        click.echo(f"✅ HTML report generated: {report_file}")

if __name__ == "__main__":
    analyze_repo()