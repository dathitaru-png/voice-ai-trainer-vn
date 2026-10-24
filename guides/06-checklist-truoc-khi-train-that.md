# 06 — Checklist trước khi train thật

Trước khi đưa dữ liệu thật vào huấn luyện, kiểm tra từng mục sau:

## Dữ liệu

- [ ] Mọi file WAV mở được, đúng sample rate và số kênh đã định.
- [ ] `voicetrain validate` báo 0 vấn đề trên toàn bộ manifest.
- [ ] Transcript đã chuẩn hoá bằng cùng một quy tắc (xem bài 02).
- [ ] Tập train / validation / test không trùng nhau, chia bằng seed cố định.
- [ ] Đã nghe thử ngẫu nhiên vài mẫu để phát hiện file hỏng, nhiễu,
      hoặc transcript sai.

## Quyền và pháp lý

- [ ] Có sự đồng ý rõ ràng của mọi người nói cho mục đích huấn luyện.
- [ ] Biết rõ giấy phép của mọi nguồn dữ liệu bên ngoài.
- [ ] Không đưa dữ liệu giọng nói thật vào kho mã nguồn công khai.
- [ ] Có quy trình xoá dữ liệu khi người nói rút lại sự đồng ý.

## Tài nguyên và kỳ vọng

- [ ] Ước tính thời gian train và dung lượng lưu trữ trước khi chạy.
- [ ] Đặt baseline đơn giản trước (ví dụ: mô hình nhỏ, ít epoch) rồi
      mới mở rộng.
- [ ] Ghi lại seed, siêu tham số, và phiên bản dữ liệu cho mỗi lần chạy,
      để kết quả có thể tái lập.
- [ ] Nhớ rằng WER tốt trên tập test của mình chưa chắc đã tốt ngoài
      đời thật: giọng, micro, và môi trường đều khác nhau.
