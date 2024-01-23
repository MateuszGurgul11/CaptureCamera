import cv2
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils #program rusuje linie laczace palce
mp_drawing_styles = mp.solutions.drawing_styles #styl dla lini pokazywanych na rece *opcjonalne*
mphands = mp.solutions.hands    #program wykrywa reke na kamerce

cam = cv2.VideoCapture(0)
hands = mphands.Hands()

if not cam.isOpened():
    print("Błąd wyswietlania kamerki!")
    exit()

while True:
    successFrame, frame = cam.read()
    frame = cv2.cvtColor(cv2.flip(frame, 1), cv2.COLOR_BGR2RGB)    #odwrocenie kamerki aby uniknac odbicia lustrzanego

    results = hands.process(frame)  #Wywoluje proces detekcji

    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)  #Dostosowanie kolorow kamery

    if(results.multi_hand_landmarks):   #Proram sprawdza czy sa wykryte rece jezeli tak program rysuje punkty na dloni
        for hand_landmarks in results.multi_hand_landmarks: #program itreuje przez kazda wykryta dlon
            mp_drawing.draw_landmarks(  #Program rusje punkty i łączenia
                frame,
                hand_landmarks, mphands.HAND_CONNECTIONS
            )

    if not successFrame:
        print("Błąd odczytu klatki!")
        break

    cv2.imshow('HandCam', frame)


    if(cv2.waitKey(1) & 0xFF == ord('q')):
        break

cam.release()
cv2.destroyAllWindows()