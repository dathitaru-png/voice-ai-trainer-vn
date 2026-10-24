# 04 — Vòng lặp huấn luyện

Vòng lặp huấn luyện trong `voicetrain.train` gồm 4 bước lặp lại:

1. **Dự đoán** — mô hình tính xác suất cho từng lớp (softmax).
2. **Đo lỗi** — hàm mất mát cross-entropy so sánh dự đoán với nhãn thật.
3. **Tính gradient** — đạo hàm của mất mát theo từng trọng số.
4. **Cập nhật** — trừ gradient nhân với tốc độ học (learning rate).

## Đọc đường cong loss

- Loss giảm đều qua các epoch: vòng lặp đang học.
- Loss giảm rồi tăng lại: có thể tốc độ học quá cao hoặc dữ liệu nhiễu.
- Loss trên tập train giảm nhưng trên tập validation tăng: **overfitting**
  — mô hình học thuộc lòng thay vì học quy luật.

## Chia tập dữ liệu

Dùng `voicetrain.dataset.split` với một seed cố định để chia train /
validation / test. Ba tập phải **không trùng nhau**, và tập test chỉ được
chạm tới một lần duy nhất, lúc đánh giá cuối cùng.

## Demo trong dự án

Demo dùng dữ liệu tổng hợp: ba lớp âm (trầm, trung, cao) tách biệt rõ
ràng theo năng lượng dải tần. Nó chứng minh vòng lặp chạy đúng, không
chứng minh mô hình nhận dạng được giọng nói thật — đừng nhầm hai việc
này với nhau.

## Tự kiểm tra

- Vì sao tốc độ học quá lớn lại làm loss dao động?
- Overfitting thì nên làm gì trước: thêm dữ liệu hay tăng mô hình?
