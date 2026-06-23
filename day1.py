import cv2
import numpy as np

def smart_change_photo():
    img = cv2.imread('text.jpg')
    if img is None: return

    # 1. 转 HSV
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # 2. 针对浅蓝色调整阈值
    lower_blue = np.array([75, 40, 40]) 
    upper_blue = np.array([115, 255, 255])
    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    # 3. 【重点】形态学操作：去除衣服上的红点噪声
    kernel = np.ones((5, 5), np.uint8)
    # 开启运算：先腐蚀（消灭小红点），再膨胀（恢复背景大区域）
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    # 加上模糊，让边缘更平滑
    mask = cv2.GaussianBlur(mask, (5, 5), 0)

    # 4. 换色
    res = img.copy()
    res[mask > 128] = (0, 0, 255) # 128是中间值，代表被选中的背景

    cv2.imshow('Result_Improved', res)
    cv2.imwrite('result_improved.jpg', res)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    smart_change_photo()