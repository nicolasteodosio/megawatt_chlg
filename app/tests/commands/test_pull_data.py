from unittest import mock

from django.core.management import call_command, CommandError
from django.test import TestCase
from model_mommy import mommy

from app.models import Plant


class TestPullDataCommand(TestCase):
    def setUp(self) -> None:
        self.monitoring_service_mock = mock.patch('app.services.monitoring.MonitoringService').start()

    def tearDown(self) -> None:
        mock.patch.stopall()

    def test_call_command_name_required(self):
        opt = {'fromdate': '2019-10-10',
               'todate': '2019-10-10'}
        self.assertRaises(CommandError, call_command, 'pull_data', **opt)

    def test_call_command_fromdate_required(self):
        opt = {'name': 'test',
               'todate': '2019-10-10'}
        self.assertRaises(CommandError, call_command, 'pull_data', **opt)

    def test_call_command_todate_required(self):
        opt = {'name': 'test',
               'fromdate': '2019-10-10',
               }
        self.assertRaises(CommandError, call_command, 'pull_data', **opt)

    def test_call_command_required_parameters(self):
        self.assertRaises(CommandError, call_command, 'pull_data')

    def test_call_command_plant_dont_exist(self):
        opt = {'name': 'test',
           'fromdate': '2019-10-10',
           'todate': '2019-10-10',
           }
        self.assertRaises(CommandError, call_command, 'pull_data', **opt)
        self.monitoring_service_mock.assert_not_called()

    def test_call_command_invalid_date(self):
        mommy.make(Plant, name='test')
        opt = {'name': 'test',
           'fromdate': '2019-1010',
           'todate': '2019-10-10',
           }
        self.assertRaises(CommandError, call_command, 'pull_data', **opt)
        self.monitoring_service_mock.assert_not_called()

    def test_call_command_invalid_date_with_hour(self):
        mommy.make(Plant, name='test')
        opt = {'name': 'test',
           'fromdate': '2019-10-10',
           'todate': '2019-10-10 12:22:00',
           }
        self.assertRaises(CommandError, call_command, 'pull_data', **opt)
        self.monitoring_service_mock.assert_not_called()

    def test_call_command_correct_parameters(self):
        mommy.make(Plant, name='test')
        opt = {'name': 'test',
               'fromdate': '2019-10-10',
               'todate': '2019-10-10',}
        call_command('pull_data', **opt)
        self.monitoring_service_mock.assert_called_once_with(end_date='2019-10-10', plant='test', start_date='2019-10-10')
        self.monitoring_service_mock.return_value.pull_data.assert_called_once()
