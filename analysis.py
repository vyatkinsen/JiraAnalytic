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


if __name__ == "__main__":
    data = make_request({'jql': 'project=KAFKA AND status=Closed ORDER BY createdDate', 'maxResults': '1000',
                         'expand': 'changelog',
                         'fields': 'created,resolutiondate'})
    task_1(data)
