import unittest

import aws_account_janitor.resources as resources


class ResourcesTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    def test_split_resource_arn__ec2(self):
        arn = 'arn:aws:ec2:eu-west-1:123456789:instance/i-0eb7b7c0dbec036ba'
        self.assertEqual(
          self._create_arn_dict([arn, 'ec2', 'eu-west-1', '123456789',
                                'instance', 'i-0eb7b7c0dbec036ba']),
          resources.split_resource_arn(arn))

    def test_split_resource_arn__s3(self):
        arn = 'arn:aws:s3:::bucketname'
        self.assertEqual(
          self._create_arn_dict([arn, 's3', '', '', 'bucketname', '']),
          resources.split_resource_arn(arn))

    def test_split_resource_arn__rds(self):
        arn = 'arn:aws:rds:eu-west-1:123456789:es:foo-eventsubscription'
        self.assertEqual(
          self._create_arn_dict([arn, 'rds', 'eu-west-1', '123456789',
                                'es', 'foo-eventsubscription']),
          resources.split_resource_arn(arn))
        arn = 'arn:aws:rds:eu-west-1:123456789:db:bar-db'
        self.assertEqual(
          self._create_arn_dict([arn, 'rds', 'eu-west-1', '123456789', 'db', 'bar-db']),
          resources.split_resource_arn(arn))

    def test_split_resource_arn__lambda(self):
        arn = 'arn:aws:lambda:eu-west-1:123456789:function:name'
        self.assertEqual(
          self._create_arn_dict([arn, 'lambda', 'eu-west-1', '123456789', 'function', 'name']),
          resources.split_resource_arn(arn))

    def test_collapse_tags(self):
        raw_tags = [
            {
              "Key": "foo",
              "Value": "1"
            },
            {
              "Key": "bar",
              "Value": "2"
            }
            ]
        self.assertEqual([('foo', '1'), ('bar', '2')], resources.collapse_tags(raw_tags))

    def _create_arn_dict(self, values):
        keys = ['arn', 'service', 'region', 'account_id', 'name', 'id']
        return dict(zip(keys, values))
