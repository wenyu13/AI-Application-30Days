import cv2

def main():
    # 1. 打开摄像头 (0代表默认摄像头)
    cap = cv2.VideoCapture(0)

    # 检查摄像头是否打开
    if not cap.isOpened():
        print("错误：无法打开摄像头")
        return

    # 2. 读取前两帧，作为对比的起点
    # frame1 是我们用来展示的当前画面
    # frame2 是用来和下一帧做对比的参考
    ret, frame1 = cap.read()
    ret, frame2 = cap.read()

    print("监控已启动，按 'Esc' 键退出...")

    while cap.isOpened():
        # 3. 计算两帧之间的差异
        # absdiff 会把两张图中像素变化大的地方标出来
        diff = cv2.absdiff(frame1, frame2)
        
        # 4. 图像预处理（这是CV的核心三部曲）
        # (1) 转灰度：运动检测不需要颜色信息
        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        # (2) 高斯模糊：过滤掉摄像头的小噪点
        blur = cv2.GaussianBlur(gray, (21, 21), 0)
        # (3) 二值化：把变化显著的地方变纯白，不动的变纯黑
        _, thresh = cv2.threshold(blur, 40, 255, cv2.THRESH_BINARY)
        # (4) 膨胀：把断断续续的白点连成一大块，方便识别
        dilated = cv2.dilate(thresh, None, iterations=5)

        # 5. 寻找图像中的轮廓（即发生运动的物体形状）
        contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            # 6. 灵敏度过滤
            # 如果运动物体的面积太小（比如苍蝇飞过），就忽略它
            if cv2.contourArea(contour) < 10000:
                continue
            
            # 7. 锁定目标：画出红框
            (x, y, w, h) = cv2.boundingRect(contour)
            cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.putText(frame1, "WARNING: MOVEMENT", (10, 30), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        # 8. 显示结果
        cv2.imshow("Smart Monitor", frame1)

        # 9. 迭代画面：把旧的帧替换掉，读取新的一帧
        frame1 = frame2
        ret, frame2 = cap.read()

        # 按 Esc 键退出 (Esc的ASCII码是27)
        if cv2.waitKey(10) == 27:
            break

    # 10. 释放资源
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()