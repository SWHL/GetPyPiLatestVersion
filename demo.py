# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
from get_pypi_latest_version import GetPyPiLatestVersion

obtainer = GetPyPiLatestVersion()

package_name = "rapidocr-openvino"
latest_version, all_versions = obtainer(package_name, return_all_versions=True)
print(latest_version)
print(all_versions)
