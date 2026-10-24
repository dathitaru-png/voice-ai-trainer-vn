# 01 — Pipeline đào tạo Voice AI: tổng quan

Đào tạo một mô hình giọng nói gồm 5 chặng, và chặng nào làm ẩu thì chặng
sau cũng hỏng theo:

1. **Dữ liệu** — thu âm, kiểm tra chất lượng, viết bản ghi (transcript).
2. **Chuẩn hoá** — đưa transcript về một dạng thống nhất (xem bài 02).
3. **Đặc trưng** — biến sóng âm thành số mà mô hình học được (xem bài 03).
4. **Huấn luyện** — vòng lặp tối ưu hàm mất mát trên tập train, kiểm tra
   trên tập validation (xem bài 04).
5. **Đánh giá** — đo WER/CER trên tập test chưa từng thấy (xem bài 05).

Mã nguồn tương ứng trong VoiceTrainer VN:

- Dữ liệu và manifest: `voicetrain.dataset`, `voicetrain.audio`
- Chuẩn hoá: `voicetrain.textnorm`
- Đặc trưng: `voicetrain.features`
- Huấn luyện: `voicetrain.train`
- Đánh giá: `voicetrain.eval`

## Tự kiểm tra

- Vì sao không được đánh giá mô hình trên chính dữ liệu đã train?
- Nếu transcript có chỗ viết "2", chỗ viết "hai", mô hình sẽ học gì?
