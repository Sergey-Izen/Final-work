
import requests
import json
import time

# Данные
texts = ["Hello", "Good Cat", "Привет"]
token = "y0__xD5n6XfAxjblgMghcqQzRSgjrxLLzVxCXL1WpjcPOU-rqZmVA"
group_name = "Fpy_134"

yandex_headers = {'Authorization': f'OAuth {token}'}

# Создание папки на Яндекс.Диске
create_folder_url = "https://cloud-api.yandex.net/v1/disk/resources"
params = {'path': f'/{group_name}'}
requests.put(create_folder_url, headers=yandex_headers, params=params)

backup_info = []

for text in texts:
    # Получение картинки
    url = f"https://cataas.com/cat/says/{text}"
    response = requests.get(url)
    image_data = response.content

    # Создание уникального имени
    file_name_base = text.replace(' ', '_')
    file_name = f"{file_name_base}_{int(time.time())}.jpg"

    # Загрузка на Яндекс.Диск
    upload_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
    params = {
        'path': f'/{group_name}/{file_name}',
        'overwrite': 'true'
    }
    response = requests.get(upload_url, headers=yandex_headers, params=params)
    upload_href = response.json()['href']
    requests.put(upload_href, data=image_data)

    # Сохранение информации
    backup_info.append({
        'file_name': file_name,
        'file_size_bytes': len(image_data),
        'upload_time': time.strftime('%Y-%m-%d %H:%M:%S'),
        'text_on_image': text
    })

    print(f"Загружено: {file_name}")
    time.sleep(1)  # Пауза между запросами

# Сохранение JSON со всеми картинками
with open('backup_info.json', 'w') as f:
    json.dump(backup_info, f, indent=2)

print("Все картинки сохранены на Яндекс.Диске")