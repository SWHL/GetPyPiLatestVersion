# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
import argparse
from typing import Dict, List, Optional, Tuple, Union

import requests

REQUESTS_TIMEOUT = 15


class GetPyPiLatestVersion:
    """Get the latest version of the specified python package name in the pypi."""

    def __init__(self, url: str = "https://pypi.org/") -> None:
        self._base_url = url
        self.pip_versions = []

    def __call__(
        self, package_name: str, return_all_versions: bool = False
    ) -> Optional[Union[str, Tuple[str, List]]]:
        try:
            package_datas = self.get_package_data(package_name)
        except GetPypiLatestVersionError as exc:
            raise GetPypiLatestVersionError(exc) from exc

        latest_ver = self.get_latest_version(package_datas)
        if return_all_versions:
            all_versions = self.get_all_release_versions(package_datas)
            return latest_ver, all_versions
        return str(latest_ver)

    def get_package_data(self, package_name: str):
        url = f"https://pypi.org/pypi/{package_name}/json"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data

        if response.status_code == 404:
            raise GetPypiLatestVersionError(f"Not found {package_name}")

        raise GetPypiLatestVersionError(
            "Failed to retrieve version information from PyPI."
        )

    def get_latest_version(self, package_datas):
        return package_datas["info"]["version"]

    def get_all_release_versions(self, package_info: Dict):
        release_list = []
        for version_num, version_info in package_info["releases"].items():
            if version_info[0]["yanked"]:
                continue
            release_list.append(str(version_num))
        return release_list

    @staticmethod
    def version_add_one(version: Optional[str], add_loc: int = -1) -> str:
        """Add one for direct version.

        Args:
            version (Optional[str]): current version num
            add_loc (int, optional): Where to add one from the back to front. Default is -1. e.g. 4.0.7, when `add_loc=-1` → 4.0.8, `add_loc=-2` → 4.1.0， `add_loc=-3` → 5.0.0.

        Returns:
            str: the version after adding one.
        """
        if not version:
            return "1.0.0"

        version_list = version.split(".")
        if abs(add_loc) > len(version_list):
            raise ValueError(
                f"add_loc must be between [-{len(version_list)}, -1]. But now add_loc is {add_loc}."
            )

        add_one_ver_num = str(int(version_list[add_loc]) + 1)
        if add_loc != -1:
            version_list[add_loc + 1 :] = ["0"] * len(version_list[add_loc + 1 :])

        version_list[add_loc] = add_one_ver_num
        new_version = ".".join(version_list)
        return new_version


class GetPypiLatestVersionError(Exception):
    pass


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "package_name",
        type=str,
        help="The specified python package name. e.g. opencv-python.",
    )
    parser.add_argument(
        "-a",
        "--all_versions",
        default=False,
        action="store_true",
        help="Whether to return all release versions. Default is False.",
    )
    args = parser.parse_args()

    obtainer = GetPyPiLatestVersion()

    latest_version = obtainer(args.package_name, args.all_versions)
    if args.all_versions:
        print(latest_version[0])
        print(latest_version[1])
    else:
        print(latest_version)


if __name__ == "__main__":
    main()
