import subprocess
from pathlib import Path
from pprint import pprint

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
            if short_sha: #only commit if this is full
                commit = {
                    "short_sha": short_sha,
                    "subject": subject.strip()
                }
                if body.strip():
                    commit["body"] = body.strip()
                commits.append(commit)
        return commits[::-1]
    
    def reformat_commits_for_llm(self, commits):
        """
        Reformats the commits list into a string suitable for LLM prompts.
        Each commit is shown as:
        1. subject
        Description: body (if present)
        """
        lines = []
        for i, c in enumerate(commits, start=1):  # latest changes shown first
            lines.append(f"{i}. {c['subject']}")
            if c.get("body"):
                lines.append(f"   Description: {c['body']}")
        return "\n".join(lines)
                         
    def get_repo_context():
        # TO DO LATER: CONNECT TO GITHUB API TO GET REPO ABOUT SECTION
        pass

if __name__ == "__main__":
    #last_sha = "dc77e8e"
    last_sha = ""
    git_checker = GitChecker()

    commits = git_checker.get_commits_since(last_sha=last_sha)
    if commits:
        pprint(commits)
        print(git_checker.reformat_commits_for_llm(commits))
    else:
        print("No new commits since last.")