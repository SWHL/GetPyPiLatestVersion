# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
import argparse
import re
import subprocess
from typing import Dict, List, Optional, Tuple, Union

import requests
from html5lib.html5parser import parse

REQUESTS_TIMEOUT = 15


class GetPyPiLatestVersion():
    """Get the latest version of the specified python package name in the pypi.
    """

    def __init__(self, url: str = "https://pypi.org/",) -> None:
        self._base_url = url
        self.pip_versions = []

    def __call__(self, package_name: str,
                 return_all_versions: bool = False) -> Union[str, Tuple[str, List]]:
        """_summary_

        Args:
            package_name (str): The name of the package you want to get the latest version.
            return_all_versions (bool, optional): Whether to return all release versions. Default is :code:`False` .

        Raises:
            ValueError: The exception is thrown when no valid package information is found.

        Returns:
            Union[str, Tuple[str, List]]: the latest version. When :code:`return_all_versions=True` , Return Tuple: :code:`[latest_version_str, all_release_list]`
        """
        try:
            all_versions_web = self.get_by_spider_web(package_name)
        except ValueError as e:
            raise e

        latest_ver_web = all_versions_web[0]

        latest_ver_pip = self.get_by_pip_index(package_name)

        all_concat_ver = list(set(all_versions_web).union(self.pip_versions))
        all_concat_ver.sort(reverse=True)

        latest_ver = latest_ver_web or latest_ver_pip or ''
        if return_all_versions:
            return latest_ver, all_concat_ver
        return latest_ver

    def get_by_spider_web(self, package_name: str) -> str:
        search = {"q": package_name}
        response = requests.session().get(
            self._base_url + "search", params=search, timeout=REQUESTS_TIMEOUT
        )

        content = parse(response.content, namespaceHTMLElements=False)
        search_packages = content.findall(".//*[@class='package-snippet']")

        package_info = {}
        for result in search_packages:
            name_element = result.find("h3/*[@class='package-snippet__name']")
            version_element = result.find(
                "h3/*[@class='package-snippet__version']")
            package_href = result.attrib.get('href')

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
                if package_href:
                    package_info['href'] = self._base_url + package_href
                package_info['latest'] = version
                break

        if not package_info:
            raise ValueError(f'No version information of {package_name}. '
                             'Please check if the package name correct.')
        all_versions = self.get_all_release_versions(package_info)
        return all_versions

    def get_all_release_versions(self, package_info: Dict):
        history_url = package_info['href'] + '#history'
        response = requests.session().get(history_url,
                                          timeout=REQUESTS_TIMEOUT)
        content = parse(response.content, namespaceHTMLElements=False)
        a_elements = content.findall(
            './/*[@class="release"]/a[@class="card release__card"]')

        release_list = [package_info['latest']]
        for i, a_ele in enumerate(a_elements):
            p_ele = a_ele.find('p[@class="release__version"]')

            # 查看是否是yanked 版本
            yanked_ele = p_ele.find('span[@class="badge badge--danger"]')
            if yanked_ele is not None:
                # 有值，则说明是yanked
                continue

            cur_version = [v.strip() for v in p_ele.text.split('\n')
                           if v.strip()][0]
            release_list.append(cur_version)
        release_list.sort(reverse=True)
        return release_list

    def get_by_pip_index(self, package_name: str) -> List:
        output = subprocess.run(["pip", "index", "versions", package_name],
                                capture_output=True)
        output = output.stdout.decode('utf-8')
        if output:
            return self.extract_version(output)
        return ''

    def extract_version(self, message: str) -> str:
        """Extract the version string matched the semver 2.0.0 from the string.

        Args:
            message (str): the text with the version num.

        Returns:
            str: '' or 'x.x.x'
        """
        pattern = r'\d+\.(?:\d+\.)*\d+'
        matched_versions = re.findall(pattern, message)
        all_versions = list(set(matched_versions))
        all_versions.sort(reverse=True)

        if all_versions:
            self.pip_versions = all_versions
            return all_versions[0]
        return ''

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
            return '1.0.0'

        version_list = version.split('.')
        if abs(add_loc) > len(version_list):
            raise ValueError(
                f'add_loc must be between [-{len(version_list)}, -1]. But now add_loc is {add_loc}.')

        add_one_ver_num = str(int(version_list[add_loc]) + 1)
        if add_loc != -1:
            version_list[add_loc+1:] = ['0'] * len(version_list[add_loc+1:])

        version_list[add_loc] = add_one_ver_num
        new_version = '.'.join(version_list)
        return new_version


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('package_name', type=str,
                        help='The specified python package name. e.g. opencv-python.')
    parser.add_argument('-a', '--all_versions',
                        default=False, action="store_true",
                        help="Whether to return all release versions. Default is False.")
    args = parser.parse_args()

    obtainer = GetPyPiLatestVersion()

    latest_version = obtainer(args.package_name, args.all_versions)
    if args.all_versions:
        print(latest_version[0])
        print(latest_version[1])
    else:
        print(latest_version)


if __name__ == '__main__':
    main()
