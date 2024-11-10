import os
import requests
from dotenv import load_dotenv
from exceptions import JiraAPIException

load_dotenv()


def make_request(payload):
    try:
        response = requests.get(os.getenv('JIRA_URL'), params=payload)
        response.raise_for_status()
        return response.json()['issues']
    except requests.exceptions.RequestException as e:
        raise JiraAPIException(f"Ошибка при запросе к JIRA: {e}")
