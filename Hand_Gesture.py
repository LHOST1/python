import cv2
import mediapipe as mp

# MediaPipe Hands modülünün başlatılması
mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.5)
mpDraw = mp.solutions.drawing_utils

# Webcam'in başlatılması
cap = cv2.VideoCapture(0)

while True:
    # Webcam'den kare okuma
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # Hands modülü ile el tespiti
    results = hands.process(imgRGB)

    if results.multi_hand_landmarks:
        for handslms in results.multi_hand_landmarks:
            # El landmark'larının çizimi
            mpDraw.draw_landmarks(img, handslms, mpHands.HAND_CONNECTIONS)

            # El landmark'larının koordinatlarının alınması
            landmarks = []
            for lm in handslms.landmark:
                h, w, _ = img.shape
                lmx, lmy = int(lm.x * w), int(lm.y * h)
                landmarks.append((lmx, lmy))

    # Sonuçların görüntülenmesi
    cv2.imshow("El Hareketi Tanima", img)
    
    # Çıkış için 'q' tuşuna basılması
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Webcam'in serbest bırakılması ve pencerenin kapatılması
cap.release()
cv2.destroyAllWindows()
