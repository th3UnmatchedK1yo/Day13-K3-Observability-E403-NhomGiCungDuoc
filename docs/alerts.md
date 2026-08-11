# Template Alert và Runbook

Mỗi alert phải dựa trên triệu chứng người dùng hoặc SLO, không dựa trực tiếp vào tên implementation nội bộ.

## Alert 1: high_latency_p95

- **Tên:** high_latency_p95
- **Severity:** warning
- **SLI/SLO liên quan:** latency_p95_ms (Mục tiêu: < 3000ms cho 99.5% request)
- **Điều kiện và thời gian duy trì:** latency_p95 > 3000ms duy trì liên tục trong 5 phút.
- **Ảnh hưởng tới người dùng:** Người dùng cảm thấy ứng dụng chat bị chậm đáng kể, làm giảm trải nghiệm và có thể dẫn đến việc rời bỏ ứng dụng.
- **Ba bước kiểm tra đầu tiên:**
  1. Mở Langfuse Dashboard xem biểu đồ độ trễ để xác nhận xu hướng tăng đột biến.
  2. Xem trace chi tiết trong Langfuse (waterfall) để tìm ra span (chẳng hạn RAG hay LLM) đang tốn nhiều thời gian nhất.
  3. Kiểm tra logs hệ thống bằng Correlation ID của các request chậm để xem có timeout hay deadlock nào không.
- **Mitigation tạm thời:** Mở rộng (scale up) số lượng instance của service bị nghẽn hoặc giảm độ phức tạp của context đưa vào LLM để nhận kết quả nhanh hơn.
- **Owner:** on-call-engineer

## Alert 2: elevated_error_rate

- **Tên:** elevated_error_rate
- **Severity:** critical
- **SLI/SLO liên quan:** error_rate_pct (Mục tiêu: < 2% cho 99% request)
- **Điều kiện và thời gian duy trì:** error_rate_pct > 5% duy trì liên tục trong 3 phút.
- **Ảnh hưởng tới người dùng:** Người dùng thường xuyên nhận được thông báo lỗi, không thể hoàn thành đoạn chat, ảnh hưởng nghiêm trọng đến luồng công việc.
- **Ba bước kiểm tra đầu tiên:**
  1. Kiểm tra bảng `error_breakdown` trên Dashboard để xem loại lỗi phổ biến nhất (ví dụ: `TimeoutError`, `AuthenticationError`, `LLMRateLimit`).
  2. Dùng Correlation ID truy vết các request bị 500 lỗi để đọc chi tiết exception trong logs JSON.
  3. Kiểm tra trạng thái của các API bên thứ 3 (như OpenAI, Langfuse) có đang bị gián đoạn (outage) hay không.
- **Mitigation tạm thời:** Nếu API bên thứ 3 bị lỗi, có thể bật cờ fallback sang model LLM khác, hoặc áp dụng circuit breaker. Nếu nguyên nhân từ server, khởi động lại instance lỗi hoặc rollback bản deploy mới nhất.
- **Owner:** on-call-engineer

## Alert 3: cost_budget_exceeded

- **Tên:** cost_budget_exceeded
- **Severity:** warning
- **SLI/SLO liên quan:** daily_cost_usd (Mục tiêu: < 2.5 USD / ngày)
- **Điều kiện và thời gian duy trì:** daily_cost_usd > 2.5 USD
- **Ảnh hưởng tới người dùng:** Không ảnh hưởng trực tiếp đến người dùng, nhưng ảnh hưởng đến lợi nhuận và ngân sách của dự án/công ty.
- **Ba bước kiểm tra đầu tiên:**
  1. Kiểm tra Dashboard chỉ số `Tokens` để xác định liệu cost tăng do lượng tokens quá lớn hay lượng traffic tăng đột biến.
  2. Xác định mô hình (model) nào đang ngốn chi phí nhiều nhất bằng thẻ tags trong Langfuse.
  3. Kiểm tra có sự tấn công DDoS hay lạm dụng API từ một nhóm người dùng cố định hay không.
- **Mitigation tạm thời:** Tạm thời giới hạn lượng context tối đa đẩy vào LLM, hoặc điều phối chuyển sang model rẻ hơn (ví dụ chuyển từ Sonnet-3.5 sang Haiku) trong giờ cao điểm. Áp dụng rate limiting chặt hơn với người dùng.
- **Owner:** team-lead
