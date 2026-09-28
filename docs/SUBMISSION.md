# Hướng dẫn nộp bài Day 13

## 1. Tên repository bài nộp

Bài nhóm dùng cấu trúc:

```text
K4-L3-DAY13-TenNhom-Monitoring-LLMOps
```

Ví dụ: `K4-L3-DAY13-TraceMasters-Monitoring-LLMOps`.

Tên viết không dấu, không khoảng trắng và ngăn cách bằng dấu `-`. Chỉ dùng tên bài cá nhân nếu Lab Coach có thông báo riêng.

## 2. Nộp ở đâu và nộp thông tin gì?

Mỗi thành viên tự nộp trên VLearn LMS/Codelabs:

1. URL repository chung của nhóm.
2. Commit SHA cuối dùng để chấm.

Deadline mặc định là 23:59:59 ngày diễn ra lab theo múi giờ Asia/Ho_Chi_Minh. Nếu có thông báo khác, dùng mốc chính thức mới nhất của Lab Coach/Key Coach.

Commit SHA phải tồn tại trên remote và chứa đầy đủ source, config, report và evidence. Các thay đổi sau deadline không được dùng để chấm nếu không có thông báo gia hạn.

## 3. Cấu trúc bắt buộc

```text
K4-L3-DAY13-TenNhom-Monitoring-LLMOps/
├── app/                         # source đã hoàn thiện
├── config/                      # dashboard, SLO, alert và challenge gốc
├── data/                        # input mẫu; không commit log chứa PII
├── docs/
│   ├── alerts.md                # runbook cho ba alert
│   └── TEAM.md                  # thành viên, vai trò và file report cá nhân
├── scripts/                     # load test, incident và validators
├── tests/                       # public tests và test bổ sung
├── submission/
│   ├── reports/
│   │   ├── GROUP_REPORT.md
│   │   ├── INDIVIDUAL_REPORT_TEMPLATE.md
│   │   └── INDIVIDUAL_MSSV_HoVaTen.md
│   └── evidence/
│       ├── README.md
│       └── các file evidence của nhóm
├── README.md
├── requirements.txt
└── .env.example
```

Mỗi thành viên phải có đúng một file `INDIVIDUAL_MSSV_HoVaTen.md`. Ví dụ: `INDIVIDUAL_123456_NguyenVanAn.md`.

## 4. Quy tắc chung cho evidence

Evidence phải chứng minh kết quả chạy trên commit SHA được nộp:

- Ảnh phải đọc được tên màn hình/panel, giá trị, time range và ID liên quan.
- Không cắt mất thông tin cần đối chiếu, nhưng phải che secret và PII.
- Dùng dữ liệu test của repo; không dùng dữ liệu thật của người dùng.
- Test/validator có thể lưu dạng ảnh `.png` hoặc output text `.txt`.
- Source, YAML, runbook và commit được dẫn bằng đường dẫn/link; không cần chụp toàn bộ code.
- Mọi đường dẫn trong report phải là đường dẫn tương đối và mở được trên GitHub.
- Không dùng evidence của nhóm khác hoặc của lớp khác.

Từ file trong `submission/reports/`, dẫn ảnh như sau:

```markdown
![Dashboard overview](../evidence/11-dashboard-overview.png)
```

Không dùng đường dẫn cục bộ như `C:\Users\...` hoặc `/home/student/...`.

## 5. Checklist evidence bắt buộc

Tên file dưới đây là gợi ý để nhóm dễ quản lý; có thể dùng tên khác nếu report dẫn đúng.

| Evidence | Nội dung phải nhìn thấy hoặc kiểm chứng được | File gợi ý |
|---|---|---|
| Test cuối | Lệnh `python -m pytest -q`, số test pass/fail | `01-pytest.png` hoặc `.txt` |
| Log validator | Kết quả cuối của `validate_logs.py`, điểm tối thiểu 80/100 | `02-log-validator.png` |
| Dashboard validator | Kết quả `validate_dashboard.py`, đủ 6/6 | `03-dashboard-validator.png` |
| Structured log | Log JSON có timestamp, event, `correlation_id`, model, env, feature và latency | `04-structured-log.png` |
| PII redaction | Input test chứa PII giả và log đầu ra đã che email/điện thoại/CCCD/thẻ | `05-pii-redaction.png` |
| Trace list | Danh sách tối thiểu 10 traces | `06-trace-list.png` |
| Trace waterfall | Một trace có root observation, retrieval và generation theo đúng quan hệ cha-con | `07-trace-waterfall.png` |
| Trace metadata | `correlation_id`, model, prompt name/version/label, token và cost; không có PII thô | `08-trace-metadata.png` |
| Prompt versions | Prompt v1/v2 và các label `baseline`, `candidate`, `production` | `09-prompt-versions.png` |
| Prompt rollback | Trạng thái trước/sau khi promote hoặc rollback `production`; kèm trace ID của hai version trong report | `10-prompt-rollback.png` |
| Dashboard runtime | Đủ 6 panel, có dữ liệu, time range, đơn vị và threshold/SLO line | `11-dashboard-overview.png` |
| Incident metric | Metric bất thường và khoảng thời gian xảy ra challenge | `12-incident-metric.png` |
| Incident log | Log line bất thường có `correlation_id` | `13-incident-log.png` |
| Incident trace | Trace có cùng `correlation_id`, thấy span gây chậm/lỗi | `14-incident-trace.png` |
| Git contribution | Commit/PR, file/hàm và artifact của từng thành viên | link trong report cá nhân |

Nếu dashboard không thể đọc rõ trong một ảnh, tách thành `11a-dashboard-latency-errors.png` và `11b-dashboard-cost-token-quality.png`.

## 6. Evidence nào không cần chụp ảnh?

Không cần screenshot các file sau vì giảng viên kiểm tra trực tiếp trên commit:

- `config/slo.yaml`;
- `config/alert_rules.yaml`;
- `docs/alerts.md`;
- source code và tests;
- `docs/TEAM.md`;
- commit/PR.

Trong `GROUP_REPORT.md` hoặc report cá nhân, hãy dẫn đúng file, section, commit hoặc PR liên quan.

## 7. Yêu cầu riêng cho incident

Evidence incident chỉ hợp lệ khi ba tín hiệu cùng chỉ về một request hoặc cùng khoảng sự cố:

```text
Metric bất thường
        ↓
Log có correlation_id
        ↓
Trace có cùng correlation_id
        ↓
Span gây ảnh hưởng
        ↓
Root cause và hành động xử lý
```

`GROUP_REPORT.md` phải ghi challenge ID, khoảng thời gian, metric cụ thể, log line/`correlation_id`, trace ID, span gây ảnh hưởng, root cause, fix action và preventive measure.

Không sửa, tự tạo hoặc lấy `config/challenge.json` từ lớp khác.

## 8. Báo cáo nhóm và báo cáo cá nhân

### Báo cáo nhóm

Cả nhóm cùng hoàn thiện một file `submission/reports/GROUP_REPORT.md`. Báo cáo này chứa:

- thành viên và vai trò;
- kết quả baseline và kết quả cuối;
- logging, PII, tracing và prompt version;
- dashboard, SLO, error budget và alerts;
- chuỗi điều tra incident;
- kết luận và hạn chế còn lại;
- đường dẫn tới toàn bộ evidence bắt buộc.

### Báo cáo cá nhân

Mỗi thành viên sao chép `INDIVIDUAL_REPORT_TEMPLATE.md` thành file riêng. Báo cáo cá nhân phải có:

- nhiệm vụ trực tiếp thực hiện;
- file/hàm đã sửa;
- commit/PR và evidence;
- input nhận từ thành viên khác và output bàn giao;
- một quyết định kỹ thuật và lý do;
- một lỗi/blocker đã xử lý;
- cách hiểu luồng Metrics → Logs → Traces;
- điều học được và phần chưa hoàn thành, nếu có.

Nội dung phải khớp `docs/TEAM.md` và lịch sử Git. Giữ nguyên file template cho các thành viên khác sử dụng.

## 9. Không được nộp

- `.env`, Langfuse secret, API key hoặc token.
- PII nguyên văn trong log, trace, screenshot hoặc report.
- `.venv/`, cache, dependency đã cài hoặc file sinh ra không phục vụ chấm.
- Evidence của nhóm/lớp khác.
- Evidence giả, ảnh đã chỉnh sửa làm sai lệch kết quả.
- `config/challenge.json` đã bị tự ý sửa.
- Ảnh dashboard trống hoặc ảnh không đọc được thông tin cần chấm.

## 10. Kiểm tra trước khi push

Chạy trên commit cuối:

```bash
python -m pytest -q
python scripts/validate_logs.py
python scripts/validate_dashboard.py
git status --short
git log -1 --oneline
```

Checklist cuối:

- [ ] Source và TODO bắt buộc đã hoàn thành.
- [ ] Test, log validator và dashboard validator có evidence.
- [ ] Có tối thiểu 10 traces, waterfall, metadata và prompt rollback.
- [ ] Dashboard đủ 6 panel; SLO/error budget và 3 alert/runbook đã hoàn thiện.
- [ ] Incident evidence nối đúng metric → log → trace.
- [ ] Có một `GROUP_REPORT.md` và một report riêng cho mỗi thành viên.
- [ ] `TEAM.md`, report cá nhân và lịch sử Git khớp nhau.
- [ ] Không có secret, PII thô hoặc evidence sai lớp.
- [ ] Tất cả link/ảnh mở được trực tiếp trên GitHub.
- [ ] Mỗi thành viên đã nộp URL repo và commit SHA cuối.
