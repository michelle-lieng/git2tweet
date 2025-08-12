import os
import json
from datetime import datetime

STATE_PATH = "state.json"
INITIAL_STATE = {
    "history": [],
    "latest": {
        "last_overall_post_date": None,
        "current_day_number": 0,
        "latest_posted_sha": None,
        #"per_repo_last_posted_sha": {}, # TODO: MULTIPLE REPO LATER!
        "last_tweet_id": None
    }
}

def extract_latest_sha(path=STATE_PATH):
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(INITIAL_STATE, f, indent=2)
        print(f"Created new state file at {path}")
        return None
    else:
        print(f"State file already exists at {path}")
        with open(path, "r", encoding="utf-8") as f:
            state = json.load(f)
        latest_sha = state.get("latest").get("latest_posted_sha")
        print(f"Latest posted SHA: {latest_sha}")
        return latest_sha
    
def update_state(tweet_id, repo_name, repo_commits, path=STATE_PATH):
    date_today = datetime.now().strftime("%Y-%m-%d")
    with open(path, "r", encoding="utf-8") as f:
        state = json.load(f)
    history = state.get("history")
    day_number = len(history) + 1
    history.append({"date_today": date_today,
                    "day_number": day_number,
                    "tweet_id": tweet_id,
                    "repo": {
                        repo_name: repo_commits
                    }
                    })
    latest = state.get("latest")
    latest["last_overall_post_date"] = date_today
    latest["current_day_number"] = day_number
    latest["latest_posted_sha"] = repo_commits[-1]["short_sha"]
    latest["last_tweet_id"]=  tweet_id
    with open(path, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)
    print("UPDATED!")

if __name__ == "__main__":
    extract_latest_sha()
    repo_commits = [{'body': 'simple initial layout + set up basic code to test the twitter api',
  'short_sha': '321368c',
  'subject': 'initial commit'},
 {'short_sha': 'dc77e8e', 'subject': 'create CHANGELOG.md'},
 {'short_sha': 'ba128b3', 'subject': 'created test for llm to generate tweet'},        
 {'body': 'this code added returns a list of commit messages and descriptions '        
          'since the given last sha',
  'short_sha': 'f7550a2',
  'subject': 'basic script to get last commits since'},
 {'short_sha': 'dbd5bd3', 'subject': 'fix bugs + testing more examples'},
 {'body': 'made the code into a class + updated system prompt to not hint at '
          'future plans',
  'short_sha': 'cb1f274',
  'subject': 'refactored the tweet generator code'},
 {'short_sha': 'd997d7d', 'subject': 'update readme'},
 {'short_sha': 'c1819f0', 'subject': 'reformat to a class'},
 {'short_sha': '3616107', 'subject': 'reformat to a class'}]
    repo_name = "git2tweet"
    update_state("1234",repo_name, repo_commits)