import cv2
import mediapipe as mp

# MediaPipe Pose modülünün başlatılması
mpPose = mp.solutions.pose
pose = mpPose.Pose(static_image_mode=False, min_detection_confidence=0.5, min_tracking_confidence=0.5)
mpDraw = mp.solutions.drawing_utils

# Vücut parça renkleri
body_part_colors = {
    mpPose.PoseLandmark.NOSE: (255, 0, 0),               # Mavi renk
    mpPose.PoseLandmark.LEFT_SHOULDER: (0, 255, 0),       # Yeşil renk
    mpPose.PoseLandmark.RIGHT_SHOULDER: (0, 0, 255),      # Kırmızı renk
}

# Webcam'in başlatılması
cap = cv2.VideoCapture(0)

while True:
    # Webcam'den kare okuma
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # Pose tespiti
    results = pose.process(imgRGB)
    
    if results.pose_landmarks:
        # Landmark'ların çizimi
        mpDraw.draw_landmarks(img, results.pose_landmarks, mpPose.POSE_CONNECTIONS,
                              landmark_drawing_spec=mpDraw.DrawingSpec(color=(0, 0, 255),
                                                                      thickness=2, circle_radius=2),
                              connection_drawing_spec=mpDraw.DrawingSpec(color=(255, 0, 0),
                                                                         thickness=2, circle_radius=2),
                              )
        # Vücut parçalarının renkli dairelerle işaretlenmesi
        for landmark, landmark_color in body_part_colors.items():
            if results.pose_landmarks.landmark[landmark]:
                lmx = int(results.pose_landmarks.landmark[landmark].x * img.shape[1])
                lmy = int(results.pose_landmarks.landmark[landmark].y * img.shape[0])
                cv2.circle(img, (lmx, lmy), 5, landmark_color, -1)

    # Sonuçların görüntülenmesi
    cv2.imshow("Yuz Tanima", img)

    # Çıkış için 'q' tuşuna basılması
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Webcam'in serbest bırakılması ve pencerenin kapatılması
cap.release()
cv2.destroyAllWindows()
