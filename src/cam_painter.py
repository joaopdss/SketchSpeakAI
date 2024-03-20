import numpy as np
import cv2
import tensorflow as tf
import hand_tracking_module as hand_tracking
import time

class Drawing():

    def __init__(self):
        self.img_canvas = np.zeros((720, 1280, 3), np.uint8)
        self.recording = False
        self.cap = cv2.VideoCapture(0)
        self.cap.set(3, 1288)
        self.cap.set(4, 728)


    def start(self):
        hand_detector = hand_tracking.handDetector()
        draw_color = (0, 0, 255)
        xp, yp = 0, 0
        select_colors = False
        select_recording = False
        action = 0  # {0: Nothing, 1: "Draw", 2: "Erase", 3: "Select Color"}

        header_img = cv2.imread("../images/header.jpg")
        colors = cv2.imread("../images/colors.jpg")

        end_time = 0
        start_time = time.time()

        while True:
            _, frame = self.cap.read()

            if _:
                frame = cv2.flip(frame, 1)
                frame = hand_detector.find_hands(frame)
                lm_list = hand_detector.find_position(frame)

                if len(lm_list) != 0:
                    xp, yp = 0, 0
                    x1, y1 = lm_list[8][1:]
                    x2, y2 = lm_list[12][1:]

                    fingers = hand_detector.fingers_up()

                    # If pointer and middle fingers are up, we can select rubber, pencil or send draw to NN
                    if fingers[1] and fingers[2]:

                        if y1 < 125:
                            if 1000 < x1 < 1100:
                                action = 1
                            elif 1100 < x1 < 1280:
                                draw_color = (0, 0, 0)
                                action = 2
                            elif 850 < x1 < 950:
                                select_colors = True
                                action = 3
                            elif 525 < x1 < 695 and y1 > 20 and (end_time - start_time) > 5 and not select_recording:
                                select_recording = True
                                action = 0

                                if not self.recording:
                                    print("recording")
                                    self.recording = True
                                else:
                                    print("not recording")
                                    self.recording = False

                        elif 125 < y1 < 250 and select_colors and action == 3:

                            if 145 < y1 < 190 and 790 < x1 < 845:
                                draw_color = (49, 49, 255)
                            elif 210 < y1 < 245 and 790 < x1 < 845:
                                draw_color = (0, 255, 0)
                            elif 145 < y1 < 190 and 910 < x1 < 965:
                                draw_color = (196, 102, 255)
                            elif 210 < y1 < 245 and 910 < x1 < 965:
                                draw_color = (255, 182, 56)
                            elif 145 < y1 < 190 and 1030 < x1 < 1085:
                                draw_color = (89, 222, 255)
                            elif 210 < y1 < 245 and 1030 < x1 < 1085:
                                draw_color = (217, 217, 217)

                            frame[125:250, 760:1140] = colors
                        else:
                            select_colors = False
                            select_recording = False

                        cv2.rectangle(frame, (x1, y1 - 25), (x2, y2 + 25), draw_color, cv2.FILLED)

                    # If pointer finger is up and middle finger down, can draw/erase
                    if fingers[1] and not fingers[2]:
                        cv2.circle(frame, (x1, y1), 15, draw_color, cv2.FILLED)

                        if xp == 0 and yp == 0:
                            xp, yp = x1, y1

                        if action == 2:
                            cv2.line(frame, (xp, yp), (x1, y1), draw_color, 225)
                            cv2.line(self.img_canvas, (xp, yp), (x1, y1), draw_color, 225)
                        elif action == 1:
                            cv2.line(frame, (xp, yp), (x1, y1), draw_color, 25)
                            cv2.line(self.img_canvas, (xp, yp), (x1, y1), draw_color, 25)

                        xp, yp = x1, y1

                img_gray = cv2.cvtColor(self.img_canvas, cv2.COLOR_BGR2GRAY)
                _, img_inv = cv2.threshold(img_gray, 50, 255, cv2.THRESH_BINARY_INV)
                img_inv = cv2.cvtColor(img_inv, cv2.COLOR_GRAY2BGR)
                frame = cv2.bitwise_and(frame, img_inv)
                frame = cv2.bitwise_or(frame, self.img_canvas)

                frame[0:125, 0:1280] = header_img

                if not self.recording:
                    cv2.putText(frame, "Start recording", (535, 65), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
                else:
                    cv2.putText(frame, "Stop recording", (535, 65), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)

                cv2.imshow("Frame", frame)
                cv2.waitKey(1)

            end_time = time.time()

        cap.release()
        cv2.destroyAllWindows()