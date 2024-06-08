import importlib
import sys
import subprocess
requiredLibraries = ['getpass', 'json','os', 'requests', 'urllib3']
for lib in requiredLibraries:
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
fileToUpload = open(os.path.join(currentDirectory, fileName), 'rb')
rootUrl = 'https://' + input('\nВведите IP или FQDN адрес сервера PT SB: ') + '/api/v1'
token = getpass.getpass(prompt='Введите токен доступа к PT SB по API: ')

print(f'\nФайл {fileName} отправляется на PT SandBox...')
uploadFileToScanUrl = rootUrl + '/storage/uploadScanFile'
uploadResponse = requests.post(uploadFileToScanUrl, files={'file': fileToUpload}, verify=False, headers={'X-API-Key': token})
uploadResponse.raise_for_status()
scanId = uploadResponse.json()['data']['file_uri']
print(f'Файл {fileName} загружен. ID - {scanId}\n')
fileToUpload.close()

cacheEnabled = False
if (input('Использовать результаты предыдущих проверок? (y/n): ') == 'y'): cacheEnabled = True

print('\nДоступные образы для проверки:\n')
getImagesOnServerUrl = rootUrl + '/engines/sandbox/getImages'
imagesResponse = requests.get(getImagesOnServerUrl, verify=False, headers={'X-API-Key': token})
imagesResponse.raise_for_status()
for eachImage in imagesResponse.json()['data']:
    print(f'{eachImage["image_id"]}')
imageId = input('\nУкажите образ для проверки: ')

print('\nСоздается и выполняется задача на проверку...')
createScanTaskUrl = rootUrl + '/analysis/createScanTask'
scanParametrs = {
    'file_uri': scanId,
    'file_name': fileName,
    'short_result': False,
    'options': {
        'analysis_depth': 5,
        'cache_enabled': cacheEnabled,
        'passwords_for_unpack': ['infected'],
        'mark_suspicious_files_options': {
            'max_depth_exceeded': True
        },
        'sandbox': {
            'enabled': True,
            'image_id': imageId,
            'analysis_duration': 60,
            'save_video': True
        }
    }
}

print('\n' + json.dumps(scanParametrs, indent=4) + '\n')

startScanResponse = requests.post(createScanTaskUrl, json=scanParametrs, verify=False, headers={'X-API-Key': token})
startScanResponse.raise_for_status()
scanId = startScanResponse.json()['data']['scan_id']
print(f'Задача выполнена. ID - {scanId}\n')

print('Получение результатов проверки...')
checkResultsUrl = rootUrl + '/analysis/checkTask'
checkResultsResponse = requests.post(checkResultsUrl, json={'scan_id': scanId}, verify=False, headers={'X-API-Key': token})
checkResultsResponse.raise_for_status()
print('Результат получен:')
print(json.dumps(checkResultsResponse.json(), indent=4))