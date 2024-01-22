import cv2

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Błąd odczytu kamery!")
    exit()
else:
    print("Udało sić wczytać kamerkę")

while True:
    success, frame =  cap.read()

    if not success:
        print("Błąd odczytu klatek!")
        break


    cv2.imshow('Kamera', frame)

    if(cv2.waitKey(1) & 0xFF == ord('n')):
        break

cap.release()
cv2.destroyAllWindows()