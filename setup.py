# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
import os
import sys
from pathlib import Path

import setuptools

from get_pypi_latest_version import GetPyPiLatestVersion


def get_readme():
    root_dir = Path(__file__).resolve().parent
    readme_path = str(root_dir / 'README.md')
    with open(readme_path, 'r', encoding='utf-8') as f:
        readme = f.read()
    return readme


MODULE_NAME = 'get_pypi_latest_version'

obtainer = GetPyPiLatestVersion()

latest_version = obtainer(MODULE_NAME)
VERSION_NUM = obtainer.version_add_one(latest_version)

if len(sys.argv) > 2:
    match_str = ' '.join(sys.argv[2:])
    matched_versions = obtainer.extract_version(match_str)
    if matched_versions:
        VERSION_NUM = matched_versions
sys.argv = sys.argv[:2]
os.system(f"""echo "version = '{VERSION_NUM}'" >> {MODULE_NAME}/__init__.py""")

setuptools.setup(
    name=MODULE_NAME,
    version=VERSION_NUM,
    platforms='Any',
    description='Get the latest version of the specified python package name in the pypi.',
    long_description=get_readme(),
    long_description_content_type='text/markdown',
    author='SWHL',
    author_email='liekkaskono@163.com',
    url='https://github.com/SWHL/GetPyPiLatestVersion',
    download_url='https://github.com/SWHL/GetPyPiLatestVersion.git',
    license='Apache-2.0',
    include_package_data=True,
    install_requires=['html5lib>=1.1', 'requests>=2.28.1', 'pip>=21.2'],
    packages=[MODULE_NAME],
    keywords=[
        'pypi,latest_version'
    ],
    classifiers=[
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    python_requires='>=3.6,<3.12',
    entry_points={
        'console_scripts': [f'{MODULE_NAME}={MODULE_NAME}.main:main'],
    },
    project_urls={
        "Documentation": "https://getpypilatestversion.readthedocs.io/",
        "Source": "https://github.com/SWHL/GetPyPiLatestVersion",
        "Changelog": "https://github.com/SWHL/GetPyPiLatestVersion#change-log",
    }
)
