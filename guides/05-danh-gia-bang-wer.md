# 05 — Đánh giá bằng WER và CER

## WER là gì

Word Error Rate = (thay thế + xoá + thêm) / số từ trong bản ghi chuẩn.
Ví dụ: chuẩn "a b c", mô hình đoán "a c" thì thiếu một từ, WER = 1/3.

WER = 0 nghĩa là khớp hoàn toàn. WER có thể vượt 1 nếu mô hình thêm
nhiều từ thừa.

## CER là gì

Character Error Rate làm tương tự ở cấp ký tự, sau khi bỏ khoảng trắng.
CER hữu ích khi mô hình sai chính tả nhưng vẫn gần đúng từ.

## Đọc lỗi đúng cách

- **Thay thế** nhiều: mô hình nhầm âm tương tự nhau.
- **Xoá** nhiều: mô hình bỏ sót từ, thường do nói nhanh hoặc tiếng nhỏ.
- **Thêm** nhiều: mô hình "nghe ra" từ không có thật, thường do nhiễu.

Dùng `voicetrain.eval.per_utterance_report` để xem lỗi từng câu, đừng
chỉ nhìn một con số trung bình.

## Cạm bẫy thường gặp

- Đánh giá trên dữ liệu đã train: số đẹp nhưng vô nghĩa.
- Chuẩn hoá khác nhau giữa bản ghi chuẩn và bản đoán: "2" và "hai" sẽ
  bị tính là lỗi dù cùng một nghĩa. Luôn chuẩn hoá cả hai phía bằng
  cùng một hàm (`voicetrain.textnorm.normalize`).
- So sánh WER giữa hai bộ dữ liệu khác nhau: không có ý nghĩa.

## Tự kiểm tra

- Chuẩn "xin chào", đoán "xin chao" thì WER và CER là bao nhiêu?
- Vì sao WER có thể lớn hơn 1?
