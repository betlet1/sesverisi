FreeSound'dan Ses Dosyalarını İndirme ve Google Drive'a Yükleme
Bu Python projesi, FreeSound web sitesinden ses dosyalarını indirip, bu dosyaları Google Drive'a yüklemek için tasarlanmıştır. Proje, Selenium ile sayfada gezinir, giriş yapar, ses dosyalarını bulur ve indirir. İndirilen dosyalar, Google Drive API kullanılarak belirli bir klasöre yüklenir.

Gereksinimler
Python 3.x
pip paket yöneticisi
Gerekli Kütüphaneler
Bu projeyi çalıştırmak için aşağıdaki Python kütüphanelerinin kurulu olması gerekmektedir:

requests
selenium
google-auth
google-api-python-client
google-auth-httplib2
google-api-python-client
webdriver-manager
time
Bu kütüphaneleri kurmak için aşağıdaki komutu çalıştırabilirsiniz:

bash
Kodu kopyala
pip install requests selenium google-auth google-api-python-client google-auth-httplib2 webdriver-manager
Google Drive API Ayarları
1. Google Cloud Console'da Proje Oluşturma
Google Cloud Console üzerinden yeni bir proje oluşturun.
Google Drive API'yi etkinleştirin.
2. Servis Hesabı ve JSON Dosyası
Google Cloud Console'dan bir Servis Hesabı oluşturun.
Bu servis hesabı için JSON anahtar dosyasını indirin.
service_account.json dosyasını projeye dahil edin.
3. Klasör ID'si
Google Drive'da dosyaların yükleneceği klasör ID'sini belirleyin ve bu ID'yi FOLDER_ID değişkenine ekleyin.
Kullanım
Servis Hesabı Ayarları: SERVICE_ACCOUNT_FILE değişkenine Google Cloud Console'dan aldığınız JSON dosyasının adını yazın.

Giriş Bilgileri: FreeSound'a giriş yapabilmek için kullanıcı adı (username) ve şifrenizi (password) girin.

İndirme ve Yükleme İşlemi: Kod, belirttiğiniz sayfalarda ses dosyalarını bulacak, indirilecek dosyaları belirleyecek ve Google Drive'a yükleyecektir.

FreeSound'dan ses dosyaları .wav formatında indirilecektir.
Dosyalar, belirttiğiniz Google Drive klasörüne yüklenir.
Kod Açıklaması
Google Drive API ile Yükleme:

upload_file() fonksiyonu, Google Drive'a dosya yüklemek için kullanılır.
Yükleme işlemi için MediaIoBaseUpload kullanılır ve dosya Google Drive'da belirtilen klasöre yüklenir.
FreeSound'dan Ses Dosyalarını İndirme:

Selenium kullanılarak FreeSound sayfasına gidilir.
Kullanıcı girişi yapılır ve ses dosyalarının bulunduğu sayfada gezilir.
İlgili ses dosyalarının indirilmesi için bağlantılar toplanır.
requests ile dosyalar indirilir ve ardından upload_file fonksiyonu ile Google Drive'a yüklenir.
Önemli Notlar
Giriş İşlemi: Kullanıcı adı ve şifrenizin doğru olduğundan emin olun.
Yükleme Hedefi: Dosyaların yüklenmesi, doğru Google Drive klasör ID'sine bağlıdır.
İndirme URL'si: Yalnızca geçerli .wav uzantılı dosyalar indirilecektir.
Sayfa Sınırı: Kod, 350 sayfaya kadar ses dosyalarını arar. Sayfa sayısını ihtiyacınıza göre değiştirebilirsiniz.
Yasal Uyarılar
Bu kod, sadece ses dosyalarını kişisel kullanım amacıyla indirip yüklemek içindir.
Ses dosyalarının telif haklarına saygı gösterilmelidir.
