# Test Grade Calculator
*Giới thiệu*: Đây là 1 chương trình đơn giản để tính toán và phân tích điểm bài thi trắc nghiệm. Đối với mỗi lớp học giáo viên cần chấm bài, sẽ có 1 file `.txt` tương ứng có tên của lớp học đó, nội dung bên trong chứa mã sinh viên và câu trả lời tương ứng của từng sinh viên. 

Chương trình sẽ kiểm tra format của mã sinh viên và tổng số câu trả lời có hợp lệ hay không. Đối với những bài hợp lệ, chương trình sẽ chấm điểm dựa trên đáp án đã có sẵn (*answer_key*), tính toán điểm *cao nhất*, *thấp nhất* và *điểm trung bình* của cả lớp. Sau đó, chương trình sẽ export số điểm đã chấm vào thưc mục `Output`, tên file sẽ tương ứng với tên của lớp.

Ngoài ra, người dùng có thể lựa chọn chấm từng lớp, hoặc chấm toàn bộ các lớp đã có dữ liệu trong thư mục input (`Data Files`). 

## 1. Cài đặt và chạy chương trình
- Cài đặt các package phụ thuộc:

    `pip install -r requirements.txt`

- Chạy chương trình và làm theo hướng dẫn:

    `python lastname_firstname_grade_the_exams.py`

## 2. Giới thiệu về chương trình:
**_class lastname_firstname_grade_the_exams.TestGradeCalculator()_**

Class `TestGradeCalculator` sẽ đảm nhận thực hiện toàn bộ chức năng của chương trình. Để bắt đầu, khởi tạo 1 instance của `TestGradeCalculator` rồi gọi method `grade()` để thực hiện các bước tiếp theo.

### grade()
Method chính thực hiện chức năng của chương trình. Mục đích của method này là đóng vai trò làm wrapper cho các method `user_input()` (lấy input từ thư mục dữ liệu) và `execute_grading()` (thực hiện các chức năng chính sau khi đã có input).

### user_input()
Nhận yêu cầu từ người dùng. Người dùng có thể nhập `class1` để chọn 1 lớp, hoặc `all` để chọn tất cả các lớp đang có sẵn trong thư mục dữ liệu. Xử lý lỗi trong trường hợp người dùng nhập sai tên.  

#### **Returns:**

**file : str**

### execute_grading(files)
Wrapper cho các method chức năng chính, bao bồm `select_class()`, `check_valid()`, `score()`, `output_to_file()` và `reset_data()`.
#### **Parameters:**
**files : list-like**

Danh sách các file mà chương trình sẽ chạy.

### select_class(file)
Mở file trùng tên với lớp học đang được chấm điểm. Đọc và lưu danh sách học viên.
#### **Parameters:**
**file : str**

### check_valid()
Đối với danh sách của các học viên đã lưu, duyệt qua từng học viên để kiểm tra mã sinh viên hợp lệ và số câu trả lời hợp lệ. Trường hợp nào không hợp lệ sẽ thông báo lý do ra màn hình. 

Đối với những trường hợp hợp lệ, lưu thông tin của học viên vào 1 dataframe để chấm điểm.
### score()
Chấm điểm từng học viên dựa bằng cách so sánh với đáp án mẫu (*answer_key*). In ra màn hình các thông số cơ bản: *điểm cao nhất*, *điểm thấp nhất*, *điểm trung bình*, *điểm median*, *range của điểm*.
### output_to_file()
Lưu điểm đã chấm của học viên vào thư mục `output`, tên file sẽ tương ứng với tên của lớp. 
### reset_data()
Reset lại dataframe đang dùng để chứa thông tin của học viên. 
### calculate_score(answer)
Method hỗ trợ. So sánh câu trả lời của học viên với đáp án, cộng 4 điểm đối với câu trả lời đúng và trừ 1 điểm đối với những câu trả lời sai.
