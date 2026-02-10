# /// script
# requires-python = ">=3.11"
# dependencies = ["click"]
# ///

"""
TOOL: Tool Scanner
DESCRIPTION: Lists all available tools in 'tools/scripts/' with their descriptions.
USAGE: ./tools/run run tools/scripts/list_tools.py
"""

import os
import re
import ast
from pathlib import Path

TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))

def extract_metadata(file_path):
    """Extracts description and usage from docstring or comments."""
    description = "No description available."
    usage = "N/A"

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Try parsing as python to get docstring
        try:
            tree = ast.parse(content)
            docstring = ast.get_docstring(tree)
            if docstring:
                # Look for explicit metadata fields in docstring
                desc_match = re.search(r'DESCRIPTION:\s*(.*)', docstring, re.IGNORECASE)
                if desc_match:
                    description = desc_match.group(1).strip()
                else:
                    # Fallback to first line of docstring
                    description = docstring.split('\n')[0].strip()

                usage_match = re.search(r'USAGE:\s*(.*)', docstring, re.IGNORECASE)
                if usage_match:
                    usage = usage_match.group(1).strip()
        except:
            pass
            
        return description, usage
    except Exception:
        return "Error reading file.", "Error"

def main():
    print("🛠️  Mental Refinery Tool Catalog\n")
    # Format: Script Name | Description | Usage
    # Adjust widths as needed.
    
    # Header
    print(f"{'SCRIPT':<25} | {'DESCRIPTION':<45} | {'USAGE'}")
    print("-" * 100)
    
    scripts = sorted([f for f in os.listdir(TOOLS_DIR) if f.endswith('.py') and f != '__init__.py'])
    
    count = 0
    for script in scripts:
        path = os.path.join(TOOLS_DIR, script)
        desc, usage = extract_metadata(path)
        
        # Skip internal helpers if marked
        if desc.startswith("INTERNAL"): 
            continue
        
        # Truncate description if too long for cleaner display
        if len(desc) > 42:
            desc = desc[:42] + "..."
            
        print(f"{script:<25} | {desc:<45} | {usage}")
        count += 1
        
    print("-" * 100)
    print(f"Total: {count} tools found.")

if __name__ == "__main__":
    main()

