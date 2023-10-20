import cv2
import mediapipe as md

md_drawing = md.solutions.drawing_utils  # used to draw points on the body
md_drawing_styles = md.solutions.drawing_styles  # for styles
md_pose = md.solutions.pose  # main function for posing

count = 0
position = None

cap = cv2.VideoCapture(0)  # webcam input

with md_pose.Pose(
    min_detection_confidence=0.7,  # Accuracy of coordinates (play around with these)
    min_tracking_confidence=0.7) as pose:
    while cap.isOpened():
        success, image = cap.read()  # image is webcam image and success is whether we are getting any live footage from it
        if not success:
            print("camera is not working")
            break

        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)  # basically gets the image and we must flip it
        result = pose.process(image)

        # contains coordinate list
        imageList = []
        if result.pose_landmarks:
            md_drawing.draw_landmarks(
                image, result.pose_landmarks, md_pose.POSE_CONNECTIONS)  # lines which connect dots on video
            for id, im in enumerate(result.pose_landmarks.landmark):  # iterate through all landmarks
                h, w, _ = image.shape  # we need height and width of video
                X, Y = int(im.x * w), int(im.y * h)  # then we multiply by ratio to get exact coordinate
                imageList.append([id, X, Y])

        # basically if your shoulders are higher than elbows then you are up
        # if your shoulders are lower than elbows you are down
        if len(imageList) != 0:
            if (imageList[12][2] and imageList[11][2] >= imageList[14][2] and imageList[13][2]):
                position = "down"
            if (imageList[12][2] and imageList[11][2] <= imageList[14][2] and imageList[13][2]) and position == "down":
                position = "up"
                count += 1
                print(count)

        # exit condition
        cv2.imshow("push up counter", cv2.flip(image, 1))
        key = cv2.waitKey(1)
        if key == ord('q'):
            break

cap.release()
