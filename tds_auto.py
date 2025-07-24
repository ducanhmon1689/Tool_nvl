import sys
import subprocess
import os

# --- PHẦN KIỂM TRA VÀ CÀI ĐẶT THƯ VIỆN TỰ ĐỘNG ---
print("Đang kiểm tra các thư viện cần thiết...")

# Danh sách các thư viện cần thiết
required_libraries = ['requests', 'pystyle']

for lib in required_libraries:
    try:
        # Thử import thư viện
        __import__(lib)
        print(f"-> Thư viện '{lib}' đã được cài đặt.")
    except ImportError:
        # Nếu import lỗi, tiến hành cài đặt
        print(f"-> Thư viện '{lib}' chưa có, đang tiến hành cài đặt...")
        try:
            # Sử dụng sys.executable để đảm bảo dùng đúng pip của phiên bản Python đang chạy
            subprocess.check_call([sys.executable, "-m", "pip", "install", lib])
            print(f"-> Đã cài đặt thành công '{lib}'.")
        except subprocess.CalledProcessError:
            # Báo lỗi nếu cài đặt không thành công
            print(f"LỖI: Không thể tự động cài đặt thư viện '{lib}'.")
            print(f"Vui lòng mở Command Prompt (cmd) hoặc Terminal và chạy lệnh sau:")
            print(f"pip install {lib}")
            sys.exit(1) # Thoát chương trình nếu không cài được thư viện quan trọng

print("Tất cả thư viện cần thiết đã sẵn sàng!\n")
# --- KẾT THÚC PHẦN KIỂM TRA THƯ VIỆN ---

# --- PHẦN MÃ BOT NGUYÊN BẢN BẮT ĐẦU TỪ ĐÂY ---
den = "\033[1;90m"
luc = "\033[1;32m"
trang = "\033[1;37m"
red = "\033[1;31m"
vang = "\033[1;33m"
tim = "\033[1;35m"
lamd = "\033[1;34m"
lam = "\033[1;36m"
purple = "\e[35m"
hong = "\033[1;95m"

thanh_xau= red + "[" + trang+ "=.=" + red + "] " + trang + "=> "
thanh_dep= red + "[" + trang+ "=.=" + red + "] " + trang + "=> "

from pystyle import Add, Center, Anime, Colors, Colorate, Write, System
import requests, json
from sys import platform
from time import sleep
from datetime import datetime
from time import strftime

# Khai báo biến toàn cục ở đây
total = 0
may = 'mb' if platform[0:3] == 'lin' else 'pc'
follow_error_count = 0 # Biến đếm lỗi follow chung liên tiếp
unfollow_detected_count = 0 # Biến đếm "Nhả follow" liên tiếp
MAX_FOLLOW_ERRORS = 5 # Giới hạn lỗi follow chung
MAX_UNFOLLOW_DETECTED = 5 # Giới hạn "Nhả follow" liên tiếp

# Import the send_follow_request function from follow_like.py
try:
    from follow_like import send_follow_request
except ImportError:
    print(f"{red}Lỗi: Không thể nhập 'send_follow_request' từ 'follow_like.py'. "
          f"Vui lòng đảm bảo 'follow_like.py' nằm cùng thư mục.{trang}")
    sys.exit(1)

def banner():
    os.system("cls" if os.name == "nt" else "clear")
    banner = f"""
TOOL TDS Tiktok
"""
    for X in banner:
        sys.stdout.write(X)
        sys.stdout.flush()
        sleep(0.00125)

def bongoc(so):
    for i in range(so):
        print(red+'────', end = '' )
    print('')

class TraoDoiSub_Api (object):
    def __init__ (self, token):
        self.token = token

    def main(self):
        try:
            main = requests.get('https://traodoisub.com/api/?fields=profile&access_token='+self.token).json()
            try:
                return main['data']
            except:
                return False
        except:
            return False
    def run(self, user):
        try:
            run = requests.get(f'https://traodoisub.com/api/?fields=tiktok_run&id={user}&access_token={self.token}').json()
            try:
                return run['data']
            except:
                return False
        except:
            return False
    #tiktok_like, tiktok_follow
    def get_job(self, type):
        try:
            get = requests.get(f'https://traodoisub.com/api/?fields={type}&access_token={self.token}')
            return get
        except:
            return False

    def cache(self, id, type):
        try:
            cache = requests.get(f'https://traodoisub.com/api/coin/?type={type}&id={id}&access_token={self.token}').json()
            try:
                cache['cache']
                return True
            except:
                return False
        except:
            return False

    def nhan_xu(self, id, type):
        try:
            nhan = requests.get(f'https://traodoisub.com/api/coin/?type={type}&id={id}&access_token={self.token}')
            try:
                xu = nhan.json()['data']['xu']
                msg = nhan.json()['data']['msg']
                job = nhan.json()['data']['job_success']
                xuthem = nhan.json()['data']['xu_them']
                global total
                total+=xuthem
                bongoc(14)
                print(f'{lam}Nhận Thành Công {job} Nhiệm Vụ {red}| {luc}{msg} {red}| {luc}TOTAL {vang}{total} {luc}Xu {red}| {vang}{xu} ')
                bongoc(14)
                if job == 0:
                    return 0
            except:
                if '"code":"error","msg"' in nhan.text:
                    hien = nhan.json()['msg']; print(red+hien, end = '\r'); sleep(2); print(' '*len(hien), end = '\r')
                else:
                    print(red+'Nhận Xu Thất Bại !', end = '\r'); sleep(2); print('                                                       ', end = '\r')
                return False
        except:
            print(red+'Nhận Xu Thất Bại !', end = '\r'); sleep(2); print('                                                       ', end = '\r')
            return False

def delay(dl):
    try:
        for i in range(dl, -1, -1):
            print(f'{vang}[{trang}Mango{vang}][{trang}'+str(i)+vang+']           ',end='\r')
            sleep(1)
    except:
        sleep(dl)
        print(dl,end='\r')

def chuyen(link, may):
    global follow_error_count
    global unfollow_detected_count

    if may == 'mb':
        os.system(f'xdg-open "{link}"')
    else:
        os.system(f'cmd /c start "{link}"')

    print(f"{vang}Đang chờ 3 giây sau khi mở liên kết...{trang}", end='\r')
    sleep(3)
    print("                                                              ", end='\r')

    if "tiktok.com" in link or "tiktoknow://" in link:
        follow_result = send_follow_request()
        if follow_result == "Nhả follow":
            unfollow_detected_count += 1
            follow_error_count = 0
            print(f"{red}Nhả follow! Liên tiếp: {unfollow_detected_count}/{MAX_UNFOLLOW_DETECTED}{trang}")
            if unfollow_detected_count >= MAX_UNFOLLOW_DETECTED:
                print(f"{red}Đã phát hiện nhả follow {MAX_UNFOLLOW_DETECTED} lần liên tiếp. Dừng bot.{trang}")
                sys.exit(1)
        elif follow_result == "Follow ok":
            print(f"{luc}Follow ok!{trang}")
            follow_error_count = 0
            unfollow_detected_count = 0
        elif isinstance(follow_result, str) and follow_result.startswith("Error:"):
            follow_error_count += 1
            unfollow_detected_count = 0
            print(f"{red}Yêu cầu follow thất bại (Lỗi chung): {follow_result}. Liên tiếp: {follow_error_count}/{MAX_FOLLOW_ERRORS}{trang}")
            if follow_error_count >= MAX_FOLLOW_ERRORS:
                print(f"{red}Đã đạt số lỗi follow liên tiếp tối đa ({MAX_FOLLOW_ERRORS}). Dừng bot.{trang}")
                sys.exit(1)
        else:
            follow_error_count += 1
            unfollow_detected_count = 0
            print(f"{red}Yêu cầu follow thất bại (Phản hồi không rõ): {follow_result}. Liên tiếp: {follow_error_count}/{MAX_FOLLOW_ERRORS}{trang}")
            if follow_error_count >= MAX_FOLLOW_ERRORS:
                print(f"{red}Đã đạt số lỗi follow liên tiếp tối đa ({MAX_FOLLOW_ERRORS}). Dừng bot.{trang}")
                sys.exit(1)

def main():
    dem=0
    global follow_error_count
    global unfollow_detected_count
    banner()

    # Đọc token và username từ file tk.txt
    if not os.path.exists('tk.txt'):
        print(f"{red}Lỗi: File 'tk.txt' không tồn tại. Vui lòng tạo file với định dạng: username<tab>token{trang}")
        sys.exit(1)
    
    with open('tk.txt', 'r') as f:
        line = f.readline().strip()
        try:
            user_cau_hinh, token = line.split('\t')
        except ValueError:
            print(f"{red}Lỗi: File 'tk.txt' không đúng định dạng. Cần chứa username và token, phân cách bởi dấu tab.{trang}")
            sys.exit(1)

    tds = TraoDoiSub_Api(token)
    data = tds.main()
    try:
        xu = data['xu']
        xudie = data['xudie']
        user = data['user']
        print(lam+'Đăng Nhập Thành Công ')
    except:
        print(red+'Access Token Không Hợp Lệ! Vui lòng kiểm tra file tk.txt')
        sys.exit(1)

    bongoc(14)
    banner()
    print(f'{thanh_xau}{luc}Tên Tài Khoản: {vang}{user} ')
    print(f'{thanh_xau}{luc}Xu Hiện Tại: {vang}{xu}')
    print(f'{thanh_xau}{luc}Xu Bị Phạt: {vang}{xudie} ')

    # Cài đặt mặc định
    nhiem_vu = '2'  # Tự động chọn nhiệm vụ Follow
    nv_nhan = 8     # Sau 8 job thì nhận xu
    dl = 6         # Thời gian delay là 6 giây

    print(f'{thanh_xau}{luc}Nhiệm Vụ Đã Chọn Mặc Định: {vang}Follow')
    print(f'{thanh_xau}{luc}Sau {vang}{nv_nhan} {luc}Nhiệm Vụ Thì Nhận Xu')
    print(f'{thanh_xau}{luc}Thời Gian Delay Mặc Định: {vang}{dl} {luc}Giây')
    bongoc(14)

    while True:
        ntool=0
        cau_hinh=tds.run(user_cau_hinh)
        if cau_hinh != False:
            user=cau_hinh['uniqueID']
            id_acc=cau_hinh['id']
            bongoc(14)
            print(f'{luc}Đang Cấu Hình ID: {vang}{id_acc} {red}| {luc}User: {vang}{user} {red}| ')
            bongoc(14)
        else:
            print(f'{red}Cấu Hình Thất Bại User: {vang}{user_cau_hinh} ')
            sys.exit(1)

        while True:
            if ntool==1 or ntool==2:break
            # Nhiệm vụ Follow (chính)
            if '2' in nhiem_vu:
                listfollow = tds.get_job('tiktok_follow')
                if listfollow == False:
                    print(red+'Không Get Được Nhiệm Vụ Follow              ', end = '\r');sleep(2); print('                                                        ', end = '\r')
                elif 'error' in listfollow.text:
                    if listfollow.json()['error'] == 'Thao tác quá nhanh vui lòng chậm lại':
                        coun = listfollow.json()['countdown']
                        print(red+f'Đang Get Nhiệm Vụ Follow, chờ: {str(round(coun, 3))} giây... ', end = '\r'); sleep(coun); print(' ' * 60, end = '\r')
                    elif listfollow.json()['error'] == 'Vui lòng ấn NHẬN TẤT CẢ rồi sau đó tiếp tục làm nhiệm vụ để tránh lỗi!':
                        nhan = tds.nhan_xu('TIKTOK_FOLLOW_API', 'TIKTOK_FOLLOW')
                    else:
                        print(red+listfollow.json()['error'] , end ='\r');sleep(2); print('                                                        ', end = '\r')
                else:
                    try:
                        listfollow = listfollow.json()['data']
                    except:
                        print(red+'Hết Nhiệm Vụ Follow                             ', end = '\r');sleep(2); print('                                                        ', end = '\r')
                        continue
                    if len(listfollow) == 0:
                        print(red+'Hết Nhiệm Vụ Follow                             ', end = '\r');sleep(2); print('                                                        ', end = '\r')
                    else:
                        print(luc+f'Tìm Thấy {vang}{len(listfollow)} {luc}Nhiệm Vụ Follow                       ', end = '\r');sleep(2); print('                                                        ', end = '\r')
                        for i in listfollow:
                            id = i['id']
                            link = i['link']
                            chuyen(link, may)
                            cache = tds.cache(id, 'TIKTOK_FOLLOW_CACHE')
                            if cache != True:
                                tg=datetime.now().strftime('%H:%M:%S')
                                hien = f'{vang}[{red}X{vang}] {red}| {lam}{tg} {red}| {vang}FOLLOW {red}| {trang}{id} {red}|'; print(hien, end = '\r');sleep(1); print('                                                                                        ', end = '\r')
                            else:
                                dem+=1
                                tg=datetime.now().strftime('%H:%M:%S')
                                print(f'{vang}[{trang}{dem}{vang}] {red}| {lam}{tg} {red}| {Colorate.Horizontal(Colors.yellow_to_red, "FOLLOW")} {red}| {trang}{id} {red}|')
                                delay(dl)
                                if dem % nv_nhan == 0:
                                    nhan = tds.nhan_xu('TIKTOK_FOLLOW_API', 'TIKTOK_FOLLOW')
                                    if nhan == 0:
                                        print(f'{vang}Nhận xu thất bại. Thử lại sau 5 giây...{trang}')
                                        sleep(5)
                                        nhan = tds.nhan_xu('TIKTOK_FOLLOW_API', 'TIKTOK_FOLLOW')
                                        if nhan == 0:
                                            print(luc+'Nhận xu thất bại lần 2. Acc Tiktok của bạn ổn chứ?')
                                            print(f'{thanh_xau}{luc}Tự động tiếp tục sau 2 giây...')
                                            sleep(2)
                                            chon = ''
                                            if chon == '1':
                                                ntool=2
                                                break
                                            elif chon =='2':
                                                ntool = 1
                                                break
                                            bongoc(14)
            if ntool==1 or ntool==2:break
            # Nhiệm vụ Follow Tiktok Now
            if '3' in nhiem_vu:
                listfollow = tds.get_job('tiktok_follow')
                if listfollow == False:
                    print(red+'Không Get Được Nhiệm Vụ Follow              ', end = '\r');sleep(2); print('                                                        ', end = '\r')
                elif 'error' in listfollow.text:
                    if listfollow.json()['error'] == 'Thao tác quá nhanh vui lòng chậm lại':
                        coun = listfollow.json()['countdown']
                        print(f'{red}Đang Get Nhiệm Vụ Follow Tiktok Now, chờ: {str(round(coun, 3))} giây... ', end = '\r'); sleep(coun); print(' ' * 60, end = '\r')
                    elif listfollow.json()['error'] == 'Vui lòng ấn NHẬN TẤT CẢ rồi sau đó tiếp tục làm nhiệm vụ để tránh lỗi!':
                        nhan = tds.nhan_xu('TIKTOK_FOLLOW_API', 'TIKTOK_FOLLOW')
                    else:
                        print(red+listfollow.json()['error'] , end ='\r');sleep(2); print('                                                        ', end = '\r')
                else:
                    try:
                        listfollow = listfollow.json()['data']
                    except:
                        print(red+'Hết Nhiệm Vụ Follow                             ', end = '\r');sleep(2); print('                                                        ', end = '\r')
                        continue
                    if len(listfollow) == 0:
                        print(red+'Hết Nhiệm Vụ Follow                             ', end = '\r');sleep(2); print('                                                        ', end = '\r')
                    else:
                        print(f'{luc}Tìm Thấy {vang}{len(listfollow)} {luc}Nhiệm Vụ Follow                       ', end = '\r');sleep(2); print('                                                        ', end = '\r')
                        for i in listfollow:
                            id = i['id']
                            uid = id.split('_')[0]
                            link = i['link']
                            que = i['uniqueID']
                            if may == 'mb':
                                chuyen(f'tiktoknow://user/profile?user_id={uid}', may)
                            else:
                                chuyen(f'https://now.tiktok.com/@{que}', may)
                            cache = tds.cache(id, 'TIKTOK_FOLLOW_CACHE')
                            if cache != True:
                                tg=datetime.now().strftime('%H:%M:%S')
                                hien = f'{vang}[{red}X{vang}] {red}| {lam}{tg} {red}| {vang}FOLLOW_TIKTOK_NOW {red}| {trang}{id} {red}|'; print(hien, end = '\r');sleep(1); print('                                                                                        ', end = '\r')
                            else:
                                dem+=1
                                tg=datetime.now().strftime('%H:%M:%S')
                                print(f'{vang}[{trang}{dem}{vang}] {red}| {lam}{tg} {red}| {Colorate.Horizontal(Colors.yellow_to_red, "FOLLOW_TIKTOK_NOW")} {red}| {trang}{id} {red}|')
                                delay(dl)
                                if dem % nv_nhan == 0:
                                    nhan = tds.nhan_xu('TIKTOK_FOLLOW_API', 'TIKTOK_FOLLOW')
                                    if nhan == 0:
                                        print(f'{vang}Nhận xu thất bại. Thử lại sau 5 giây...{trang}')
                                        sleep(5)
                                        nhan = tds.nhan_xu('TIKTOK_FOLLOW_API', 'TIKTOK_FOLLOW')
                                        if nhan == 0:
                                            print(luc+'Nhận xu thất bại lần 2. Acc Tiktok của bạn ổn chứ?')
                                            print(f'{thanh_xau}{luc}Tự động tiếp tục sau 2 giây...')
                                            sleep(2)
                                            chon = ''
                                            if chon == '1':
                                                ntool=2
                                                break
                                            elif chon =='2':
                                                ntool = 1
                                                break
                                            bongoc(14)
main()
