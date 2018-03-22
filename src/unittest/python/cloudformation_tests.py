from datetime import datetime
import unittest
from unittest.mock import patch, MagicMock, call

import aws_account_janitor.cloudformation as cloudformation


class CloudformationTests(unittest.TestCase):

    def cf_list_stacks_mock(self, StackStatusFilter=None):
        cf_status = [
            'CREATE_IN_PROGRESS', 'CREATE_FAILED', 'CREATE_COMPLETE',
            'ROLLBACK_IN_PROGRESS', 'ROLLBACK_FAILED', 'ROLLBACK_COMPLETE',
            'DELETE_IN_PROGRESS', 'DELETE_FAILED', 'DELETE_COMPLETE',
            'UPDATE_IN_PROGRESS', 'UPDATE_COMPLETE_CLEANUP_IN_PROGRESS',
            'UPDATE_COMPLETE', 'UPDATE_ROLLBACK_IN_PROGRESS', 'UPDATE_ROLLBACK_FAILED',
            'UPDATE_ROLLBACK_COMPLETE_CLEANUP_IN_PROGRESS', 'UPDATE_ROLLBACK_COMPLETE',
            'REVIEW_IN_PROGRESS']

        stacks = []
        for status in cf_status:
            if (StackStatusFilter and status in StackStatusFilter) or StackStatusFilter is None:
                stacks.append(
                    {
                        'StackId': 'string',
                        'StackName': 'stack-{}'.format(status),
                        'TemplateDescription': 'string',
                        'CreationTime': datetime(2015, 1, 1),
                        'LastUpdatedTime': datetime(2015, 1, 1),
                        'DeletionTime': datetime(2015, 1, 1),
                        'StackStatus': status,
                        'StackStatusReason': 'string',
                        'ParentId': 'string',
                        'RootId': 'string'
                    })
        return {'StackSummaries': stacks}

    def test_cf_list_stacks_mock(self):
        self.assertEqual(17, len(self.cf_list_stacks_mock()['StackSummaries']))
        res = self.cf_list_stacks_mock(StackStatusFilter=['DELETE_FAILED'])
        self.assertEqual(1, len(res['StackSummaries']))
        res = self.cf_list_stacks_mock(StackStatusFilter=['DELETE_FAILED', 'CREATE_FAILED'])
        self.assertEqual(2, len(res['StackSummaries']))

    @patch('boto3.client')
    def test_list_stacknames_by_status(self, mock):
        client = MagicMock()
        client.list_stacks.side_effect = self.cf_list_stacks_mock
        mock.return_value = client

        result = cloudformation.list_stacknames_by_status(status='DELETE_FAILED')
        self.assertEqual(1, len(result))
        self.assertEqual('stack-DELETE_FAILED', result[0])

    @patch('click.confirm')
    @patch('aws_account_janitor.cloudformation.list_stacknames_by_status')
    @patch('boto3.client')
    def test_cleanup__happy_path(self,
                                 mock_boto3, mock_list_stacknames_by_status, mock_click_confirm):
        client = MagicMock()
        mock_boto3.return_value = client
        mock_list_stacknames_by_status.return_value = ['foo-stack', 'bar-stack']
        mock_click_confirm.return_value = True

        cloudformation.cleanup(status='DELETE_FAILED')
        mock_list_stacknames_by_status.assert_called_with('DELETE_FAILED')
        calls = [call(StackName='foo-stack'), call(StackName='bar-stack')]
        client.delete_stack.assert_has_calls(calls)

    @patch('click.confirm')
    @patch('aws_account_janitor.cloudformation.list_stacknames_by_status')
    @patch('boto3.client')
    def test_cleanup__not_confirmed(self,
                                    mock_boto3,
                                    mock_list_stacknames_by_status, mock_click_confirm):
        client = MagicMock()
        mock_boto3.return_value = client
        mock_list_stacknames_by_status.return_value = ['foo-stack']
        mock_click_confirm.return_value = False

        cloudformation.cleanup(status='FOO')
        mock_list_stacknames_by_status.assert_called_with('FOO')
        client.delete_stack.assert_not_called()

    @patch('aws_account_janitor.cloudformation.list_stacknames_by_status')
    @patch('boto3.client')
    def test_cleanup__non_interactive(self, mock_boto3, mock_list_stacknames_by_status):
        client = MagicMock()
        mock_boto3.return_value = client
        mock_list_stacknames_by_status.return_value = ['foo-stack']

        cloudformation.cleanup(status='FOO', interactive=False)
        mock_list_stacknames_by_status.assert_called_with('FOO')
        calls = [call(StackName='foo-stack')]
        client.delete_stack.assert_has_calls(calls)
