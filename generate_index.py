import os
from pathlib import Path
import html

EXCLUDE_DIRS = {'.git', '.github', '__pycache__'}
EXCLUDE_FILES = {'generate_index.py'}

def generate_index(dir_path: Path):
    entries = sorted(dir_path.iterdir(), key=lambda p: (p.is_file(), p.name.lower()))
    index_path = dir_path / 'index.html'
    rel_path = dir_path.relative_to(Path.cwd())

    with index_path.open('w', encoding='utf-8') as f:
        f.write('<!DOCTYPE html><html><head><meta charset="UTF-8">')
        f.write(f'<title>Index of /{rel_path}</title></head><body>\n')
        f.write(f'<h1>Index of /{rel_path}</h1><ul>\n')
        
        if rel_path != Path('.'):
            f.write(f'<li><a href="../">../</a></li>\n')

        for entry in entries:
            if entry.name in EXCLUDE_FILES or entry.name.startswith('.'):
                continue
            name = html.escape(entry.name)
            slash = '/' if entry.is_dir() else ''
            f.write(f'<li><a href="{name}{slash}">{name}{slash}</a></li>\n')

        f.write('</ul></body></html>\n')

def walk_and_generate(base_dir: Path):
    for root, dirs, files in os.walk(base_dir):
        root_path = Path(root)
        # Remove excluded dirs in-place so os.walk doesn't descend into them
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS and not d.startswith('.')]
        generate_index(root_path)

if __name__ == "__main__":
    walk_and_generate(Path.cwd())
