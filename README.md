# Parking-Detection-Application

Bu proje, Python ve OpenCV kütüphanesini kullanarak statik bir otopark görüntüsü veya video akışı üzerinde park yerlerinin doluluk durumunu tespit eden bir görüntü işleme uygulamasıdır.

## 🚀 Özellikler

- **İnteraktif Park Yeri Seçimi:** Kullanıcı, fareyi kullanarak park yerlerini manuel olarak belirleyebilir.
- **Görüntü İşleme:** Adaptif eşikleme (Adaptive Threshold) ve morfolojik işlemler kullanılarak araçlar tespit edilir.
- **Gerçek Zamanlı Analiz:** Belirlenen alanlardaki piksel yoğunluğuna göre park yerinin "Dolu" veya "Boş" olduğu anlık olarak gösterilir.
- **Görsel Geri Bildirim:**
  - 🟢 **Yeşil:** Boş park yeri.
  - 🔴 **Kırmızı:** Dolu park yeri.
- **Sayaç:** Toplam boş park yeri sayısını ekranda gösterir.

## 🛠️ Gereksinimler

Bu projeyi çalıştırmak için bilgisayarınızda Python kurulu olmalıdır. Ayrıca aşağıdaki kütüphanelere ihtiyacınız vardır:

- `opencv-python`
- `cvzone`
- `numpy`

## 📦 Kurulum

1. Projeyi bilgisayarınıza indirin.
2. Gerekli kütüphaneleri yüklemek için terminal veya komut satırında şu komutu çalıştırın:

```bash
pip install opencv-python cvzone numpy
```

3. Çalışılacak otopark görselinin (carpark1.png) proje dizininde bulunduğundan emin olun.

▶️ Kullanım
Projeyi çalıştırmak için terminalde şu komutu girin:
python carpark.py

Uygulama açıldığında carpark1.png görseli yüklenecektir.

🎮 Kontroller
Sol Tık (Mouse): Yeni bir park yeri kutusu ekler.
Sağ Tık (Mouse): Var olan bir park yeri kutusunu siler.
'C' Tuşu: Ekrandaki tüm park yeri işaretlerini temizler.
ESC Tuşu: Programdan çıkar.

⚙️ Nasıl Çalışır?
Görüntü Ön İşleme: Görüntü gri tona çevrilir (cvtColor) ve bulanıklaştırılır (GaussianBlur).
Eşikleme (Threshold): adaptiveThreshold kullanılarak görüntü siyah-beyaz hale getirilir. Bu işlem araçları arka plandan ayırır.
Gürültü Temizleme: medianBlur ve dilate işlemleri ile görüntüdeki parazitler temizlenir ve araç hatları belirginleştirilir.
Piksel Sayımı: Kullanıcının belirlediği dikdörtgen alanlar içindeki beyaz pikseller (araç varlığı) sayılır (countNonZero).
Karar Verme: Sayılan piksel miktarı, belirlenen PIXEL_THRESHOLD (varsayılan: 900) değerinden yüksekse alan "Dolu", düşükse "Boş" olarak işaretlenir.

📝 Notlar
Boyut Ayarı: width ve height değişkenleri (şu an 107x48), kullanılan resimdeki park yeri boyutlarına göre carpark.py içinden değiştirilebilir.
Hassasiyet: Işık koşullarına göre PIXEL_THRESHOLD değerini kod içerisinden güncelleyebilirsiniz.

Bu proje BİL456 dersi kapsamında geliştirilmiştir.
