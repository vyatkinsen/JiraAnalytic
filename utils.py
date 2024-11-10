from datetime import datetime


def get_status_times(issue):
    changelog = issue['changelog']['histories']
    status_times = {}

    previous_status = 'Open'
    previous_time = datetime.strptime(issue['fields']['created'], '%Y-%m-%dT%H:%M:%S.%f%z')

    for history in changelog:
        for item in history['items']:
            if item['field'] == 'status':
                current_status = item['toString']
                if current_status == 'Closed':
                    continue
                current_time = datetime.strptime(history['created'], '%Y-%m-%dT%H:%M:%S.%f%z')

                time_spent = (current_time - previous_time).days
                if previous_status in status_times:
                    status_times[previous_status] += time_spent
                else:
                    status_times[previous_status] = time_spent

                previous_status = current_status
                previous_time = current_time

    resolved_time = datetime.strptime(issue['fields']['resolutiondate'], '%Y-%m-%dT%H:%M:%S.%f%z')
    time_spent = (resolved_time - previous_time).days
    if previous_status in status_times:
        status_times[previous_status] += time_spent
    else:
        status_times[previous_status] = time_spent

    return status_times


def get_assignee_time(issue, assignee_name):
    created_time = datetime.strptime(issue['fields']['created'], '%Y-%m-%dT%H:%M:%S.%f%z')
    changelog = issue.get('changelog', {}).get('histories', [])

    for history in changelog:
        for item in history['items']:
            if item['field'] == 'assignee' and item['toString'] == assignee_name:
                assignee_set_time = datetime.strptime(history['created'], '%Y-%m-%dT%H:%M:%S.%f%z')
                return assignee_set_time

    return created_time
