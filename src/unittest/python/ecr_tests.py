import boto3
import unittest2 as unittest
from unittest.mock import patch
from moto import mock_ecr


from aws_account_janitor.ecr import list_images, purge_images

EXAMPLE_DOCKER_MANIFEST = '''
    {
  "schemaVersion": 2,
  "mediaType": "application/vnd.docker.distribution.manifest.list.v2+json",
  "manifests": [
    {
      "mediaType": "application/vnd.docker.image.manifest.v2+json",
      "size": 7143,
      "digest": "sha256:e692418e4cbaf90ca69d05a66403747baa33ee08806650b51fab815ad7fc331f",
      "platform": {
        "architecture": "ppc64le",
        "os": "linux",
      }
    },
    {
      "mediaType": "application/vnd.docker.image.manifest.v2+json",
      "size": 7682,
      "digest": "sha256:5b0bcabd1ed22e9fb1310cf6c2dec7cdef19f0ad69efa1f392e94a4333501270",
      "platform": {
        "architecture": "amd64",
        "os": "linux",
        "features": [
          "sse4"
        ]
      }
    }
  ]
}
'''


class ECRTests(unittest.TestCase):

    def setup(self):
        client = boto3.client('ecr')
        client.create_repository(repositoryName='foo')
        client.put_image(
            repositoryName='foo',
            imageManifest=EXAMPLE_DOCKER_MANIFEST,
            imageTag='bar'
        )
        client.put_image(
            repositoryName='foo',
            imageManifest=EXAMPLE_DOCKER_MANIFEST,
            imageTag='bar2'
        )

    # not implemented in moto yet
    @mock_ecr
    def _disabled_test_purge_images(self):
        self.setup()
        self.assertEqual(2, len(list_images('foo')), 'start with 2 images')
        purge_images('foo')
        self.assertEqual(0, len(list_images('foo')))

    @mock_ecr
    def test_list_images(self):
        client = boto3.client('ecr')
        client.create_repository(repositoryName='foo')
        client.put_image(
            repositoryName='foo',
            imageManifest=EXAMPLE_DOCKER_MANIFEST,
            imageTag='bar'
        )
        client.put_image(
            repositoryName='foo',
            imageManifest=EXAMPLE_DOCKER_MANIFEST,
            imageTag='bar2'
        )
        self.assertEqual(2, len(list_images('foo')))
