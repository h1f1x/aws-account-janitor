import boto3
import time
from .logging import log

client = boto3.client('ecr')



def purge_images(repository_name):
    image_ids = [imageDigest for imageDigest in list_images(repository_name)]
    client.batch_delete_image(repositoryName=repository_name, imageIds=image_ids)


def list_images(repository_name):
    response = client.list_images(
        repositoryName=repository_name)
    return response['imageIds']
