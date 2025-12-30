Milesight UG Serisi LoRaWAN Ağ Geçidi Sinyal Analiz Aracı
Bu proje, Milesight IoT UG56, UG65 ve UG67 serisi LoRaWAN ağ geçitleri (gateway) üzerinden geçen sensör verilerini analiz etmek ve görselleştirmek için geliştirilmiş bir Python & Streamlit uygulamasıdır.
Bu script sayesinde, sahadaki cihazlarınızın RSSI (Sinyal Gücü) ve SNR (Sinyal-Gürültü Oranı) değerlerini grafiksel olarak izleyebilir, bağlantı sorunlarını tespit edebilir ve geçmiş veri paketlerini detaylı bir tablo halinde inceleyebilirsiniz.
🚀 Özellikler
• Görsel Analiz: Cihaz bazlı RSSI ve SNR değerlerinin zaman çizelgesi üzerinde interaktif grafikleri.
• Detaylı Veri Tablosu: Ağ geçidinden geçen paketlerin (DevEUI, Frekans, SF, Zaman Damgası vb.) anlık ve geriye dönük listesi.
• Hata Tespiti: Düşük sinyal seviyelerini görselleştirerek kör noktaların veya arızalı sensörlerin tespiti.
• API Entegrasyonu: Milesight HTTP API'si üzerinden güvenli veri çekimi.
🛠️ Kurulum
Projeyi çalıştırmadan önce bilgisayarınızda Python'un kurulu olduğundan emin olun. Gerekli kütüphaneleri yüklemek için terminalde aşağıdaki komutu çalıştırın:
pip install streamlit requests pandas plotly
⚙️ Yapılandırma ve Önemli Uyarı (Şifre Alma İşlemi)
Milesight ağ geçitlerinin güncel firmware sürümleri (60.0.0.42-r5 ve sonrası), API güvenliği için düz metin şifreleri kabul etmez. API'ye bağlanabilmek için tarayıcı üzerinden şifrelenmiş (encrypted) parolanızı almanız gerekmektedir.
🔐 Şifreli Parola Nasıl Alınır?
Script içerisindeki password alanına kendi şifrenizi yazmamalısınız. Bunun yerine aşağıdaki adımları izleyerek token alımında kullanılan şifreli metni bulmalısınız:
1. Chrome veya kullandığınız tarayıcıda Milesight Gateway web arayüzüne gidin.
2. Giriş yapmadan önce klavyeden F12 tuşuna basarak Geliştirici Araçlarını (Developer Tools) açın.
3. Network (Ağ) sekmesine tıklayın.
4. Kullanıcı adı ve şifrenizi girerek Login butonuna basın.
5. Ağ listesinde beliren login (veya internal/login) isteğine tıklayın.
6. Sağ tarafta açılan panelden Payload (veya Form Data) sekmesine gelin.
7. Burada password alanının karşısında yazan uzun ve karmaşık metni (Örn: sI/7ewBCeWunDs6JXXtSHg==) kopyalayın.
Not: Bu şifreli metni Python kodunuzdaki parola alanına yapıştırın. Kullanıcı adı genellikle admin'dir.
▶️ Kullanım
1. Repo içerisindeki Python dosyasını (örneğin app.py) indirin.
2. Dosya içerisindeki GATEWAY_IP bölümüne cihazınızın IP adresini girin (Örn: 192.168.1.5).
3. Terminali açın ve uygulamanın olduğu klasöre giderek şu komutu çalıştırın:
streamlit run app.py
4. Açılan tarayıcı penceresinde, yukarıdaki adımla elde ettiğiniz şifreli parolayı ve kullanıcı adını girerek verileri çekmeye başlayın.
📚 API Dokümantasyonu
Bu proje, Milesight Gateway HTTP API spesifikasyonlarına sadık kalınarak hazırlanmıştır.
• Login İşlemi: /api/internal/login
• Paket Verileri: /api/urpackets
Detaylı API dokümantasyonu için Milesight resmi web sitesini ziyaret edebilir veya bu repo içerisindeki referans belgeleri inceleyebilirsiniz.
⚠️ Yasal Uyarı
Bu araç, yerel ağınızdaki cihazları analiz etmek için geliştirilmiştir. HTTPS bağlantılarında yerel ağ sertifikası kullanıldığı için tarayıcınız veya Python konsolunuz "Güvenli Değil" (InsecureRequestWarning) uyarısı verebilir, bu yerel ağ çalışmaları için normaldir.
