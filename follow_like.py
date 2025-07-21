import requests
import time
import os
import sys
import json
import subprocess

# Thiết lập thư mục log
log_dir = os.path.join(os.path.dirname(__file__), 'log')
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, 'follow_client.log')

def log(message):
    """Ghi log vào console và file"""
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    print(f"{timestamp} - {message}")
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(f"{timestamp} - {message}\n")

def get_device_id():
    """Lấy device_id của thiết bị Android"""
    try:
        result = subprocess.run(['getprop', 'ro.serialno'], capture_output=True, text=True, check=True)
        device_id = result.stdout.strip()
        # log(f"Device ID: {device_id}") # Đã chú thích/xóa theo yêu cầu trước
        return device_id
    except Exception as e:
        log(f"Lỗi khi lấy device_id: {str(e)}")
        return "Error: Cannot get device_id" # Trả về lỗi dạng string để TDS5 có thể bắt

def send_follow_request(url='http://10.0.0.2:8000/follow'):
    """Gửi yêu cầu Follow đến web server trên PC và nhận kết quả"""
    try:
        device_id = get_device_id()
        if device_id.startswith("Error:"): # Kiểm tra lỗi từ get_device_id
            return device_id

        headers = {'Content-Type': 'application/json'}
        data = {'task': 'FOLLOW', 'device_id': device_id}
        # log(f"Đang gửi yêu cầu đến {url} với device_id: {device_id}") # Đã chú thích/xóa theo yêu cầu trước
        response = requests.post(url, json=data, headers=headers, timeout=20)
        response.raise_for_status() # Raises HTTPError for bad responses (4xx or 5xx)
        result = response.json()
        # log(f"Kết quả từ server: {result}") # Đã chú thích/xóa theo yêu cầu trước
        
        # Đảm bảo trả về chuỗi "Follow ok" hoặc "Nhả follow" từ trường 'result'
        # Hoặc một thông báo lỗi nếu trường 'result' không tồn tại
        return result.get('result', 'Error: No "result" field from server')

    except requests.exceptions.RequestException as e:
        log(f"Lỗi khi gửi yêu cầu HTTP hoặc nhận phản hồi: {e}")
        return f"Error: Request failed - {str(e)}"
    except json.JSONDecodeError as e:
        log(f"Lỗi giải mã JSON từ phản hồi: {e}. Phản hồi: {response.text if 'response' in locals() else 'Không có phản hồi'}")
        return f"Error: JSON decode failed - {str(e)}"
    except Exception as e:
        log(f"Lỗi không xác định trong send_follow_request: {e}")
        return f"Error: Unexpected error - {str(e)}"
