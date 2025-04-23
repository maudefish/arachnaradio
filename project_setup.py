# project_setup.py

import sys
from pyprojroot import here

def setup_project_path():
    root = here()
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))
