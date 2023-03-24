# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
from get_pypi_latest_version import GetPyPiLatestVersion


obtainer = GetPyPiLatestVersion()

package_name = 'opencv-python'
latest_version = obtainer(package_name)
print(latest_version)
