#!/usr/bin/env python3
"""
PyDriller Example Script for Analyzing the SWE-agent Repository

This script demonstrates various ways to use PyDriller to extract information
from the SWE-agent Git repository.
"""

from pydriller import Repository
from datetime import datetime

# Path to the SWE-agent repository
REPO_PATH = '/home/rober/Desktop/Security_smells_thesis/swe-agent-repo/SWE-agent'


def example_1_basic_commit_info():
    """Print basic information about the last 10 commits"""
    print("=" * 80)
    print("EXAMPLE 1: Basic Commit Information (Last 10 commits)")
    print("=" * 80)
    
    count = 0
    for commit in Repository(REPO_PATH).traverse_commits():
        print(f"\nCommit: {commit.hash}")
        print(f"Author: {commit.author.name} <{commit.author.email}>")
        print(f"Date: {commit.author_date}")
        print(f"Message: {commit.msg[:100]}...")  # First 100 chars
        print(f"Files changed: {commit.files}")
        print(f"Insertions: {commit.insertions}, Deletions: {commit.deletions}")
        
        count += 1
        if count >= 10:
            break


def example_2_modified_files():
    """Show modified files in recent commits"""
    print("\n" + "=" * 80)
    print("EXAMPLE 2: Modified Files in Last 5 Commits")
    print("=" * 80)
    
    count = 0
    for commit in Repository(REPO_PATH).traverse_commits():
        print(f"\n[{commit.hash[:8]}] {commit.msg[:50]}")
        for file in commit.modified_files:
            print(f"  - {file.change_type.name}: {file.filename}")
            print(f"    Added: {file.added_lines}, Deleted: {file.deleted_lines}")
        
        count += 1
        if count >= 5:
            break


def example_3_filter_by_author():
    """Filter commits by a specific author"""
    print("\n" + "=" * 80)
    print("EXAMPLE 3: Filter Commits by Author")
    print("=" * 80)
    
    # First, find the most active author
    authors = {}
    for commit in Repository(REPO_PATH).traverse_commits():
        author_name = commit.author.name
        authors[author_name] = authors.get(author_name, 0) + 1
    
    if authors:
        most_active_author = max(authors, key=authors.get)
        print(f"\nMost active author: {most_active_author} ({authors[most_active_author]} commits)")
        
        # Show last 5 commits from this author
        print(f"\nLast 5 commits from {most_active_author}:")
        count = 0
        for commit in Repository(REPO_PATH, only_authors=[most_active_author]).traverse_commits():
            print(f"  [{commit.author_date.strftime('%Y-%m-%d')}] {commit.msg[:60]}")
            count += 1
            if count >= 5:
                break


def example_4_filter_by_date():
    """Filter commits by date range"""
    print("\n" + "=" * 80)
    print("EXAMPLE 4: Filter Commits by Date (Last 30 days)")
    print("=" * 80)
    
    since_date = datetime(2024, 11, 1)
    to_date = datetime(2024, 12, 7)
    
    commits_in_range = []
    for commit in Repository(REPO_PATH, since=since_date, to=to_date).traverse_commits():
        commits_in_range.append(commit)
    
    print(f"\nCommits between {since_date.date()} and {to_date.date()}: {len(commits_in_range)}")
    
    if commits_in_range:
        print("\nFirst 5 commits in this range:")
        for commit in commits_in_range[:5]:
            print(f"  [{commit.author_date.strftime('%Y-%m-%d')}] {commit.hash[:8]} - {commit.msg[:60]}")


def example_5_filter_by_filepath():
    """Filter commits that modified specific files"""
    print("\n" + "=" * 80)
    print("EXAMPLE 5: Commits that Modified Specific Files (e.g., Python files in sweagent/)")
    print("=" * 80)
    
    target_path = "sweagent/"
    commits_found = []
    
    count = 0
    for commit in Repository(REPO_PATH, filepath=target_path).traverse_commits():
        commits_found.append(commit)
        count += 1
        if count >= 10:
            break
    
    print(f"\nFound {len(commits_found)} commits (showing first 10)")
    for commit in commits_found:
        print(f"\n[{commit.hash[:8]}] {commit.author.name} - {commit.author_date.strftime('%Y-%m-%d')}")
        print(f"  Message: {commit.msg[:60]}")
        # Show which files in the path were modified
        for file in commit.modified_files:
            if target_path in file.new_path or (file.old_path and target_path in file.old_path):
                print(f"    {file.change_type.name}: {file.filename}")


def example_6_code_complexity():
    """Analyze code complexity of modified files"""
    print("\n" + "=" * 80)
    print("EXAMPLE 6: Code Complexity Analysis (Last 5 commits)")
    print("=" * 80)
    
    count = 0
    for commit in Repository(REPO_PATH).traverse_commits():
        print(f"\n[{commit.hash[:8]}] {commit.msg[:50]}")
        
        for file in commit.modified_files:
            # Only analyze Python files
            if file.filename and file.filename.endswith('.py'):
                if file.complexity:
                    print(f"  {file.filename}:")
                    print(f"    Complexity: {file.complexity}")
                    print(f"    LOC: {file.nloc}")
                    if file.methods:
                        print(f"    Methods: {len(file.methods)}")
        
        count += 1
        if count >= 5:
            break


def example_7_diff_analysis():
    """Show diff information for modified files"""
    print("\n" + "=" * 80)
    print("EXAMPLE 7: Diff Analysis (Last 3 commits)")
    print("=" * 80)
    
    count = 0
    for commit in Repository(REPO_PATH).traverse_commits():
        print(f"\n[{commit.hash[:8]}] {commit.msg[:50]}")
        
        for file in commit.modified_files[:3]:  # Limit to first 3 files per commit
            print(f"\n  File: {file.filename}")
            print(f"  Change Type: {file.change_type.name}")
            
            if file.diff_parsed:
                added = file.diff_parsed['added']
                deleted = file.diff_parsed['deleted']
                
                if added:
                    print(f"    Added lines: {len(added)}")
                    # Show first 2 added lines
                    for line_no, line_content in list(added)[:2]:
                        print(f"      +{line_no}: {line_content[:70]}")
                
                if deleted:
                    print(f"    Deleted lines: {len(deleted)}")
                    # Show first 2 deleted lines
                    for line_no, line_content in list(deleted)[:2]:
                        print(f"      -{line_no}: {line_content[:70]}")
        
        count += 1
        if count >= 3:
            break


def example_8_statistics():
    """Generate repository statistics"""
    print("\n" + "=" * 80)
    print("EXAMPLE 8: Repository Statistics")
    print("=" * 80)
    
    total_commits = 0
    total_authors = set()
    total_files_changed = 0
    total_insertions = 0
    total_deletions = 0
    file_types = {}
    
    # Analyze last 100 commits for stats
    for commit in Repository(REPO_PATH).traverse_commits():
        total_commits += 1
        total_authors.add(commit.author.name)
        total_files_changed += commit.files
        total_insertions += commit.insertions
        total_deletions += commit.deletions
        
        # Track file types
        for file in commit.modified_files:
            if file.filename:
                ext = file.filename.split('.')[-1] if '.' in file.filename else 'no_ext'
                file_types[ext] = file_types.get(ext, 0) + 1
        
        if total_commits >= 100:
            break
    
    print(f"\nStatistics from last {total_commits} commits:")
    print(f"  Unique authors: {len(total_authors)}")
    print(f"  Total files changed: {total_files_changed}")
    print(f"  Total insertions: {total_insertions}")
    print(f"  Total deletions: {total_deletions}")
    print(f"  Net changes: {total_insertions - total_deletions}")
    
    print(f"\nTop 10 most modified file types:")
    sorted_types = sorted(file_types.items(), key=lambda x: x[1], reverse=True)
    for ext, count in sorted_types[:10]:
        print(f"  .{ext}: {count} changes")


def main():
    """Run all examples"""
    print("\n" + "=" * 80)
    print("PyDriller Analysis of SWE-agent Repository")
    print("=" * 80)
    
    # Uncomment the examples you want to run:
    
    example_1_basic_commit_info()
    # example_2_modified_files()
    # example_3_filter_by_author()
    # example_4_filter_by_date()
    # example_5_filter_by_filepath()
    # example_6_code_complexity()
    # example_7_diff_analysis()
    # example_8_statistics()
    
    print("\n" + "=" * 80)
    print("Analysis complete!")
    print("=" * 80)


if __name__ == "__main__":
    main()
