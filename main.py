import datetime
import requests
from plyer import notification
import time
import apikey_file

# Hava durumu API'si için endpoint URL'si
url = "http://api.weatherapi.com/v1/current.json"

# API anahtarınızı buraya ekleyin
api_key = apikey_file.api_key

# Sorgulamak istediğiniz şehir adını buraya yazın
city = "Tarsus"

# API'ye gönderilecek parametreleri ayarlayın
parameters = {
    "key": api_key,
    "q": city,
    "aqi": "no"  # Hava kalitesi indeksini almak istemiyorsanız "no" olarak ayarlayabilirsiniz
}

try:
    # API'ye GET isteği gönderin
    response = requests.get(url=url, params=parameters)

    # Yanıtı kontrol edin ve hava durumu verilerini alın
    if response.status_code == 200:
        weather_data = response.json()

        # Hava durumu verilerini işleyin
        temperature = weather_data["current"]["temp_c"]
        humidity = weather_data["current"]["humidity"]
        condition = weather_data["current"]["condition"]["text"]

        # Bildirim için gerekli bilgilerin ayarlanması
        title = f"{city}'ta Hava Durumu"
        message = f"Sıcaklık: {temperature}°C\nNem: %{humidity}\nDurum: {condition}"

        # Bildirimi belirli bir saatte göndermek için saat ve dakika değerlerini ayarlayın
        hour = 10
        minute = 30

        # Şu anki saat ve dakika bilgisini alın
        concurrent_hour = datetime.datetime.now().hour
        current_minute = datetime.datetime.now().minute

        # Bildirimi belirtilen saat ve dakikada göndermek için gerekli süreyi hesaplayın
        delay_hours = hour - concurrent_hour
        delay_minutes = minute - current_minute

        # Eğer belirtilen saat ve dakika geçmişse, bildirimi ertelemeden hemen gönderin

        if delay_hours < 0 or (delay_hours == 0 and delay_minutes < 0):
            notification.notify(
                title=title,
                message=message,
                app_icon="weathericon.ico",  # .ico formatında olması gerekir
                timeout=30
            )
        else:
            # Bildirimi belirtilen saat ve dakikada göndermek için gerekli süreyi uyku moduna alın
            delay_seconds = delay_hours * 3600 + delay_minutes * 60
            time.sleep(delay_seconds)

            # Bildirimi gönderin
            notification.notify(
                title=title,
                message=message,
                app_icon="weathericon.ico",
                timeout=30
            )
    else:
        print("Hava durumu verisi alınamadı. API yanıtı:", response.status_code)
except:
    print("Hava durumu bilgisi alma başarısız")


