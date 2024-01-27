import cv2
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mphands = mp.solutions.hands

cap = cv2.VideoCapture(0)
hands = mphands.Hands()

if not cap.isOpened():
    print("error")
    exit()

while True:
    scap, frame = cap.read()

    frame = cv2.cvtColor(cv2.flip(frame, 1), cv2.COLOR_BGR2RGB)
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    result = hands.process(frame)

    fingers_up = [0, 0, 0, 0, 0]

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                frame,
                hand_landmarks,
                mphands.HAND_CONNECTIONS,
                landmark_drawing_spec = mp_drawing.DrawingSpec(color = (184, 3, 255), thickness = 2, circle_radius = 4),
                connection_drawing_spec = mp_drawing.DrawingSpec(color = (0, 0, 0), thickness = 2)
            )

            # Pobierz końce dłoni (wierzchołki palców)
            finger_tip_indices = [4, 8, 12, 16, 20]

            for i, tip_index in enumerate(finger_tip_indices):
                tip_point = hand_landmarks.landmark[tip_index]
                wrist_point = hand_landmarks.landmark[0]
                if tip_point.y < wrist_point.y:
                    # Sprawdź, czy lista ma odpowiednią długość
                    if i < len(fingers_up):
                        fingers_up[i] = 1

            finger_tips = [(int(hand_landmarks.landmark[i].x * frame.shape[1]), int(hand_landmarks.landmark[i].y * frame.shape[0])) for i in finger_tip_indices]

            # Znajdź współrzędne lewego górnego i prawego dolnego rogu kwadratu
            min_x = min(finger_tips, key=lambda x: x[0])[0]
            min_y = min(finger_tips, key=lambda x: x[1])[1]
            max_x = max(finger_tips, key=lambda x: x[0])[0]
            max_y = max(finger_tips, key=lambda x: x[1])[1]

            # Narysuj kwadrat wokół dłoni
            cv2.rectangle(frame, (min_x, min_y), (max_x, max_y), (0, 255, 0), 2)

            finger_count = fingers_up.count(1)

            # Odczytaj wielkość kwadratu
            square_size = max_x - min_x

            # Sprawdź, czy palec jest uniesiony na podstawie wielkości kwadratu
            if square_size > 200:  # Przykładowa wartość progowa
                cv2.putText(frame, f"Palec uniesiono palec {finger_tips[i]}", (10, 60), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
            else:
                cv2.putText(frame, "Palec jest schowany", (10, 60), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
    cv2.imshow('hand_capture', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
