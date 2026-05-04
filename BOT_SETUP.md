# Discord Bot Setup Guide

This guide will help you set up the Discord bot for automating session recap uploads.

## What the Bot Does

The bot allows you to upload session recap HTML files directly from Discord. Instead of:
1. Getting the `session_X_recap.html` file
2. Running `python add_page.py session_X_recap.html "Session X"` locally

You can now simply use the `/add_page` command in Discord to do both automatically!

## Prerequisites

- Python 3.8 or higher
- A Discord server where you have admin permissions
- A GitHub Personal Access Token (for git push)
- Git installed and configured

## Step 1: Create a Discord Application

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click **New Application**
3. Name it something like "Session Recap Bot"
4. Go to the **Bot** tab
5. Click **Add Bot**
6. Under TOKEN, click **Copy** to copy your bot token
7. Save this token somewhere safe (you'll need it in Step 3)

## Step 2: Set Bot Permissions

1. In the Developer Portal, go to **OAuth2** → **URL Generator**
2. Select these scopes:
   - `bot`
3. Select these permissions:
   - `Send Messages`
   - `Embed Links`
   - `Attach Files`
   - `Read Message History`
4. Copy the generated URL and open it in your browser
5. Select a Discord server and authorize the bot

## Step 3: Configure Environment Variables

1. In your repository, create a `.env` file in the root directory:

```bash
DISCORD_TOKEN=your_bot_token_here
REPO_PATH=/path/to/uncharted-worlds-notes
```

Replace:
- `your_bot_token_here` with the token from Step 1
- `/path/to/uncharted-worlds-notes` with the full path to your repository

**Important:** Add `.env` to your `.gitignore` to avoid committing secrets!

Example `.env`:
```
DISCORD_TOKEN=MTk4NjIyNDgzNDU4MTI4MzI4.ClnnLQ.ZrFoKVnqKVgRA_oN...
REPO_PATH=/home/user/projects/uncharted-worlds-notes
```

## Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 5: Configure Git

The bot uses git to commit and push changes. Make sure you have git configured:

```bash
git config user.name "Your Name"
git config user.email "your@email.com"
```

If you use SSH keys, make sure your SSH key is added to your GitHub account.
If you use HTTPS, GitHub may require a Personal Access Token for pushing.

## Step 6: Run the Bot

```bash
python3 discord_bot.py
```

You should see:
```
YourBotName#1234 has connected to Discord!
Synced X command(s)
```

Keep this running! The bot needs to be active to respond to commands.

## Using the Bot

### `/add_page` Command

In your Discord server, use:

```
/add_page
  html_file: [upload your HTML file]
  page_title: [enter the page title]
```

**Example:**
- Upload: `session_8_recap.html`
- Page title: `Session 8`

The bot will:
1. ✅ Accept the HTML file
2. ✅ Save it to your repository
3. ✅ Run `add_page.py` to update `index.html`
4. ✅ Commit and push changes automatically
5. ✅ Send a confirmation message

### `/help_page` Command

Shows help information about using the bot.

## Hosting Options

The bot needs to run continuously to respond to commands. You have several options:

### Option 1: Your Local Machine
- Simplest to set up
- Must keep the terminal open and your machine running
- Good for testing

### Option 2: VPS (Virtual Private Server)
- Services like Linode, DigitalOcean, AWS
- Costs $5-20+ per month
- Reliable and always on
- Requires some Linux knowledge

### Option 3: Free Hosting
- **Railway.app** - Free tier available, generous limits
- **Replit** - Free tier with 24/7 uptime option
- **Glitch** - Free tier available

## Troubleshooting

### Bot doesn't respond to commands
- Make sure the bot is running (`python3 discord_bot.py`)
- Check that you've authorized the bot in your Discord server
- Verify the bot has permissions to send messages in the channel

### "DISCORD_TOKEN not set in .env file"
- Create `.env` file in the root directory
- Copy your token from the Discord Developer Portal
- Format: `DISCORD_TOKEN=your_token_here`

### "Error: [html_file] not found"
- Make sure you're uploading a valid HTML file
- The file should match the expected naming pattern (e.g., `session_X_recap.html`)

### "Script execution failed"
- Check that `add_page.py` exists in your repository
- Verify git is configured correctly
- Make sure you have push access to the repository

### Git push fails
- If using SSH: Ensure your SSH key is added to your GitHub account
- If using HTTPS: You may need to use a Personal Access Token instead of your password
- Check your git configuration: `git config user.name` and `git config user.email`

## Files

- `discord_bot.py` - Main bot code
- `requirements.txt` - Python dependencies
- `.env` - Configuration (create yourself, not in repo)
- `add_page.py` - Existing script that the bot calls

## Security Notes

- Never commit `.env` to your repository
- Keep your Discord bot token secret
- Use a Personal Access Token with minimal required permissions for GitHub
- If your token is compromised, regenerate it immediately in the Discord Developer Portal

## Support

If you encounter issues:
1. Check the troubleshooting section above
2. Make sure all dependencies are installed: `pip install -r requirements.txt`
3. Verify all configuration in `.env` is correct
4. Check Discord bot has correct permissions in your server
