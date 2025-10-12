#!/usr/bin/env python3
"""
Simple launcher script for Mail Organizer
"""

import sys
import os
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

if __name__ == "__main__":
    from main import main
    sys.exit(main())
