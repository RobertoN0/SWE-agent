# PyDriller Guide for SWE-agent Repository Analysis

## Overview
PyDriller is a Python framework for mining Git repositories. It allows you to extract detailed information about commits, developers, modifications, diffs, and source code metrics.

## Installation

### Option 1: Virtual Environment (Recommended)
```bash
# Create a virtual environment
python3 -m venv venv_pydriller

# Activate it
source venv_pydriller/bin/activate

# Install PyDriller
pip install pydriller
```

### Option 2: System-wide (if allowed)
```bash
pip install pydriller
```

### Requirements
- Python 3.4 or newer
- Git installed on your system

## Basic Usage

### Simple Example
```python
from pydriller import Repository

# Analyze the SWE-agent repository
for commit in Repository('/path/to/SWE-agent').traverse_commits():
    print(f'Hash: {commit.hash}, Author: {commit.author.name}')
```

## Key Features & Commands

### 1. **Commit Information**

Access comprehensive commit metadata:

```python
from pydriller import Repository

for commit in Repository('path/to/repo').traverse_commits():
    # Basic info
    print(commit.hash)              # Commit hash
    print(commit.msg)                # Commit message
    print(commit.author.name)        # Author name
    print(commit.author.email)       # Author email
    print(commit.author_date)        # Author date
    print(commit.committer.name)     # Committer name
    print(commit.committer_date)     # Commit date
    
    # Statistics
    print(commit.insertions)         # Lines added
    print(commit.deletions)          # Lines deleted
    print(commit.files)              # Number of files changed
    print(commit.lines)              # Total lines (add + delete)
    
    # Context
    print(commit.branches)           # Branches containing this commit
    print(commit.in_main_branch)     # Boolean: is in main branch
    print(commit.merge)              # Boolean: is merge commit
    print(commit.parents)            # List of parent commit hashes
```

### 2. **Filter Commits by Date**

```python
from datetime import datetime
from pydriller import Repository

# Commits in a specific date range
since = datetime(2024, 1, 1)
to = datetime(2024, 12, 31)

for commit in Repository('path/to/repo', since=since, to=to).traverse_commits():
    print(f'{commit.author_date}: {commit.msg}')
```

### 3. **Filter by Author**

```python
from pydriller import Repository

# Only commits by specific authors
for commit in Repository('path/to/repo', 
                        only_authors=['John Doe', 'Jane Smith']).traverse_commits():
    print(f'{commit.author.name}: {commit.msg}')
```

### 4. **Filter by File Path**

```python
from pydriller import Repository

# Only commits that modified specific files/paths
for commit in Repository('path/to/repo', 
                        filepath='sweagent/agent/').traverse_commits():
    print(f'{commit.hash}: Modified files in sweagent/agent/')
```

### 5. **Filter by Commit Range**

```python
from pydriller import Repository

# Between two specific commits
for commit in Repository('path/to/repo',
                        from_commit='abc123',
                        to_commit='def456').traverse_commits():
    print(commit.hash)

# Or from a specific commit tag
for commit in Repository('path/to/repo',
                        from_tag='v1.0').traverse_commits():
    print(commit.hash)
```

### 6. **Modified Files Analysis**

Each commit contains a list of modified files with detailed information:

```python
from pydriller import Repository

for commit in Repository('path/to/repo').traverse_commits():
    for file in commit.modified_files:
        # File paths
        print(file.old_path)          # Path before change
        print(file.new_path)          # Path after change
        print(file.filename)          # Just the filename
        
        # Change type
        print(file.change_type.name)  # ADD, DELETE, MODIFY, or RENAME
        
        # Line changes
        print(file.added_lines)       # Number of lines added
        print(file.deleted_lines)     # Number of lines deleted
        
        # Source code
        print(file.source_code)       # Current source code
        print(file.source_code_before) # Source before change
        
        # Metrics
        print(file.nloc)              # Lines of code
        print(file.complexity)        # Cyclomatic complexity
        print(file.token_count)       # Number of tokens
        
        # Methods (for supported languages)
        print(file.methods)           # List of all methods
        print(file.methods_before)    # Methods before change
        print(file.changed_methods)   # Only changed methods
```

### 7. **Diff Analysis**

Access detailed diff information:

```python
from pydriller import Repository

for commit in Repository('path/to/repo').traverse_commits():
    for file in commit.modified_files:
        # Raw diff (like git diff)
        print(file.diff)
        
        # Parsed diff
        if file.diff_parsed:
            # Added lines: list of (line_number, line_content)
            for line_no, content in file.diff_parsed['added']:
                print(f'+{line_no}: {content}')
            
            # Deleted lines: list of (line_number, line_content)
            for line_no, content in file.diff_parsed['deleted']:
                print(f'-{line_no}: {content}')
```

### 8. **Code Complexity & Metrics**

Analyze code complexity using Lizard (supports many languages):

```python
from pydriller import Repository

for commit in Repository('path/to/repo').traverse_commits():
    for file in commit.modified_files:
        if file.filename.endswith('.py'):
            print(f'File: {file.filename}')
            print(f'Complexity: {file.complexity}')
            print(f'LOC: {file.nloc}')
            print(f'Token count: {file.token_count}')
            
            # Method-level analysis
            for method in file.methods:
                print(f'  Method: {method.name}')
                print(f'  Complexity: {method.complexity}')
                print(f'  LOC: {method.nloc}')
                print(f'  Parameters: {len(method.parameters)}')
```

### 9. **Branch Analysis**

```python
from pydriller import Repository

# Only commits in specific branches
for commit in Repository('path/to/repo', 
                        only_in_branch='main').traverse_commits():
    print(commit.hash)

# Get all branches containing a commit
for commit in Repository('path/to/repo').traverse_commits():
    print(f'{commit.hash} is in branches: {commit.branches}')
```

### 10. **Multiple Repositories**

Analyze multiple repositories in sequence:

```python
from pydriller import Repository

repos = [
    'path/to/repo1',
    'path/to/repo2',
    'https://github.com/user/repo3.git'  # Can also use remote URLs
]

for commit in Repository(path_to_repo=repos).traverse_commits():
    print(f'{commit.project_path}: {commit.hash}')
```

## Advanced Filtering

### Combine Multiple Filters

```python
from datetime import datetime
from pydriller import Repository

# Multiple filters together
for commit in Repository(
    path_to_repo='path/to/repo',
    since=datetime(2024, 1, 1),
    to=datetime(2024, 12, 31),
    only_authors=['John Doe'],
    only_in_branch='main',
    filepath='sweagent/',
    only_no_merge=True  # Exclude merge commits
).traverse_commits():
    print(commit.hash)
```

### Filter by Commit Message

```python
from pydriller import Repository
import re

pattern = re.compile(r'fix|bug', re.IGNORECASE)

for commit in Repository('path/to/repo').traverse_commits():
    if pattern.search(commit.msg):
        print(f'Bug fix: {commit.hash} - {commit.msg}')
```

### Filter by Modifications

```python
from pydriller import Repository

# Only commits that modified Python files
for commit in Repository('path/to/repo').traverse_commits():
    python_files = [f for f in commit.modified_files 
                   if f.filename and f.filename.endswith('.py')]
    if python_files:
        print(f'{commit.hash}: Modified {len(python_files)} Python files')
```

## Common Use Cases

### 1. Repository Statistics

```python
from pydriller import Repository
from collections import defaultdict

stats = {
    'total_commits': 0,
    'authors': set(),
    'files_changed': 0,
    'insertions': 0,
    'deletions': 0
}

for commit in Repository('path/to/repo').traverse_commits():
    stats['total_commits'] += 1
    stats['authors'].add(commit.author.name)
    stats['files_changed'] += commit.files
    stats['insertions'] += commit.insertions
    stats['deletions'] += commit.deletions

print(f"Total commits: {stats['total_commits']}")
print(f"Unique authors: {len(stats['authors'])}")
print(f"Total insertions: {stats['insertions']}")
print(f"Total deletions: {stats['deletions']}")
```

### 2. Find Most Active Contributors

```python
from pydriller import Repository
from collections import Counter

authors = Counter()

for commit in Repository('path/to/repo').traverse_commits():
    authors[commit.author.name] += 1

# Top 10 contributors
for author, count in authors.most_common(10):
    print(f'{author}: {count} commits')
```

### 3. Track File History

```python
from pydriller import Repository

def get_file_history(repo_path, filepath):
    """Get all commits that modified a specific file"""
    history = []
    
    for commit in Repository(repo_path, filepath=filepath).traverse_commits():
        for mod in commit.modified_files:
            if filepath in (mod.new_path or '') or filepath in (mod.old_path or ''):
                history.append({
                    'hash': commit.hash,
                    'date': commit.author_date,
                    'author': commit.author.name,
                    'message': commit.msg,
                    'change_type': mod.change_type.name,
                    'added': mod.added_lines,
                    'deleted': mod.deleted_lines
                })
    
    return history

# Usage
history = get_file_history('/path/to/repo', 'sweagent/agent/agent.py')
for entry in history:
    print(f"{entry['date']}: {entry['message'][:50]}")
```

### 4. Code Churn Analysis

```python
from pydriller import Repository
from collections import defaultdict

# Track how much each file changes
file_churn = defaultdict(lambda: {'adds': 0, 'dels': 0, 'commits': 0})

for commit in Repository('path/to/repo').traverse_commits():
    for file in commit.modified_files:
        if file.new_path:
            file_churn[file.new_path]['adds'] += file.added_lines
            file_churn[file.new_path]['dels'] += file.deleted_lines
            file_churn[file.new_path]['commits'] += 1

# Files with highest churn
sorted_files = sorted(file_churn.items(), 
                     key=lambda x: x[1]['adds'] + x[1]['dels'], 
                     reverse=True)

print("Top 10 files by churn:")
for filepath, stats in sorted_files[:10]:
    total_churn = stats['adds'] + stats['dels']
    print(f"{filepath}: {total_churn} lines changed in {stats['commits']} commits")
```

### 5. Find Security-Related Changes

```python
from pydriller import Repository
import re

security_keywords = ['security', 'vulnerability', 'cve', 'exploit', 
                    'sanitize', 'validate', 'injection', 'xss']

pattern = re.compile('|'.join(security_keywords), re.IGNORECASE)

security_commits = []

for commit in Repository('/home/rober/Desktop/Security_smells_thesis/swe-agent-repo/SWE-agent').traverse_commits():
    if pattern.search(commit.msg):
        security_commits.append({
            'hash': commit.hash,
            'date': commit.author_date,
            'author': commit.author.name,
            'message': commit.msg,
            'files': [f.filename for f in commit.modified_files]
        })

print(f"Found {len(security_commits)} security-related commits")
for sc in security_commits:
    print(f"\n{sc['hash'][:8]} - {sc['date']}")
    print(f"  {sc['message'][:100]}")
```

## Configuration Options

### Git Diff Algorithms

```python
from pydriller import Repository

# Use different diff algorithms
repo = Repository('path/to/repo', histogram_diff=True)  # Histogram algorithm
repo = Repository('path/to/repo', histogram_diff=False) # Default algorithm
```

### Skip Whitespace Changes

```python
from pydriller import Repository

# Ignore whitespace in diffs
repo = Repository('path/to/repo', skip_whitespaces=True)
```

### Order Commits

```python
from pydriller import Repository

# Order by date (default)
repo = Repository('path/to/repo', order='date-order')

# Topological order
repo = Repository('path/to/repo', order='topo-order')

# Author date order
repo = Repository('path/to/repo', order='author-date-order')

# Reverse order
repo = Repository('path/to/repo', order='reverse')
```

## Information You Can Extract

### From Commits:
- Hash, message, author, committer
- Dates and timezones
- Parent commits
- Branches
- Insertions/deletions/files changed
- Whether it's a merge commit
- Project name and path
- Delta Maintainability Model (DMM) metrics

### From Modified Files:
- File paths (old and new)
- Change type (ADD, DELETE, MODIFY, RENAME)
- Diff (raw and parsed)
- Source code (before and after)
- Number of lines added/deleted
- Code metrics (LOC, complexity, token count)
- Methods and their metrics
- Changed methods only

### From Methods (in supported languages):
- Method name
- Parameters
- Lines of code
- Cyclomatic complexity
- Token count
- Start and end line numbers

## Example Script Location

A complete example script with 8 different analysis examples is available at:
```
/home/rober/Desktop/Security_smells_thesis/swe-agent-repo/SWE-agent/pydriller_example.py
```

Run it with:
```bash
source venv_pydriller/bin/activate
python pydriller_example.py
```

## Documentation

Full documentation available at: https://pydriller.readthedocs.io/

### Key Pages:
- **Overview/Install**: https://pydriller.readthedocs.io/en/latest/intro.html
- **Getting Started**: https://pydriller.readthedocs.io/en/latest/tutorial.html
- **Repository API**: https://pydriller.readthedocs.io/en/latest/repository.html
- **Commit API**: https://pydriller.readthedocs.io/en/latest/commit.html
- **ModifiedFile API**: https://pydriller.readthedocs.io/en/latest/modifiedfile.html
- **API Reference**: https://pydriller.readthedocs.io/en/latest/reference.html

## Tips

1. **Performance**: Iterating through all commits can be slow for large repos. Use filters to limit the scope.

2. **Memory**: PyDriller uses a generator pattern, so it's memory-efficient even for large repositories.

3. **Remote Repos**: You can analyze remote repositories by URL. PyDriller will clone them temporarily.

4. **Language Support**: Code metrics work for many languages (Python, Java, C++, JavaScript, etc.) via Lizard.

5. **Merge Commits**: The modified_files list might be empty for merge commits. Use `only_no_merge=True` to skip them.

6. **Export to CSV**: You can easily export data to CSV for further analysis using Python's csv module.

## Quick Reference

```python
from pydriller import Repository

# Basic iteration
for commit in Repository('path').traverse_commits():
    pass

# Common filters
Repository(path, 
          since=datetime,           # Start date
          to=datetime,              # End date
          from_commit='hash',       # Start from commit
          to_commit='hash',         # End at commit
          from_tag='v1.0',          # Start from tag
          to_tag='v2.0',            # End at tag
          only_in_branch='main',    # Specific branch
          only_authors=['name'],    # Specific authors
          only_no_merge=True,       # Skip merges
          filepath='path/',         # Specific files
          skip_whitespaces=True,    # Ignore whitespace
          order='date-order')       # Commit ordering
```
