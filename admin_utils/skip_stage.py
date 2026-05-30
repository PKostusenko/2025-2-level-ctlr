"""
Check if lab stage should be skipped based on target score.
"""

import argparse
import json
import sys
from pathlib import Path

from quality_control.console_logging import get_child_logger
from quality_control.lab_settings import LabSettings
from quality_control.project_config import ProjectConfig

from admin_utils.constants import PROJECT_CONFIG_PATH, PROJECT_ROOT

logger = get_child_logger(__file__)


def get_target_score(lab_path: str) -> int | None:
    """
    Get target score from settings.json file in specified lab directory.

    Args:
        lab_path (str): Path to laboratory work directory

    Returns:
        int | None: Target score if found in settings.json, None otherwise
    """
    try:
        settings = LabSettings(Path(lab_path) / "settings.json")
        return settings.target_score
    except (FileNotFoundError, json.JSONDecodeError, KeyError) as e:
        logger.error(f"Error getting target score: {e}")
        return None


def main() -> None:
    """
    Main function that checks if lab stage should be skipped.
    Prints the reason for skipping if stage should be skipped
    due to target_score == 0 or if no lab in project_config.json,
    otherwise prints nothing (exit code 1).
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--lab-path", required=True, help="Path to laboratory work directory")
    args = parser.parse_args()

    project_config = ProjectConfig(PROJECT_CONFIG_PATH)
    if PROJECT_ROOT / args.lab_path not in project_config.get_labs_paths(root_dir=PROJECT_ROOT):
        print(f"Skipping: no {args.lab_path} in Project Config.")
        sys.exit(0)

    target_score = get_target_score(args.lab_path)

    if target_score == 0:
        print(f"Skipping: target score 0 for {args.lab_path}.")
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
