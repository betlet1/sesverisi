from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import requests
from bs4 import BeautifulSoup

# WebDriver'ı başlat
options = webdriver.ChromeOptions()
options.headless = False  # Tarayıcıyı görünür yapmak için False yapın
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# URL: Dosyaların nereden alınacağı
base_url = "https://www.openmusicarchive.org/browse_tag.php?tag=Diamond%20Disc"

# Tarayıcıda sayfayı aç
driver.get(base_url)

# Sayfanın tam URL'sini yazdır
print(f"Sayfa URL'si: {driver.current_url}")

# Sayfanın HTML içeriğini al
html_content = driver.page_source

# BeautifulSoup ile HTML içeriği parse et
soup = BeautifulSoup(html_content, 'html.parser')

# .mp3 ile biten tüm linklerin contentten okunması
mp3_links = soup.find_all('a', href=True)
mp3_links = [link['href'] for link in mp3_links if link['href'].endswith('.mp3')]

# MP3 Dosyalarının indirilmesi
for mp3_link in mp3_links:
    # Absolute URL'yi oluştur
    if not mp3_link.startswith('http'):
        mp3_link = "https://www.openmusicarchive.org/" + mp3_link

    # Gidilen sayfayı tarayıcıda göster
    print(f"Tarayıcıda açılıyor: {mp3_link}")
    driver.get(mp3_link)

    # Sayfanın URL'sini yazdır
    print(f"Gidilen Sayfa: {driver.current_url}")

    # MP3 dosyasının URL'si ve bulunduğu sayfa
    print(f"MP3 dosyasının URL'si: {mp3_link}")

    # İndirme işlemi için MP3 dosyasını download et
    try:
        mp3_response = requests.get(mp3_link)

        # Bellekte dosya saklama (isteğe bağlı, örneğin Google Drive'a yüklemek)
        # file_stream = io.BytesIO(mp3_response.content)
        # upload_file(file_stream, os.path.basename(mp3_link))

        print(f"Başarıyla indirildi: {mp3_link}")
    except Exception as e:
        print(f"Dolayısıyla indirmede problem yaşandı: {mp3_link}: {e}")

# Sayfa işleminden sonra tarayıcıyı kapat
driver.quit()
