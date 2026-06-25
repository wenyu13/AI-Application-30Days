import cv2
import numpy as np

def start_virtual_paint():
    cap = cv2.VideoCapture(0)
    
    # 1. 定义我们要追踪的颜色范围 (这里以【蓝色】为例)
    # 面试考点：HSV比RGB更适合追踪，因为H(色调)稳定
    lower_color = np.array([100, 100, 100]) 
    upper_color = np.array([130, 255, 255])

    # 2. 创建一个空白画布，用来记录绘画轨迹
    # 这个画布和摄像头画面一样大，初始全是黑色
    canvas = None

    # 上一次画笔的位置（用来连线）
    prev_x, prev_y = 0, 0

    print("虚拟画笔已启动！拿起蓝色物体开始绘画，按 'c' 清屏，按 'q' 退出。")

    while True:
        ret, frame = cap.read()
        if not ret: break
        frame = cv2.flip(frame, 1) # 水平翻转，像照镜子一样自然

        # 初始化画布
        if canvas is None:
            canvas = np.zeros_like(frame)

        # 3. 图像预处理
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lower_color, upper_color)
        
        # 消除杂色噪点
        mask = cv2.erode(mask, None, iterations=1)
        mask = cv2.dilate(mask, None, iterations=2)

        # 4. 寻找物体的中心点
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if contours:
            # 找到面积最大的轮廓
            c = max(contours, key=cv2.contourArea)
            if cv2.contourArea(c) > 500: # 面积过滤
                # 获取最小外接圆，得到中心点坐标
                ((x, y), radius) = cv2.minEnclosingCircle(c)
                curr_x, curr_y = int(x), int(y)

                # 5. 绘图逻辑
                if prev_x == 0 and prev_y == 0:
                    prev_x, prev_y = curr_x, curr_y
                
                # 在画布上画线 (画笔颜色设为绿色 0,255,0，粗细为5)
                cv2.line(canvas, (prev_x, prev_y), (curr_x, curr_y), (0, 255, 0), 5)
                
                # 更新坐标
                prev_x, prev_y = curr_x, curr_y
                
                # 画一个实时的小圆点作为光标
                cv2.circle(frame, (curr_x, curr_y), int(radius), (255, 0, 0), 2)
        else:
            # 如果没检测到物体，重置起始点
            prev_x, prev_y = 0, 0

        # 6. 将画布叠加到原图上
        # 原理：将原图中画布有颜色的地方替换掉
        frame = cv2.addWeighted(frame, 1, canvas, 1, 0)

        cv2.imshow("Virtual Paint", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'): break
        if key == ord('c'): canvas = np.zeros_like(frame) # 清屏

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    start_virtual_paint()