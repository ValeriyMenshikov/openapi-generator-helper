import os
import sys
import pathlib
import requests
import subprocess
from requests.exceptions import ConnectionError, ReadTimeout, ConnectTimeout, ConnectionError, Timeout
from concurrent.futures import ThreadPoolExecutor
from typing import List



def generate_clients(swagger_list: List[dict],
                     generator_path: str,
                     temp_directory: str,
                     version_check: bool = True,
                     template_path: str = None) -> list:
    """
    Функция для генерации клиентской библиотеки
    :param swagger_list: список словарей [ {'url': 'package_name'} ]
    :param generator_path: путь к openapi-generator
    :param temp_directory: директория куда будут сохраняться сгенерированные пакеты
    :param version_check: если флаг False, то клиенты будут обновляться принудительно
    :param template_path: путь к альтернативным шаблонам mustache
    :return: список путей к сгенерированным клиентам
    """
    path = pathlib.Path(__file__).parent
    if not template_path:
        template_path = path.joinpath('python_templates')

    commands = []
    packages = []

    for swagger in swagger_list:
        swagger_url = swagger['url']
        package_name = swagger['package_name']

        if version_check:
            swagger_version = get_swagger_version(swagger_url)
            package_version = get_package_version(package_name)
            if swagger_version == package_version:
                continue

        package_path = f'{temp_directory}/{package_name}'
        packages.append(package_path)
        com = "java -jar {0} generate -i {1} -g python -o {2} --package-name {3} --api-name-suffix {3} -t {4}".format(
            generator_path,
            swagger_url,
            package_path,
            package_name,
            template_path
        )
        commands.append(com)

    if commands:
        with ThreadPoolExecutor(max_workers=10) as executor:
            list(map(lambda command: executor.submit(os.system, command), commands))

    return packages


def install(packages: List[str],
            extra_index_url: str = None):
    """
    Функция для установки сгенерированных клиентских библиотек
    :param packages: список путей к библиотекам
    :param extra_index_url: параметр для указания альтернативного pypi репозитория
    :return:
    """
    if packages:
        for package in packages:
            command = [sys.executable, "-m", "pip", "install", package]
            if extra_index_url:
                command.append(f'--extra-index-url={extra_index_url}')
            subprocess.check_call(command)


def get_package_version(package_name: str) -> str:
    """
    Функция для получения версии установленной библиотеки
    :param package_name: название библиотеки
    :return: версия библиотеки
    """
    loc = {}
    code = f'''import {package_name}; version = {package_name}.__version__'''
    try:
        exec(code, globals(), loc)
    except (ModuleNotFoundError, AttributeError):
        version = None
    else:
        version = loc.get('version')
    return version


def get_swagger_version(url: str) -> str:
    """
    Функция для получения версии API клиента из спецификации swagger
    :param url: url адрес swagger
    :return:
    """
    try:
        swagger_spec = requests.get(url).json()
    except (ConnectionError,
            ReadTimeout,
            ConnectTimeout,
            ConnectionError,
            Timeout,
            KeyError):
        swagger_spec = {}
    version = swagger_spec.get("info", dict()).get("version")
    return version
