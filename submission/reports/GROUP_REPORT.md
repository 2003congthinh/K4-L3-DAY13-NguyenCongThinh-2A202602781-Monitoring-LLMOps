# Báo cáo nhóm — K4-L3B Day 13 Monitoring & LLMOps

> Đây là báo cáo chung của cả nhóm. Chỉ nộp **một file** này cho mỗi nhóm.
> Khi dẫn evidence, dùng đường dẫn tương đối từ file này, ví dụ `../evidence/dashboard.png`.

## 1. Thông tin nhóm

- **Tên nhóm:**
- **Lớp:** K4-L3B
- **Repository URL:**
- **Commit SHA cuối:**
- **Challenge ID:**

| Họ và tên | MSSV | Vai trò chính | File báo cáo cá nhân |
|---|---|---|---|
| | | | `INDIVIDUAL_MSSV_HoVaTen.md` |

### Evidence index

Điền đường dẫn tương đối tới evidence thực tế của nhóm. Có thể dùng nhiều ảnh cho một mục nếu cần.

| Evidence | Đường dẫn |
|---|---|
| Pytest cuối | `../evidence/01-pytest.png` |
| Log validator | `../evidence/02-log-validator.png` |
| Dashboard validator | `../evidence/03-dashboard-validator.png` |
| Structured log | `../evidence/04-structured-log.png` |
| PII redaction | `../evidence/05-pii-redaction.png` |
| Trace list | `../evidence/06-trace-list.png` |
| Trace waterfall | `../evidence/07-trace-waterfall.png` |
| Trace metadata | `../evidence/08-trace-metadata.png` |
| Prompt versions | `../evidence/09-prompt-versions.png` |
| Prompt rollback | `../evidence/10-prompt-rollback.png` |
| Dashboard runtime | `../evidence/11-dashboard-overview.png` |
| Incident metric | `../evidence/12-incident-metric.png` |
| Incident log | `../evidence/13-incident-log.png` |
| Incident trace | `../evidence/14-incident-trace.png` |

## 2. Kết quả kỹ thuật

| Nội dung | Baseline | Kết quả cuối | Evidence |
|---|---|---|---|
| `validate_logs.py` | | | |
| `validate_dashboard.py` | | | |
| `pytest` | | | |
| Số traces hợp lệ | | | |
| Số PII leak | | | |
| Latency P95 / TTFT P95 | | | |
| Retrieval success rate | | | |

## 3. Logging và tracing

- **Cách truyền correlation ID:**
- **Evidence correlation ID:**
- **Cách redact PII:**
- **Evidence PII redaction:**
- **Evidence trace waterfall:**
- **Giải thích một span đáng chú ý:**

## 4. Prompt versioning

- **Prompt name:**
- **Version/label baseline:**
- **Version/label candidate:**
- **Trace ID của mỗi version:**
- **Bằng chứng promote/rollback:**

## 5. Dashboard, SLO và alerts

- **Evidence dashboard đủ 6 panel:**
- **SLO và lý do chọn:**
- **Error budget:**
- **Ba alert và runbook tương ứng:**

## 6. Điều tra challenge

- **Challenge ID:**
- **Khoảng thời gian điều tra:**
- **Triệu chứng từ metrics:**
- **Log line và correlation ID liên quan:**
- **Trace ID liên quan:**
- **Root cause:**
- **Fix action:**
- **Preventive measure:**

## 7. Kết luận của nhóm

- **Nhóm đã hoàn thành:**
- **Hạn chế còn lại:**
- **Bài học chính về Metrics → Logs → Traces:**

## 8. Checklist trước khi nộp

- [ ] Các số liệu trong báo cáo được lấy từ commit SHA cuối.
- [ ] Mọi evidence dùng đường dẫn tương đối và mở được.
- [ ] Mỗi thành viên có đúng một báo cáo cá nhân trong thư mục này.
- [ ] Phân công khớp `docs/TEAM.md` và lịch sử Git.
- [ ] Không có secret, API key hoặc PII thô.
