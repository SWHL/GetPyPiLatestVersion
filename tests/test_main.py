# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
import sys
from pathlib import Path

import pytest

cur_dir = Path(__file__).resolve().parent
root_dir = cur_dir.parent

sys.path.append(str(root_dir))

from get_pypi_latest_version import GetPyPiLatestVersion, GetPypiLatestVersionError

obtainer = GetPyPiLatestVersion()


def test_extract_version():
    msg = "feat(rapidocr_onnxruntime): bump to v1.0.0"
    version = obtainer.extract_version(msg)
    assert version == "1.0.0"


def test_return_all_versions():
    _, all_versions = obtainer("rapidocr_onnxruntime", return_all_versions=True)
    assert len(all_versions) > 0


def test_add_one():
    version = "1.4.0"
    result = obtainer.version_add_one(version, add_major=True)
    assert result == "2.4.0"

    result = obtainer.version_add_one(version, add_minor=True)
    assert result == "1.5.0"

    result = obtainer.version_add_one(version, add_patch=True)
    assert result == "1.4.1"


def test_right_package_name():
    latest_version = obtainer("opencv-python")
    assert len(latest_version) > 0


def test_wrong_name():
    with pytest.raises(GetPypiLatestVersionError) as exc_info:
        obtainer("opencv-pytho")
    assert exc_info.type is GetPypiLatestVersionError
