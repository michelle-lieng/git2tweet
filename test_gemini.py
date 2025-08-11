import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load API key from .env
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise RuntimeError("Missing GEMINI_API_KEY in .env")

# Configure Gemini
genai.configure(api_key=api_key)

# Create model
model = genai.GenerativeModel(
    "gemini-1.5-flash",
    generation_config={
        "temperature": 0.7,         # creativity (0.0 = deterministic, 1.0 = more random)
        "max_output_tokens": 70,   # ~rough max words/tokens, 1 token ≈ 4 chars in English => 200 characters
        "top_p": 0.9,               # nucleus sampling
        "top_k": 40                 # limits sampling pool
    }
)

# Example commits and daynumber for testing
# commits = """initial commit (321368c)
# simple initial layout + set up basic code to test the twitter api
# """
commits = "Integrated follow up github repo tweet - enabled now that the following tweet in the thread is the github repo link of the repo updated"
daynumber = 2
project_context="""
Git2tweet is a github to twitter bot that automatically scans my github repo for latest commits,
creates a viral twitter post for the #100daysofcode challenge and posts it.
"""

# Send a test prompt
prompt = prompt = f"""
You are an expert viral Twitter copywriter.

Commits:
<<COMMITS>>
{commits}
<<END>>

Project context:
<<CONTEXT>>
{project_context}
<<END>>

Write ONE tweet.

Hard rules (must follow exactly):
- Start with: "Day {daynumber} of #100DaysOfCode " then a single emoji.
- Then insert exactly ONE newline (\n).
- After that, write the rest of the tweet.
- Use 1–3 relevant emojis total.
- You may include other relevant hashtags, but #100DaysOfCode must only appear once at the start of the tweet.
- Keep it ≤ 280 characters total.
- Output ONLY the tweet text. No quotes, no prefixes, no explanations.
"""
# TO DO LATER: Fix problems with the double #100daysofcode hashtag sometimes due to the projext context

response = model.generate_content(prompt)

# Print output
print("Gemini output:")
print(response.text)
