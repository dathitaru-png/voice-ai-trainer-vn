# 02 — Thu thập và chuẩn hoá dữ liệu

## Thu âm

- Ưu tiên 16 kHz, mono, 16-bit cho nhận dạng tiếng nói; cao hơn tốn
  dung lượng mà ít cải thiện độ chính xác.
- Ghi âm ở nơi yên tĩnh, giữ khoảng cách micro ổn định, tránh tiếng
  vọng và tiếng quạt.
- Luôn xin phép và ghi rõ sự đồng ý của người nói trước khi dùng giọng
  của họ để huấn luyện (xem bài 06).

## Manifest

Mỗi dòng trong manifest JSONL là một cặp âm thanh + bản ghi:

```json
{"audio": "data/utt_001.wav", "transcript": "xin chào mọi người", "duration": 1.2}
```

Dùng `voicetrain validate manifest.jsonl` để kiểm tra file tồn tại,
thời lượng trong khoảng cho phép, và transcript không rỗng.

## Quy tắc bản ghi

- Viết thường toàn bộ, dấu câu thống nhất: không khoảng trắng trước dấu
  câu, một khoảng trắng sau dấu câu.
- Số viết thành chữ: `2` thành `hai`, `21` thành `hai mươi mốt`
  (xem `voicetrain.textnorm.number_to_words`).
- Không bao giờ tẩy dấu tiếng Việt: "đào" và "dao" là hai từ khác nhau.

## Tự kiểm tra

- Vì sao manifest tách riêng khỏi file âm thanh lại dễ kiểm tra hơn?
- Một bản ghi dài 0,2 giây hoặc 90 giây nên xử lý thế nào?
