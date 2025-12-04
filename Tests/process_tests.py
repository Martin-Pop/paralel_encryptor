import unittest
from unittest.mock import patch, Mock

class ProcessTests(unittest.TestCase):

    def test_clean_up_zombies_on_failure(self):

        worker_count = 3
        mock_config = {}

        with patch('encryption.worker_handler.Process') as MockProcess:

            process_1 = Mock()
            process_2 = Mock()
            process_3 = Mock()

            MockProcess.side_effect = [process_1, process_2, process_3]

            process_1.start.return_value = None
            process_2.start.return_value = None
            process_3.start.side_effect = Exception("System limit reached")

            try:

                import encryption.worker_handler as wh
                wh.start_workers(worker_count, mock_config)

            except Exception:
                pass #should err

            process_1.terminate.assert_called()
            process_2.terminate.assert_called()


if __name__ == '__main__':
    unittest.main()