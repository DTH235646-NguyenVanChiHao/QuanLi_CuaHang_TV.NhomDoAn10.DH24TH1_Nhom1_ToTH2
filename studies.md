# QuanLi_CuaHang_TV.NhomDoAn10.DH24TH1_Nhom1_ToTH2




#Download

- customtkinter

- messagebox <- Tkinter

- pip install Pillow

- pip install pyodbc
- pip install tkcalendar => import DateEntry


//Lỗi này xảy ra vì bạn đang sử dụng %s (của MySQL) thay vì ? (của SQL Server/pyodbc). Dưới đây là code sửa lỗi:

There isn't do - while in python => using while true: instead


🧨 2. Không bao giờ gọi mainloop() trong CTkToplevel

mainloop() chỉ được gọi một lần duy nhất trong toàn ứng dụng (ở cửa sổ chính).
Gọi add_product_window.mainloop() bên trong khiến vòng lặp Tkinter chạy lặp thêm tầng mới → gây lỗi rối loạn tài nguyên và binding.


🔹 Quy tắc 3: Dùng sticky để canh lề

sticky cho phép căn vị trí trong ô (giống text alignment).

Code	Kết quả
sticky="w"	Căn trái (west)
sticky="e"	Căn phải (east)
sticky="nsew"	Kéo giãn cả 4 hướng (fill toàn ô)


#bản chất của subform và cách hoạt động của main loop


#Kiểm tra đối tượng trước khi thêm vào db

#có cách nào để không tắt db khi đang sửe dụng cho đến khi tắt không
#nên tắt hay nên mở db khi sử dụng sẽ tối ưu hơn

#sửa tên cho đúng

#sửa vnd -> lên cột thay vì để ở phần giá trị được lưu



# What did I learn from this project

# Tuple () => using ? sẽ tự động thêm '' và không phân biệt hoa thường - chữ có dấu 

⚠️ Nguyên nhân chính

Trong Python, khi bạn truyền một giá trị duy nhất vào tuple mà không có dấu phẩy (,),
thì Python không hiểu đó là tuple, mà chỉ là một giá trị đơn lẻ.

➡️ Nghĩa là dòng trên thực ra không phải tuple — nên pyodbc nhận sai kiểu dữ liệu, khiến SQL Server không hiểu đúng cú pháp.

✅ Cách sửa đúng

Thêm dấu phẩy (,) để tạo tuple thực sự có 1 phần tử:

self.cursor.execute(query, (filter_value,))

Câu hỏi rất hay — và câu trả lời là:
👉 Có, pyodbc tự động thêm dấu nháy đơn ' ' xung quanh giá trị (kể cả có khoảng trắng hoặc ký tự đặc biệt), khi bạn dùng câu truy vấn có tham số ? đúng cách.


#Mặc định của sql server : là hoa hay thường
🧩 1. Mặc định trong SQL Server

Trong hầu hết cơ sở dữ liệu SQL Server, các bảng hoặc cột được tạo với collation mặc định là không phân biệt hoa thường (case-insensitive).

SQL_Latin1_General_CP1_CI_AS
Trong đó:

CI = Case Insensitive → không phân biệt hoa thường.

AS = Accent Sensitive → có phân biệt dấu tiếng Việt.

# phủ định giá trị  => using global

        self.false = not self.false
        ascending = self.false


#create event => onchange

# Nghiene cuuws autofill voi auto complete in entry


#trace_ad

Hàm trace_add() yêu cầu một con trỏ đến hàm (function reference),
không phải kết quả của hàm đó.

❌ self.on_text_change(column=...) → gọi ngay, chạy một lần, trả về None

✅ lambda *args: self.on_text_change(column=...) → chưa gọi, chỉ chạy khi có thay đổi

#db

📘 Tóm lại
Nguyên nhân	Hướng xử lý
Gọi db.conn.close() trong sự kiện đang lặp	❌ Sai
Đóng connection sau mỗi truy vấn	❌ Sai
Đóng connection khi app thoát	✅ Đúng
Mở connection một lần, dùng lại nhiều lần	✅ Đúng

%A → nghĩa là: kết thúc bằng chữ A

A% → nghĩa là: bắt đầu bằng chữ A

%A% → nghĩa là: chứa chữ A ở bất kỳ vị trí nào


# to refresh anywhere => create refresh_data()


# day 
today_str = date.today().strftime('%Y-%m-%d')


# get value from pages

app -> pages[] = new page() 

app = self 

app.pages[your required page].properties.properties