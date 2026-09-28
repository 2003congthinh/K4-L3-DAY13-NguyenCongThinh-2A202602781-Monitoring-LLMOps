# Hướng dẫn nộp bài Day 13

## 1 Tên repository bài nộp

Bài nhóm dùng cấu trúc:

```text
K4-L3-DAY13-TenNhom-Monitoring-LLMOps
```

Ví dụ: `K4-L3-DAY13-TraceMasters-Monitoring-LLMOps`.

Nếu Lab Coach chỉ định bài cá nhân, dùng:

```text
K4-L3-DAY13-HoVaTen-MSSV-Monitoring-LLMOps
```

Tên viết không dấu, không khoảng trắng và ngăn cách bằng dấu `-`.

## 2 Nơi nộp và deadline

- Mỗi cá nhân nộp URL repo nhóm và commit SHA cuối trên VLearn LMS/Codelabs.
- Deadline mặc định: 23:59:59 ngày diễn ra lab, múi giờ Asia/Ho_Chi_Minh.
- Nếu có thông báo khác, dùng mốc chính thức mới nhất của Lab Coach/Key Coach.

## 3 Cấu trúc bắt buộc

```text
K4-L3-DAY13-TenNhom-Monitoring-LLMOps/
├── app/                       # source đã hoàn thiện
├── config/                    # schema, dashboard, SLO, alert, challenge gốc
├── data/                      # input mẫu; không commit log chứa PII
├── docs/
│   ├── alerts.md              # runbook cho ba alert đã điền
│   ├── CHECKPOINTS.md
│   ├── RUBRIC.md
│   ├── RULES.md
│   ├── SUBMISSION.md
│   └── TEAM.md
├── scripts/                   # load test, incident, validators
├── tests/                     # public tests và test bổ sung
├── submission/
│   ├── reports/
│   │   ├── GROUP_REPORT.md
│   │   ├── INDIVIDUAL_REPORT_TEMPLATE.md
│   │   └── INDIVIDUAL_MSSV_HoVaTen.md  # một file cho mỗi thành viên
│   └── evidence/
├── README.md
├── requirements.txt
└── .env.example
```

## 4 Evidence bắt buộc

- Kết quả cuối của `validate_logs.py`.
- Danh sách tối thiểu 10 traces và một trace waterfall.
- Hai prompt version, hai trace gắn đúng version/label và một bằng chứng rollback.
- Log có correlation ID và metadata.
- Bằng chứng PII đã được redact.
- Kết quả dashboard validator và ảnh dashboard đủ sáu nhóm chỉ số.
- SLO, alert rules và runbook.
- Điều tra challenge gồm challenge ID, metric, log/correlation ID, trace ID, root cause, fix và preventive measure.
- `TEAM.md`, báo cáo cá nhân và commit/PR của từng thành viên.

## 5 Quy tắc báo cáo nhóm và cá nhân

- Cả nhóm cùng hoàn thiện **một** file `submission/reports/GROUP_REPORT.md` cho kết quả chung, dashboard, SLO/alert và incident.
- Mỗi thành viên sao chép `INDIVIDUAL_REPORT_TEMPLATE.md` thành `INDIVIDUAL_MSSV_HoVaTen.md` trong cùng thư mục `submission/reports/`.
- Báo cáo cá nhân phải nêu phần trực tiếp thực hiện, commit/PR, evidence, quyết định kỹ thuật, blocker và bài học; nội dung phải khớp lịch sử Git.
- Không sửa hoặc xóa file template để thành viên khác vẫn có thể sử dụng.

## 6 Không được nộp

- `.env`, secret, token, `.venv/`, cache hoặc dependency đã cài.
- Log/screenshot chứa PII chưa che.
- Evidence của nhóm/lớp khác.
- `config/challenge.json` đã bị tự ý sửa.
- File lớn hoặc generated artifact không phục vụ việc chấm.

## 7 Kiểm tra trước khi push

```powershell
python -m pytest -q
python scripts/validate_logs.py
python scripts/validate_dashboard.py
git status --short
git log -1 --oneline
```

Sau khi push, kiểm tra repo clone được, commit SHA tồn tại, đủ một báo cáo nhóm và một báo cáo cho mỗi thành viên, và mọi đường dẫn evidence mở được.
