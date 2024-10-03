# fabric-testing
**Author: Lau Johansson**

![](https://debruyn.dev/2023/all-microsoft-fabric-icons-for-diagramming/Fabric_final_x256.png)


This library enables you to deploy python tests to [Microsoft Fabric](https://www.microsoft.com/en-us/microsoft-fabric).<br>

In short you can:
* Tests: Deploy and run custom tests
* Wheel: Deploy custom wheel that you want to test
* Requirements: Deploy custom requirements for the tests

With this CLI, it is possible to test functionalities like ``CREATE TABLE`` or ``MERGE INTO``.<br>
Also, working with Fabric built-in libraries like the ``notebookutils``. <br>

## Why do you need it?
With this CLI, you can run tests like the one below. It will enable you to run on-cluster
testing.

This will especially help two scenarios:
* CICD - automated testing: Submit and fetch tests in your Azure Pipelines / Github Workflows
* In a local development setup (your own computer), where you develop using a IDE - you can now deploy tests directly into Fabric

Lets say, you want to test some logic you have made, that creates a table and insert some data. 

How can you test the following code for Fabric today?  (Without actually have a Fabric open)


```python
import unittest
import uuid
from pyspark.sql import SparkSession


class CreateTable(unittest.TestCase):
    """
    This is an example of interacting with the default lakehouse.
    
    """
    def test_create_table(self):
        spark = SparkSession \
        .builder \
        .appName("fabric-testing example") \
        .config("spark.some.config.option", "some-value") \
        .getOrCreate()
        
        _uuid = _uuid = uuid.uuid4().hex

        table_name = f"test_table_{_uuid}"
        
        # Create table in default lakehouse
        spark.sql(f"CREATE TABLE {table_name} (col1 int)")
        
        # Insert data into table
        spark.sql(f"INSERT INTO {table_name} values (22)")

        # Assert data in the table
        table_with_one_row = spark.sql(f"select * from {table_name}")
        self.assertIsNotNone(table_with_one_row.count(), 1)
```

## Installation

[![PyPI version](https://badge.fury.io/py/fabric-testing.svg)](https://pypi.org/project/fabric-testing/)
[![PyPI](https://img.shields.io/pypi/dm/fabric-testing)](https://pypi.org/project/fabric-testing/)
```powershell
pip install fabric-testing
```

## CLI Usage

Deploy python tests to Fabric. You do not necessarily **need** to add a wheel or requirements, 
maybe you just have some tests you want to run inside Fabric:

```powershell
fabric-testing-submit `
    --tests-path <path> `
    --whl-path <path> ` #(optional)
    --requirements-file <path> ` #(optional)
    --workspace-name <name> `
    --workspace-id <id> `
    --lakehouse-name <name> `
    --lakehouse-id <id>
```

Fetch the notebook status from Fabric:
```powershell
fabric-testing-fetch `
    --tenant-id <your-tenant-id> `
    --url <your-fetch-url>

# or if you want to use logged fetch url
fabric-testing-fetch `
    --tenant-id <your-tenant-id> `
    --fetch-url-log-file-path <path-to-log-file>
```

If you want to follow along more "interactively", you can find the test run in the [Fabric Monitor](https://app.fabric.microsoft.com/monitoringhub?experience=data-engineering):


The interaction with OneLake use default azure login settings. 
Therefore, remember to login to the expected user (or spn):

```powershell
az login --tenant <tenant-id>
```

## How does it work?

The submit CLI does the following:
* Collects wheel, requirement file and python tests
* Uploads to OneLake
* Runs a test notebook as a job inside Fabric

The fetch CLI does the following:
* Load fetch url from submit
* Poll status from the Jobs API (the Fabric Monitor)

## Authentication support

### Fetch
Fetch should be fully supported both User and Service Principal

### Submit
Submit is only fully supported for User.

Currently the Job scheduler API only support ``User`` identity.

Fabric-testing library are expected to work for service principals
when these APIs support the identity. See the documentation:

* https://learn.microsoft.com/en-us/rest/api/fabric/core/job-scheduler/get-item-job-instance?tabs=HTTP
* https://learn.microsoft.com/en-us/rest/api/fabric/core/job-scheduler/get-item-schedule?tabs=HTTP


## Prerequisites
* Python 3.x (align the Fabric version with the version used in your tests)
* A Microsoft Fabric subscription
* Azure CLI (for authentication)
* Required permissions in the Fabric workspace (access to OneLake, ability to create and run notebooks)
  * User or service principal needs at the right level of access to the Fabric workspace
    * Needs access to onelake
    * Needs access to create and run notebooks
    * If your tests require other permissions, of course, give the permission to the SPN


# Limitations and known issues

* Ensure that the lakehouse for the test-upload (OneLake) in the same workspace as where you execute the notebook runs
* Referencing between test-files will cause import errors
* The test notebook that gets uploaded uses ``!pip`` and not ``%pip`` - although Microsoft recommends the last one.
  * This is due to challenges in activating inline-installation when running an on-demand job


# Future improvements
* Automatically extracts workspaceId and lakehouseId, so the user only needs to add names
* If the [create notebook API](https://learn.microsoft.com/en-us/rest/api/fabric/notebook/items/create-notebook?tabs=HTTP) supports uploading a base64 encoded .py file, instead of uploading .ipynb files - that could perhaps be preferable.
* Make it possible distinguish between the lakehouse for uploading the load test-files and the lakehouse that is chosen as default when testing

## Contributing

Contributions are welcome! To contribute:
- Fork the repository
- Create a new branch for your feature or bug fix
- Submit a pull request

Please ensure that your code follows the existing style and includes unit tests for any new features.
See the ``pyproject.toml`` or the ``.github/workflows/pr.yml`` to inspect which ruff format/linting checks are made, and which tests are executed.


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Changelog

### Version 0.1.0
- Initial release with CLI for submitting and fetching tests from Microsoft Fabric

