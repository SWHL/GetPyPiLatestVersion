## get_pypi_latest_version

<p>
    <a href=""><img src="https://img.shields.io/badge/Python->=3.6,<3.12-aff.svg"></a>
    <a href=""><img src="https://img.shields.io/badge/OS-Linux%2C%20Win%2C%20Mac-pink.svg"></a>
    <a href="https://pypi.org/project/get_pypi_latest_version/"><img alt="PyPI" src="https://img.shields.io/pypi/v/get_pypi_latest_version"></a>
    <a href="https://pepy.tech/project/get-pypi-latest-version"><img src="https://static.pepy.tech/personalized-badge/get-pypi-latest-version?period=total&units=abbreviation&left_color=grey&right_color=blue&left_text=Downloads"></a>
    <a href="https://semver.org/"><img alt="SemVer2.0" src="https://img.shields.io/badge/SemVer-2.0-brightgreen"></a>
<a href='https://getpypilatestversion.readthedocs.io/en/latest/?badge=latest'>
    <img src='https://readthedocs.org/projects/getpypilatestversion/badge/?version=latest' alt='Documentation Status' />
</a>
</p>

### 1. Install package by pypi

```bash
pip install get_pypi_latest_version
```

### 2. Run by command line

- Usage:

    ```bash
    $ get_pypi_latest_version -h
    usage: get_pypi_latest_version [-h] [-a] package_name

    positional arguments:
    package_name        The specified python package name. e.g. opencv-python.

    optional arguments:
    -h, --help          show this help message and exit
    -a, --all_versions  Whether to return all release versions. Default is
                        False.
    ```

- Example:

    ```bash
    $ get_pypi_latest_version opencv-python
    # 4.7.0.72

    $ get_pypi_latest_version opencv-python -a
    # 4.7.0.72
    # ['4.7.0.72', '4.7.0.68', '4.6.0.66', '4.5.5.64', '4.5.5.62', '4.5.4.60', '4.5.4.58', '4.5.3.56', '4.5.2.54', '4.5.2.52', '4.5.1.48', '4.4.0.46', '4.4.0.44', '4.4.0.42', '4.4.0.40', '4.3.0.38', '4.3.0.36', '4.2.0.34', '4.2.0.32', '4.1.2.30', '4.1.1.26', '4.1.0.25', '4.0.1.24', '4.0.0.21', '3.4.9.33', '3.4.8.29', '3.4.7.28', '3.4.6.27', '3.4.5.20', '3.4.4.19', '3.4.3.18', '3.4.2.17', '3.4.18.65', '3.4.17.63', '3.4.17.61', '3.4.16.59', '3.4.16.57', '3.4.15.55', '3.4.14.53', '3.4.14.51', '3.4.13.47', '3.4.11.45', '3.4.11.43', '3.4.11.41', '3.4.10.37', '3.4.1.15', '3.4.0.14']

    # case: package name error
    $ get_pypi_latest_version opencv
    # ValueError: No version information of opencv-pytho. Please check if the package name correct.
    ```

### 3. Use by python script

```python
from get_pypi_latest_version import GetPyPiLatestVersion

obtainer = GetPyPiLatestVersion()

package_name = 'opencv-python'
latest_version = obtainer(package_name)
print(latest_version)

result = obtainer(package_name, return_all_versions=True)
latest_version = result[0]
all_versions = result[1]
print(latest_version)
print(all_versions)
```

### Reference

- [poetry](https://github.com/python-poetry/poetry/blob/master/src/poetry/repositories/pypi_repository.py#L36)
