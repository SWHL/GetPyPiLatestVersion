# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
import argparse
from typing import Dict, List, Optional, Tuple, Union
import re
import requests
from packaging.version import parse

REQUESTS_TIMEOUT = 45


class GetPyPiLatestVersion:
    def __init__(self, url: str = "https://pypi.org/pypi"):
        self._base_url = url

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
        json_url = f"{self._base_url}/{package_name}/json"
        response = requests.get(json_url, timeout=REQUESTS_TIMEOUT)
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

    def extract_version(self, message: str) -> str:
        """Extract the version string matched the semver 2.0.0 from the string.

        Args:
            message (str): the text with the version num.

        Returns:
            str: '' or 'x.x.x'
        """
        pattern = r"\d+\.(?:\d+\.)*\d+"
        matched_versions = re.findall(pattern, message)
        all_versions = list(set(matched_versions))
        all_versions.sort(key=matched_versions.index)

        if all_versions:
            return all_versions[0]
        return ""

    @staticmethod
    def version_add_one(
        version: Optional[str],
        add_patch: bool = False,
        add_minor: bool = False,
        add_major: bool = False,
    ) -> str:
        if not version:
            return "1.0.0"

        version = parse(version)

        patch = version.micro
        minor = version.minor
        major = version.major

        if add_patch:
            patch += 1

        if add_minor:
            minor += 1

        if add_major:
            major += 1

        return f"{major}.{minor}.{patch}"


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
