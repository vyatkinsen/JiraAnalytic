from jira_utils import make_request
from tasks import *


def main():
    is_running = True

    while is_running:
        choice = input("Выберите номер задачи (1 – 6 или 0 для выхода): ")

        match choice:
            case "1":
                data = make_request(
                    {'jql': 'project=KAFKA AND status=Closed ORDER BY createdDate', 'maxResults': '1000',
                     'expand': 'changelog',
                     'fields': 'created,resolutiondate'})
                task_1(data)

            case "2":
                data = make_request(
                    {'jql': 'project=KAFKA AND status=Closed ORDER BY createdDate', 'maxResults': '1000',
                     'expand': 'changelog',
                     'fields': 'created,resolutiondate'})
                task_2(data)

            case "3":
                data = make_request(
                    {'jql': 'project=KAFKA AND status in (Open, Resolved) AND created >= -90d AND text ~ "created"',
                     'maxResults': '1000',
                     'expand': 'changelog',
                     'fields': 'created,resolutiondate'})
                task_3(data)

            case "4":
                data = make_request(
                    {'jql': 'project=KAFKA AND (assignee IS NOT EMPTY OR reporter IS NOT EMPTY)', 'maxResults': '1000',
                     'fields': 'assignee,reporter'})
                task_4(data)

            case "5":
                username = input("\nВведите имя пользователя: ")
                data = make_request({
                    'jql': f'project=KAFKA AND status=Closed AND assignee={username}',
                    'maxResults': '1000',
                    'fields': 'created,resolutiondate',
                    'expand': 'changelog'
                })
                task_5(data, username)
                pass

            case "6":
                data = make_request({
                    'jql': 'project=KAFKA AND status=Closed',
                    'maxResults': '1000',
                    'fields': 'priority'
                })
                task_6(data)

            case "0":
                exit(0)

            case _:
                print("Неверный выбор задачи. Пожалуйста, выберите 1, 2, 3, 4, 5 или 6.")


if __name__ == "__main__":
    main()