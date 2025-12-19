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