'''
Source: https://www.youtube.com/watch?v=0ndJEnL3hNU&t=29s

Yêu câu 
  - Custom lại giao diện đăng nhập cho đẹp
  - thêm database để phân quyền : User Admin 
  - ..
'''

import customtkinter as ctk
from tkinter import messagebox  # có thể thay bằng CTkMessagebox nếu bạn cài thêm lib đó

class LoginPage:
    def __init__(self, root, on_login_success):
        """
        root: cửa sổ CTk chính
        on_login_success: hàm callback sẽ chạy khi đăng nhập thành công
        """
        self.root = root
        self.on_login_success = on_login_success

        self.root.geometry("400x300")

        # Khung chính
        self.frame = ctk.CTkFrame(self.root, corner_radius=10)
        self.frame.pack(expand=True, padx=20, pady=20)

        # Tiêu đề
        lbl = ctk.CTkLabel(self.frame, text="Đăng nhập", font=ctk.CTkFont(size=20, weight="bold"))
        lbl.pack(pady=10)

        # Khung form nhập
        form = ctk.CTkFrame(self.frame)
        form.pack(pady=10, padx=10)

        # Tên đăng nhập
        ctk.CTkLabel(form, text="Tên đăng nhập").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.username_entry = ctk.CTkEntry(form, width=180)
        self.username_entry.grid(row=0, column=1, padx=5, pady=5)

        # Mật khẩu
        ctk.CTkLabel(form, text="Mật khẩu").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.password_entry = ctk.CTkEntry(form, show="*", width=180)
        self.password_entry.grid(row=1, column=1, padx=5, pady=5)

        # Nút đăng nhập
        login_btn = ctk.CTkButton(self.frame, text="Đăng nhập", command=self._on_login)
        login_btn.pack(pady=12)

    def _on_login(self):
        user = self.username_entry.get().strip()
        pwd = self.password_entry.get().strip()

        if not user or not pwd:
            messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập đầy đủ thông tin")
            return

        # Giả lập kiểm tra tài khoản
        if user == "ChiHao" and pwd == "123":
            messagebox.showinfo("Thành công", "Đăng nhập thành công!")
            self.frame.destroy()  # xoá form login
            self.on_login_success()  # gọi hàm hiển thị app chính
        else:
            messagebox.showerror("Lỗi", "Sai tên đăng nhập hoặc mật khẩu!")