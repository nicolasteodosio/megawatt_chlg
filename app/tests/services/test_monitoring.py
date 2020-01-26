from unittest import mock
from unittest.mock import Mock

from django.test import TestCase

from app.services.monitoring import MonitoringService


class TestMonitoringService(TestCase):

    def setUp(self) -> None:
        self.request_session_mock = mock.patch('app.services.monitoring.requests_retry_session').start()

    def tearDown(self) -> None:
        mock.patch.stopall()

    def test_class_instance_required_parameter_plant(self):
        self.assertRaises(TypeError, MonitoringService, start_date='2020-02-02', end_date='2020-10-10')

    def test_class_instance_required_parameter_start_date(self):
        self.assertRaises(TypeError, MonitoringService, plant='test', end_date='2020-10-10')

    def test_class_instance_required_parameter_end_date(self):
        self.assertRaises(TypeError, MonitoringService, start_date='2020-02-02', plant='test')

    def test_pull_data_successfully(self):
        self.request_session_mock.return_value.get.return_value = Mock(json={'test': 'test'})
        monitoring_service = MonitoringService(start_date='2020-02-02', end_date='2020-10-10', plant='test')

        data = monitoring_service.pull_data()
        self.assertEqual(data, {'test': 'test'})
