# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
import argparse
import re
import subprocess
from typing import Optional

import requests
from html5lib.html5parser import parse

REQUESTS_TIMEOUT = 15


class GetPyPiLatestVersion():
    """Get the latest version of the specified python package name in the pypi.
    """
    def __init__(self, url: str = "https://pypi.org/",) -> None:
        self._base_url = url

    def __call__(self, package_name: str) -> str:
        """call

        Args:
            package_name (str): The name of the package you want to get the latest version.

        Returns:
            str: the latest version
        """
        latest_ver_web = self.get_by_spider_web(package_name)
        latest_ver_pip = self.get_by_pip_index(package_name)

        if latest_ver_web and latest_ver_pip:
            if latest_ver_web != latest_ver_pip:
                return latest_ver_web
            return latest_ver_web

        latest_ver = latest_ver_web or latest_ver_pip
        return latest_ver

    def get_by_spider_web(self, package_name: str) -> str:
        search = {"q": package_name}
        response = requests.session().get(
            self._base_url + "search", params=search, timeout=REQUESTS_TIMEOUT
        )

        content = parse(response.content, namespaceHTMLElements=False)
        search_packages = content.findall(".//*[@class='package-snippet']")
        for result in search_packages:
            name_element = result.find("h3/*[@class='package-snippet__name']")
            version_element = result.find("h3/*[@class='package-snippet__version']")

            if (
                name_element is None
                or version_element is None
                or not name_element.text
                or not version_element.text
            ):
                continue

            name = name_element.text
            version = version_element.text
            if name == package_name.replace('_', '-'):
                return version
        return ''

    def get_by_pip_index(self, package_name: str) -> str:
        output = subprocess.run(["pip", "index", "versions", package_name],
                                capture_output=True)
        output = output.stdout.decode('utf-8')
        if output:
            return self.extract_version(output)
        return ''

    @staticmethod
    def extract_version(message: str) -> str:
        """Extract the version string matched the semver 2.0.0 from the string.

        Args:
            message (str): the text with the version num.

        Returns:
            str: '' or 'x.x.x'
        """
        pattern = r'\d+\.(?:\d+\.)*\d+'
        matched_versions = re.findall(pattern, message)
        if matched_versions:
            return matched_versions[0]
        return ''

    @staticmethod
    def version_add_one(version: Optional[str], add_loc: int = -1) -> str:
        """Add one for direct version.

        Args:
            version (Optional[str]): current version num
            add_loc (int, optional): Where to add one. Defaults to -1.

        Returns:
            str: the version after adding one.
        """
        if not version:
            return '1.0.0'

        version_list = version.split('.')
        mini_version = str(int(version_list[add_loc]) + 1)
        version_list[add_loc] = mini_version
        new_version = '.'.join(version_list)
        return new_version


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('package_name', type=str,
                        help='The specified python package name. e.g. opencv-python.')
    args = parser.parse_args()

    obtainer = GetPyPiLatestVersion()

    latest_version = obtainer(args.package_name)
    print(latest_version)


if __name__ == '__main__':
    main()
