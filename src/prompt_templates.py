"""
This is where all the llm prompt templates for our
tweet generator will be.
"""

class TwitterPromptTemplates:
    """
    This prompt template is specifically for the #100daysofcode 
    challenge.

    TO DO LATER: Fix problems with the double #100daysofcode hashtag 
    sometimes due to the projext context
    """
    @staticmethod
    def challenge_100_days_of_code_prompt(commits: str = None,
                                          project_context: str = None,
                                          day_number: int = 1
                                          ) -> str:
        return f"""
You are an expert viral Twitter copywriter.

You will look at my commits + project context and summarise ONLY what I accomplished today 
into a high-quality post for my #100DaysOfCode challenge. Also give a bit of context of the project too.

IMPORTANT:
- DO NOT mention or hint at future plans, next steps, or what I will do next.
- ONLY describe what I did today.

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
- Start with: "Day {day_number} of #100DaysOfCode " then a single emoji.
- Then insert exactly ONE newline (\n).
- After that, write the rest of the tweet.
- Use 1–3 relevant emojis total.
- You may include other relevant hashtags, but #100DaysOfCode must only appear once at the start of the tweet.
- Keep it ≤ 280 characters total.
- Output ONLY the tweet text. No quotes, no prefixes, no explanations.
"""
