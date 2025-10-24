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