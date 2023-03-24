## get_pypi_latest_version
<p>
    <a href=""><img src="https://img.shields.io/badge/Python->=3.7,<=3.10-aff.svg"></a>
    <a href=""><img src="https://img.shields.io/badge/OS-Linux%2C%20Win%2C%20Mac-pink.svg"></a>
    <a href="https://pypi.org/project/get_pypi_latest_version/"><img alt="PyPI" src="https://img.shields.io/pypi/v/get_pypi_latest_version"></a>
</p>


### 1. Install package by pypi.
```bash
$ pip install get_pypi_latest_version
```

### 2. Run by command line.
- Usage:
    ```bash
    $ get_pypi_latest_version -h
    usage: get_pypi_latest_version [-h] package_name

    positional arguments:
    package_name  The specified python package name. e.g. opencv-python.

    optional arguments:
    -h, --help    show this help message and exit
    ```
- Example:
    ```bash
    $ get_pypi_latest_version opencv-python
    # 4.7.0.72
    ```

### 3. Use by python script.
```python
from get_pypi_latest_version import GetPyPiLatestVersion

obtainer = GetPyPiLatestVersion()

package_name = 'opencv-python'
latest_version = obtainer(package_name)
print(latest_version)
```

### Reference
- [poetry](https://github.com/python-poetry/poetry/blob/master/src/poetry/repositories/pypi_repository.py#L36)