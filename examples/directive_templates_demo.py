# -*- coding: utf-8 -*-
"""Direction prompt templates handoff demo."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from dramaforge.directive.prompt_templates import DIRECTION_SYSTEM, DIRECTION_USER, MOS_RUBRIC


def main():
    print("=== system ===")
    print(DIRECTION_SYSTEM)
    print("=== user ===")
    print(DIRECTION_USER.format(script="你好世界", direction="温柔一点"))
    print("=== mos rubric ===")
    print(MOS_RUBRIC)


if __name__ == "__main__":
    main()
