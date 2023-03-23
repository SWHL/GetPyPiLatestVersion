# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
from pathlib import Path

import setuptools


def get_readme():
    root_dir = Path(__file__).resolve().parent
    readme_path = str(root_dir / 'README.md')
    with open(readme_path, 'r', encoding='utf-8') as f:
        readme = f.read()
    return readme


MODULE_NAME = 'get_pypi_latest_version'

setuptools.setup(
    name=MODULE_NAME,
    version='0.0.1',
    platforms="Any",
    description="A cross platform OCR Library based on OnnxRuntime.",
    long_description=get_readme(),
    long_description_content_type='text/markdown',
    author="SWHL",
    author_email="liekkaskono@163.com",
    url="https://github.com/SWHL/GetPyPiLatestVersion",
    download_url='https://github.com/SWHL/GetPyPiLatestVersion.git',
    license='Apache-2.0',
    include_package_data=True,
    install_requires=["html5lib>=1.1", "requests>=2.28.1"],
    packages=[MODULE_NAME],
    keywords=[
        'pypi,latest_version'
    ],
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    entry_points={
        'console_scripts': [f'{MODULE_NAME}={MODULE_NAME}.main:main'],
    }
)
