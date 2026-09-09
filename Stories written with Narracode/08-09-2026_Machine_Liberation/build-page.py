"""Build the current edition; earlier builder is preserved in snapshot v5."""
from pathlib import Path
import runpy

if __name__ == "__main__":
    runpy.run_path(str(Path(__file__).with_name("build-page-v4.py")), run_name="__main__")
