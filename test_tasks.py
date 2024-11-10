import unittest
from unittest.mock import patch
from tasks import *


class TestTaskFunctions(unittest.TestCase):
    @patch('matplotlib.pyplot.show')
    def test_task_1(self, mock_show):
        issues = [
            {
                'fields': {
                    'assignee': {'displayName': 'User1'},
                    'created': '2024-10-01T10:00:00.000+0000',
                    'resolutiondate': '2024-10-01T15:00:00.000+0000'
                }
            },
            {
                'fields': {
                    'assignee': {'displayName': 'User2'},
                    'created': '2024-10-01T10:00:00.000+0000',
                    'resolutiondate': '2024-10-02T15:00:00.000+0000'
                }
            },
            {
                'fields': {
                    'assignee': {'displayName': 'User3'},
                    'created': '2024-10-01T10:00:00.000+0000',
                    'resolutiondate': '2024-10-04T15:00:00.000+0000'
                }
            }
        ]

        task_1(issues)

        # Проверяем, что график был построен (проверка наличия оси X)
        ax = plt.gca()
        x_labels = [label.get_text() for label in ax.get_xticklabels()]

        # Проверяем, что ось X содержит правильные значения (например, дни: 0, 1, 3)
        self.assertIn('0.0', x_labels)
        self.assertIn('1.0', x_labels)
        self.assertIn('3.0', x_labels)

        # Проверяем, что функция не выдала ошибку при построении графика
        self.assertTrue(ax.has_data())

    @patch("matplotlib.pyplot.hist")
    @patch("tasks.get_status_times")
    def test_task_2(self, mock_get_status_times, mock_hist):
        issues = [
            {'fields': {'created': '2024-11-01T12:00:00.000+0000', 'resolutiondate': '2024-11-05T12:00:00.000+0000',
                        'changelog': {'histories': []}}},
            {'fields': {'created': '2024-10-01T12:00:00.000+0000', 'resolutiondate': '2024-10-05T12:00:00.000+0000',
                        'changelog': {'histories': []}}}
        ]

        mock_get_status_times.return_value = {'Open': 4, 'In Progress': 2}  # Мокаем статусные данные

        task_2(issues)
        mock_hist.assert_called()  # Проверяем, что hist был вызван

    @patch("matplotlib.pyplot.plot")
    def test_task_3(self, mock_plot):
        issues = [
            {'fields': {'created': '2024-11-01T12:00:00.000+0000', 'resolutiondate': '2024-11-05T12:00:00.000+0000'}},
            {'fields': {'created': '2024-10-01T12:00:00.000+0000', 'resolutiondate': '2024-10-05T12:00:00.000+0000'}}
        ]

        task_3(issues)
        mock_plot.assert_called()  # Проверяем, что plot был вызван

    @patch("matplotlib.pyplot.barh")
    def test_task_4(self, mock_barh):
        issues = [
            {'fields': {'assignee': {'displayName': 'User1'}, 'reporter': {'displayName': 'User2'}}},
            {'fields': {'assignee': {'displayName': 'User2'}, 'reporter': {'displayName': 'User3'}}}
        ]

        task_4(issues)
        mock_barh.assert_called()  # Проверяем, что barh был вызван

    @patch("matplotlib.pyplot.bar")
    def test_task_5(self, mock_bar):
        issues = [
            {
                'fields': {
                    'assignee': {'displayName': 'User1'},
                    'resolutiondate': '2024-10-05T12:00:00.000+0000',
                    'created': '2024-09-25T08:30:00.000+0000'
                }
            }
        ]

        task_5(issues, 'User1')
        mock_bar.assert_called()  # Проверяем, что bar был вызван

    @patch("matplotlib.pyplot.bar")
    def test_task_6(self, mock_bar):
        issues = [
            {'fields': {'priority': {'name': 'High'}}},
            {'fields': {'priority': {'name': 'Low'}}}
        ]

        task_6(issues)
        mock_bar.assert_called()  # Проверяем, что bar был вызван


if __name__ == '__main__':
    unittest.main()
