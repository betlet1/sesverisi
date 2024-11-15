from selenium import webdriver
from selenium.common import TimeoutException, StaleElementReferenceException
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import requests
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

# Çerezler ve başlıklar
cookies = {
    "preferSpectrogram": "no",
    "disallowSimultaneousAudioPlayback": "no",
    "systemPrefersDarkTheme": "no",
    "cookieConsent": "yes",
    "csrftoken": "eumpT1uCjeiPan2UMLZyjb5BfQoXxZ5fckz0P9ZGx4bwQG7aHoJlSBRfKbHgZ0ui",
    "sessionid": "kt8jkxrrbyd8ywgfbwkjvspipo8vjc00"
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
    'Accept': 'application/octet-stream'
}

# İndirme işlemi fonksiyonu
def download_file(url, cookies, headers, download_folder="sesdosyalari"):
    file_name = url.split("/")[-1]
    file_path = os.path.join(download_folder, file_name)

    response = requests.get(url, cookies=cookies, headers=headers, stream=True)
    try:
        if response.status_code == 200:
            with open(file_path, 'wb') as f:
                try:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                    print(f"Dosya indirildi: {file_path}")
                except TimeoutException:
                    print("kaldı mı.")
        else:
            print(f"İndirme başarısız oldu: {response.status_code}")
    except TimeoutException:
        print("kaldı mı.")

# Tarayıcıyı başlatma
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Freesound giriş sayfasına gitme
driver.get('https://freesound.org/')

# Giriş butonuna tıklayın (Modal açılacak)
login_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '//button[@data-toggle="login-modal"]'))
)
login_button.click()

# Modal açılmasını bekleyin (Form elemanlarını içeren modal)
WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.ID, "loginModal"))
)

# Kullanıcı adı ve şifre alanlarını bulun
username_field = driver.find_element(By.ID, 'id_username')
password_field = driver.find_element(By.ID, 'id_password')

# Giriş için kullanıcı adı ve şifre
username = 'betlet_'  # Kendi kullanıcı adınızı buraya yazın
password = 'ssEE78nm.'  # Kendi şifrenizi buraya yazın
username_field.send_keys(username)  # Kullanıcı adını girme
password_field.send_keys(password)  # Şifreyi girme
# Giriş formunu gönderin
password_field.send_keys(Keys.RETURN)

# Giriş işlemini tamamlamayı bekleme ve mesaj yazdırma
try:
    WebDriverWait(driver, 10).until(
        EC.url_changes('https://freesound.org/')
    )
    print("Giriş başarıyla tamamlandı!")
except TimeoutException:
    print("Giriş işlemi zaman aşımına uğradı.")

# Sayfalar arasında gezinme ve şarkı linklerini indirme
def scrape_sounds():
    for page in range(1, 351):  # 350 sayfa gezilecek
        print(f"Sayfa {page} yükleniyor...")
        driver.get(f'https://freesound.org/search/?q=music&f=type%3A%22wav%22&page={page}#sound')
        time.sleep(2)

        # Sayfada ses linklerini bulma
        sound_links = driver.find_elements(By.XPATH, '//a[contains(@class, "bw-link--black") and starts-with(@href, "/people/")]')

        if not sound_links:
            print("Hiç ses linki bulunamadı.")
            continue

        print(f"{len(sound_links)} adet ses linki bulundu.")

        for index, link in enumerate(sound_links):
            if index == 0:  # İlk linki atla
                print("İlk link atlanıyor.")
                continue

            try:
                # Sayfa URL'sini al
                sound_page_url = link.get_attribute("href")
                print(f"Detay sayfasına gidiliyor: {sound_page_url}")

                if not sound_page_url:
                    print("Geçersiz URL, atlanıyor.")
                    continue

                driver.get(sound_page_url)
                time.sleep(2)

                # İndirme butonunu bekleyin
                download_button = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located(
                        (By.XPATH, '//a[contains(@class, "sound-download-button") and @href]')
                    )
                )
                print("İndirme butonu bulundu.")

                # İndirme URL'sini al
                download_url = download_button.get_attribute("href")
                if download_url.endswith(".wav"):
                    download_file(download_url, cookies, headers)
                else:
                    print(f"Atlanıyor: {download_url}")

            except TimeoutException:
                print("İndirme butonu bulunamadı, sonraki öğeye geçiliyor.")
            except StaleElementReferenceException:
                print("Stale element hatası, öğe yeniden bulunuyor.")
            except Exception as e:
                print(f"Beklenmedik bir hata oluştu: {e}")

        print(f"Sayfa {page} işlem tamamlandı.")

# İndirme işlemini başlat
scrape_sounds()

# Tarayıcıyı kapatma
driver.quit()
