# 03 — Đặc trưng âm thanh

Mô hình không "nghe" sóng âm trực tiếp; nó học trên các con số rút ra
từ sóng âm, gọi là đặc trưng. VoiceTrainer VN dùng ba đặc trưng cơ bản
trong `voicetrain.features`:

## Khung (frame)

Âm thanh được cắt thành các khung ngắn (ví dụ 256 mẫu, khoảng 32 ms ở
8 kHz). Mọi đặc trưng đều tính trên từng khung, vì giọng nói thay đổi
theo thời gian.

## Năng lượng khung (frame energy)

Trung bình bình phương biên độ. Khung im lặng có năng lượng gần 0, khung
có tiếng nói có năng lượng cao. Dùng để phát hiện đoạn im lặng.

## Tỷ lệ qua zero (zero-crossing rate)

Tỷ lệ cặp mẫu liên tiếp đổi dấu. Tín hiệu tần số cao hoặc nhiễu đổi dấu
nhiều hơn. Đây là một dấu hiệu rẻ tiền để phân biệt tiếng nói với tạp âm.

## Phổ và năng lượng theo dải tần

Phép biến đổi Fourier rời rạc (DFT) cho biết năng lượng phân bố theo tần
số. `band_energies` cộng dồn năng lượng vào các dải tần, ví dụ trầm /
trung / cao. Một âm thuần 440 Hz dồn năng lượng vào dải trầm — đó chính
là cách bài kiểm tra của dự án xác minh tính đúng đắn của DFT.

Trong hệ thống thật, người ta dùng MFCC hoặc log-mel, nhưng nguyên lý
giống nhau: biến sóng âm thành vector số giữ lại thông tin phân biệt.

## Tự kiểm tra

- Vì sao năng lượng khung cao chưa chắc đã là tiếng nói?
- Một khung toàn số 0 có phổ như thế nào?
