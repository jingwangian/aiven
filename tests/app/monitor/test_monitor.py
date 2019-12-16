import json
from unittest.mock import Mock, patch
from app.monitor.monitor import CPUMetric


class TestCPUMetric:
    def test_init(self):
        cpu = CPUMetric(1, 2, 3, 4, 5, '2019-01-01')

        assert cpu.name == 'cpu_metric'
        assert cpu.created_at == '2019-01-01'

    def test_dump_to_string(self):
        metric_input = {
            "machine_id": 100,
            "user": 200,
            "nice": 2,
            "system": 150,
            "idle": 60,
            "created_at": '2019-01-01 01:02:03'
        }

        cpu = CPUMetric(**metric_input)

        dump_string = cpu.dump_to_string()

        assert dump_string == json.dumps(metric_input)

    def test_save_to_db(self, mocker):
        cpu = CPUMetric(1, 2, 3, 4, 5, '2019-01-01')

        connection = Mock()
        cur = Mock()

        connection.cursor.return_value.__enter__ = Mock(return_value=cur)
        connection.cursor.return_value.__exit__ = Mock()
        cpu.save_to_db(connection)

        cur.execute.assert_called_once()
        connection.commit.assert_called_once()
        # assert 1 == 0

    def test_create_table(self, mocker):
        cpu = CPUMetric(1, 2, 3, 4, 5, '2019-01-01')

        connection = Mock()
        cur = Mock()

        connection.cursor.return_value.__enter__ = Mock(return_value=cur)
        connection.cursor.return_value.__exit__ = Mock()
        cpu.save_to_db(connection)

        cur.execute.assert_called_once()
        connection.commit.assert_called_once()
