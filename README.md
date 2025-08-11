# Github to Twitter Bot

My current usecase is to set up a bot that can automatically summarise all my latest github changes and format a post for twitter for my #100daysofcode challenge.

## Setting up Twitter/X API Keys

To post tweets, you need API keys and access tokens from the Twitter Developer Portal.

1. Create a Developer Account: Go to developer.x.com and sign in with your Twitter/X account.
2. In the Developer Portal, click Projects & Apps → Overview → Add App.
3. Then name your app (e.g., 100DaysBot) + select Bot.
4. Go to your app’s Settings → User authentication settings and turn on.
5. Set App permissions to Read and write, fill in a Callback URL (can be http://localhost:3000 for testing) and add a Website URL (e.g., your GitHub profile). Click save.
6. Generate Your neccessary keys and tokens to save to the .env file.
