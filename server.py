import socket
import threading

# Cấu hình server
HOST = '127.0.0.1'
PORT = 5000

# Danh sách client (socket -> username)
clients = {}

# Gửi tin nhắn đến tất cả client (trừ người gửi)
def broadcast(message, sender_socket):
    for client_socket in clients:
        if client_socket != sender_socket:
            try:
                client_socket.send(message.encode('utf-8'))
            except:
                client_socket.close()
                del clients[client_socket]

# Xử lý từng client
def handle_client(client_socket):
    try:
        # Nhận username từ client khi vừa kết nối
        username = client_socket.recv(1024).decode('utf-8')
        clients[client_socket] = username
        print(f"[KẾT NỐI] {username} đã tham gia chat!")

        # Thông báo đến tất cả mọi người
        broadcast(f"{username} đã tham gia phòng chat!", client_socket)

        while True:
            msg = client_socket.recv(1024).decode('utf-8')
            if not msg:
                break

            # Nếu client thoát
            if msg.lower() == "/quit":
                print(f"[THOÁT] {username} đã rời phòng chat.")
                broadcast(f"{username} đã rời phòng chat.", client_socket)
                break

            print(f"[{username}]: {msg}")
            broadcast(f"{username}: {msg}", client_socket)

    except:
        pass
    finally:
        # Xóa client khi mất kết nối
        if client_socket in clients:
            del clients[client_socket]
        client_socket.close()

# Khởi chạy server
def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen()

    print(f"[SERVER] Đang chạy tại {HOST}:{PORT}")

    while True:
        client_socket, address = server_socket.accept()
        thread = threading.Thread(target=handle_client, args=(client_socket,))
        thread.start()

if __name__ == "__main__":
    start_server()
