import socket
import threading

# Cấu hình server
HOST = '127.0.0.1'
PORT = 5000

# Nhận tin nhắn từ server
def receive_messages(sock):
    while True:
        try:
            message = sock.recv(1024).decode('utf-8')
            if message:
                print(message)
            else:
                print("Mất kết nối tới server.")
                break
        except:
            print("Lỗi khi nhận dữ liệu từ server.")
            break

# Gửi tin nhắn lên server
def send_messages(sock, username):
    while True:
        try:
            msg = input()
            if msg.lower() == "/quit":
                sock.send(msg.encode('utf-8'))
                print("Bạn đã thoát khỏi chat.")
                break

            # Gửi tin nhắn kèm nội dung
            sock.send(msg.encode('utf-8'))

            # Chỉ hiển thị lại tin nhắn công khai (không phải lệnh hoặc tin nhắn riêng tư)
            if not msg.startswith('/') and not msg.startswith('@'):
                print(f"{username}: {msg}")
        except:
            print("Lỗi khi gửi tin nhắn!")
            break

# Khởi chạy client
def start_client():
    username = input("Nhập tên của bạn: ")

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((HOST, PORT))
    except:
        print("Không thể kết nối đến server!")
        return

    # Gửi username lên server ngay sau khi kết nối
    sock.send(username.encode('utf-8'))

    print("Kết nối thành công tới server!")
    print("Các lệnh có sẵn:")
    print("  /quit - Thoát khỏi chat")
    print("  /users hoặc /online - Xem danh sách người dùng online")
    print("  @username tin_nhắn - Gửi tin nhắn riêng tư")
    print("-" * 50)

    # Thread nhận tin nhắn
    thread_receive = threading.Thread(target=receive_messages, args=(sock,))
    thread_receive.daemon = True  # Đảm bảo thread tự động thoát khi main thread kết thúc
    thread_receive.start()

    # Thread gửi tin nhắn
    send_messages(sock, username)

    sock.close()

if __name__ == "__main__":
    start_client()
