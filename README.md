# manim-decribe-world

Đồ án Lab 1 môn Machine Learning, xây dựng bằng Manim để minh họa các ý tưởng về world model, embodied AGI và các kịch bản liên quan đến học máy qua video ngắn.

## Thông tin nhóm
|MSSV|Họ Tên|
|---|---|
|23120146|Hoàng Ngọc|
|23120165|Lê Đức Thành|
|23120173|Khổng Đức Tiến|

## Thông tin môn học
- Lớp: CQ2023/21
- Môn: Nhập môn học máy
- Mã môn: CSC14005


## Mục lục
- [Tổng quan](#tong-quan)
- [Cấu trúc dự án](#cau-truc-du-an)
- [Yêu cầu](#yeu-cau)
- [Cách cài đặt](#cach-cai-dat)
- [Cách chạy](#cach-chay)
- [Ghi chú](#ghi-chu)

## Tổng quan
Dự án gồm nhiều scene Manim được chia theo từng chủ đề:
- `topic1`: Scaling Foundation World Models as a Path to Embodied AGI.
- `topic2`: Physics-Grounded World Models: Generation, Interaction, and Evaluation.
- `topic3`: Breaking the Algorithmic Ceiling in Pre-Training with an Inference-first Perspective.

## Cấu trúc dự án
- `assets/`: tài nguyên dùng trong video, bao gồm âm thanh và dữ liệu phụ trợ.
- `src/manim.cfg`: cấu hình Manim mặc định của dự án.
- `src/topic1/`: các scene chính của chủ đề 1 và script render hàng loạt.
- `src/topic2/`: các scene thuộc chủ đề 2.
- `src/topic3/`: các scene thuộc chủ đề 3.
- `requirements.txt`: danh sách thư viện cần cài.

## Yêu cầu
- Python
- Manim
- `manim-voiceover`
- `azure-cognitiveservices-speech`

## Cách cài đặt
Tạo môi trường ảo và cài thư viện từ thư mục gốc của dự án:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Cách chạy
Vì cấu hình Manim nằm trong `src/`, hãy chuyển vào thư mục này trước khi render:

```powershell
Set-Location src
```

Render một scene riêng lẻ:

```powershell
manim -qm topic1/scene_01_hook.py Scene01Hook
```

Render toàn bộ Topic 1 bằng script có sẵn:

```powershell
powershell -ExecutionPolicy Bypass -File topic1/render_all.ps1
```

Nếu `manim` không có trong `PATH`, có thể chạy theo cách sau:

```powershell
..\.venv\Scripts\python.exe -m manim -qm topic1/scene_01_hook.py Scene01Hook
```

## Ghi chú
- Ảnh, âm thanh và tài nguyên phụ trợ nên được truy cập bằng đường dẫn tương đối từ thư mục `assets/`.
- Cấu hình mặc định của dự án đang dùng chất lượng trung bình để render nhanh hơn.
- Video xuất ra sẽ nằm trong thư mục `media/` của Manim.
