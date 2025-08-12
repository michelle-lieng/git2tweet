import yaml
from git_checker import GitChecker
from post_to_twitter import TwitterClient
from check_state import TweetState
from gemini_tweet_generator import GeminiTweetGenerator
import os
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError("Missing GEMINI_API_KEY in .env")

class Git2TweetBot:
    def __init__(self, config_path:str="config.yaml"):
        self.config = self._load_config(config_path)
        self.start_date = self.config.get("start_date")
        self.repo_path = self.config.get("repo_path")[0]
        self.repo_name = self.config["repo_context"][self.repo_path][0]['Name']
        self.repo_context = self.config["repo_context"][self.repo_path][1]['Context']

    @staticmethod
    def _load_config(path="config.yaml"):
        with open(path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
        return config
    
    def main(self):
        # STEP 1: Check state for last SHA + day number otherwise initialise state.json
        latest_sha, latest_day_number = TweetState().extract_latest_state_info()
        
        # STEP 2: Get all git commits since last SHA
        git_checker = GitChecker(self.repo_path)
        commits = git_checker.get_commits_since(latest_sha)
        reformatted_commits = git_checker.reformat_commits_for_llm(commits)

        print(reformatted_commits)
        print(latest_day_number+1)

        # STEP 3: LLM generate tweet from commits
        tweet = GeminiTweetGenerator(api_key).generate_tweet(reformatted_commits,
                                                    self.repo_context,
                                                    latest_day_number+1)
        
        print(tweet)

        # STEP 4: Post tweet to twitter for #100daysofcode challenge
        user_input = input("Do you want to post this tweet? (y/n): ").strip().lower()
        if user_input == "y":
            tweet_id = TwitterClient().post_tweet(tweet)
            print("Tweet posted!!")
            # update state.json
            TweetState().update_state(tweet_id, 
                                      self.repo_name,
                                      commits)
        else:
            print("Tweet not posted.")

# Usage example
if __name__ == "__main__":
    x = Git2TweetBot()
    config = x._load_config()

    repo_path = config["repo_path"][0]
    print(config["repo_context"][repo_path][0]['Name'])
    x.main()

    