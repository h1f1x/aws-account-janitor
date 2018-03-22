import time
import unittest
from unittest.mock import patch, MagicMock, call

import aws_account_janitor.logs as logs


class CloudwatchLogsTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    def describe_log_groups(self, nextToken=None):
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
                        'retentionInDays': 7,
                        'metricFilterCount': 0,
                        'arn': 'string',
                        'storedBytes': 123
                    },
                    {
                        'logGroupName': 'xxx',
                        'creationTime': 123,
                        'retentionInDays': 14,
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

    def describe_log_streams(self, logGroupName, orderBy, descending, limit):
        return {
            'logStreams': [
                {
                    'logStreamName': 'string',
                    'creationTime': 1,
                    'firstEventTimestamp': 1,
                    'lastEventTimestamp': 123,
                    'lastIngestionTime': 123,
                    'uploadSequenceToken': 'string',
                    'arn': 'string',
                    'storedBytes': 123
                },
            ]
        }

    @patch('boto3.client')
    def test_describe_log_groups_paginated_results(self, mock):
        client = MagicMock()
        client.describe_log_groups.side_effect = self.describe_log_groups
        mock.return_value = client

        result = logs.list_log_groups()
        calls = [call(), call(nextToken='string')]
        client.describe_log_groups.assert_has_calls(calls)
        print(result)
        self.assertEqual(4, len(result))

    @patch('aws_account_janitor.logs.list_log_groups')
    def test_list_log_groups_wo_retention(self, mock):
        mock.return_value = self.describe_log_groups()['logGroups']
        result = logs.list_log_groups_wo_retention()
        print(result)
        self.assertEqual(1, len(result))

    @patch('boto3.client')
    def test_get_last_event_time(self, mock):
        client = MagicMock()
        client.describe_log_streams.side_effect = self.describe_log_streams
        mock.return_value = client

        result = logs.get_last_event_time('foo')
        self.assertEqual(123, result)

    @patch('boto3.client')
    def test_get_last_event_time__no_streams(self, mock):
        client = MagicMock()
        client.describe_log_streams.return_value = {'logStreams': []}
        mock.return_value = client

        result = logs.get_last_event_time('foo')
        self.assertEqual(None, result)

    @patch('aws_account_janitor.logs.get_time_in_millis')
    @patch('aws_account_janitor.logs.get_offset')
    @patch('aws_account_janitor.logs.list_log_groups')
    @patch('aws_account_janitor.logs.get_last_event_time')
    def test_list_not_used_log_groups(self,
                                      mock_get_last_event_time,
                                      mock_list_log_groups,
                                      mock_get_offset,
                                      mock_get_time_in_millis):
        mock_list_log_groups.return_value = {
            'logGroupName': 'foo',
            'retentionInDays': 7,
        }, {
            'logGroupName': 'bar',
            'retentionInDays': 14,
        }
        mock_get_time_in_millis.return_value = 100
        mock_get_last_event_time.return_value = 80
        mock_get_offset.side_effect = [7, 14]
        result = logs.list_not_used_log_groups()
        self.assertEqual(1, len(result))

    @patch('aws_account_janitor.logs.get_time_in_millis')
    @patch('aws_account_janitor.logs.list_log_groups')
    def test_list_not_used_log_groups__skip_wo_retention(self,
                                                         mock_list_log_groups,
                                                         mock_get_time_in_millis):
        mock_list_log_groups.return_value = {'logGroupName': 'foo'},
        {'logGroupName': 'bar'}
        result = logs.list_not_used_log_groups()
        self.assertEqual(0, len(result))
