# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
import argparse

from html5lib.html5parser import parse
import requests

REQUESTS_TIMEOUT = 15


class GetPyPiLatestVersion():
    def __init__(self, url: str = "https://pypi.org/",) -> None:
        self._base_url = url

    def __call__(self, package_name: str) -> str:
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

            description_element = result.find(
                "p[@class='package-snippet__description']"
            )
            description = (
                description_element.text
                if description_element is not None and description_element.text
                else ""
            )

            if name == package_name.replace('_', '-'):
                return version
        return ''


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
