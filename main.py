import requests
import json
import time
import os


class CataasAPI:
    """Класс для работы с API Cataas (Cat as a Service)"""

    def __init__(self):
        self.base_url = "https://cataas.com"

    def get_cat_with_text(self, text):
        """Получает изображение кота с текстом"""
        url = f"{self.base_url}/cat/says/{text}"
        response = requests.get(url)
        response.raise_for_status()
        return response.content

    def generate_filename(self, text):
        """Генерирует уникальное имя файла на основе текста"""
        file_name_base = text.replace(' ', '_')
        return f"{file_name_base}_{int(time.time())}.jpg"


class YandexDiskAPI:
    """Класс для работы с API Яндекс.Диска"""

    def __init__(self, token=None):
        self.token = token or os.getenv('YANDEX_DISK_TOKEN')
        if not self.token:
            raise ValueError("Токен Яндекс.Диска не найден. Установите переменную окружения YANDEX_DISK_TOKEN")

        self.base_url = "https://cloud-api.yandex.net/v1/disk"
        self.headers = {'Authorization': f'OAuth {self.token}'}

    def create_folder(self, folder_path):
        """Создает папку на Яндекс.Диске"""
        url = f"{self.base_url}/resources"
        params = {'path': folder_path}

        response = requests.put(url, headers=self.headers, params=params)

        if response.status_code not in [201, 409]:
            response.raise_for_status()

    def upload_file(self, file_data, remote_path):
        """Загружает файл на Яндекс.Диск"""
        # Получаем URL для загрузки
        url = f"{self.base_url}/resources/upload"
        params = {
            'path': remote_path,
            'overwrite': 'true'
        }

        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()

        upload_href = response.json()['href']

        # Загружаем файл
        upload_response = requests.put(upload_href, data=file_data)
        upload_response.raise_for_status()


def main():
    # Конфигурация
    texts = ["Hello", "Good Cat", "Привет"]
    group_name = "Fpy_134"

    try:
        # Создаем экземпляры классов
        cataas_api = CataasAPI()
        yandex_api = YandexDiskAPI(token="НУЖНО УКАЗАТЬ ТОКЕН")

        # Создание папки на Яндекс.Диске
        yandex_api.create_folder(f'/{group_name}')

        backup_info = []

        for text in texts:
            # Получение картинки и загрузка на Яндекс.Диск
            image_data = cataas_api.get_cat_with_text(text)
            file_name = cataas_api.generate_filename(text)
            remote_path = f'/{group_name}/{file_name}'
            yandex_api.upload_file(image_data, remote_path)

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

    except Exception as e:
        print(f"Произошла ошибка: {e}")


if __name__ == "__main__":
    main()
