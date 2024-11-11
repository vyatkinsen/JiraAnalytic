from setuptools import setup, find_packages


def parse_requirements(filename):
    with open(filename, 'r') as f:
        return [line.strip() for line in f.readlines() if line.strip() and not line.startswith("#")]


setup(
    name='JiraAnalytic',  # Название вашего проекта
    version='0.1',  # Версия вашего проекта
    packages=find_packages(),  # Автоматически находит все пакеты в проекте
    install_requires=parse_requirements('requirements.txt'),  # Чтение зависимостей из requirements.txt
    python_requires='>=3.12',  # Требуемая версия Python
    author='Arseny Vyatkin',  # Автор проекта
    author_email='vyatkin.aa@edu.spbstu.ru',  # Электронная почта автора
    description='A small training project for working with Jira',  # Описание проекта
    long_description=open('README.md').read(),  # Полное описание из файла README.md
    long_description_content_type='text/markdown',  # Формат содержимого README.md
    include_package_data=True,  # Включает все файлы, указанные в MANIFEST.in
    scripts=['main.py'],
    test_suite='tests'
)
