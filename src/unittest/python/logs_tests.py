import boto3
import unittest
from moto import mock_logs
from unittest.mock import patch, MagicMock, call

import aws_account_janitor.logs as logs


class CloudwatchLogsTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    def get_log_groups(self, nextToken=None):
        log_groups = [
            {
                'logGroups': [
                    {
                        'logGroupName': 'foo',
                        'creationTime': 123,
                        'metricFilterCount': 0,
                        'arn': 'string',
                        'storedBytes': 123
                    },
                    {
                        'logGroupName': 'bar',
                        'creationTime': 123,
                        'metricFilterCount': 0,
                        'arn': 'string',
                        'storedBytes': 123
                    },
                    {
                        'logGroupName': 'xxx',
                        'creationTime': 123,
                        'retentionInDays': 123,
                        'metricFilterCount': 0,
                        'arn': 'string',
                        'storedBytes': 123
                    },
                ],
                'nextToken': 'string'
            }, {
                'logGroups': [
                    {
                        'logGroupName': 'zzz',
                        'creationTime': 123,
                        'retentionInDays': 123,
                        'metricFilterCount': 123,
                        'arn': 'string',
                        'storedBytes': 123
                    },
                ]}
            ]
        if nextToken:
            if nextToken == 'string':
                return log_groups[1]
            else:
                raise
        else:
            return log_groups[0]

    @patch('boto3.client')
    def test_get_log_groups_paginated_results(self, mock):
        client = MagicMock()
        client.describe_log_groups.side_effect = self.get_log_groups
        mock.return_value = client

        result = logs.get_log_groups()
        calls = [call(), call(nextToken='string')]
        client.describe_log_groups.assert_has_calls(calls)
        print(result)
        self.assertEqual(4, len(result))

    @patch('aws_account_janitor.logs.get_log_groups')
    def test_get_log_groups_wo_retention(self, mock):
        mock.return_value = self.get_log_groups()['logGroups']
        result = logs.get_log_groups_wo_retention()
        print(result)
        self.assertEqual(2, len(result))
