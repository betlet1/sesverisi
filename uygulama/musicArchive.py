import io
import os
import requests
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

# Google Drive API için ayarlar
SCOPES = ['https://www.googleapis.com/auth/drive.file']
SERVICE_ACCOUNT_FILE = 'service_account.json'  # JSON dosyanızın adı
FOLDER_ID = '13t9QvPmNiUe-fcdriNDRfSOX2b2gAv-_'  # Yüklemek istediğiniz klasörün ID'si

# Yetkilendirme Bilgilerini Ayarla
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# Google Drive Servisini Başlat
service = build('drive', 'v3', credentials=credentials)


# Dosya Yükleme Fonksiyonu
def upload_file(file_path, file_name):
    file_metadata = {
        'name': file_name,
        'parents': [FOLDER_ID]  # Yüklemek istediğiniz klasörün ID'si
    }

    media = MediaIoBaseUpload(io.FileIO(file_path, 'rb'), mimetype='audio/mp3')

    # Dosyayı yükleme
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    print(f"Dosya yüklendi: {file_name} (ID: {file['id']})")


# WebDriver'ı başlat
options = webdriver.ChromeOptions()
options.headless = False  # Tarayıcıyı görünür yapmak için False yapın
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# URL: Dosyaların nereden alınacağı
base_url = "https://www.openmusicarchive.org/browse_tag.php?tag=Diamond%20Disc"

# Tarayıcıda sayfayı aç
driver.get(base_url)

# Sayfanın HTML içeriğini al
html_content = driver.page_source

# BeautifulSoup ile HTML içeriği parse et
soup = BeautifulSoup(html_content, 'html.parser')

# .mp3 ile biten tüm linklerin contentten okunması
mp3_links = soup.find_all('a', href=True)
mp3_links = [link['href'] for link in mp3_links if link['href'].endswith('.mp3')]

# İndirilen dosyaların kaydedileceği klasörü kontrol et ve oluştur
download_folder = 'downloads'
if not os.path.exists(download_folder):
    os.makedirs(download_folder)

# MP3 Dosyalarının indirilmesi ve Google Drive'a yüklenmesi
for mp3_link in mp3_links:
    # Absolute URL'yi oluştur
    if not mp3_link.startswith('http'):
        mp3_link = "https://www.openmusicarchive.org/" + mp3_link

    # MP3 dosyasını indir
    try:
        mp3_response = requests.get(mp3_link)
        file_name = mp3_link.split("/")[-1]  # Dosya adını URL'den al
        file_path = os.path.join(download_folder, file_name)

        # Dosyayı kaydet
        with open(file_path, 'wb') as f:
            f.write(mp3_response.content)

        print(f"Başarıyla indirildi: {mp3_link}")

        # Google Drive'a yükle
        upload_file(file_path, file_name)

    except requests.exceptions.RequestException as e:
        print(f"İndirme hatası: {mp3_link} - {e}")

    except Exception as e:
        print(f"Başka bir hata oluştu: {mp3_link} - {e}")

# Sayfa işleminden sonra tarayıcıyı kapat
driver.quit()
