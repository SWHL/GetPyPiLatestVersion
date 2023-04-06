# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
import sys
from pathlib import Path

import pytest

cur_dir = Path(__file__).resolve().parent
root_dir = cur_dir.parent

sys.path.append(str(root_dir))

from get_pypi_latest_version import GetPyPiLatestVersion

obtainer = GetPyPiLatestVersion()


def test_right_package_name():
    latest_version = obtainer('opencv-python')
    assert len(latest_version) > 0


def test_wrong_name():
    with pytest.raises(ValueError) as exc_info:
        obtainer('opencv-pytho')
    assert exc_info.type is ValueError
