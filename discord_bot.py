#!/usr/bin/env python3

import os
import sys
import subprocess
import tempfile
from pathlib import Path
from dotenv import load_dotenv
import discord
from discord.ext import commands
from discord import app_commands

# Load environment variables
load_dotenv()

# Configuration
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
REPO_PATH = os.getenv('REPO_PATH', '.')

# Validate configuration
if not DISCORD_TOKEN:
    print("Error: DISCORD_TOKEN not set in .env file")
    sys.exit(1)

# Setup bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(f"Failed to sync commands: {e}")

@bot.tree.command(name="add_page", description="Add a new page to the repository")
@app_commands.describe(
    html_file="The session recap HTML file to upload",
    page_title="The title for this page (e.g., 'Session 8')"
)
async def add_page_command(interaction: discord.Interaction, html_file: discord.Attachment, page_title: str):
    """
    Upload an HTML recap file and add it to the repository.
    
    Args:
        html_file: The HTML file to upload
        page_title: The title to display in the index
    """
    await interaction.response.defer()
    
    try:
        # Validate file type
        if not html_file.filename.endswith('.html'):
            await interaction.followup.send("❌ Error: File must be an HTML file (.html)")
            return
        
        # Validate page title
        if not page_title or len(page_title.strip()) == 0:
            await interaction.followup.send("❌ Error: Page title cannot be empty")
            return
        
        # Create a temporary directory for processing
        with tempfile.TemporaryDirectory() as temp_dir:
            # Download the file
            temp_file_path = os.path.join(temp_dir, html_file.filename)
            await html_file.save(temp_file_path)
            
            # Copy to repo directory
            repo_file_path = os.path.join(REPO_PATH, html_file.filename)
            with open(temp_file_path, 'rb') as src:
                with open(repo_file_path, 'wb') as dst:
                    dst.write(src.read())
            
            # Change to repo directory and run the script
            original_cwd = os.getcwd()
            try:
                os.chdir(REPO_PATH)
                
                # Run add_page.py
                result = subprocess.run(
                    [sys.executable, 'add_page.py', html_file.filename, page_title],
                    capture_output=True,
                    text=True,
                    check=True
                )
                
                # Success message
                embed = discord.Embed(
                    title="✅ Page Added Successfully",
                    color=discord.Color.green()
                )
                embed.add_field(name="File", value=html_file.filename, inline=False)
                embed.add_field(name="Title", value=page_title, inline=False)
                embed.add_field(name="Status", value="Committed and pushed to repository", inline=False)
                
                await interaction.followup.send(embed=embed)
                
            except subprocess.CalledProcessError as e:
                # Error from add_page.py script
                error_msg = f"Script Error:\n```\n{e.stderr}\n```" if e.stderr else "Script execution failed"
                embed = discord.Embed(
                    title="❌ Script Error",
                    description=error_msg,
                    color=discord.Color.red()
                )
                await interaction.followup.send(embed=embed)
                
            finally:
                os.chdir(original_cwd)
    
    except Exception as e:
        embed = discord.Embed(
            title="❌ Error",
            description=f"An error occurred: {str(e)}",
            color=discord.Color.red()
        )
        await interaction.followup.send(embed=embed)

@bot.tree.command(name="help_page", description="Get help on using the add_page command")
async def help_command(interaction: discord.Interaction):
    """Show help information for the bot"""
    embed = discord.Embed(
        title="Session Recap Bot Help",
        description="This bot automates adding session recap pages to your repository",
        color=discord.Color.blue()
    )
    embed.add_field(
        name="/add_page",
        value="Add a new session recap to the repository\n"
              "**Parameters:**\n"
              "• `html_file`: Upload your session_X_recap.html file\n"
              "• `page_title`: Display name (e.g., 'Session 8')\n\n"
              "**Example:** Upload session_8_recap.html with title 'Session 8'",
        inline=False
    )
    embed.add_field(
        name="What It Does",
        value="1. Receives your HTML recap file\n"
              "2. Saves it to the repository\n"
              "3. Updates index.html with a link to the new page\n"
              "4. Commits and pushes changes to GitHub",
        inline=False
    )
    embed.add_field(
        name="Requirements",
        value="• HTML file must end with `.html`\n"
              "• Page title cannot be empty\n"
              "• Bot must have access to the repository",
        inline=False
    )
    
    await interaction.response.send_message(embed=embed)

# Run the bot
if __name__ == '__main__':
    bot.run(DISCORD_TOKEN)
