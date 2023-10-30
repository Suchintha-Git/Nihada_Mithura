import os
from cvzone.HandTrackingModule import HandDetector
import cv2

# Initialize variables for total marks and correct answer count
total_marks = 0
correct_answer_count = 0

# Define correct answers for each question
correct_answers = [2, 3, 1, 2, 1]

# Try to access the first available camera (camera index 0)
cap = cv2.VideoCapture(0)

# Check if the camera opened successfully
if not cap.isOpened():
    print("Error: Could not open camera.")
else:
    cap.set(3, 640)
    cap.set(4, 480)

    imgBackground = cv2.imread("Resources/Background.png")

    folderPathModes = "Resources/Modes"
    listImgModesPath = os.listdir(folderPathModes)
    listImgModes = []
    for imgModePath in listImgModesPath:
        listImgModes.append(cv2.imread(os.path.join(folderPathModes, imgModePath)))
    print(listImgModes)

    modeType = 0
    selection = -1
    counter = 0
    selectionSpeed = 7

    detector = HandDetector(detectionCon=0.8, maxHands=1)
    modePosition = [(1198, 139), (1198, 272), (1194, 400)]

    while True:
        success, img = cap.read()

        if not success:
            print("Error: Could not read frame.")
            break

        hands, img = detector.findHands(img)
        imgBackground[139:139 + 480, 50:50 + 640] = img
        imgBackground[0:720, 847:1280] = listImgModes[modeType]

        if hands:
            hand1 = hands[0]
            fingers1 = detector.fingersUp(hand1)

            if fingers1 == [0, 1, 0, 0, 0]:
                if selection != 1:
                    counter = 1
                selection = 1

            elif fingers1 == [0, 1, 1, 0, 0]:
                if selection != 2:
                    counter = 1
                selection = 2

            elif fingers1 == [0, 1, 1, 1, 0]:
                if selection != 3:
                    counter = 1
                selection = 3
            else:
                selection = -1
                counter = 0

            if counter > 0:
                counter += 1
                print(counter)

                # Calculate the angle of the circle based on counter and selection
                angle = counter * selectionSpeed

                if angle <= 360:
                    # Draw the circle based on the angle
                    cv2.ellipse(imgBackground, modePosition[selection - 1], (58, 58), 0, 0, angle, (0, 255, 0), 10)

                if angle >= 360 and modeType < len(correct_answers):
                    if selection == correct_answers[modeType]:
                        correct_answer_count += 1  # Increase correct answer count
                        total_marks += 20

                if counter * selectionSpeed > 360:
                    modeType += 1
                    counter = 0
                    selection = -1

        if modeType < len(correct_answers):
            cv2.imshow("Background", imgBackground)
        else:
            cv2.putText(imgBackground, f"Correct Answers: {correct_answer_count}", (900, 220), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 0), 2)
            cv2.putText(imgBackground, f"Total Marks: {total_marks}", (900, 280), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 0), 2)
            cv2.imshow("Background", imgBackground)

        if modeType == 6:  # Show the final result image and keep it open
            cv2.waitKey(0)
            break
        elif cv2.waitKey(1) & 0xFF == ord('q'):
            break

    print(f"Number of correct answers: {correct_answer_count}")
    print(f"Total Marks: {total_marks}")

# Release the camera when finished
cap.release()
cv2.destroyAllWindows()
