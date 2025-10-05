import socket
import threading
import tkinter as tk
from tkinter import messagebox, scrolledtext, ttk

class ChatClientGUI:
    def __init__(self):
        self.HOST = '127.0.0.1'
        self.PORT = 5000
        self.socket = None
        self.username = ""
        
        self.root = tk.Tk()
        self.root.title("Chat Application")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        self.create_login_window()

    def create_login_window(self):
        self.login_frame = tk.Frame(self.root)
        self.login_frame.pack(expand=True)
        
        tk.Label(self.login_frame, text="Chat Application", font=("Arial", 20)).pack(pady=20)
        tk.Label(self.login_frame, text="Nhập tên của bạn:", font=("Arial", 12)).pack()
        
        self.username_entry = tk.Entry(self.login_frame, font=("Arial", 12), width=20)
        self.username_entry.pack(pady=10)
        self.username_entry.bind("<Return>", lambda e: self.connect_to_server())
        
        tk.Button(self.login_frame, text="Kết nối", command=self.connect_to_server,
                 font=("Arial", 12), bg="#4CAF50", fg="white").pack(pady=10)

    def connect_to_server(self):
        self.username = self.username_entry.get().strip()
        if not self.username:
            messagebox.showerror("Lỗi", "Vui lòng nhập tên!")
            return
        
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.HOST, self.PORT))
            self.socket.send(self.username.encode('utf-8'))
            
            self.login_frame.destroy()
            self.create_chat_window()
            
            self.receive_thread = threading.Thread(target=self.receive_messages, daemon=True)
            self.receive_thread.start()
            
        except Exception as e:
            messagebox.showerror("Lỗi kết nối", f"Không thể kết nối đến server: {str(e)}")

    def create_chat_window(self):
        self.root.title(f"Chat Application - {self.username}")
        
        # Frame chính
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Frame trái (chat)
        left_frame = tk.Frame(main_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Khu vực hiển thị tin nhắn
        tk.Label(left_frame, text="Tin nhắn:", font=("Arial", 12, "bold")).pack(anchor=tk.W)
        self.message_display = scrolledtext.ScrolledText(
            left_frame, state=tk.DISABLED, height=20, font=("Arial", 10)
        )
        self.message_display.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # cấu hình tag màu
        self.message_display.tag_configure("join", foreground="green")
        self.message_display.tag_configure("leave", foreground="red")
        self.message_display.tag_configure("whisper", foreground="purple")
        self.message_display.tag_configure("normal", foreground="black")
        
        input_frame = tk.Frame(left_frame)
        input_frame.pack(fill=tk.X, pady=(0, 5))
        
        self.message_entry = tk.Entry(input_frame, font=("Arial", 11))
        self.message_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        self.message_entry.bind("<Return>", lambda e: self.send_message())
        
        tk.Button(input_frame, text="Gửi", command=self.send_message,
                 font=("Arial", 10), bg="#2196F3", fg="white").pack(side=tk.RIGHT)
        
        # Frame phải (danh sách người dùng và lệnh)
        right_frame = tk.Frame(main_frame, width=200)
        right_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 0))
        right_frame.pack_propagate(False)
        
        # Danh sách người dùng online
        tk.Label(right_frame, text="Người dùng online:", font=("Arial", 11, "bold")).pack(anchor=tk.W)
        self.users_listbox = tk.Listbox(right_frame, height=8, font=("Arial", 9))
        self.users_listbox.pack(fill=tk.X, pady=(0, 10))
        self.users_listbox.bind("<Double-1>", self.on_user_double_click)
        
        # Nút cập nhật danh sách
        tk.Button(right_frame, text="Cập nhật danh sách", command=self.refresh_users,
                 font=("Arial", 9)).pack(fill=tk.X, pady=(0, 10))
        
        # Hướng dẫn sử dụng
        instructions_frame = tk.LabelFrame(right_frame, text="Hướng dẫn", font=("Arial", 10))
        instructions_frame.pack(fill=tk.X, pady=(0, 10))
        
       
        instructions = [
            "/quit - Thoát",
            "/users - Xem online",
            "@user tin_nhắn - Riêng tư",
            "Double-click user để chat riêng"
        ]
        
        for instruction in instructions:
            tk.Label(instructions_frame, text=instruction, font=("Arial", 8),
                    anchor=tk.W, justify=tk.LEFT).pack(fill=tk.X, padx=5, pady=1)

        
        # Nút thoát
        tk.Button(right_frame, text="Thoát", command=self.disconnect,
                 font=("Arial", 10), bg="#F44336", fg="white").pack(fill=tk.X, pady=(10, 0))
        
        # Tự động cập nhật danh sách người dùng
        self.root.after(1000, lambda: self.socket.send("/users".encode('utf-8')))

    def receive_messages(self):
        while True:
            try:
                message = self.socket.recv(1024).decode('utf-8')
                if message:
                    self.display_message(message)
                    
                    # Cập nhật danh sách người dùng nếu nhận được thông tin online
                    if message.startswith("[ONLINE]"):
                        self.update_users_list(message)
                else:
                    break
            except:
                break

    def display_message(self, message):
        tag = "normal"
        if "tham gia" in message:
            tag = "join"
        elif "rời" in message:
            tag = "leave"
        elif message.startswith("[RIÊNG TƯ") or message.startswith("[Đến"):
            tag = "whisper"

        self.message_display.config(state=tk.NORMAL)
        self.message_display.insert(tk.END, message + "\n", tag)
        self.message_display.config(state=tk.DISABLED)
        self.message_display.see(tk.END)


    def update_users_list(self, online_message):
        try:
            # Trích xuất danh sách từ "[ONLINE] Người dùng đang online: user1, user2, ..."
            users_part = online_message.split(": ")[1]
            users = [user.strip() for user in users_part.split(",") if user.strip()]
            
            self.users_listbox.delete(0, tk.END)
            for user in users:
                if user != self.username:  # Không hiển thị chính mình
                    self.users_listbox.insert(tk.END, user)
        except:
            pass

    def send_message(self):
        message = self.message_entry.get().strip()
        if not message:
            return
        
        try:
            self.socket.send(message.encode('utf-8'))
            
            # Hiển thị tin nhắn của mình (nếu không phải lệnh hoặc tin nhắn riêng tư)
            if not message.startswith('/') and not message.startswith('@'):
                self.display_message(f"{self.username}: {message}")
            
            self.message_entry.delete(0, tk.END)
            
            if message.lower() == "/quit":
                self.disconnect()
        except:
            messagebox.showerror("Lỗi", "Không thể gửi tin nhắn!")

    def on_user_double_click(self, event):
        selection = self.users_listbox.curselection()
        if selection:
            username = self.users_listbox.get(selection[0])
            self.message_entry.delete(0, tk.END)
            self.message_entry.insert(0, f"@{username} ")
            self.message_entry.focus()

    def refresh_users(self):
        try:
            self.socket.send("/users".encode('utf-8'))
        except:
            pass

    def disconnect(self):
        try:
            if self.socket:
                self.socket.send("/quit".encode('utf-8'))
                self.socket.close()
        except:
            pass
        finally:
            self.root.destroy()

    def run(self):
        self.root.protocol("WM_DELETE_WINDOW", self.disconnect)
        self.root.mainloop()

if __name__ == "__main__":
    app = ChatClientGUI()
    app.run()