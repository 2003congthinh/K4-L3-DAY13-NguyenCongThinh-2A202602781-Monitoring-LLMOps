# K4-L3B — Lab Day 13: Monitoring & LLMOps

> **Loại repository:** đề bài/starter dành riêng cho lớp K4-L3B  
> **Hình thức làm bài:** nhóm 3–5 học viên  
> **Thời lượng trên lớp:** khoảng 120 phút  
> **Deadline mặc định:** 23:59:59 trong ngày học, múi giờ Asia/Ho_Chi_Minh

Bạn sẽ biến một AI API “hộp đen” thành hệ thống có thể trả lời ba câu hỏi: **hệ thống có vấn đề gì, request nào bị ảnh hưởng và bước nào là nguyên nhân**. Quy trình điều tra đúng theo slide là **Metrics → Logs → Traces**:

1. Metrics cho biết triệu chứng và khoảng thời gian.
2. Logs giúp tìm request cụ thể qua `correlation_id`.
3. Trace của request đó cho biết span nào chậm hoặc lỗi.

Repo dùng fake LLM nên không cần API key mô hình trả phí. Langfuse dùng để quan sát trace và quản lý prompt version.

## Kết quả cần đạt

Sau lab, nhóm có thể:

- tạo structured log dạng JSON, truyền correlation ID và che PII trước khi ghi log;
- đo latency P50/P95/P99, TTFT, traffic, error, token, cost, retrieval success và quality proxy;
- tạo ít nhất 10 traces trên Langfuse, có span tree đọc được và metadata không chứa PII;
- liên kết trace với prompt name/label/version và chứng minh được một lần rollback;
- dựng dashboard 6 panel, định nghĩa một SLO cùng error budget và ba alert có runbook;
- viết incident note có chuỗi bằng chứng metric → log → trace.

## Sản phẩm phải nộp

- Source đã hoàn thiện các `TODO` bắt buộc.
- `submission/REPORT.md` đã điền và evidence đặt trong `submission/evidence/`.
- `docs/TEAM.md` ghi đúng thành viên, vai trò, commit/PR và phần học được.
- Kết quả tests, log validator và dashboard validator trên commit cuối.
- Ảnh dashboard có dữ liệu; ít nhất 10 trace IDs; một trace waterfall; prompt v1/v2 và evidence rollback.
- Một SLO/error budget, ba alert symptom-based có `duration`, kênh Slack và runbook.

## Bắt đầu nhanh

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
```

macOS/Linux:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
cp .env.example .env
```

Điền project Langfuse do Lab Coach cung cấp vào `.env`:

```dotenv
LANGFUSE_PUBLIC_KEY=pk-lf-...
LANGFUSE_SECRET_KEY=sk-lf-...
LANGFUSE_BASE_URL=https://cloud.langfuse.com
LANGFUSE_PROMPT_NAME=day13-chat
LANGFUSE_PROMPT_LABEL=production
```

Chạy API ở terminal thứ nhất:

```bash
uvicorn app.main:app --reload --env-file .env
```

Chạy baseline ở terminal thứ hai:

```bash
python scripts/load_test.py
python scripts/validate_logs.py
python scripts/validate_dashboard.py
python -m pytest -q
```

Baseline log chưa đạt là bình thường vì các `TODO` của CP1 chưa được làm. Ghi lại kết quả baseline vào report trước khi sửa.

## Lộ trình 120 phút

| Mốc | Thời gian | Việc chính | Hoàn thành khi |
|---|---:|---|---|
| CP0 | 0–15 phút | Setup, chạy API và baseline | `/health` trả `ok: true`, log được tạo |
| CP1 | 15–40 phút | Correlation ID, structured log, PII | `validate_logs.py` đạt ít nhất 80/100 |
| CP2 | 40–80 phút | Trace, prompt, dashboard, SLO/alert | có span tree; dashboard validator đạt 6/6 |
| CP3 | 80–105 phút | Điều tra challenge K4-L3B | có metric, log và trace cùng một request |
| CP4 | 105–120 phút | Report, evidence và kiểm tra cuối | tests/validators chạy xong trên commit nộp |

Chi tiết từng checkpoint nằm trong [docs/CHECKPOINTS.md](docs/CHECKPOINTS.md).

## Các phần cần làm

### CP1 — Logging và PII

- `app/middleware.py`: xóa context cũ; nhận `x-request-id` hoặc sinh `req-<8-hex>`; bind ID; trả ID và response time trong header.
- `app/main.py`: bind `user_id_hash`, `session_id`, `feature`, `model`, `env` trước log `request_received`.
- `app/logging_config.py`: chạy PII scrubber trước bước ghi file/render JSON.
- `app/pii.py`: hoàn thiện pattern và tests cho email, điện thoại Việt Nam, CCCD và thẻ thanh toán.

`validate_logs.py` đọc toàn bộ `data/logs.jsonl`. Sau khi lưu baseline, hãy xóa hoặc đổi tên log cũ, khởi động lại API rồi đo lại để không bị tính các dòng chưa scrub.

### CP2 — Tracing, prompt và dashboard

Starter dùng Langfuse Python SDK v4 và mới tạo root observation cho `LabAgent.run`. Nhóm cần thêm child observation cho:

- retrieval: loại `retriever` hoặc `span`;
- LLM call: loại `generation`, có model, prompt, `input_tokens`, `output_tokens` và cost.

Không capture raw prompt/output chứa PII. Correlation ID phải xuất hiện trong trace metadata để nối trace với log.

Dashboard dùng `data/logs.jsonl` làm nguồn chuẩn và giữ đúng 6 panel trong `config/dashboard.yaml`. Panel latency phải có P50/P95/P99 và TTFT; panel errors phải thể hiện cả retrieval success. Sau đó hoàn thiện:

- `config/slo.yaml`: giải thích hoặc điều chỉnh SLO, tính error budget;
- `config/alert_rules.yaml`: ba alert symptom-based, có duration, severity, owner, Slack channel và runbook;
- `docs/alerts.md`: cách kiểm tra và mitigation cho từng alert.

### CP3 — Challenge chính thức

Chỉ chạy khi Lab Coach thông báo mở challenge của K4-L3B:

```bash
python scripts/inject_incident.py
python scripts/load_test.py --challenge --concurrency 5
```

Điều tra theo thứ tự:

1. Xem dashboard để xác định metric xấu và khoảng thời gian.
2. Lọc `data/logs.jsonl`, lấy một `correlation_id` của request bất thường.
3. Tìm trace có cùng `correlation_id`, rồi so sánh các span.
4. Ghi root cause, fix action và preventive measure vào report.

Không sửa, thay thế hoặc lấy `config/challenge.json` từ lớp khác.

## Kiểm tra trước khi nộp

```bash
python -m pytest -q
python scripts/validate_logs.py
python scripts/validate_dashboard.py
git status --short
git log -1 --oneline
```

- [ ] Không có `.env`, secret, `.venv/`, PII thô hoặc evidence của nhóm khác.
- [ ] Mọi ảnh trong report dùng đường dẫn tương đối và mở được.
- [ ] Mỗi thành viên có đóng góp kỹ thuật kiểm chứng được.
- [ ] Nhóm demo được luồng Metrics → Logs → Traces → Root cause.

## Tên repo bài nộp

Repo này là **repo đề bài**, nên tên chính thức là `K4-L3B-Day13-Monitoring-LLMOps` (mẫu `K4-L3B-TenBai`). Repo bài nộp của nhóm dùng mẫu:

```text
K4-L3-DAY13-TenNhom-Monitoring-LLMOps
```

Ví dụ: `K4-L3-DAY13-TraceMasters-Monitoring-LLMOps`. Mỗi thành viên nộp URL của repo nhóm và commit SHA cuối trên VLearn LMS/Codelabs. Xem đầy đủ tại [docs/SUBMISSION.md](docs/SUBMISSION.md).

## Tài liệu trong repo

- [SETUP.md](docs/SETUP.md): cài đặt và xử lý lỗi môi trường.
- [CHECKPOINTS.md](docs/CHECKPOINTS.md): đầu ra và cách tự kiểm tra từng mốc.
- [GUIDE.md](docs/GUIDE.md): gợi ý kỹ thuật khi bị kẹt.
- [PROMPT_VERSIONING.md](docs/PROMPT_VERSIONING.md): prompt v1/v2, label và rollback.
- [DASHBOARD_SETUP.md](docs/DASHBOARD_SETUP.md): mapping dữ liệu cho 6 panel.
- [RUBRIC.md](docs/RUBRIC.md), [RULES.md](docs/RULES.md), [SUBMISSION.md](docs/SUBMISSION.md): cách chấm, quy định và cách nộp.
