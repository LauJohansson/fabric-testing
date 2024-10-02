import json
import re
from urllib.request import urlopen

from packaging.version import parse

init_file_path = "src/fabrictesting/__init__.py"


def main():
    # find out what version to use
    pypi_v = get_test_pypi_version()
    local_v = get_local_version()
    if local_v > pypi_v:
        version = local_v.base_version
    else:
        version = f"{pypi_v.major}.{pypi_v.minor}.{pypi_v.micro+1}"

    # Update the __version__ in __init__.py
    update_version_in_init(version)


def get_local_version():
    with open(init_file_path) as f:
        content = f.read()
        # Use regex to extract the version number
        version_match = re.search(r"__version__\s*=\s*['\"]([^'\"]+)['\"]", content)
        if version_match:
            v = parse(version_match.group(1))
            return v
        else:
            return parse("0.0.0")


def update_version_in_init(version):
    with open(init_file_path, "r") as f:
        content = f.read()

    # Use regular string formatting to build the new version line
    new_content = re.sub(
        r"__version__\s*=\s*['\"][^'\"]+['\"]", f'__version__ = "{version}"', content
    )

    print("Writes version:")
    print(new_content)

    with open(init_file_path, "w") as f:
        f.write(new_content)


def get_test_pypi_version():
    try:
        test_pypi = json.load(urlopen("https://test.pypi.org/pypi/fabric-testing/json"))
        test_pypi_version = parse(test_pypi["info"]["version"])
        return test_pypi_version
    except:  # noqa: E722  # bare except is fine in this simple case
        return parse("0.0.0")


if __name__ == "__main__":
    main()
