import cv2

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Błąd odczytu kamery!")
    exit()

while True:
    sCap, frame =  cap.read()

    if not sCap:
        print("Błąd odczytu klatek!")
        break

    cv2.imshow('Kamera', frame)

    if(cv2.waitKey(1) & 0xFF == ord('n')):
        break

cap.release()
cv2.destroyAllWindows()