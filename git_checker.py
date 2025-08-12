import subprocess
from pathlib import Path

class GitChecker:
    def __init__(self, repo_path: str = "."):
        self.repo_path = Path(repo_path) #default to run git in the current folder (this repo)

    def get_commits_since(self, last_sha=None):
        """
        Return a list of commit messages (and shas) since last_sha.

        How does this work?
        -------------------
        Typing `git log  --pretty="%s||%h||%b"` into terminal outputs the commits like:
        commit name||SHA||commit description
        commit name2||SHA2||commit description2

        You can also specify get get all commits since the last SHA:
        E.g. typing `git log dc77e8e..HEAD --pretty="%s||%h||%b"`
        created test for llm to generate tweet||ba128b3|| added gemini test
        """
        fmt = "%s||%h||%b"  # commit subject || short SHA || body
        command = ["git", "log", f"--pretty={fmt}"]

        if last_sha:
            command.insert(2, f"{last_sha}..HEAD")
        else:
            # default: all commits
            pass

        out = subprocess.check_output(command, cwd=self.repo_path, text=True).strip()
        commits = []
        for line in out.splitlines():
            subject, short_sha, body = (line.split("||") + ["", ""])[:3]
            commits.append({
                "subject": subject.strip(),
                "short_sha": short_sha,
                "body": body.strip()
            })
        return commits
    
    def get_repo_context():
        # TO DO LATER: CONNECT TO GITHUB API TO GET REPO ABOUT SECTION
        pass

if __name__ == "__main__":
    #last_sha = "dc77e8e"
    last_sha = ""

    git_checker = GitChecker()

    if last_sha:
        commits = git_checker.get_commits_since(last_sha=last_sha)
    else:
        commits = git_checker.get_commits_since()

    if commits:
        print("\nCommits since last:")
        for i,c in enumerate(commits[::-1], start=1): #latest changes shown first
            #print(f"- {c['subject']} ({c['short_sha']})")
            print(f"{i}. {c['subject']}")
            if c['body']:
                print(f"  Description: {c['body']}")
    else:
        print("No new commits since last.")