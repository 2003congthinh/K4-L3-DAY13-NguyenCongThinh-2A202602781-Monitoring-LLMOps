# Chuẩn bị môi trường K4-L3B Day 13

Các lệnh dưới đây chạy từ thư mục gốc của repository cá nhân. Không chia sẻ `.env` với học viên khác hoặc giữa hai lớp.

## Yêu cầu

- Python 3.11 trở lên.
- Git.
- Tài khoản hoặc project Langfuse do Lab Coach cung cấp.
- Docker Desktop chỉ cần khi tự chọn chạy Langfuse local.

## 1. Tạo virtual environment

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

## 2. Cấu hình Langfuse — mặc định dùng chung/cloud

Ưu tiên project dùng chung do Lab Coach cung cấp hoặc Langfuse Cloud. Điền host và key của project vào `.env`:

```dotenv
LANGFUSE_PUBLIC_KEY=
LANGFUSE_SECRET_KEY=
LANGFUSE_BASE_URL=https://cloud.langfuse.com
LANGFUSE_PROMPT_NAME=day13-chat
LANGFUSE_PROMPT_LABEL=production
```

Không commit `.env`. Nếu chưa có key, app vẫn chạy bằng prompt local; bạn vẫn làm được log, metrics và public tests nhưng chưa có evidence trace/prompt version.

## 3. Tùy chọn: chạy Langfuse local bằng Docker Compose

Phần này không bắt buộc và không được cộng điểm riêng. Chỉ dùng khi bạn không truy cập được project chung/cloud và máy có Docker Desktop đủ tài nguyên.

Ở một thư mục nằm ngoài repo bài nộp:

```bash
git clone https://github.com/langfuse/langfuse.git langfuse-local
cd langfuse-local
docker compose up -d
```

Chờ container `langfuse-web` sẵn sàng, sau đó mở `http://localhost:3000`, tạo project và lấy public/secret key. Trong repo lab, đặt:

```dotenv
LANGFUSE_BASE_URL=http://localhost:3000
LANGFUSE_PUBLIC_KEY=pk-lf-...
LANGFUSE_SECRET_KEY=sk-lf-...
```

Khi kết thúc buổi lab, dừng stack từ thư mục `langfuse-local`:

```bash
docker compose down
```

Không dùng `docker compose down -v` nếu còn cần dữ liệu trace/prompt trong volume. Xem hướng dẫn cập nhật tại [Langfuse Docker Compose](https://langfuse.com/self-hosting/deployment/docker-compose).

## 4. Kiểm tra cài đặt

Terminal 1:

```bash
uvicorn app.main:app --reload --env-file .env
```

Terminal 2:

```bash
python scripts/load_test.py
python scripts/validate_logs.py
python scripts/validate_dashboard.py
python -m pytest -q
```

API mặc định chạy tại `http://127.0.0.1:8000`; health check ở `/health`, metrics ở `/metrics`.

## Lỗi thường gặp

- PowerShell chặn `Activate.ps1`: chạy `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` rồi activate lại.
- `ModuleNotFoundError`: kiểm tra virtual environment đã được activate và chạy lại `pip install -r requirements.txt`.
- `ModuleNotFoundError: No module named 'app'` hoặc `'scripts'` khi chạy test: dùng `python -m pytest -q` từ thư mục gốc thay vì gọi `pytest` trực tiếp.
- Không có `data/logs.jsonl`: bảo đảm API đang chạy trước khi chạy load test.
- Không thấy trace: kiểm tra ba biến `LANGFUSE_*`, sau đó khởi động lại API.
- Trace ghi `prompt_source=local-fallback`: kiểm tra host/key và prompt name/label trong `.env`.
- Docker local không lên: chạy `docker compose ps`, kiểm tra Docker Desktop và tài nguyên máy; có thể quay về project chung/cloud.
- Challenge chưa chạy: chờ Lab Coach release `config/challenge.json`.
