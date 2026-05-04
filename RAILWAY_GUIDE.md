# Railway.app Deployment Guide

This guide will help you deploy the Discord bot to Railway.app, a free/cheap hosting platform that's perfect for Discord bots.

## What is Railway?

Railway is a simple cloud hosting platform that:
- Offers a **free tier** with generous limits
- Auto-deploys from GitHub
- Handles environment variables securely
- Keeps your bot running 24/7
- No credit card required to start

## Prerequisites

- GitHub account (free)
- Discord bot token (you already have this!)
- Railway.app account (create for free)

## Step 1: Push Your Code to GitHub

Your bot code needs to be in a GitHub repository. If it's not already there:

1. Create a new repository on GitHub (or use your existing one)
2. Make sure these files are committed:
   - `discord_bot.py`
   - `add_page.py`
   - `requirements.txt`
   - `.env.example`
   - `.gitignore` (should include `.env`)

3. Push your code:
```bash
git add .
git commit -m "Add Discord bot files"
git push origin main
```

## Step 2: Create Railway Account

1. Go to [Railway.app](https://railway.app)
2. Click **Start Project**
3. Sign in with GitHub (easiest method)
4. Authorize Railway to access your GitHub account

## Step 3: Create New Project on Railway

1. Click **Create New Project**
2. Select **Deploy from GitHub repo**
3. Find and select your repository
4. Railway will automatically detect it's a Python project

## Step 4: Configure Environment Variables

Railway needs your Discord token. Set it up:

1. In the Railway dashboard, go to your project
2. Click on the service/deployment
3. Go to the **Variables** tab
4. Add your environment variables:
   ```
   DISCORD_TOKEN=your_bot_token_here
   ```

**Important:** For Railway, you do NOT need to set `REPO_PATH` because the bot won't be able to access your local NAS files. Instead, you'll use the GitHub API to commit changes. See "GitHub Integration" below.

## Step 5: Modify Bot for Railway (GitHub API Integration)

Since Railway doesn't have access to your local NAS repository, you need to update the bot to use the GitHub API instead of git commands.

I'll create an updated version of `discord_bot.py` that uses PyGithub to commit files directly to your repository via the GitHub API.

You'll need to:

1. **Create a GitHub Personal Access Token:**
   - Go to GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
   - Click **Generate new token (classic)**
   - Select these scopes:
     - `repo` (full control of private repositories)
   - Copy the token

2. **Add to Railway Variables:**
   ```
   DISCORD_TOKEN=your_discord_token
   GITHUB_TOKEN=your_github_token
   GITHUB_REPO=your_username/uncharted-worlds-notes
   ```

3. **Install additional dependency:**
   Update `requirements.txt`:
   ```
   discord.py>=2.3.0
   python-dotenv>=1.0.0
   PyGithub>=2.1.1
   ```

## Step 6: Deploy

Railway automatically deploys when you push to GitHub.

1. Make your code changes (including requirements.txt update)
2. Commit and push:
   ```bash
   git add .
   git commit -m "Update bot for Railway deployment"
   git push origin main
   ```
3. Go to Railway dashboard
4. Watch the deployment in the **Deployments** tab
5. Once it shows "Success", your bot is live! ✅

## Step 7: Monitor Your Bot

In the Railway dashboard:
- **Logs** tab - See real-time output from your bot
- **Metrics** tab - CPU, memory usage, etc.
- **Deployments** tab - View deployment history

## How It Works

With the GitHub API integration:

1. You upload an HTML file to Discord
2. Bot sends the file directly to GitHub via the API
3. Your repository is updated automatically
4. No local NAS access needed!

## Free Tier Limits

Railway's free tier includes:
- **$5 free credits/month** - Enough for a simple bot
- Auto-sleeping: If unused, the deployment sleeps (your bot may take a few seconds to respond after inactivity, but it will wake up)
- Generous bandwidth

After free tier, you pay ~$5-20/month for continuous uptime depending on usage.

## Troubleshooting

### Bot not responding in Discord
- Check the **Logs** in Railway dashboard
- Make sure `DISCORD_TOKEN` is set correctly
- Verify the bot is authorized in your Discord server

### Deployment fails
- Check the **Deployments** tab for error logs
- Make sure all files are in your GitHub repository
- Verify `requirements.txt` is correctly formatted

### "ModuleNotFoundError" errors
- Make sure you've updated `requirements.txt` with all dependencies
- Push changes to GitHub
- Trigger a new deployment

### GitHub commit fails
- Check that `GITHUB_TOKEN` is correct
- Verify the token has `repo` scope
- Check that `GITHUB_REPO` is formatted as `username/reponame`

## Comparison: NAS vs Railway

| Feature | NAS (Docker) | Railway |
|---------|-------------|---------|
| Cost | Free | Free/Pay-as-you-go |
| Setup | More complex | Very simple |
| 24/7 uptime | Yes | Yes (free tier may sleep) |
| GitHub integration | Via local git | Direct API |
| Power consumption | Uses NAS power | Hosted servers |
| Local control | Full | Limited |

## Next Steps

1. Push code to GitHub (if not already)
2. Create Railway account
3. Connect your GitHub repo
4. Set environment variables (Discord token, GitHub token, GitHub repo)
5. Update `requirements.txt` and `discord_bot.py` for API integration
6. Push changes - Railway auto-deploys
7. Check logs to verify it's running
8. Test with `/add_page` in Discord

## Alternative: Keep Using Docker on NAS

If you prefer not to use Railway, you can stick with the Docker approach on your NAS. Both work great - it's just a preference for where you want to host it!

## Security Notes

- Never commit `.env` or tokens to GitHub
- Keep your `GITHUB_TOKEN` secret - treat it like a password
- If a token is compromised, regenerate it immediately in GitHub settings
- Use `.gitignore` to prevent accidental commits of secrets

## Need Help?

- Railway docs: https://docs.railway.app
- Discord.py docs: https://discordpy.readthedocs.io
- PyGithub docs: https://pygithub.readthedocs.io
