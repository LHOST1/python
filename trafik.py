import cv2
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from pytube import YouTube
from pytube.exceptions import AgeRestrictedError

# Fonksiyon: URL'yi al ve videoyu işleyerek göster
def baslat():
    try:
        # Kullanıcının girdiği URL'yi al
        url = url_girdi.get()

        # YouTube videoyu indirin ve işleyin
        yt = YouTube(url)
        stream = yt.streams.filter(file_extension="mp4", res="720p").first()
        video_path = stream.download()

        # Bellek akışını kullanarak VideoCapture nesnesini oluşturun
        cap = cv2.VideoCapture(video_path)

        # Arka plan çıkarımı için nesne oluşturun
        fgbg = cv2.createBackgroundSubtractorMOG2(detectShadows=True)

        # Önceki karenin zaman damgasını tutuyoruz
        prev_frame_time = datetime.now()

        while True:
            # Bellek akışından bir kare okuyun
            ret, frame = cap.read()

            # Görüntüye zemin çıkarımı uyguluyoruz
            fgmask = fgbg.apply(frame)

            # Konturları buluyoruz
            contours, hierarchy = cv2.findContours(fgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            for contour in contours:
                # Kontur alanlarını hesaplıyoruz
                area = cv2.contourArea(contour)
                # Belirli eşik değerinin üzerindeki konturları çizdiriyoruz
                if area > 1200:
                    x, y, w, h = cv2.boundingRect(contour)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 255), 3)
                    cv2.putText(frame, "Hareket Algilandi", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            # Güncel karenin zaman damgasını alıyoruz
            new_frame_time = datetime.now()

            # Zaman farkını hesaplayıp fps'yi yazdırıyoruz
            time_diff_seconds = (new_frame_time - prev_frame_time).total_seconds()
            fps = 1 / time_diff_seconds

            fps = round(fps * 1, 0)
            cv2.putText(frame, "FPS: " + str(fps) + "", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            prev_frame_time = new_frame_time

            # Videoyu ekranda göster
            cv2.imshow('Video', frame)

            # Kullanıcıdan 'q' tuşuna basarak çıkış yapmasını bekleyin
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Bellek akışını serbest bırakın ve pencereyi kapatın
        cap.release()
        cv2.destroyAllWindows()

    except AgeRestrictedError:
        messagebox.showinfo("Uyarı", "Bu video 18 yaş veya üzeri içerik olduğundan dolayı izlenemiyor.")

# Ana pencereyi oluştur
root = tk.Tk()
root.title("Video İşleme Programı")

# URL giriş alanını oluştur
url_girdi = ttk.Entry(root, width=50)
url_girdi.grid(row=0, column=0, padx=10, pady=10, columnspan=2)

# "Başlat" düğmesini oluştur
baslat_dugme = ttk.Button(root, text="Başlat", command=baslat)
baslat_dugme.grid(row=1, column=0, padx=10, pady=10, columnspan=2)

# Ana döngüyü başlat
root.mainloop()