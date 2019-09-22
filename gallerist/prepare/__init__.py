import os
import logging
import azure.functions as func
from gallerist import Gallerist
from galleristazurestorage import AzureBlobFileStore
from azure.common import AzureMissingResourceHttpError
from azure.storage.common import CloudStorageAccount
from essentials.json import dumps
from roconfiguration import Configuration, ConfigurationError


def load_configuration() -> Configuration:
    configuration = Configuration()
    configuration.add_yaml_file('gallerist.yaml')
    configuration.add_yaml_file('gallerist-secrets.yaml')
    configuration.add_environmental_variables('GALLERIST_')
    return configuration


def _ensure_configuration(**kwargs):
    for key, value in kwargs.items():
        if not value:
            raise ConfigurationError(f'Missing `{key}` configuration')


def get_store():
    configuration = load_configuration()
    account_name = configuration.account_name
    account_key = configuration.account_key
    container_name = configuration.container_name

    _ensure_configuration(account_name=account_name, 
                          account_key=account_key, 
                          container_name=container_name)

    return AzureBlobFileStore(CloudStorageAccount(account_name=account_name, account_key=account_key), container_name)


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    picture = req.params.get('picture')

    if not picture:
        return func.HttpResponse(
             "Missing `picture` parameter",
             status_code=400
        )

    try:
        gallerist = Gallerist(get_store())
    except ConfigurationError:
        logging.exception('Configuration error')
        return func.HttpResponse(
             "Configuration error.",
             status_code=500
        )

    try:
        metadata = gallerist.process_image(picture)
    except AzureMissingResourceHttpError:
        return func.HttpResponse(
             "Source picture not found",
             status_code=404
        )

    return func.HttpResponse(dumps(metadata), mimetype='application/json')
