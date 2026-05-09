from pathlib import Path


src_dir = Path("src")

for folder in [src_dir, *src_dir.rglob("*")]:
    if folder.is_dir():
        init_file = folder / "__init__.py"
        init_file.touch(exist_ok=True)