'''
Requirements

  - can show the small notification on the botton right of window 
 -  Can show the products within the frame + image (if can)
 - add the products into bill
 - the button to pay -> show the qr -> successful paying -> decrease the total of those products
                                                         -> cards -> ...
'''


import customtkinter as ctk
from decimal import Decimal
import random
from tkinter import messagebox
from PIL import Image, ImageTk

# QR Code (nếu có cài)
try:
    import qrcode
    QR_AVAILABLE = True
except Exception:
    QR_AVAILABLE = False

# Dữ liệu mẫu sản phẩm
PRODUCTS = [
    {"id": f"P{i:03d}", "name": f"Product {i}", "price": Decimal(10000 + i*5000), "stock": random.randint(0, 30)}
    for i in range(1, 31)
]


class Sales:
    def __init__(self, parent, app):
        print("Success - sales")
        self.app = app
        self.invoice_items = []

        # Frame chính
        self.frame = ctk.CTkFrame(parent, corner_radius=10)
        self.frame.pack(fill="both", expand=True, padx=16, pady=16)

        # Header
        ctk.CTkLabel(self.frame, text="Bán hàng", font=ctk.CTkFont(size=18, weight="bold")).pack(anchor='w')

        # Body
        body = ctk.CTkFrame(self.frame, fg_color="transparent")
        body.pack(fill='both', expand=True, pady=8)

        # Left: Danh sách sản phẩm
        left = ctk.CTkFrame(body, fg_color="transparent")
        left.pack(side='left', fill='both', expand=True)

        search_frame = ctk.CTkFrame(left, fg_color="transparent")
        search_frame.pack(fill='x', pady=4)
        ctk.CTkLabel(search_frame, text="Tìm sản phẩm:").pack(side='left')
        self.search_var = ctk.StringVar()
        self.search_var.trace_add('write', lambda *a: self._render_products())
        ctk.CTkEntry(search_frame, textvariable=self.search_var, placeholder_text="Nhập tên sản phẩm...").pack(side='left', padx=6)

        # Danh sách sản phẩm (có scrollbar)
        self.products_frame = ctk.CTkScrollableFrame(left, label_text="Danh sách sản phẩm")
        self.products_frame.pack(fill='both', expand=True, pady=4)

        # Right: Hóa đơn
        right = ctk.CTkFrame(body, width=360, corner_radius=8)
        right.pack(side='right', fill='y', padx=8)
        ctk.CTkLabel(right, text="Hoá đơn", font=ctk.CTkFont(size=14, weight="bold")).pack(pady=6)

        self.invoice_list = ctk.CTkTextbox(right, width=300, height=320, wrap="none")
        self.invoice_list.pack(padx=6, pady=6)

        btns = ctk.CTkFrame(right, fg_color="transparent")
        btns.pack(pady=6)
        ctk.CTkButton(btns, text="Thanh toán", command=self._on_pay).pack(side='left', padx=6)
        ctk.CTkButton(btns, text="Clear", command=self._clear_invoice).pack(side='left', padx=6)

        self.total_label = ctk.CTkLabel(right, text="Tổng: 0", font=ctk.CTkFont(size=13))
        self.total_label.pack(pady=6)

        # Render ban đầu
        self._render_products()

    # ---------------------------------------------------
    # Hiển thị danh sách sản phẩm
    def _render_products(self):
        for widget in self.products_frame.winfo_children():
            widget.destroy()

        query = self.search_var.get().lower()
        filtered = [p for p in PRODUCTS if query in p['name'].lower()]

        for p in filtered:
            card = ctk.CTkFrame(self.products_frame, corner_radius=6)
            card.pack(fill='x', padx=4, pady=4)

            ctk.CTkLabel(card, text=p['name'], font=ctk.CTkFont(size=12, weight="bold")).pack(anchor='w')
            ctk.CTkLabel(card, text=f"Giá: {self.currency_format(p['price'])} | Tồn: {p['stock']}").pack(anchor='w')
            ctk.CTkButton(card, text="Thêm", width=80, command=lambda prod=p: self._add_to_invoice(prod)).pack(anchor='e', pady=4)

    # ---------------------------------------------------
    # Thêm sản phẩm vào hoá đơn
    def _add_to_invoice(self, product):
        if product['stock'] <= 0:
            messagebox.showerror("Lỗi", "Sản phẩm không đủ số lượng")
            return

        item = next((i for i in self.invoice_items if i['id'] == product['id']), None)
        if item:
            item['qty'] += 1
        else:
            self.invoice_items.append({
                'id': product['id'],
                'name': product['name'],
                'price': product['price'],
                'qty': 1
            })
        self._refresh_invoice()

    # ---------------------------------------------------
    # Cập nhật danh sách hoá đơn
    def _refresh_invoice(self):
        self.invoice_list.delete("1.0", "end")
        total = 0
        for it in self.invoice_items:
            line = f"{it['name']} x{it['qty']} - {self.currency_format(it['price'] * it['qty'])} VNĐ\n"
            self.invoice_list.insert("end", line)
            total += int(it['price'] * it['qty'])
        self.total_label.configure(text=f"Tổng: {self.currency_format(total)} VNĐ")

    def _clear_invoice(self):
        self.invoice_items = []
        self._refresh_invoice()

    # ---------------------------------------------------
    # Thanh toán
    def _on_pay(self):
        if not self.invoice_items:
            messagebox.showinfo("Hoá đơn rỗng", "Vui lòng thêm sản phẩm trước khi thanh toán")
            return

        total = sum(int(it['price'] * it['qty']) for it in self.invoice_items)

        if QR_AVAILABLE:
            self._show_qr_payment(total)
        else:
            if messagebox.askyesno("Xác nhận", "Thanh toán bằng tiền mặt?"):
                self.app.show_toast(self.app.root, "Thanh toán thành công")
                self._clear_invoice()

    # ---------------------------------------------------
    # Hiển thị QR code thanh toán
    def _show_qr_payment(self, amount):
        top = ctk.CTkToplevel(self.app.root)
        top.title("QR Payment")
        top.geometry("300x400")
        ctk.CTkLabel(top, text=f"Thanh toán: {self.currency_format(amount)} VNĐ",
                     font=ctk.CTkFont(size=14, weight="bold")).pack(pady=8)

        # Tạo mã QR
        qr = qrcode.make(f"PAY://{amount}")
        img = ImageTk.PhotoImage(qr.resize((240, 240)))
        lbl = ctk.CTkLabel(top, image=img, text="")
        lbl.image = img
        lbl.pack(pady=6)

        ctk.CTkButton(top, text="Đã thanh toán", command=lambda: self._confirm_payment(top)).pack(pady=6)

    def _confirm_payment(self, top):
        self.app.show_toast(self.app.root, "Thanh toán thành công")
        self._clear_invoice()
        top.destroy()

    # ---------------------------------------------------
    @staticmethod
    def currency_format(x):
        try:
            return f"{int(x):,}"
        except Exception:
            return str(x)
