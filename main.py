import cv2
import datetime
import numpy as np
from datetime import datetime

cap = cv2.VideoCapture('video.mp4')

fgbg = cv2.createBackgroundSubtractorMOG2(detectShadows=True)

# Önceki karenin zaman damgasını tutuyoruz  
prev_frame_time = datetime.now()

while True:

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
           cv2.putText(frame, "Hareket Algilandi", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX,  0.5, (0, 255, 0), 2)
                  

    # Güncel karenin zaman damgasını alıyoruz
    new_frame_time = datetime.now()

    # Zaman farkını hesaplayıp fps'yi yazdırıyoruz
    time_diff_seconds = (new_frame_time - prev_frame_time).total_seconds()
    fps = 1/time_diff_seconds
    

    fps = round(fps * 1.5, 0)
    cv2.putText(frame, "Hiz: "+str(fps)+"", (10,40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

    prev_frame_time = new_frame_time  
    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()