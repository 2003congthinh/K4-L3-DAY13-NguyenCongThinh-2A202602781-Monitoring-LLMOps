# Gợi ý làm bài

## Khi log thiếu correlation ID

Theo dõi một request từ middleware đến response. Kiểm tra context có được xóa trước request mới, gán vào logger và trả lại trong response header hay chưa.

## Khi log thiếu metadata

Xác định metadata nào thuộc toàn request và metadata nào chỉ xuất hiện sau khi agent chạy xong. Bind context trước dòng `request_received` để các log sau dùng chung context.

## Khi còn PII trong log

Kiểm tra thứ tự processor: dữ liệu phải được scrub trước khi JSON được render và ghi xuống file. Thử với email, số điện thoại và số thẻ mẫu.

## Khi đã sửa code nhưng validator vẫn báo lỗi cũ

`validate_logs.py` đọc toàn bộ `data/logs.jsonl`, kể cả các dòng ghi từ trước khi sửa code. Lưu kết quả baseline làm evidence, sau đó xóa hoặc đổi tên file log, khởi động lại API và chạy lại load test trước khi đo.

## Khi trace chỉ có một observation

Starter code chỉ gắn `@observe` cho `LabAgent.run`, nên waterfall chưa tách được thời gian retrieval và LLM. Với Langfuse Python SDK v4, thêm child observation loại `retriever`/`span` cho `retrieve` và loại `generation` cho `FakeLLM.generate`; generation phải có model, prompt, usage và cost. Không có child observation thì không khoanh vùng được bước chậm ở CP3.

## Khi metrics báo xấu nhưng chưa biết nguyên nhân

1. Dùng metrics xác định khoảng thời gian và loại triệu chứng.
2. Lọc log trong khoảng đó và lấy correlation ID của request bất thường.
3. Tìm trace có cùng correlation ID.
4. So sánh thời gian và trạng thái các span.
5. Chỉ kết luận khi evidence khớp ở cả ba lớp.

## Khi dashboard khó đọc

Mỗi panel cần tên, đơn vị, khoảng thời gian và threshold. Ưu tiên 6 panel chính thay vì thêm nhiều biểu đồ không phục vụ quyết định.

Chạy `python scripts/validate_dashboard.py` trước. Nếu validator qua nhưng dashboard vẫn sai, đối chiếu từng event/field với bảng trong [DASHBOARD_SETUP.md](DASHBOARD_SETUP.md), đặc biệt `response_sent.latency_ms` và `response_sent.quality_score`.

## Khi prompt luôn hiện `local-v1`

1. Kiểm tra `LANGFUSE_PUBLIC_KEY`, `LANGFUSE_SECRET_KEY` và `LANGFUSE_BASE_URL`.
2. Kiểm tra prompt name/label trong `.env` có tồn tại trên đúng project không.
3. Khởi động lại API sau khi đổi `.env`.
4. Mở trace metadata: `prompt_source=local` nghĩa là chưa bật Langfuse; `local-fallback` nghĩa là đã bật nhưng fetch prompt lỗi.

Không sửa code để ghi giả version. Làm theo [PROMPT_VERSIONING.md](PROMPT_VERSIONING.md) và lấy trace thật làm evidence.
