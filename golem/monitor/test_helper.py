import sys
from unittest import mock, TestCase
from uuid import uuid4

from golem.clientconfigdescriptor import ClientConfigDescriptor
from golem.monitor.model.nodemetadatamodel import NodeMetadataModel
from golem.monitor.monitor import SystemMonitor
from golem.monitorconfig import MONITOR_CONFIG


def meta_data():
    client_mock = mock.MagicMock()
    client_mock.get_key_id = mock.MagicMock(return_value='CLIID')
    client_mock.session_id = 'SESSID'
    client_mock.config_desc = ClientConfigDescriptor()
    client_mock.mainnet = False
    client_mock.concent_service.enabled = True
    return NodeMetadataModel(client_mock, sys.platform, 'app_version')


class MonitorTestBaseClass(TestCase):
    def setUp(self):
        self.monitor = SystemMonitor(meta_data(), MONITOR_CONFIG)
