#!/usr/bin/env python3

import os
import sys
import io
from pathlib import Path
from dotenv import load_dotenv
import discord
from discord.ext import commands
from discord import app_commands
from github import Github
import base64

# Load environment variables
load_dotenv()

# Configuration
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
GITHUB_REPO = os.getenv('GITHUB_REPO')

# Validate configuration
if not DISCORD_TOKEN:
    print("Error: DISCORD_TOKEN not set in environment variables")
    sys.exit(1)

if not GITHUB_TOKEN or not GITHUB_REPO:
    print("Error: GITHUB_TOKEN and GITHUB_REPO must be set for Railway deployment")
    print("Set these in your Railway project variables")
    sys.exit(1)

# Initialize GitHub API
try:
    g = Github(GITHUB_TOKEN)
    repo = g.get_repo(GITHUB_REPO)
    print(f"Connected to GitHub repo: {GITHUB_REPO}")
except Exception as e:
    print(f"Error connecting to GitHub: {e}")
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
        
        # Download the file from Discord
        file_content = await html_file.read()
        
        # Upload HTML file to GitHub
        try:
            # Try to get existing file (to update it)
            try:
                existing_file = repo.get_contents(html_file.filename)
                repo.update_file(
                    path=html_file.filename,
                    message=f"Update {html_file.filename}",
                    content=file_content,
                    sha=existing_file.sha
                )
                file_status = "updated"
            except:
                # File doesn't exist, create it
                repo.create_file(
                    path=html_file.filename,
                    message=f"Add {html_file.filename}",
                    content=file_content
                )
                file_status = "created"
            
            # Get the current index.html
            index_file = repo.get_contents("index.html")
            index_content = index_file.content
            
            # Decode from base64
            index_content = base64.b64decode(index_content).decode('utf-8')
            
            # Create new link
            new_link = f'''        <li>
          <a href="{html_file.filename}">{page_title}</a>    
        </li>'''
            
            # Insert before </ul>
            updated_content = index_content.replace('      </ul>', f'{new_link}\n      </ul>')
            
            # Check if the link is already in index (avoid duplicates)
            if new_link.strip() in index_content:
                embed = discord.Embed(
                    title="⚠️ Link Already Exists",
                    description=f"The link for '{page_title}' is already in index.html",
                    color=discord.Color.yellow()
                )
                embed.add_field(name="File", value=html_file.filename, inline=False)
                embed.add_field(name="Title", value=page_title, inline=False)
                await interaction.followup.send(embed=embed)
                return
            
            # Update index.html
            repo.update_file(
                path="index.html",
                message=f"Add {page_title}",
                content=updated_content,
                sha=index_file.sha
            )
            
            # Success message
            embed = discord.Embed(
                title="✅ Page Added Successfully",
                color=discord.Color.green()
            )
            embed.add_field(name="File", value=html_file.filename, inline=False)
            embed.add_field(name="Title", value=page_title, inline=False)
            embed.add_field(name="File Status", value=file_status.capitalize(), inline=False)
            embed.add_field(name="Repository", value=GITHUB_REPO, inline=False)
            embed.add_field(name="Status", value="Committed to repository via GitHub API", inline=False)
            
            await interaction.followup.send(embed=embed)
            
        except Exception as e:
            error_msg = str(e)
            embed = discord.Embed(
                title="❌ GitHub Error",
                description=f"Failed to update repository:\n```\n{error_msg}\n```",
                color=discord.Color.red()
            )
            await interaction.followup.send(embed=embed)
    
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
              "2. Uploads it to the GitHub repository\n"
              "3. Updates index.html with a link to the new page\n"
              "4. Commits changes to GitHub",
        inline=False
    )
    embed.add_field(
        name="Requirements",
        value="• HTML file must end with `.html`\n"
              "• Page title cannot be empty\n"
              "• Link shouldn't already exist in index.html",
        inline=False
    )
    
    await interaction.response.send_message(embed=embed)

# Run the bot
if __name__ == '__main__':
    bot.run(DISCORD_TOKEN)
