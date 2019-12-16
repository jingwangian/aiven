from app.app import start_etl


import app

from dataclasses import dataclass
from unittest.mock import Mock, patch


@dataclass
class Record:
    key: bytes
    value: bytes


@dataclass
class MockMetric:
    name: str
    load_from_string: any


class TestApp:
    @patch('app.monitor.monitor.get_metrics')
    @patch('app.utils.pubsub.Consumer.get_consumer')
    @patch('app.db.dbc')
    def test_start_etl(self, mock_dbc, mock_get_consumer, mock_get_metrics):
        print(mock_dbc)

        r1 = Record(b'cpu_metric', b'100')
        r2 = Record(b'mem_metric', b'200')
        r3 = Record(b'dis_metric', b'300')

        mock_get_consumer.return_value = [r1, r2, r3]

        mock_cpumetric = Mock()
        mock_memmetric = Mock()

        mock_CPUMetric = Mock()
        mock_MemMetric = Mock()

        # mock_get_metrics.return_value = [mock_CPUMetric, mock_MemMetric]
        mock_get_metrics.return_value = [
            MockMetric("cpu_metric", mock_CPUMetric),
            MockMetric("mem_metric", mock_MemMetric)]

        mock_CPUMetric.return_value = mock_cpumetric
        mock_MemMetric.return_value = mock_memmetric

        start_etl()

        mock_cpumetric.save_to_db.assert_called_once()
        mock_memmetric.save_to_db.assert_called_once()

    def test_start_monitor(self):
        pass
