import os
import sys

__version__ = "feature/v1.2.0"

sys.path.append(os.path.dirname(os.path.realpath(__file__)))
print(f"The new syspath - {sys.path}")
