import cv2
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mphands = mp.solutions.hands
cap = cv2.VideoCapture(0)
hands = mphands.Hands()

index_finger_text = ""
midle_finger_text = ""
sum_text = ""

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
                landmark_drawing_spec = mp_drawing.DrawingSpec(color = (184, 3, 255), thickness = 2, circle_radius = 4),
                connection_drawing_spec = mp_drawing.DrawingSpec(color = (0, 0, 0), thickness = 2)
            )
        
            finger_tip_indices = [4, 8, 12, 16, 20]

            def index_finger():
                global index_finger_text
                tip_index = 8
                base_index = 5

                tip_point = hand_landmarks.landmark[tip_index]
                base_point = hand_landmarks.landmark[base_index]

                if tip_point.y < base_point.y:
                    #cv2.putText(frame, "Palec wskazujacy jest podniesiony", (10, 60), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 2)
                    index_finger_text = '1'
            
            def midle_finger():
                global midle_finger_text
                tip_index = 12
                base_index = 9

                tip_point = hand_landmarks.landmark[tip_index]
                base_point = hand_landmarks.landmark[base_index]

                if tip_point.y < base_point.y:
                    #cv2.putText(frame, "Srodkowy palec jest podniesiony",(10, 60), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 2)
                    midle_finger_text = "2"

            def sum():
                global sum_text
                tip_index1 = 8 
                tip_index2 = 20
                base_index1 = 5 
                base_index2 = 17 

                tip_point1 = hand_landmarks.landmark[tip_index1]
                base_point1 = hand_landmarks.landmark[base_index1]
                tip_point2 = hand_landmarks.landmark[tip_index2]
                base_point2 = hand_landmarks.landmark[base_index2]

                if tip_point1.y and tip_point2.y < base_point1.y and base_point2.y:
                    #cv2.putText(frame, '+', (10, 60), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 2)
                    sum_text = '+'

            def restart():
                global index_finger_text, midle_finger_text, sum_text
                tip_index = 4
                base_index = 5

                tip_point = hand_landmarks.landmark[tip_index]
                base_point = hand_landmarks.landmark[base_index]

                if tip_point.y > base_point.y:
                    index_finger_text = ''
                    midle_finger_text = ''
                    sum_text = ''

            index_finger()
            midle_finger()
            sum()
            restart()

            cv2.putText(frame, index_finger_text, (10, 60), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 2)
            cv2.putText(frame, sum_text, (30, 60), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 2)
            cv2.putText(frame, midle_finger_text, (60, 60), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 2)

    cv2.imshow('finger_detection', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

