#!/usr/bin/env python3
"""
MkDocs to Starlight Migration Script
Converts MkDocs markdown files to Astro Starlight MDX format.
"""

import re
import os
import shutil
import yaml
from pathlib import Path

# === CONFIGURATION ===
MKDOCS_DIR = Path("./mkdocs-docs")  # Your MkDocs docs/ folder
OUTPUT_DIR = Path("./starlight-docs")  # Output for converted files
MKDOCS_YML = Path("./mkdocs.yml")  # Your mkdocs.yml

def convert_frontmatter(content: str, filepath: Path) -> str:
    """
    Extract title from first H1, remove Notion metadata, add Starlight frontmatter.
    """
    lines = content.split('\n')
    title = filepath.stem.replace('-', ' ').title()
    description = ""
    
    # Find and extract H1 title
    new_lines = []
    found_title = False
    skip_metadata = False
    
    for i, line in enumerate(lines):
        # Extract title from first H1
        if not found_title and line.startswith('# '):
            title = line[2:].strip()
            found_title = True
            continue  # Remove the H1, title goes in frontmatter
        
        # Skip Notion-style metadata block (Created:, Tags:, Owner:)
        if line.startswith('Created:') or line.startswith('Tags:') or line.startswith('Owner:'):
            continue
        
        new_lines.append(line)
    
    # Build Starlight frontmatter
    frontmatter = f"""---
title: "{title}"
description: "{description}"
---

"""
    
    return frontmatter + '\n'.join(new_lines).lstrip('\n')


def convert_admonitions(content: str) -> str:
    """
    Convert MkDocs admonitions to Starlight Asides.
    
    MkDocs:  !!! warning "Title"
                 Content here
    
    Starlight: :::warning[Title]
               Content here
               :::
    """
    # Pattern matches !!! type "optional title" followed by indented content
    pattern = r'!!! (\w+)(?: "([^"]*)")?\n((?:    .+\n?)+)'
    
    def replacer(match):
        admon_type = match.group(1)
        title = match.group(2) or ""
        content = match.group(3)
        
        # Map MkDocs types to Starlight types
        type_map = {
            'note': 'note',
            'info': 'note',
            'tip': 'tip',
            'hint': 'tip',
            'warning': 'caution',
            'caution': 'caution',
            'danger': 'danger',
            'error': 'danger',
        }
        starlight_type = type_map.get(admon_type, 'note')
        
        # Remove 4-space indent from content
        dedented = '\n'.join(line[4:] if line.startswith('    ') else line 
                           for line in content.rstrip().split('\n'))
        
        if title:
            return f":::{starlight_type}[{title}]\n{dedented}\n:::\n"
        else:
            return f":::{starlight_type}\n{dedented}\n:::\n"
    
    return re.sub(pattern, replacer, content)


def convert_image_paths(content: str, filepath: Path) -> str:
    """
    Update image paths for Astro's asset handling.
    Images in subfolders like arduino-ide/image.png stay relative.
    """
    # For now, keep relative paths - they'll work if we copy the image folders too
    return content


def process_file(src: Path, dest: Path):
    """Process a single markdown file."""
    content = src.read_text(encoding='utf-8')
    
    # Apply conversions
    content = convert_frontmatter(content, src)
    content = convert_admonitions(content)
    content = convert_image_paths(content, src)
    
    # Write as .mdx
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(content, encoding='utf-8')
    print(f"  ✓ {src} → {dest}")


def parse_nav(nav_items, base_path="", order_counter=None):
    """
    Recursively parse mkdocs.yml nav into Starlight sidebar config.
    Returns a list of sidebar items.
    """
    if order_counter is None:
        order_counter = [0]
    
    sidebar_items = []
    
    for item in nav_items:
        if isinstance(item, str):
            # Direct file reference
            sidebar_items.append(item.replace('.md', ''))
        elif isinstance(item, dict):
            for label, value in item.items():
                if isinstance(value, str):
                    # Single page: "Label: path/to/file.md"
                    order_counter[0] += 1
                    sidebar_items.append({
                        'label': label,
                        'slug': value.replace('.md', ''),
                        'order': order_counter[0]
                    })
                elif isinstance(value, list):
                    # Section with children
                    children = parse_nav(value, base_path, order_counter)
                    sidebar_items.append({
                        'label': label,
                        'items': children
                    })
    
    return sidebar_items


def generate_sidebar_config(mkdocs_yml: Path) -> str:
    """Generate Starlight sidebar configuration from mkdocs.yml nav."""
    
    # Custom loader that ignores Python-specific tags
    class IgnoreTagLoader(yaml.SafeLoader):
        pass
    
    def ignore_unknown(loader, tag_suffix, node):
        return None
    
    IgnoreTagLoader.add_multi_constructor('tag:yaml.org,2002:python/', ignore_unknown)
    IgnoreTagLoader.add_multi_constructor('!', ignore_unknown)
    
    with open(mkdocs_yml, 'r', encoding='utf-8') as f:
        config = yaml.load(f, Loader=IgnoreTagLoader)
    
    nav = config.get('nav', [])
    sidebar = parse_nav(nav)
    
    # Format as JavaScript
    output = "// Generated sidebar config - paste into astro.config.mjs\n"
    output += "sidebar: [\n"
    
    def format_item(item, indent=2):
        spaces = "  " * indent
        if isinstance(item, str):
            return f'{spaces}"{item}",'
        elif isinstance(item, dict):
            if 'items' in item:
                # Section/group
                children = '\n'.join(format_item(child, indent+1) for child in item['items'])
                return f"""{spaces}{{
{spaces}  label: '{item['label']}',
{spaces}  items: [
{children}
{spaces}  ],
{spaces}}},"""
            else:
                # Single page
                return f'{spaces}{{ label: "{item["label"]}", slug: "{item["slug"]}" }},'
    
    for item in sidebar:
        output += format_item(item) + "\n"
    
    output += "]"
    return output


def migrate(mkdocs_docs: Path, output: Path, mkdocs_yml: Path):
    """Run the full migration."""
    print(f"\n📦 Migrating MkDocs → Starlight")
    print(f"   Source: {mkdocs_docs}")
    print(f"   Output: {output}\n")
    
    # Clean output dir
    if output.exists():
        shutil.rmtree(output)
    output.mkdir(parents=True)
    
    # Process all .md files
    print("📄 Converting files:")
    for src_file in mkdocs_docs.rglob("*.md"):
        relative = src_file.relative_to(mkdocs_docs)
        dest_file = output / relative.with_suffix('.mdx')
        process_file(src_file, dest_file)
    
    # Copy image folders (any folder containing images)
    print("\n🖼️  Copying assets:")
    for img_dir in mkdocs_docs.rglob("*"):
        if img_dir.is_dir() and any(img_dir.glob("*.png")) or any(img_dir.glob("*.gif")) or any(img_dir.glob("*.jpg")):
            relative = img_dir.relative_to(mkdocs_docs)
            dest_dir = output / relative
            if not dest_dir.exists():
                shutil.copytree(img_dir, dest_dir)
                print(f"  ✓ {relative}/")
    
    # Generate sidebar config
    print("\n⚙️  Generating sidebar config:")
    sidebar_config = generate_sidebar_config(mkdocs_yml)
    config_file = output / "_sidebar_config.js"
    config_file.write_text(sidebar_config)
    print(f"  ✓ {config_file}")
    
    print("\n✅ Migration complete!")
    print(f"\nNext steps:")
    print(f"  1. Copy {output}/* to src/content/docs/")
    print(f"  2. Copy sidebar config from {config_file} to astro.config.mjs")
    print(f"  3. Review and fix any broken image paths")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) >= 3:
        mkdocs_docs = Path(sys.argv[1])
        mkdocs_yml = Path(sys.argv[2])
        output = Path(sys.argv[3]) if len(sys.argv) > 3 else OUTPUT_DIR
    else:
        print("Usage: python migrate_mkdocs.py <docs_folder> <mkdocs.yml> [output_folder]")
        print("Example: python migrate_mkdocs.py ./docs ./mkdocs.yml ./converted")
        sys.exit(1)
    
    migrate(mkdocs_docs, output, mkdocs_yml)
