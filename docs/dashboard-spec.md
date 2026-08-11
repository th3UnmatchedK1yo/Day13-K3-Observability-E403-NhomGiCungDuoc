# Yêu cầu dashboard

Contract có thể kiểm tra bằng máy nằm tại `config/dashboard.yaml`. Hướng dẫn dựng và kiểm tra runtime nằm tại [DASHBOARD_SETUP.md](DASHBOARD_SETUP.md).

Dashboard chính bao gồm 6 nhóm thông tin sau, được thiết lập bằng Langfuse Dashboard (hoặc Grafana):

### 1. Latency (Thời gian phản hồi)
- **Tên panel:** Latency percentiles
- **Đơn vị:** ms (milliseconds)
- **Khoảng thời gian mặc định:** 1 giờ
- **Ngưỡng (Threshold / SLO line):** P95 <= 3000ms
- **Công cụ sử dụng:** Langfuse Dashboard

### 2. Traffic (Lưu lượng truy cập)
- **Tên panel:** Request traffic
- **Đơn vị:** requests_per_minute (QPS)
- **Khoảng thời gian mặc định:** 1 giờ
- **Ngưỡng (Threshold / SLO line):** >= 1 (có request)
- **Công cụ sử dụng:** Langfuse Dashboard

### 3. Error (Tỷ lệ lỗi)
- **Tên panel:** Error rate and breakdown
- **Đơn vị:** phần trăm (%)
- **Khoảng thời gian mặc định:** 1 giờ
- **Ngưỡng (Threshold / SLO line):** Error rate <= 2%
- **Công cụ sử dụng:** Langfuse Dashboard

### 4. Cost (Chi phí)
- **Tên panel:** Cost over time
- **Đơn vị:** USD
- **Khoảng thời gian mặc định:** 1 giờ
- **Ngưỡng (Threshold / SLO line):** Total <= 2.5 USD
- **Công cụ sử dụng:** Langfuse Dashboard

### 5. Tokens (Sử dụng Token)
- **Tên panel:** Input and output tokens
- **Đơn vị:** tokens
- **Khoảng thời gian mặc định:** 1 giờ
- **Ngưỡng (Threshold / SLO line):** Total <= 50,000 tokens
- **Công cụ sử dụng:** Langfuse Dashboard

### 6. Quality (Chất lượng phản hồi)
- **Tên panel:** Quality proxy
- **Đơn vị:** score (từ 0 đến 1)
- **Khoảng thời gian mặc định:** 1 giờ
- **Ngưỡng (Threshold / SLO line):** >= 0.75
- **Công cụ sử dụng:** Langfuse Dashboard

Tiêu chuẩn trình bày chung:
- Khoảng thời gian mặc định: 1 giờ.
- Tự refresh mỗi 30 giây.
- Chỉ giữ 6 panel quan trọng ở lớp chính.

Kiểm tra contract trước khi chụp evidence:

```bash
python scripts/validate_dashboard.py
```
