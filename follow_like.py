import os
import time
import subprocess
from datetime import datetime

# Thiết lập thư mục log
log_dir = os.path.join(os.path.dirname(__file__), 'log')
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, 'follow_client.log')

def log(message):
    """Ghi log vào console và file"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"{timestamp} - {message}")
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(f"{timestamp} - {message}\n")

def perform_action(action_type):
    """Thực hiện hành động Follow trên TikTok sử dụng Termux API"""
    try:
        if action_type.lower() != 'follow':
            log(f"Hành động {action_type} không được hỗ trợ!")
            return "Error: Unsupported action"
        
        # Giả lập nhấn nút Follow trên TikTok
        # Tọa độ (x, y) cần điều chỉnh tùy thiết bị
        x, y = 500, 600  # Tọa độ giả định cho nút Follow
        cmd = f"termux-toast 'Thực hiện Follow' && input tap {x} {y}"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            log("Đã nhấn Follow thành công")
            time.sleep(1)  # Đợi để đảm bảo hành động hoàn tất
            return "Follow ok"
        else:
            log(f"Lỗi khi nhấn Follow: {result.stderr}")
            return "Nhả follow"
    except Exception as e:
        log(f"Lỗi khi thực hiện Follow: {str(e)}")
        return f"Error: {str(e)}"

def send_follow_request(url='http://10.0.0.2:8000/follow'):
    """Hàm để tương thích với tds5.py, gọi perform_action và trả kết quả"""
    # Vì chạy trên Termux, không cần gọi web server, gọi thẳng perform_action
    result = perform_action('follow')
    log(f"Kết quả: {result}")
    return result

if __name__ == "__main__":
    result = send_follow_request()
    print(result)