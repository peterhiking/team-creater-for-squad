import tkinter as tk  # 导入 Tkinter 库，用于创建 GUI 界面
from PIL import Image, ImageTk  # 导入 PIL 库，用于处理图像
import socket  # 导入 socket 库，用于获取本机 IP 地址
import qrcode  # 导入 qrcode 库，用于生成二维码
import io  # 导入 io 库，用于处理字节流
from flask import Flask, request  # 导入 Flask 库，用于创建 Web 应用

# 导入 pyautogui 库，用于模拟键盘输入
import pyautogui  
import time  # 导入 time 库，用于时间相关操作
import threading  # 导入 threading 库，用于多线程处理
import os
import clipboard

# 获取本机IP地址
# 获取本机IP地址
def get_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('114.114.114.114', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip

# 生成IP地址的二维码图像
def generate_qr_code(ip_address):
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)  # 创建 QRCode 对象
    qr.add_data("http://" + ip_address + ":5000")  # 添加数据，这里是包含 IP 地址的 URL
    qr.make(fit=True)  # 生成二维码
    qr_img = qr.make_image(fill_color="black", back_color="white")  # 生成二维码图像
    return qr_img

# 创建Flask应用
app = Flask(__name__)  # 创建 Flask 应用实例

# Flask应用的HTML内容
html_content_1 = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Squad快速建队工具</title>
    <style>
        body {
            font-family: Arial, sans-serif;  /* 设置字体 */
            padding: 20px;  /* 设置页面内边距 */
        }
        h1 {
            text-align: center;  /* 设置标题居中显示 */
        }
        #text-input {
            width: 100%;  /* 设置文本输入框宽度为100% */
            padding: 15px;  /* 设置文本输入框内边距 */
            font-size: 20px;  /* 设置字体大小 */
            margin-top: 10px;  /* 设置上边距 */
            margin-bottom: 20px;  /* 设置下边距 */
            box-sizing: border-box;  /* 设置盒模型为border-box */
            border-radius: 8px;  /* 设置边框圆角 */
            border: 2px solid #ccc;  /* 设置边框样式 */
        }
        #repeat-slider {
            width: 100%;  /* 设置滑块宽度为100% */
            margin-top: 10px;  /* 设置上边距 */
            margin-bottom: 20px;  /* 设置下边距 */
        }
        #repeat-text {
            text-align: center;  /* 设置文本居中显示 */
            font-size: 20px;  /* 设置字体大小 */
            margin-bottom: 20px;  /* 设置下边距 */
        }
        #send-button {
            display: block;  /* 设置按钮以块级元素显示 */
            width: 100%;  /* 设置按钮宽度为100% */
            padding: 15px;  /* 设置按钮内边距 */
            font-size: 20px;  /* 设置字体大小 */
            background-color: #4CAF50;  /* 设置背景颜色 */
            color: white;  /* 设置字体颜色 */
            border: none;  /* 取消边框 */
            border-radius: 8px;  /* 设置边框圆角 */
            cursor: pointer;  /* 设置鼠标样式为手型 */
            transition: background-color 0.3s;  /* 设置背景颜色变化的过渡效果 */
            margin-bottom: 10px;  /* 设置下边距 */
        }
        .author {
            position: fixed;  /* 固定位置 */
            right: 10px;  /* 距离右侧10像素 */
            bottom: 10px;  /* 距离底部10像素 */
            color: grey;  /* 字体颜色 */
            font-size: 12px;  /* 字体大小 */
        }
        /* 新增样式 */
        .note {
            border: 1px solid #ccc; /* 设置边框样式 */
            padding: 10px; /* 设置内边距 */
            margin-top: 20px; /* 设置与上方元素的间距 */
            font-size: 12px; /* 设置字体大小 */
            border-radius: 5px; /* 设置边框圆角 */
        }
    </style>
</head>
<body>
    <h1>Squad快速建队工具</h1>  <!-- 标题 -->
    <form action="/send_text" method="post">  <!-- 表单，提交到/send_text路径，使用POST方法 -->
        <input type="text" id="text-input" name="text" placeholder="输入队伍名称到此处">  <!-- 文本输入框 -->
        <br>
        <input type="range" id="repeat-slider" name="repeat" min="1" max="10" value="5" oninput="updateSliderValue(this.value)">  <!-- 滑块 -->
        <div id="repeat-text">输入动作重复次数: <span id="slider-value">5</span></div>  <!-- 提示文本 -->
        <button type="submit" id="send-button">开始建队</button>  <!-- 提交按钮 -->
    </form>
    <div class="author">@莫斯菲特</div>  <!-- 添加的作者信息 -->
    <!-- 新增注意事项 -->
    <div class="note">
        注意事项：作为字数要求，英语字母数≥3个，数字字数≥4个，中文字数≥2个。
    </div>
    <script>
    function updateSliderValue(value) {  // 更新滑块值的 JavaScript 函数
        document.getElementById("slider-value").textContent = value;  // 获取元素并设置文本内容
    }
    </script>
</body>
</html>
"""


# Flask应用的路由
@app.route('/')  # 根路径
def index():
    return html_content_1  # 返回 HTML 内容

@app.route('/send_text', methods=['POST'])  # 处理表单提交的路径
def send_text():
    text = request.form['text']  # 获取表单中的文本数据
    repeat = int(request.form['repeat'])  # 获取滑块的值，转换为整数
    clipboard.copy("CreateSquad " + text + " 1")
    for _ in range(repeat):  # 根据重复次数执行操作
        pyautogui.press('`')  # 模拟按下键盘上的 '`' 键
        pyautogui.hotkey('ctrl', 'v')
        pyautogui.press('enter')
        time.sleep(0.1)  # 等待一段时间
    return html_content_1  # 返回 HTML 内容

# 启动Flask应用的函数
def run_flask_app():
    app.run(host='0.0.0.0', threaded=True)  # 在指定主机和端口上运行 Flask 应用，启用多线程支持

def quit_program():
    os._exit(0)

# 主线程中创建Tkinter应用
def main():
    ip_address = get_ip()  # 获取本机 IP 地址
    qr_img = generate_qr_code(ip_address)  # 生成二维码图像

    # 创建Tkinter窗口
    root = tk.Tk()  # 创建 Tkinter 窗口实例
    root.title("Squad快速建队工具")  # 设置窗口标题

    # 设置窗口居中显示
    window_width = 400  # 窗口宽度
    window_height = 500  # 窗口高度，根据需要调整这两个值以适应您的内容
    screen_width = root.winfo_screenwidth()  # 获取屏幕宽度
    screen_height = root.winfo_screenheight()  # 获取屏幕高度
    x_coordinate = int((screen_width/2) - (window_width/2))  # 计算窗口横坐标
    y_coordinate = int((screen_height/2) - (window_height/2))  # 计算窗口纵坐标
    root.geometry("{}x{}+{}+{}".format(window_width, window_height, x_coordinate, y_coordinate))  # 设置窗口尺寸和位置

    label_1 = tk.Label(root, text="手机扫码自动打开浏览器",
                        justify='left',
                        anchor='center',
                        font=('微软雅黑',18),
                        fg='black',
                        bg='white',
                        compound='center',
                        padx=5,
                        pady=20)
    label_1.pack()  # 将标签组件放置到窗口上

    # 显示二维码图像
    img = ImageTk.PhotoImage(qr_img)  # 创建图像实例
    panel = tk.Label(root, image=img)  # 创建标签组件显示图像
    panel.pack(padx=10, pady=10)  # 将标签组件放置到窗口上

    # 添加作者信息的标签
    author_label = tk.Label(root, text="@莫斯菲特", fg="grey", bg="white", anchor="se")
    author_label.pack(side="bottom", fill="x", padx=10, pady=10)

    # 在新线程中启动Flask应用
    flask_thread = threading.Thread(target=run_flask_app)  # 创建新线程
    flask_thread.start()  # 启动线程
    
    root.protocol("WM_DELETE_WINDOW", quit_program)
    root.resizable(False, False)
    # 启动Tkinter事件循环
    root.mainloop()  # 进入 Tkinter 事件循环，等待用户交互



if __name__ == "__main__":
    main()  # 执行主函数
