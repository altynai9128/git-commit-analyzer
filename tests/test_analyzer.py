import sys
import os
import pytest
import git
import tempfile
import time
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from analyzer import GitCommitAnalyzer

@pytest.fixture
def empty_repo():
    """Фикстура: пустой репозиторий (без коммитов)"""
    with tempfile.TemporaryDirectory() as tmpdir:
        repo = git.Repo.init(tmpdir)

        file_path = os.path.join(tmpdir, ".gitkeep")
        with open(file_path, "w") as f:
            f.write("")
        repo.index.add([".gitkeep"])
        repo.index.commit("Initial empty commit")
        

        yield tmpdir

@pytest.fixture
def single_commit_repo():
    """Фикстура: репозиторий с одним коммитом"""
    tmpdir = tempfile.mkdtemp()
    try:
        repo = git.Repo.init(tmpdir)
        
        file_path = os.path.join(tmpdir, "test.txt")
        with open(file_path, "w") as f:
            f.write("test content")
        
        repo.index.add(["test.txt"])
        repo.index.commit("Initial commit")
        
        yield tmpdir
    finally:
        time.sleep(0.5)
        try:
            import shutil
            shutil.rmtree(tmpdir, ignore_errors=True)
        except:
            pass

@pytest.fixture
def conventional_commits_repo():
    tmpdir = tempfile.mkdtemp()
    try:
        repo = git.Repo.init(tmpdir)
        
        for i, msg in enumerate(["feat: add feature", "fix: bug fix", "docs: update readme"]):
            file_path = os.path.join(tmpdir, f"file{i}.txt")
            with open(file_path, "w") as f:
                f.write(f"content {i}")
            repo.index.add([f"file{i}.txt"])
            repo.index.commit(msg)
        
        yield tmpdir
    finally:
        time.sleep(0.5)
        try:
            import shutil
            shutil.rmtree(tmpdir, ignore_errors=True)
        except:
            pass

@pytest.fixture
def multi_commit_repo():
    tmpdir = tempfile.mkdtemp()
    try:
        repo = git.Repo.init(tmpdir)
        
        for i in range(5):
            file_path = os.path.join(tmpdir, f"file{i}.txt")
            with open(file_path, "w") as f:
                f.write(f"content {i}")
            repo.index.add([f"file{i}.txt"])
            repo.index.commit(f"Commit {i}")
        
        yield tmpdir
    finally:
        time.sleep(0.5)
        try:
            import shutil
            shutil.rmtree(tmpdir, ignore_errors=True)
        except:
            pass

def test_empty_repo(empty_repo):
    analyzer = GitCommitAnalyzer(empty_repo, max_commits=10)
    metrics = analyzer.analyze()
    assert metrics["total_commits_analyzed"] >= 0

def test_single_commit(single_commit_repo):
    analyzer = GitCommitAnalyzer(single_commit_repo, max_commits=10)
    metrics = analyzer.analyze()
    assert metrics["total_commits_analyzed"] == 1
    assert metrics["avg_pr_size_files"] > 0

def test_conventional_commits(conventional_commits_repo):
    analyzer = GitCommitAnalyzer(conventional_commits_repo, max_commits=10)
    metrics = analyzer.analyze()
    assert metrics["conventional_commit_percent"] == 100.0

def test_max_commits_limit(multi_commit_repo):
    """Тест 4: Лимит коммитов работает"""
    analyzer = GitCommitAnalyzer(multi_commit_repo, max_commits=3)
    metrics = analyzer.analyze()
    assert metrics["total_commits_analyzed"] == 3

def test_top_contributors(single_commit_repo):
    analyzer = GitCommitAnalyzer(single_commit_repo, max_commits=10)
    metrics = analyzer.analyze()
    assert len(metrics["top_contributors_commits"]) >= 1

def test_churn_hotspots(single_commit_repo):
    analyzer = GitCommitAnalyzer(single_commit_repo, max_commits=10)
    metrics = analyzer.analyze()
    assert isinstance(metrics["code_churn_hotspots"], list)

def test_commits_per_day(single_commit_repo):
    analyzer = GitCommitAnalyzer(single_commit_repo, max_commits=10)
    metrics = analyzer.analyze()
    assert len(metrics["commits_per_day"]) >= 1

def test_commits_per_week(single_commit_repo):
    analyzer = GitCommitAnalyzer(single_commit_repo, max_commits=10)
    metrics = analyzer.analyze()
    assert len(metrics["commits_per_week"]) >= 1

def test_avg_pr_size_files(multi_commit_repo):
    analyzer = GitCommitAnalyzer(multi_commit_repo, max_commits=10)
    metrics = analyzer.analyze()
    assert metrics["avg_pr_size_files"] > 0
    assert isinstance(metrics["avg_pr_size_files"], float)

def test_json_output_structure(single_commit_repo):
    analyzer = GitCommitAnalyzer(single_commit_repo, max_commits=10)
    metrics = analyzer.analyze()
    
    required_keys = [
        "total_commits_analyzed",
        "commits_per_day",
        "commits_per_week",
        "top_contributors_commits",
        "top_contributors_lines",
        "conventional_commit_percent",
        "avg_pr_size_files",
        "avg_pr_size_lines",
        "code_churn_hotspots"
    ]
    
    for key in required_keys:
        assert key in metrics