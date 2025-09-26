# Chat Application - Hướng dẫn sử dụng

## Tổng quan
Ứng dụng chat đa người dùng được phát triển bằng Python với socket và threading. Ứng dụng bao gồm:
- **server.py**: Server xử lý kết nối và tin nhắn
- **client.py**: Client dạng command line 
- **client_gui.py**: Client với giao diện đồ họa (tkinter)

## Tính năng đã triển khai

### ✅ Tính năng cơ bản
- Kết nối nhiều client đồng thời
- Chat công khai (broadcast)
- Thông báo người dùng tham gia/rời khỏi
- Xử lý ngắt kết nối đột ngột

### ✅ Tính năng nâng cao
- **Tin nhắn riêng tư**: `@username tin_nhắn`
- **Xem danh sách online**: `/users` hoặc `/online`
- **Thoát**: `/quit`
- **Giao diện đồ họa** với tkinter

## Cách chạy ứng dụng

### 1. Khởi động Server
```bash
python server.py
```

### 2. Khởi động Client (Command Line)
```bash
python client.py
```

### 3. Khởi động Client (GUI)
```bash
python client_gui.py
```

## Các lệnh sử dụng

| Lệnh | Mô tả |
|------|-------|
| `@username tin_nhắn` | Gửi tin nhắn riêng tư |
| `/users` hoặc `/online` | Xem danh sách người dùng online |
| `/quit` | Thoát khỏi chat |

## Giao diện GUI

Client GUI cung cấp:
- **Khu vực chat**: Hiển thị tất cả tin nhắn
- **Ô nhập liệu**: Nhập và gửi tin nhắn
- **Danh sách online**: Hiển thị người dùng đang online
- **Double-click user**: Tự động tạo tin nhắn riêng tư
- **Các nút tiện ích**: Cập nhật danh sách, thoát

## Kiểm thử

Để kiểm thử ứng dụng:
1. Chạy server
2. Mở nhiều terminal/cửa sổ để chạy nhiều client
3. Test các tính năng:
   - Chat công khai
   - Tin nhắn riêng tư
   - Xem danh sách online
   - Thoát và vào lại

## Cấu trúc mã nguồn

```
rooom/
├── server.py          # Server chính
├── client.py          # Client command line
├── client_gui.py      # Client GUI với tkinter
└── README.md          # Tài liệu này
```

## Đánh giá so với yêu cầu đồ án

| Yêu cầu | Trạng thái |
|---------|------------|
| Server cơ bản (socket, threading) | ✅ Hoàn thành |
| Client cơ bản (kết nối, chat) | ✅ Hoàn thành |
| Tin nhắn riêng tư | ✅ Hoàn thành |
| Giao diện đồ họa (tkinter) | ✅ Hoàn thành |
| Xử lý kết nối/ngắt kết nối | ✅ Hoàn thành |
| Danh sách người dùng online | ✅ Hoàn thành |

**Tỷ lệ hoàn thành: 100%** 🎉

## Lưu ý kỹ thuật

- Server hỗ trợ tối đa 5 kết nối đồng thời đang chờ
- Sử dụng daemon threads để tự động cleanup
- Error handling toàn diện cho network errors
- Socket reuse để tránh lỗi "Address already in use"
- GUI responsive với threading riêng biệt cho network operations