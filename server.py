import socket
import threading

# Cấu hình server
HOST = '127.0.0.1'
PORT = 5000

# danh sách client
clients = {}

def broadcast(message, sender_socket):
# Gửi tin nhắn đến tất cả client (trừ người gửi)
    for client_socket in clients:
        if client_socket != sender_socket:
            try:
                client_socket.send(message.encode('utf-8'))
            except:
                client_socket.close()
                del clients[client_socket]

def send_private_message(message, target_username, sender_socket, sender_username):
    #gui tin nhan riêng
    target_socket = None
    for client_socket, username in clients.items():
        if username == target_username:
            target_socket = client_socket
            break
    
    if target_socket:
        try:
            target_socket.send(f"[RIÊNG TƯ từ {sender_username}]: {message}".encode('utf-8'))
            sender_socket.send(f"[RIÊNG TƯ đến {target_username}]: {message}".encode('utf-8'))
            return True
        except:
            target_socket.close()
            del clients[target_socket]
            return False
    else:
        sender_socket.send(f"[LỖI] Không tìm thấy người dùng '{target_username}'".encode('utf-8'))
        return False

def send_online_users(client_socket):
    # xem bao nhieu người dùng online
    user_list = list(clients.values())
    online_message = f"[ONLINE] Người dùng đang online: {', '.join(user_list)}"
    try:
        client_socket.send(online_message.encode('utf-8'))
    except:
        pass

# Xử lý từng client
def handle_client(client_socket):
    username = None
    try:
        # Nhận username từ client khi vừa kết nối
        username = client_socket.recv(1024).decode('utf-8')
        if not username:
            return
            
        clients[client_socket] = username
        print(f"[KẾT NỐI] {username} đã tham gia chat!")

        # thông báo đến tất cả mọi người
        broadcast(f"{username} đã tham gia phòng chat!", client_socket)

        while True:
            try:
                msg = client_socket.recv(1024).decode('utf-8')
                if not msg:
                    break

                # Nếu client thoát
                if msg.lower() == "/quit":
                    print(f"[THOÁT] {username} đã rời phòng chat.")
                    broadcast(f"{username} đã rời phòng chat.", client_socket)
                    break
                
                # Xem danh sách người dùng online
                elif msg.lower() == "/users" or msg.lower() == "/online":
                    send_online_users(client_socket)
                    continue
                
                # Xử lý tin nhắn riêng tư 
                elif msg.startswith('@'):
                    parts = msg.split(' ', 1)
                    if len(parts) >= 2:
                         # Bỏ ký tự '@'
                        target_username = parts[0][1:] 
                        private_message = parts[1]
                        if send_private_message(private_message, target_username, client_socket, username):
                            print(f"[RIÊNG TƯ] {username} -> {target_username}: {private_message}")
                        continue
                    else:
                        client_socket.send("[LỖI] Cú pháp: @username tin_nhắn".encode('utf-8'))
                        continue

                print(f"[{username}]: {msg}")
                broadcast(f"{username}: {msg}", client_socket)
                
            except socket.error:
                print(f"[LỖI] Mất kết nối với {username}")
                break
            except Exception as e:
                print(f"[LỖI] Lỗi khi xử lý tin nhắn từ {username}: {e}")
                break

    except socket.error:
        print(f"[LỖI] Lỗi kết nối socket")
    finally:
        # Xóa client khi mất kết nối
        if client_socket in clients:
            username = clients[client_socket]
            del clients[client_socket]
            if username:
                print(f"[NGẮT KẾT NỐI] {username} đã rời khỏi server")
                broadcast(f"{username} đã rời phòng chat.", client_socket)
        
        try:
            client_socket.close()
        except:
            pass

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Cho phép tái sử dụng địa chỉ
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        server_socket.bind((HOST, PORT))
        server_socket.listen(5)  # Tối đa 5 kết nối đang chờ
        print(f"[SERVER] Đang chạy tại {HOST}:{PORT}")
        print(f"[SERVER] Chờ kết nối từ client...")

        while True:
            try:
                client_socket, address = server_socket.accept()
                print(f"[KẾT NỐI MỚI] Từ {address[0]}:{address[1]}")
                thread = threading.Thread(target=handle_client, args=(client_socket,))
                # Thread sẽ tự động thoát khi main thread kết thúc
                thread.daemon = True  
                thread.start()
            except socket.error as e:
                print(f"[LỖI] Lỗi khi chấp nhận kết nối: {e}")
                continue
                
    except socket.error as e:
        print(f"[LỖI] Không thể khởi động server: {e}")
    except KeyboardInterrupt:
        print("\n[SERVER] Đang tắt server...")
    finally:
        server_socket.close()
        print("[SERVER] Server đã tắt.")

if __name__ == "__main__":
    start_server()
