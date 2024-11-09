import os
from collections import defaultdict
from dotenv import load_dotenv
import datetime
import numpy as np
import requests
import matplotlib.pyplot as plt


def make_request(payload):
    response = requests.get(os.getenv('JIRA_URL'), params=payload)
    return response.json()['issues']


def task_1(issues):
    times = []
    for issue in issues:
        created = datetime.datetime.strptime(issue['fields']['created'], '%Y-%m-%dT%H:%M:%S.%f%z')
        resolved = datetime.datetime.strptime(issue['fields']['resolutiondate'], '%Y-%m-%dT%H:%M:%S.%f%z')
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


def get_status_times(issue):
    changelog = issue['changelog']['histories']
    status_times = {}

    previous_status = 'Open'
    previous_time = datetime.datetime.strptime(issue['fields']['created'], '%Y-%m-%dT%H:%M:%S.%f%z')

    for history in changelog:
        for item in history['items']:
            if item['field'] == 'status':
                current_status = item['toString']
                if current_status == 'Closed':
                    continue
                current_time = datetime.datetime.strptime(history['created'], '%Y-%m-%dT%H:%M:%S.%f%z')

                time_spent = (current_time - previous_time).days
                if previous_status in status_times:
                    status_times[previous_status] += time_spent
                else:
                    status_times[previous_status] = time_spent

                previous_status = current_status
                previous_time = current_time

    resolved_time = datetime.datetime.strptime(issue['fields']['resolutiondate'], '%Y-%m-%dT%H:%M:%S.%f%z')
    time_spent = (resolved_time - previous_time).days
    if previous_status in status_times:
        status_times[previous_status] += time_spent
    else:
        status_times[previous_status] = time_spent

    return status_times


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
        created_date = datetime.datetime.strptime(issue['fields']['created'], '%Y-%m-%dT%H:%M:%S.%f%z').date()
        created_dates[created_date] += 1

        if issue['fields']['resolutiondate']:
            closed_date = datetime.datetime.strptime(issue['fields']['resolutiondate'], '%Y-%m-%dT%H:%M:%S.%f%z').date()
            closed_dates[closed_date] += 1

    min_date = min(created_dates.keys() | closed_dates.keys())
    max_date = max(created_dates.keys() | closed_dates.keys())

    all_dates = [min_date + datetime.timedelta(days=x) for x in range((max_date - min_date).days + 1)]

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


if __name__ == "__main__":
    load_dotenv()
    choice = input("Выберите номер задачи (1, 2 или 3): ")

    match choice:
        case "1":
            data = make_request({'jql': 'project=KAFKA AND status=Closed ORDER BY createdDate', 'maxResults': '1000',
                        'expand': 'changelog',
                        'fields': 'created,resolutiondate'})
            task_1(data)

        case "2":
            data = make_request({'jql': 'project=KAFKA AND status=Closed ORDER BY createdDate', 'maxResults': '1000',
                                 'expand': 'changelog',
                                 'fields': 'created,resolutiondate'})
            task_2(data)

        case "3":
            data = make_request(
                {'jql': 'project=KAFKA AND status in (Open, Closed) AND created >= -90d AND text ~ "created"',
                 'maxResults': '1000',
                 'expand': 'changelog',
                 'fields': 'created,resolutiondate'})
            task_3(data)

        case _:
            print("Неверный выбор задачи. Пожалуйста, выберите 1, 2 или 3.")