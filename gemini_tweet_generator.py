import os
from dotenv import load_dotenv
import google.generativeai as genai
from prompt_templates import TwitterPromptTemplates

# Load API key from .env
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError("Missing GEMINI_API_KEY in .env")

class GeminiTweetGenerator:
    def __init__(self,
                 api_key: str,
                 model_name: str = "gemini-2.0-flash", 
                 generation_config: dict = {
                                        "temperature": 0.7,         # creativity (0.0 = deterministic, 1.0 = more random)
                                        "max_output_tokens": 70,    # ~rough max words/tokens, 1 token ≈ 4 chars in English => 200 characters
                                        "top_p": 0.9,               # nucleus sampling
                                        "top_k": 40                 # limits sampling pool
                                    },
                 prompt_template: callable = TwitterPromptTemplates.challenge_100_days_of_code_prompt
                 ):
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(
            model_name=model_name,
            generation_config=generation_config
        )
        self.prompt_template = prompt_template
    
    def generate_tweet(self, 
                       commits: str,
                       project_context: str,
                       day_number: int):
        prompt = self.prompt_template(commits=commits, project_context=project_context, day_number=day_number)
        response = self.model.generate_content(prompt)
        return response.text

if __name__ == "__main__":
    # commits = """initial commit (321368c)
    # simple initial layout + set up basic code to test the twitter api
    # """
    #commits = "Integrated follow up github repo tweet - enabled now that the following tweet in the thread is the github repo link of the repo updated"
    commits = """
    1. initial commit
    Description: simple initial layout + set up basic code to test the twitter api
    2. create CHANGELOG.md
    3. created test for llm to generate tweet
    4.
    5. basic script to get last commits since
    Description: this code added returns a list of commit messages and descriptions since the given last sha
    6. fix bugs + testing more examples
    """
    day_number = 1
    project_context="""
    Git2tweet is a github to twitter bot that automatically scans my github repo for latest commits,
    creates a viral twitter post for the #100daysofcode challenge and posts it.
    """

    # Test it out
    generator = GeminiTweetGenerator(api_key=api_key)
    tweet = generator.generate_tweet(commits=commits,
                                     project_context=project_context,
                                     day_number=day_number)
    print(tweet)

