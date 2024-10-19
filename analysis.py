import numpy as np
import requests
import matplotlib.pyplot as plt
import datetime

# Параметры подключения к JIRA
JIRA_URL = 'https://issues.apache.org/jira/rest/api/2/search'


def make_request(payload):
    response = requests.get(JIRA_URL, params=payload)
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

    # Добавляем время нахождения задачи в последнем состоянии до момента закрытия
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

    # Строим диаграммы для каждого состояния
    for status, times in status_data.items():
        # Строим гистограмму
        plt.hist(times, bins=40, edgecolor='black')
        plt.xlabel('Количество дней')
        plt.ylabel('Количество задач')
        plt.title(f'Распределение времени в состоянии {status}')
        plt.show()

        times_filtered = [t for t in times if t <= 60]

        # Определяем границы бинов с одинаковыми интервалами на промежутке от 0 до 60 дней
        bins = np.linspace(0, 60, 41)  # 40 бинов на интервале 0-60

        # Строим гистограмму
        plt.hist(times_filtered, bins=bins, edgecolor='black')
        plt.xlabel('Количество дней')
        plt.ylabel('Количество задач')
        plt.title(f'Распределение времени в состоянии {status} на меньшем интервале')
        plt.show()


if __name__ == "__main__":
    data = make_request({'jql': 'project=KAFKA AND status=Closed ORDER BY createdDate', 'maxResults': '1000',
                         'expand': 'changelog',
                         'fields': 'created,resolutiondate'})
    task_1(data)
    task_2(data)

