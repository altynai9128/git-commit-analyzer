import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
from typing import Dict, Any
import os
from pathlib import Path

def generate_html_report(metrics: Dict[str, Any], output_file: str):
    
    commits_df = pd.DataFrame(list(metrics["commits_per_day"].items()), 
                               columns=["date", "commits"])
    fig1 = px.line(commits_df, x="date", y="commits", 
                   title="Commit Frequency Over Time",
                   labels={"date": "Date", "commits": "Number of Commits"})
    
    contributors = dict(metrics["top_contributors_commits"][:5])  
    fig2 = go.Figure(data=[go.Pie(labels=list(contributors.keys()), 
                                   values=list(contributors.values()))])
    fig2.update_layout(title="Top 5 Contributors Distribution")
    
    if metrics["code_churn_hotspots"]:
        churn_df = pd.DataFrame(metrics["code_churn_hotspots"][:8])
        fig3 = px.bar(churn_df, x="file", y="change_count",
                      title="File Churn Hotspots (last 30 days)",
                      labels={"file": "File", "change_count": "Number of Changes"},
                      color="total_lines_changed")
    
    weeks_df = pd.DataFrame(list(metrics["commits_per_week"].items()),
                             columns=["week", "commits"])
    fig4 = px.bar(weeks_df, x="week", y="commits",
                  title="Commits per Week",
                  labels={"week": "Week", "commits": "Number of Commits"})
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Git Commit History Analyzer Report</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }}
            .container {{ max-width: 1200px; margin: auto; background: white; padding: 20px; border-radius: 10px; }}
            h1 {{ color: #333; border-bottom: 3px solid #4CAF50; padding-bottom: 10px; }}
            .metric {{ display: inline-block; width: 30%; margin: 10px; padding: 15px; background: #f0f0f0; border-radius: 8px; }}
            .metric-value {{ font-size: 24px; font-weight: bold; color: #4CAF50; }}
            .chart {{ margin: 30px 0; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>📊 Git Commit History Analyzer Report</h1>
            
            <div style="text-align: center;">
                <div class="metric">
                    <div>Total Commits Analyzed</div>
                    <div class="metric-value">{metrics["total_commits_analyzed"]}</div>
                </div>
                <div class="metric">
                    <div>Conventional Commits</div>
                    <div class="metric-value">{metrics["conventional_commit_percent"]:.1f}%</div>
                </div>
                <div class="metric">
                    <div>Average PR Size</div>
                    <div class="metric-value">{metrics["avg_pr_size_files"]:.1f} files</div>
                </div>
            </div>
            
            <div class="chart">
                {fig1.to_html(full_html=False, include_plotlyjs='cdn')}
            </div>
            
            <div class="chart">
                {fig2.to_html(full_html=False, include_plotlyjs='cdn')}
            </div>
            
            <div class="chart">
                {fig3.to_html(full_html=False, include_plotlyjs='cdn') if metrics["code_churn_hotspots"] else "<p>No churn data available</p>"}
            </div>
            
            <div class="chart">
                {fig4.to_html(full_html=False, include_plotlyjs='cdn')}
            </div>
            
            <h2>📈 Top Contributors</h2>
            <table style="width: 100%; border-collapse: collapse;">
                <tr style="background: #4CAF50; color: white;">
                    <th style="padding: 10px;">Contributor</th>
                    <th style="padding: 10px;">Commits</th>
                    <th style="padding: 10px;">Lines Changed</th>
                </tr>
                {''.join([f"<tr><td style='padding: 8px; border-bottom: 1px solid #ddd;'>{name}</td><td style='padding: 8px; border-bottom: 1px solid #ddd;'>{commits}</td><td style='padding: 8px; border-bottom: 1px solid #ddd;'>{lines}</td></tr>" 
                          for (name, commits), (_, lines) in zip(metrics["top_contributors_commits"][:5], 
                                                                metrics["top_contributors_lines"][:5])])}
            </table>
            
            <h2>🔥 Top 5 Code Churn Hotspots (Last 30 Days)</h2>
            <table style="width: 100%; border-collapse: collapse;">
                <tr style="background: #ff9800; color: white;">
                    <th style="padding: 10px;">File</th>
                    <th style="padding: 10px;">Changes</th>
                    <th style="padding: 10px;">Lines Changed</th>
                </tr>
                {''.join([f"<tr><td style='padding: 8px; border-bottom: 1px solid #ddd;'>{hotspot['file'][:50]}</td><td style='padding: 8px; border-bottom: 1px solid #ddd;'>{hotspot['change_count']}</td><td style='padding: 8px; border-bottom: 1px solid #ddd;'>{hotspot['total_lines_changed']}</td></tr>" 
                          for hotspot in metrics["code_churn_hotspots"][:5]])}
            </table>
        </div>
    </body>
    </html>
    """
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)