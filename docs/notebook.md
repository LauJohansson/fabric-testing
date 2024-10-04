# Notebook creation

For now, this project executes pytests from a notebook. There will probably (or not) in the future be more 
obvious ways to launch python tests to Fabric. Nethertheless, notebooks can be created using [Item - Create Notebook](https://learn.microsoft.com/en-us/rest/api/fabric/notebook/items/create-notebook?tabs=HTTP)
. 

To investigate how a notebook is defined - we must dive into the [Notebook definition](https://learn.microsoft.com/en-us/rest/api/fabric/articles/item-management/definitions/notebook-definition).

The first information that set the boundaries of the fabric-testing project, is the supported format:
``Notebook items support the ipynb format``. 

Furthermore, three informations are important:
* Path (The file name)
* Payloadtype (InlineBase64)
* Payload (A notebook that is base 64 encoded)

With these retstrictions on how to upload notebook using the API, the initial way of uploading a notebook,
is having a notebook file ``notebook/notebook-content.ipynb``. This notebook, is a template for how to:
* Load the wheel, tests and requirements from OneLake
* Install the requirements
* Install the wheel
* Run the tests


## notebook content
I my mind, working with ``.ipynb`` files can be tricky.
* json format - difficult to review and have metadata
* cell metadata and cell output changes
* allows non-linear workflow
* difficult to test (notebooks are interactive and cell-based)

I would always recommend working with ``.py`` files. But Fabric API does not support it, so we must keep it for now. 

There are one element of the notebooks I find very useful to know. The metadata stores information on the attached
lakehouse and environment.

This project does not currently support defining environments, but could be a feature later.

When you use the fabric-testing CLI, the metadata is manipulated, and replaced with your inputs. Here you see the
how the dependencies look "under-the-hood":

The `metadata`:
```json
{
  "dependencies": {
    "environment": {},
    "lakehouse": {
      "default_lakehouse": "<lakehouse-id>",
      "default_lakehouse_name": "<lakehouse-name>",
      "default_lakehouse_workspace_id": "<workspace-id-for-the-lakehouse>"
    }
  }
}
```

Please note that this project assumes that the workspace of the notebook and the workspace of the lakehouse is the same.

## Information on .py notebooks

Notebooks can be saved as ``.py``, and when/if the API supports it, it may be beneficial to use python files instead of notebooks.
I believe the ``# Fabric notebook source`` lets Fabric know, that the python file should be interpreted as notebook.

The metadata is defined as metadata-comments:

```python
# Fabric notebook source

# METADATA ********************

# META   "dependencies": {
# META     "lakehouse": {
# META        "default_lakehouse": "<lakehouse-id>",
# META        "default_lakehouse_name": "<lakehouse-name>",
# META        "default_lakehouse_workspace_id": "<workspace-id-for-the-lakehouse>",
# META        "known_lakehouses": [
# META         {
# META           "id": "<some-id>"
# META         }
# META       ]
# META     }
# META   }
# META }
```

