import os
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from collections import defaultdict
from utils.utils import get_assignee_time, get_status_times


def task_1(issues):
    times = []
    for issue in issues:
        created = datetime.strptime(issue['fields']['created'], '%Y-%m-%dT%H:%M:%S.%f%z')
        resolved = datetime.strptime(issue['fields']['resolutiondate'], '%Y-%m-%dT%H:%M:%S.%f%z')
        open_time = (resolved - created).days
        times.append(open_time)

    plt.hist(times, bins=20, edgecolor='black')
    plt.xlabel('Количество дней в открытом состоянии')
    plt.ylabel('Количество заявок')
    plt.title('1. Потраченное время на решение задачи')
    plt.show()
    if os.getenv('ZOOM', 'false').lower() == "true":
        count = len(issues)
        times.sort()
        middle_index = int(count / 1.4)
        first_part = times[:middle_index]

        plt.hist(first_part, bins=40, edgecolor='black')
        plt.xlabel('Количество дней в открытом состоянии')
        plt.ylabel('Количество заявок')
        plt.title('1. Потраченное время на решение задачи')
        plt.show()


def task_2(issues):
    status_data = {}

    for issue in issues:
        status_times = get_status_times(issue)
        for status, time_spent in status_times.items():
            if status in status_data:
                status_data[status].append(time_spent)
            else:
                status_data[status] = [time_spent]

    for status, times in status_data.items():
        plt.hist(times, bins=40, edgecolor='black')
        plt.xlabel('Количество дней')
        plt.ylabel('Количество задач')
        plt.title(f'Распределение времени в состоянии {status}')
        plt.show()

        if os.getenv('ZOOM', 'false').lower() == "true":
            times_filtered = [t for t in times if t <= 60]
            bins = np.linspace(0, 60, 41)

            plt.hist(times_filtered, bins=bins, edgecolor='black')
            plt.xlabel('Количество дней')
            plt.ylabel('Количество задач')
            plt.title(f'Распределение времени в состоянии {status} на меньшем интервале')
            plt.show()


def task_3(issues):
    created_dates = defaultdict(int)
    closed_dates = defaultdict(int)

    for issue in issues:
        created_date = datetime.strptime(issue['fields']['created'], '%Y-%m-%dT%H:%M:%S.%f%z').date()
        created_dates[created_date] += 1

        if issue['fields']['resolutiondate']:
            closed_date = datetime.strptime(issue['fields']['resolutiondate'], '%Y-%m-%dT%H:%M:%S.%f%z').date()
            closed_dates[closed_date] += 1

    min_date = min(created_dates.keys() | closed_dates.keys())
    max_date = max(created_dates.keys() | closed_dates.keys())

    all_dates = [min_date + timedelta(days=x) for x in range((max_date - min_date).days + 1)]

    created_count = []
    closed_count = []
    cumulative_created = 0
    cumulative_closed = 0
    cumulative_created_list = []
    cumulative_closed_list = []

    for date in all_dates:
        cumulative_created += created_dates.get(date, 0)
        cumulative_closed += closed_dates.get(date, 0)

        created_count.append(created_dates.get(date, 0))
        closed_count.append(closed_dates.get(date, 0))
        cumulative_created_list.append(cumulative_created)
        cumulative_closed_list.append(cumulative_closed)

    plt.figure(figsize=(10, 6))

    plt.plot(all_dates, created_count, label='Количество заведенных задач (в день)', color='blue')
    plt.plot(all_dates, closed_count, label='Количество закрытых задач (в день)', color='green')
    plt.plot(all_dates, cumulative_created_list, label='Накопительный итог заведенных задач', color='blue',
             linestyle='dashed')
    plt.plot(all_dates, cumulative_closed_list, label='Накопительный итог закрытых задач', color='green',
             linestyle='dashed')

    plt.xlabel('Дата')
    plt.ylabel('Количество задач')
    plt.title('График заведенных и закрытых задач с накопительным итогом')
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.show()


def task_4(issues):
    user_task_count = defaultdict(int)

    for issue in issues:
        assignee = issue['fields'].get('assignee')
        reporter = issue['fields'].get('reporter')
        if assignee is not None:
            assignee_name = assignee.get('displayName')
            user_task_count[assignee_name] += 1

        if reporter is not None:
            reporter_name = reporter.get('displayName')
            user_task_count[reporter_name] += 1

    sorted_users = sorted(user_task_count.items(), key=lambda x: x[1], reverse=True)[:30]
    users, task_counts = zip(*sorted_users)

    plt.figure(figsize=(12, 8))
    plt.barh(users, task_counts, color='skyblue')
    plt.xlabel('Количество задач')
    plt.ylabel('Имя пользователя')
    plt.title('Топ-30 пользователей по количеству задач (исполнитель или репортер)')
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.show()


def task_5(issues, assignee_name):
    time_data = defaultdict(int)

    for issue in issues:
        if issue['fields']['resolutiondate']:
            assignee_time = get_assignee_time(issue, assignee_name)
            closed_time = datetime.strptime(issue['fields']['resolutiondate'], '%Y-%m-%dT%H:%M:%S.%f%z')

            time_spent_days = (closed_time - assignee_time).days
            time_data[time_spent_days] += 1

    times = list(time_data.keys())
    task_counts = list(time_data.values())

    plt.figure(figsize=(10, 6))
    plt.bar(times, task_counts, color='skyblue', edgecolor='black')
    plt.xlabel('Затраченное время на выполнение задачи (дни)')
    plt.ylabel('Количество задач')
    plt.title('Гистограмма времени выполнения задач')
    plt.grid(axis='y', linestyle='--')
    plt.show()


def task_6(issues):
    severity_data = defaultdict(int)

    for issue in issues:
        severity = issue['fields'].get('priority', {}).get('name')
        if severity:
            severity_data[severity] += 1

    severities = list(severity_data.keys())
    counts = list(severity_data.values())

    plt.bar(severities, counts, color='salmon', edgecolor='black')
    plt.xlabel('Степень серьёзности')
    plt.ylabel('Количество задач')
    plt.title('Распределение задач по степени серьезности')
    plt.grid(axis='y', linestyle='--')
    plt.show()
