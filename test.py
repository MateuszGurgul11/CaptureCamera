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

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                frame,
                hand_landmarks,
                mphands.HAND_CONNECTIONS,
                landmark_drawing_spec=mp_drawing.DrawingSpec(color=(184, 3, 255), thickness=2, circle_radius=4),
                connection_drawing_spec=mp_drawing.DrawingSpec(color=(0, 0, 0), thickness=2)
            )

            # Indeks punktów końcowych palców
            finger_tip_indices = [4, 8, 12, 16, 20]

            # Koordynaty punktów końcowych palec wskazującego (index finger) i kciuka (thumb)
            index_finger_tip = hand_landmarks.landmark[8]
            thumb_tip = hand_landmarks.landmark[4]

            # Współrzędne punktów końcowych
            index_finger_coords = (int(index_finger_tip.x * frame.shape[1]), int(index_finger_tip.y * frame.shape[0]))
            thumb_coords = (int(thumb_tip.x * frame.shape[1]), int(thumb_tip.y * frame.shape[0]))

            # Rysowanie linii łączącej palec wskazujący z kciukiem
            cv2.line(frame, index_finger_coords, thumb_coords, (255, 0, 0), 2)

    cv2.imshow('finger_detection', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
