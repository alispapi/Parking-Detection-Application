import cv2
import cvzone
import numpy as np

# Otopark yeri boyutları (Resme göre bu değerleri değiştirmeniz gerekebilir)
# Genellikle bir araç park yeri dikdörtgeni için genişlik ve yükseklik
width, height = 107, 48

# Doluluk Eşik Değeri
# Bu değeri ekranda kutucukların içinde yazan sayılara göre ayarlamalısınız.
# Boş yerler (ve engelli işaretleri) bu değerin ALTINDA kalmalı.
# Dolu yerler (arabalar) bu değerin ÜSTÜNDE olmalı.
PIXEL_THRESHOLD = 900

# Park yeri konumlarını tutacak liste (Program her açıldığında sıfırlanır)
posList = []

def mouseClick(events, x, y, flags, params):
    # Sol tık ile yeni park yeri ekle
    if events == cv2.EVENT_LBUTTONDOWN:
        posList.append((x, y))
    # Sağ tık ile var olan park yerini sil
    if events == cv2.EVENT_RBUTTONDOWN:
        for i, pos in enumerate(posList):
            x1, y1 = pos
            if x1 < x < x1 + width and y1 < y < y1 + height:
                posList.pop(i)

def checkParkingSpace(imgPro, img):
    spaceCounter = 0

    for pos in posList:
        x, y = pos
        
        # İşlenmiş resimden ilgili park yerini kırp
        imgCrop = imgPro[y:y + height, x:x + width]
        
        # Beyaz pikselleri say (Dolu alan yoğunluğu)
        count = cv2.countNonZero(imgCrop)
        
        # Eşik değeri (Bu değeri ışık ve resim durumuna göre ayarlayabilirsiniz)
        # Eğer piksel sayısı PIXEL_THRESHOLD'dan azsa boş kabul et
        if count < PIXEL_THRESHOLD:
            color = (0, 255, 0) # Yeşil (Boş)
            thickness = 5
            spaceCounter += 1
        else:
            color = (0, 0, 255) # Kırmızı (Dolu)
            thickness = 2

        # Dikdörtgen çiz
        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), color, thickness)
        # Piksel sayısını yazdır (Ayarlama yaparken yardımcı olur)
        cvzone.putTextRect(img, str(count), (x, y + height - 3), scale=1, thickness=2, offset=0, colorR=color)

    # Toplam boş yer sayısını ekrana yazdır
    cvzone.putTextRect(img, f'{spaceCounter}/{len(posList)}', (50, 50), scale=3, thickness=5, offset=20, colorR=(0,200,0))

while True:
    # Resmi yükle
    img = cv2.imread('carpark1.png')
    
    if img is None:
        print("Hata: Dosya bulunamadı. Lütfen dosya isminin doğru olduğundan emin olun.")
        break

    # Görüntü işleme adımları
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 1)
    
    # Eşikleme (Threshold) - Siyah beyaz ayrımı
    # C değerini düşürdük (16 -> 6). Bu, daha silik nesnelerin (gri araba gibi) de algılanmasını sağlar.
    imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                         cv2.THRESH_BINARY_INV, 25, 6)
    
    # Gürültü temizleme
    # Median blur değerini düşürdük (5 -> 3). Bu, ince detayların (araba hatlarının) kaybolmasını önler.
    imgMedian = cv2.medianBlur(imgThreshold, 3)
    
    # Genişletme (Dilation)
    # Kernel boyutunu biraz büyüttük ve iterasyonu artırdık.
    # Bu, araba parçalarının birleşip daha büyük bir blok oluşturmasını sağlar.
    kernel = np.ones((3, 3), np.uint8)
    imgDilate = cv2.dilate(imgMedian, kernel, iterations=2)

    # Park yerlerini kontrol et
    checkParkingSpace(imgDilate, img)

    # İşlenmiş görüntüyü de göster (Hata ayıklama için)
    # Bu pencerede beyaz görünen yerler "dolu" sayısını artırır.
    cv2.imshow("Otopark Takip Sistemi", img)
    cv2.imshow("Islenmis Goruntu (Siyah-Beyaz)", imgDilate)
    
    # Fare olaylarını dinle
    cv2.setMouseCallback("Otopark Takip Sistemi", mouseClick)
    
    # ESC tuşuna basılırsa çık
    key = cv2.waitKey(1)
    if key == 27:
        break
    # 'c' tuşuna basılırsa tüm işaretleri temizle
    elif key == ord('c') or key == ord('C'):
        posList = []

cv2.destroyAllWindows()