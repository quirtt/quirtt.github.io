#!/usr/bin/env python3
"""
Sync Obsidian vault to thoughts directory.
Run this before pushing to GitHub Pages.
"""
 
import shutil
import re
from pathlib import Path
import sys
 
# Configuration
OBSIDIAN_DIR = Path.home() / "Documents" / "Thoughts to Myself" # Update to your vault path
THOUGHTS_DIR = Path(".")
 
def convert_obsidian_to_plain(text):
    """Convert Obsidian-specific syntax to plain markdown."""
    
    # [[WikiLink]] → [WikiLink](wikilink.md)
    text = re.sub(
        r'\[\[([^\]|]+)(?:\|([^\]]+))?\]\]',
        lambda m: f'[{m.group(2) or m.group(1)}]({m.group(1).lower().replace(" ", "-").replace("_", "-")}.md)',
        text
    )
    
    # ![[image.png]] → ![](../assets/image.png)
    text = re.sub(
        r'!\[\[([^\]]+)\]\]',
        r'![\1](../assets/\1)',
        text
    )
    
    return text
 
def sync_thoughts():
    """Sync Obsidian vault to thoughts directory."""
    
    if not OBSIDIAN_DIR.exists():
        print(f"❌ Obsidian directory not found: {OBSIDIAN_DIR}")
        print("   Update OBSIDIAN_DIR in this script to point to your vault.")
        sys.exit(1)
    
    # Create thoughts directory
    THOUGHTS_DIR.mkdir(exist_ok=True)
    
    # Count files
    md_files = list(OBSIDIAN_DIR.glob("*.md"))
    if not md_files:
        print(f"⚠️  No markdown files found in {OBSIDIAN_DIR}")
        return
    
    print(f"📝 Syncing {len(md_files)} files from Obsidian...")
    
    synced_files = []
    
    for md_file in md_files:
        # Skip hidden/system files
        if md_file.name.startswith("."):
            continue
        
        # Read and convert
        content = md_file.read_text(encoding='utf-8')
        content = convert_obsidian_to_plain(content)
        
        # Write to thoughts directory
        output_file = THOUGHTS_DIR / md_file.name
        output_file.write_text(content, encoding='utf-8')
        synced_files.append(md_file.name)
        print(f"  ✓ {md_file.name}")
    
    # Generate manifest.json for the index page
    import json
    manifest = {
        "files": sorted([f for f in synced_files if not f.startswith(".")])
    }
    manifest_file = THOUGHTS_DIR / "manifest.json"
    manifest_file.write_text(json.dumps(manifest, indent=2), encoding='utf-8')
    print(f"✅ Created manifest.json with {len(synced_files)} files")
    print(f"✅ Synced {len(synced_files)} files to {THOUGHTS_DIR}/")
 
if __name__ == "__main__":
    sync_thoughts()