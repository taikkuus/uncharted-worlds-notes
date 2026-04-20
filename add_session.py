#!/usr/bin/env python3

import sys
import os
import subprocess
from pathlib import Path

def add_session(session_num, html_file, page_title):
    # Check if HTML file exists
    if not Path(html_file).exists():
        print(f"Error: {html_file} not found")
        sys.exit(1)
    
    # Read index.html
    with open('index.html', 'r') as f:
        content = f.read()
    
    # Create new link
    new_link = f'''        <li>
          <a href="{html_file}">{page_title}</a>    
        </li>'''
    
    # Insert before </ul>
    updated_content = content.replace('      </ul>', f'{new_link}\n      </ul>')
    
    # Write back
    with open('index.html', 'w') as f:
        f.write(updated_content)
    
    # Git operations
    subprocess.run(['git', 'add', html_file, 'index.html'], check=True)
    subprocess.run(['git', 'commit', '-m', f'Add {page_title}'], check=True)
    subprocess.run(['git', 'push'], check=True)
    
    print(f"✓ Added {page_title} to index and committed changes")

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Usage: python add-session.py <session_number> <html_filename> <page_title>")
        print("Example: python add-session.py 6 session_6_recap.html 'Session 6'")
        sys.exit(1)
    
    add_session(sys.argv[1], sys.argv[2], sys.argv[3])
