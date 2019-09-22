# Gallerist-AzureFunctions
Azure Functions project to process images for the web, using Python 3, [Pillow](https://pillow.readthedocs.io), [Gallerist](https://github.com/RobertoPrevato/Gallerist); reading source pictures from an [Azure Storage Blob Service](https://github.com/RobertoPrevato/Gallerist-AzureStorage), writing resized pictures inside the same storage.

Tested and proved to work with Python 3.6.8 and 3.7.0. Version 3.6.8 is currently the version recommended by Microsoft for Azure Functions 2 (as of today, the 22nd of September 2019).

# How to run locally
1. install [Azure Functions CLI](https://github.com/Azure/azure-functions-core-tools).
1. create a Python virtual environment
1. install dependencies described in `requirements.txt`
1. configure storage account name and key in YAML files, or environmental variables as described in `gallerist.yaml` comments; and also the blob container name (a container must exist already in the blob service)
1. start the functions host from the `gallerist` folder:

```bash
$ func start

## ...
/gallerist (master)$ func start

                  %%%%%%
                 %%%%%%
            @   %%%%%%    @
          @@   %%%%%%      @@
       @@@    %%%%%%%%%%%    @@@
     @@      %%%%%%%%%%        @@
       @@         %%%%       @@
         @@      %%%       @@
           @@    %%      @@
                %%
                %
```

## Seeing it in practice:
To make a manual verification and understand what's offered by this Azure Functions, do the following:

1. configure an Azure Storage account and settings for the function, as described above
1. create a container inside the Blob Service (can be private)
1. upload a picture to the container, for example using Azure Storage Explorer: Gallerist library handles by default JPG, PNG, GIF (including animated GIFs), MPO - supporting more formats require to edit the provided code
1. start the Azure Function as described above
1. hit the endpoint with a `picture` query string parameter, for example: `http://localhost:7071/api/prepare?picture=01.jpg`
1. the function generates a medium size picture, and a thumbnail picture, stores them in the same container, and returns useful metadata that can be stored and used by a client to display a front-end, like in the box below

```json
{
  "width": 2071,
  "height": 2895,
  "extension": ".jpg",
  "ratio": 0.7153713298791019,
  "mime": "image/jpeg",
  "versions": [
    {
      "id": "a7ed03d7d3b64dc98bee094d1ade12e5",
      "size_name": "medium",
      "max_side": 1200,
      "file_name": "m-a7ed03d7d3b64dc98bee094d1ade12e5.jpg"
    },
    {
      "id": "ffc5f80e1033424dbf681ad5768a56cf",
      "size_name": "thumbnail",
      "max_side": 200,
      "file_name": "t-ffc5f80e1033424dbf681ad5768a56cf.jpg"
    }
  ]
}
```

# How to run in production
Refer to [Microsoft documentation](https://docs.microsoft.com/en-us/azure/azure-functions/), choose one of the several ways to run Azure Functions 2 (e.g. in Azure Functions service, in Kubernetes using KEDA, or Knative, through Docker).
