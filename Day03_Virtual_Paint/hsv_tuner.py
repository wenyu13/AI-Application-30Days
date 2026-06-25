import cv2
import numpy as np

def nothing(x):
    pass

# 创建一个窗口用于调节
cv2.namedWindow("Trackbars")
cv2.createTrackbar("L-H", "Trackbars", 100, 179, nothing)
cv2.createTrackbar("L-S", "Trackbars", 100, 255, nothing)
cv2.createTrackbar("L-V", "Trackbars", 100, 255, nothing)
cv2.createTrackbar("U-H", "Trackbars", 130, 179, nothing)
cv2.createTrackbar("U-S", "Trackbars", 255, 255, nothing)
cv2.createTrackbar("U-V", "Trackbars", 255, 255, nothing)

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # 获取滑块的值
    l_h = cv2.getTrackbarPos("L-H", "Trackbars")
    l_s = cv2.getTrackbarPos("L-S", "Trackbars")
    l_v = cv2.getTrackbarPos("L-V", "Trackbars")
    u_h = cv2.getTrackbarPos("U-H", "Trackbars")
    u_s = cv2.getTrackbarPos("U-S", "Trackbars")
    u_v = cv2.getTrackbarPos("U-V", "Trackbars")

    lower = np.array([l_h, l_s, l_v])
    upper = np.array([u_h, u_s, u_v])

    mask = cv2.inRange(hsv, lower, upper)
    
    cv2.imshow("Frame", frame)
    cv2.imshow("Mask (Only white should be your pen)", mask)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        print(f"建议参数: lower = [{l_h}, {l_s}, {l_v}], upper = [{u_h}, {u_s}, {u_v}]")
        break

cap.release()
cv2.destroyAllWindows()