import git
from datetime import datetime, timedelta
from collections import defaultdict, Counter
import re
from typing import Dict, List, Tuple, Any
import pandas as pd

class GitCommitAnalyzer:
    def __init__(self, repo_path: str, max_commits: int = 500):
        self.repo = git.Repo(repo_path)
        self.max_commits = max_commits
        self.commits = []
        
    def analyze(self) -> Dict[str, Any]:
        self._collect_commits()
        
        return {
            "total_commits_analyzed": len(self.commits),
            "commits_per_day": self._commits_per_day(),
            "commits_per_week": self._commits_per_week(),
            "top_contributors_commits": self._top_contributors_by_commits(),
            "top_contributors_lines": self._top_contributors_by_lines(),
            "conventional_commit_percent": self._conventional_commit_percent(),
            "avg_pr_size_files": self._avg_pr_size_files(),
            "avg_pr_size_lines": self._avg_pr_size_lines(),
            "code_churn_hotspots": self._code_churn_hotspots(),
        }
    
    def _collect_commits(self):
        for commit in self.repo.iter_commits(max_count=self.max_commits):
            stats = commit.stats.total
            self.commits.append({
                "hexsha": commit.hexsha,
                "author": commit.author.name,
                "email": commit.author.email,
                "date": commit.committed_datetime,
                "message": commit.message,
                "files_changed": len(commit.stats.files),
                "lines_added": stats.get('insertions', 0),
                "lines_deleted": stats.get('deletions', 0),
                "files": list(commit.stats.files.keys())
            })
    
    def _commits_per_day(self) -> Dict[str, int]:
        by_day = defaultdict(int)
        for commit in self.commits:
            day = commit["date"].strftime("%Y-%m-%d")
            by_day[day] += 1
        return dict(sorted(by_day.items()))
    
    def _commits_per_week(self) -> Dict[str, int]:
        by_week = defaultdict(int)
        for commit in self.commits:
            week = commit["date"].strftime("%Y-W%W")
            by_week[week] += 1
        return dict(sorted(by_week.items()))
    
    def _top_contributors_by_commits(self) -> List[Tuple[str, int]]:
        contributor_commits = defaultdict(int)
        for commit in self.commits:
            contributor_commits[commit["author"]] += 1
        return sorted(contributor_commits.items(), key=lambda x: x[1], reverse=True)[:10]
    
    def _top_contributors_by_lines(self) -> List[Tuple[str, int]]:
        contributor_lines = defaultdict(int)
        for commit in self.commits:
            total_lines = commit["lines_added"] + commit["lines_deleted"]
            contributor_lines[commit["author"]] += total_lines
        return sorted(contributor_lines.items(), key=lambda x: x[1], reverse=True)[:10]
    
    def _conventional_commit_percent(self) -> float:
        pattern = r'^(feat|fix|docs|style|refactor|perf|test|chore)(\(.+\))?:'
        conventional_count = 0
        
        for commit in self.commits:
            first_line = commit["message"].split('\n')[0].strip()
            if re.match(pattern, first_line):
                conventional_count += 1
        
        if len(self.commits) == 0:
            return 0.0
        return (conventional_count / len(self.commits)) * 100
    
    def _avg_pr_size_files(self) -> float:
        if len(self.commits) == 0:
            return 0.0
        total_files = sum(c["files_changed"] for c in self.commits)
        return total_files / len(self.commits)
    
    def _avg_pr_size_lines(self) -> float:
        if len(self.commits) == 0:
            return 0.0
        total_lines = sum(c["lines_added"] + c["lines_deleted"] for c in self.commits)
        return total_lines / len(self.commits)
    
    def _code_churn_hotspots(self) -> List[Dict[str, Any]]:
        from datetime import timezone
        
        cutoff_date = datetime.now(timezone.utc) - timedelta(days=30)
        file_changes = defaultdict(lambda: {"count": 0, "lines_changed": 0})
        
        for commit in self.commits:
            commit_date = commit["date"]
            if commit_date.tzinfo is None:
                commit_date = commit_date.replace(tzinfo=timezone.utc)
            
            if commit_date >= cutoff_date:
                for file in commit["files"]:
                    file_changes[file]["count"] += 1
                    file_changes[file]["lines_changed"] += (
                        commit["lines_added"] + commit["lines_deleted"]
                    )
        
        sorted_files = sorted(
            file_changes.items(),
            key=lambda x: x[1]["count"],
            reverse=True
        )[:10]
        
        return [
            {
                "file": file,
                "change_count": data["count"],
                "total_lines_changed": data["lines_changed"]
            }
            for file, data in sorted_files
        ]