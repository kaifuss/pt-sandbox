import importlib
import sys
import subprocess
required_libraries = ['getpass', 'json','os', 'requests', 'urllib3']
for lib in required_libraries:
    try:
        importlib.import_module(lib)
    except ImportError:
        print(f"{lib} не установлена. Устанавливаем...")
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', lib])
            print(f"{lib} успешно установлена.")
        except Exception as e:
            print(f"Ошибка при установке {lib}: {e}\n Скрипт будет остановлен. Попробуйте установить {lib} вручную")
            sys.exit()

import requests
import os
import urllib3
import getpass
import json

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

currentDirectory = os.getcwd()
fileName = 'getinfo.bat'
fileToUpload = open(currentDirectory + '/'+ fileName, 'rb')
rootUrl = 'https://10.1.37.15/api/v1'
token = getpass.getpass(prompt='Token: ')

uploadFileToScanUrl = rootUrl + '/storage/uploadScanFile'
response = requests.post(uploadFileToScanUrl, files={'file': fileToUpload}, verify=False, headers={'X-API-Key': token})
response.raise_for_status()
scanId = response.json()['data']['file_uri']
print(f'Файл {fileName} загружен. ID - {scanId}')
fileToUpload.close()

createScanTaskUrl = rootUrl + '/analysis/createScanTask'
scanParametrs = {
    'file_uri': scanId,
    'file_name': fileName,
    'short_result': True,
    'options': {
        'analysis_depth': 5,
        'passwords_for_unpack': ['infected'],
        'mark_suspicious_files_options': {
            'max_depth_exceeded': True
        },
        'sandbox': {
            'enabled': True,
            'image_id': 'win7-sp1-x86',
            'analysis_duration': 60,
            'save_video': True
        }
    }
}

response = requests.post(createScanTaskUrl, json=scanParametrs, verify=False, headers={'X-API-Key': token})
response.raise_for_status()
scanId = response.json()['data']['scan_id']
print(f'Задача создана. ID - {scanId}')