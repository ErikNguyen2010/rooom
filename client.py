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
        msg = input()
        if msg.lower() == "/quit":
            sock.send(msg.encode('utf-8'))
            print("Bạn đã thoát khỏi chat.")
            break

        # Gửi tin nhắn kèm nội dung
        sock.send(msg.encode('utf-8'))

        # Hiển thị lại tin nhắn mình vừa gửi với username
        print(f"{username}: {msg}")

# Khởi chạy client
def start_client():
    username = input("Nhập tên của bạn: ")

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))

    # Gửi username lên server ngay sau khi kết nối
    sock.send(username.encode('utf-8'))

    print("Kết nối thành công tới server! Gõ '/quit' để thoát.")

    # Thread nhận tin nhắn
    thread_receive = threading.Thread(target=receive_messages, args=(sock,))
    thread_receive.start()

    # Thread gửi tin nhắn
    send_messages(sock, username)

    sock.close()

if __name__ == "__main__":
    start_client()
