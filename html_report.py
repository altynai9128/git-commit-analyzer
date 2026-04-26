import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
from typing import Dict, Any
import os
from datetime import datetime

def generate_html_report(metrics: Dict[str, Any], output_file: str):
    output_dir = os.path.dirname(output_file)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
    
    commits_df = pd.DataFrame(list(metrics["commits_per_day"].items()), 
                               columns=["date", "commits"])
    fig1 = px.line(commits_df, x="date", y="commits", 
                   title="📅 Commit Frequency Over Time",
                   labels={"date": "Date", "commits": "Number of Commits"},
                   template="plotly_white",
                   color_discrete_sequence=["#4CAF50"])
    fig1.update_layout(title_font_size=16, title_x=0.5)
    
    contributors = dict(metrics["top_contributors_commits"][:5])  
    fig2 = go.Figure(data=[go.Pie(labels=list(contributors.keys()), 
                                   values=list(contributors.values()),
                                   hole=0.3,
                                   marker=dict(colors=['#4CAF50', '#2196F3', '#FF9800', '#9C27B0', '#F44336']))])
    fig2.update_layout(title="👥 Top 5 Contributors Distribution", title_font_size=16, title_x=0.5)
    
    if metrics["code_churn_hotspots"]:
        churn_df = pd.DataFrame(metrics["code_churn_hotspots"][:8])
        fig3 = px.bar(churn_df, x="file", y="change_count",
                      title="🔥 File Churn Hotspots (last 30 days)",
                      labels={"file": "File", "change_count": "Number of Changes"},
                      color="total_lines_changed",
                      color_continuous_scale="Reds",
                      template="plotly_white")
        fig3.update_layout(title_font_size=16, title_x=0.5, xaxis_tickangle=-45)
    
    weeks_df = pd.DataFrame(list(metrics["commits_per_week"].items()),
                             columns=["week", "commits"])
    fig4 = px.bar(weeks_df, x="week", y="commits",
                  title="📊 Commits per Week",
                  labels={"week": "Week", "commits": "Number of Commits"},
                  color="commits",
                  color_continuous_scale="Blues",
                  template="plotly_white")
    fig4.update_layout(title_font_size=16, title_x=0.5)
    
    contributors_commits = metrics["top_contributors_commits"][:10]
    contributors_lines = metrics["top_contributors_lines"][:10]
    
    contributors_table_rows = ""
    for i in range(min(len(contributors_commits), len(contributors_lines))):
        name = contributors_commits[i][0]
        commits = contributors_commits[i][1]
        lines = contributors_lines[i][1] if i < len(contributors_lines) else 0
        contributors_table_rows += f"""
        <tr>
            <td class="contrib-name">{name}</td>
            <td class="contrib-commits">{commits}</td>
            <td class="contrib-lines">{lines:,}</td>
        </tr>
        """
    
    churn_hotspots = metrics["code_churn_hotspots"][:5]
    churn_table_rows = ""
    for hotspot in churn_hotspots:
        churn_table_rows += f"""
        <tr>
            <td class="file-path">{hotspot['file'][:80]}</td>
            <td class="changes-count">{hotspot['change_count']}</td>
            <td class="lines-changed">{hotspot['total_lines_changed']:,}</td>
        </tr>
        """
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Git Commit History Analyzer Report</title>
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                padding: 40px 20px;
                min-height: 100vh;
            }}
            
            .container {{
                max-width: 1400px;
                margin: 0 auto;
                background: white;
                border-radius: 24px;
                box-shadow: 0 20px 60px rgba(0,0,0,0.15);
                overflow: hidden;
            }}
            
            .header {{
                background: linear-gradient(135deg, #2E7D32 0%, #4CAF50 100%);
                color: white;
                padding: 40px;
                text-align: center;
            }}
            
            .header h1 {{
                font-size: 32px;
                margin-bottom: 10px;
                font-weight: 600;
            }}
            
            .header p {{
                font-size: 14px;
                opacity: 0.9;
            }}
            
            .metrics-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 20px;
                padding: 40px;
                background: #f8f9fa;
            }}
            
            .metric-card {{
                background: white;
                padding: 24px;
                border-radius: 16px;
                text-align: center;
                box-shadow: 0 2px 8px rgba(0,0,0,0.05);
                transition: transform 0.2s, box-shadow 0.2s;
            }}
            
            .metric-card:hover {{
                transform: translateY(-4px);
                box-shadow: 0 8px 24px rgba(0,0,0,0.1);
            }}
            
            .metric-label {{
                font-size: 14px;
                color: #6c757d;
                text-transform: uppercase;
                letter-spacing: 1px;
                margin-bottom: 12px;
            }}
            
            .metric-value {{
                font-size: 48px;
                font-weight: bold;
                color: #2E7D32;
            }}
            
            .metric-unit {{
                font-size: 16px;
                color: #6c757d;
                margin-left: 4px;
            }}
            
            .section {{
                padding: 40px;
                border-bottom: 1px solid #e9ecef;
            }}
            
            .section:last-child {{
                border-bottom: none;
            }}
            
            .section-title {{
                font-size: 24px;
                font-weight: 600;
                color: #2c3e50;
                margin-bottom: 24px;
                padding-bottom: 12px;
                border-bottom: 3px solid #4CAF50;
                display: inline-block;
            }}
            
            .chart {{
                margin: 40px 0;
            }}
            
            .table-wrapper {{
                overflow-x: auto;
                border-radius: 12px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.05);
            }}
            
            table {{
                width: 100%;
                border-collapse: collapse;
                background: white;
            }}
            
            th {{
                background: #2E7D32;
                color: white;
                padding: 14px 16px;
                text-align: left;
                font-weight: 600;
                font-size: 14px;
            }}
            
            td {{
                padding: 12px 16px;
                border-bottom: 1px solid #e9ecef;
                font-size: 14px;
            }}
            
            tr:hover {{
                background: #f8f9fa;
            }}
            
            .contrib-name {{
                font-weight: 500;
                color: #2c3e50;
            }}
            
            .contrib-commits {{
                color: #4CAF50;
                font-weight: 600;
            }}
            
            .contrib-lines {{
                color: #FF9800;
                font-weight: 500;
            }}
            
            .file-path {{
                font-family: 'Courier New', monospace;
                font-size: 13px;
                color: #495057;
            }}
            
            .changes-count {{
                color: #dc3545;
                font-weight: 600;
                text-align: center;
            }}
            
            .lines-changed {{
                color: #6c757d;
                font-weight: 500;
                text-align: right;
            }}
            
            .footer {{
                background: #f8f9fa;
                padding: 20px 40px;
                text-align: center;
                color: #6c757d;
                font-size: 12px;
            }}
            
            @media (max-width: 768px) {{
                body {{
                    padding: 20px 10px;
                }}
                .metrics-grid {{
                    grid-template-columns: 1fr;
                    padding: 20px;
                }}
                .section {{
                    padding: 20px;
                }}
                .section-title {{
                    font-size: 20px;
                }}
                .metric-value {{
                    font-size: 36px;
                }}
            }}
        </style>
        <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>📊 Git Commit History Analyzer</h1>
                <p>Comprehensive repository insights and metrics</p>
                <p style="font-size: 12px; margin-top: 8px;">Generated on {datetime.now().strftime("%B %d, %Y at %H:%M:%S")}</p>
            </div>
            
            <div class="metrics-grid">
                <div class="metric-card">
                    <div class="metric-label">📝 Total Commits Analyzed</div>
                    <div class="metric-value">{metrics["total_commits_analyzed"]:,}</div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">✅ Conventional Commits</div>
                    <div class="metric-value">{metrics["conventional_commit_percent"]:.1f}<span class="metric-unit">%</span></div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">📦 Average PR Size</div>
                    <div class="metric-value">{metrics["avg_pr_size_files"]:.1f}<span class="metric-unit">files</span></div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">📏 Avg Lines per Commit</div>
                    <div class="metric-value">{metrics["avg_pr_size_lines"]:.0f}<span class="metric-unit">lines</span></div>
                </div>
            </div>
            
            <div class="section">
                <div class="section-title">📈 Visualization</div>
                <div class="chart">{fig1.to_html(full_html=False, include_plotlyjs='cdn')}</div>
                <div class="chart">{fig2.to_html(full_html=False, include_plotlyjs='cdn')}</div>
                <div class="chart">{fig3.to_html(full_html=False, include_plotlyjs='cdn') if metrics["code_churn_hotspots"] else "<p style='text-align:center; color:#6c757d;'>No churn data available</p>"}</div>
                <div class="chart">{fig4.to_html(full_html=False, include_plotlyjs='cdn')}</div>
            </div>
            
            <div class="section">
                <div class="section-title">🏆 Top Contributors</div>
                <div class="table-wrapper">
                    <table>
                        <thead>
                            <tr>
                                <th>Contributor</th>
                                <th>Commits</th>
                                <th>Lines Changed</th>
                            </tr>
                        </thead>
                        <tbody>
                            {contributors_table_rows}
                        </tbody>
                    </table>
                </div>
            </div>
            
            <div class="section">
                <div class="section-title">🔥 Code Churn Hotspots (Last 30 Days)</div>
                <div class="table-wrapper">
                    <table>
                        <thead>
                            <tr>
                                <th>File Path</th>
                                <th>Changes</th>
                                <th>Lines Changed</th>
                            </tr>
                        </thead>
                        <tbody>
                            {churn_table_rows if churn_table_rows else "<tr><td colspan='3' style='text-align:center;'>No churn data available</td></tr>"}
                        </tbody>
                    </table>
                </div>
            </div>
            
            <div class="footer">
                <p>Generated by Git Commit History Analyzer | Data based on last {metrics["total_commits_analyzed"]} commits</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)