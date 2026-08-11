# Báo cáo Day 13 Observability

## 1. Thông tin nhóm

- Tên nhóm:
- Repository URL:
- Commit SHA cuối:
- Thành viên và vai trò:

## 2. Kết quả kỹ thuật

- Điểm `validate_logs.py`:
- Tổng số traces:
- Số PII leak còn lại:
- Link/đường dẫn dashboard:

## 3. Logging và tracing

- Evidence correlation ID:
- Evidence PII redaction:
- Evidence trace waterfall:
- Giải thích một span đáng chú ý:

## 4. Prompt versioning

- Prompt name:
- Version/label baseline:
- Version/label candidate:
- Trace ID của mỗi version:
- Bằng chứng đổi label hoặc rollback:

## 5. Dashboard, SLO và alerts

- Kết quả `validate_dashboard.py`:
- Evidence dashboard:
- SLO đã chọn và lý do:
- Alert rules và runbook:

## 6. Điều tra challenge

- Challenge ID: day13-k3-observability-v1
- Triệu chứng từ metrics: Đỉnh độ trễ (latency spike) tăng mạnh đột biến. Chỉ số P95 Latency vượt xa mức 2 giây đối với tính năng `refund`.
- Trace ID liên quan: req-252f0f66
- Log line/correlation ID liên quan: req-252f0f66
- Root cause: Hệ thống RAG (Retrieval-Augmented Generation) phản hồi rất chậm. Hàm `retrieve` bên trong `app/mock_rag.py` tốn quá nhiều thời gian gây nghẽn toàn bộ luồng xử lý (Do kịch bản sự cố `rag_slow`).
- Fix action: Khởi động lại service, tối ưu hoá vector database hoặc thêm timeout giới hạn thời gian chờ cho RAG retrieval. (Trong Lab: Tắt incident bằng cờ `--disable`).
- Preventive measure: Thiết lập Alert tự động cho chỉ số `latency_p95` (rule `high_latency_p95`). Áp dụng cơ chế Caching (bộ nhớ đệm) để trả về ngay kết quả cho các câu hỏi trùng lặp mà không cần gọi RAG. Lắp Circuit Breaker để ngắt mạch khi vector store phản hồi chậm.
## 7. Đóng góp cá nhân

Với mỗi thành viên, ghi rõ nhiệm vụ và link commit/PR tương ứng.

| Thành viên | Phần việc | Commit/PR | Điều đã học |
|---|---|---|---|
| | | | |
