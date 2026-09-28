# Evidence dùng để chấm bài

Danh sách chính thức, quy tắc chụp và cách nộp nằm tại [SUBMISSION.md](SUBMISSION.md). File này là checklist nhanh khi nhóm thu thập evidence.

## Evidence runtime bắt buộc

- [ ] Kết quả cuối của `python -m pytest -q`.
- [ ] `validate_logs.py` đạt tối thiểu 80/100.
- [ ] `validate_dashboard.py` đạt 6/6.
- [ ] Structured log có `correlation_id` và metadata.
- [ ] PII giả đã được redact trong output thực tế.
- [ ] Danh sách tối thiểu 10 traces.
- [ ] Một trace waterfall có root, retrieval và generation.
- [ ] Trace metadata có correlation ID, prompt version/label, token và cost.
- [ ] Prompt v1/v2 và bằng chứng promote/rollback.
- [ ] Dashboard runtime đủ 6 panel, time range, đơn vị và threshold.
- [ ] Incident metric, incident log và incident trace nối được bằng cùng correlation ID/khoảng sự cố.

## Artifact kiểm tra trực tiếp trên repo

Không cần chụp toàn bộ code. Dẫn link tới:

- `config/slo.yaml` và phần giải thích error budget trong group report;
- `config/alert_rules.yaml` và `docs/alerts.md`;
- source, tests và commit/PR;
- `docs/TEAM.md`;
- group report và report cá nhân.

## Chất lượng evidence

- Evidence phải thuộc commit SHA được nộp và đúng challenge của lớp.
- Ảnh phải đọc được thông tin dùng để chấm, không phải ảnh trang trống.
- Che secret và PII; không dùng dữ liệu thật.
- Đặt file trong `submission/evidence/`.
- Dẫn đường dẫn tương đối từ report, ví dụ `../evidence/07-trace-waterfall.png`.
- Metric, log và trace của incident phải cùng chỉ về một nguyên nhân.
