'''
Requirements

  - can show the small notification on the botton right of window 
 -  Can show the products within the frame + image (if can)
 - add the products into bill
 - the button to pay -> show the qr -> successful paying -> decrease the total of those products
                                                         -> cards -> ...
'''



from tkinter import ttk
import os

from tkinter import messagebox

import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
from src.config.db import DB
from datetime import datetime

# QR Code (nếu có cài)
try:
    import qrcode
    QR_AVAILABLE = True
except Exception:
    QR_AVAILABLE = False




class Sales:
    def __init__(self, parent, app,db ):
        print("Success - sales")

        #db
        self.db = db

        #Main App
        self.app = app

        #to save and show the products in bill
        self.invoice_items = []

        #toggle sort
        self.false  = False

        # Frame chính
        self.frame = ctk.CTkFrame(parent, corner_radius=10,fg_color="#F4F4F4")
        self.frame.pack(fill="both", expand=True, padx=16, pady=16)

        #Header
        # Tiêu đề
        self.title_frame = ctk.CTkFrame(self.frame, corner_radius=0,fg_color="#3CB251")
        self.title_frame.pack(fill="x",pady=(12, 0), padx=10)
        #expand true => causes the frame is stretching as much as possible

        ctk.CTkLabel(
            self.title_frame,
            text="Bán hàng",
            font=ctk.CTkFont(family="Roboto",size=24, weight="bold"),
            text_color="white"
        ).pack(anchor='center', pady=8)

        # Header
        

        # Body
        body = ctk.CTkFrame(self.frame, fg_color="transparent")
        body.pack(fill='both', expand=True, pady=(0, 12),padx=4)

        # Left: Danh sách sản phẩm
        left = ctk.CTkFrame(body, fg_color="transparent")
        left.pack(side='left', fill='both', expand=True,pady=(0, 12), padx=6)

    
         # ===== SEARCH & FILTER BAR =====
        self.frame_functional_buttons_search = ctk.CTkFrame(
            left,
            fg_color="transparent"
        )
        self.frame_functional_buttons_search.pack(fill="x", pady=12)
        self._create_search_bar()

        # Danh sách sản phẩm (có scrollbar)
        self.products_frame = ctk.CTkScrollableFrame(left, label_text="Danh sách sản phẩm",fg_color="#FFFFFF",corner_radius=8,label_fg_color="transparent",label_font=ctk.CTkFont(size=20, weight="bold"))
        self.products_frame.pack(fill='both', expand=True, pady=4)
        


        # Right: Hóa đơn
        right = ctk.CTkFrame(body, width=360, corner_radius=8)
        right.pack(side='right', fill='y', padx=8)
        ctk.CTkLabel(right, text="Hoá đơn", font=ctk.CTkFont(size=14, weight="bold")).pack(pady=6)


        #List -> contains products - quantity - Price 
        self.invoice_list = ctk.CTkTextbox(right, width=300, height=320, wrap="none")
        self.invoice_list.pack(padx=6, pady=6)


        #
        btns = ctk.CTkFrame(right, fg_color="transparent")
        btns.pack(pady=6)
        ctk.CTkButton(btns, text="Thanh toán", command=self._enter_customers).pack(side='left', padx=6)
        ctk.CTkButton(btns, text="Clear", command=self._clear_invoice).pack(side='left', padx=6)


        #the automatic sum of bill
        self.total_label = ctk.CTkLabel(right, text="Tổng: 0", font=ctk.CTkFont(size=13))
        self.total_label.pack(pady=6)

        # Render ban đầu
        self._render_products()


#========================Functionalities========================================
#refresh pages
    def refresh_pages(self):
        self._render_products()
        print("refresh sales pages successfully")
#Product section
    def _insert_Table(self,values):
        for row in values:
            # After get row from values => using tuple [(tuple of device 1) , (2) ,(3) ...]
            p = {
                "id"   : row[0],
                "name" : row[1],
                "price" : row[2],
                'stock' : row[3]
            }
            card = ctk.CTkFrame(self.products_frame, corner_radius=6,fg_color='transparent' ,border_color="black",border_width=1 )
            card.pack(fill='x', padx=4, pady=4)

            ctk.CTkLabel(card, text=p['name'], font=ctk.CTkFont(size=12, weight="bold")).pack(anchor='w',pady=(4,0),padx=4)
            ctk.CTkLabel(card, text=f"Giá: {self.currency_format(p['price'])} | Tồn: {p['stock']}").pack(anchor='w',padx = 4)
            ctk.CTkButton(card, text="Thêm", width=80, command=lambda prod=p: self._add_to_invoice(prod)).pack(anchor='e', padx = 4,pady=4)
    
    def _reset_render_products(self):
        for widget in self.products_frame.winfo_children():
            widget.destroy()

    # Hiển thị danh sách sản phẩm
    def _render_products(self):
        #reset
        self._reset_render_products()

        #get from db
        values = self.db.getItems_Products()

        # add into products section
        self._insert_Table(values)

    def sort_action(self,column= "MaSP", ):
        #toggle sort
        self.false = not self.false
        ascending = self.false

        #reset
        self._reset_render_products()
       
        #get data
        values = self.db.sort_products_in_sales_pages(self.columns[self.column_combo.get()],ascending)

        #insert into product section
        self._insert_Table(values)
        

# ---------------------------------------------------
    # Thêm sản phẩm vào hoá đơn
    def _add_to_invoice(self, product):
        if product['stock'] <= 0:
            messagebox.showerror("Lỗi", "Sản phẩm không đủ số lượng")
            return

        item = next((i for i in self.invoice_items if i['id'] == product['id']), None)
        if item:
            item['qty'] += 1
            if item['qty'] > product['stock']:
                 messagebox.showerror("Lỗi", "Sản phẩm không đủ số lượng")
                 return
        
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
    #1
    def _save_customer_info(self):
        # Lấy dữ liệu tại thời điểm người dùng nhấn Save
        self.TenNV_Nhap = self.employees_combo.get()
        self.TenKhachHang = self.entry_customers_name.get()
        self.Sdt_KhachHang = self.entry_SDT.get()

        if not self.TenKhachHang or not self.Sdt_KhachHang:
            messagebox.showerror("Thiếu thông tin", "Vui lòng nhập đầy đủ tên khách hàng và số điện thoại")
            return

        # Sau khi có thông tin, gọi thanh toán
        self._on_pay()

    #2 Thanh toán
    
    def _on_pay(self):
        
        #Total -> create the qr code with total
        total = sum(int(it['price'] * it['qty']) for it in self.invoice_items)

        if QR_AVAILABLE:
            self._show_qr_payment(total)
        else:
            if messagebox.askyesno("Xác nhận", "Thanh toán bằng tiền mặt?"):
                self.app.show_toast(self.frame, "Thanh toán thành công")
                self._clear_invoice()

    #3
    # Hiển thị QR code thanh toán
    def _show_qr_payment(self, amount):
        top = ctk.CTkToplevel(self.app.root)
        top.title("QR Payment")
        top.geometry("300x400")

        # Label title
        ctk.CTkLabel(
            top,
            text=f"Thanh toán: {self.currency_format(amount)} VNĐ",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(pady=8)

        qr = qrcode.make(f"PAY://{amount}")
        #Create based on the link  
        qr_pil = qr.get_image().convert("RGB")
        ctk_qr_img = ctk.CTkImage(light_image=qr_pil, dark_image=qr_pil, size=(240, 240))

        lbl = ctk.CTkLabel(top, image=ctk_qr_img, text="")
        lbl.image = ctk_qr_img  # keep a reference to avoid garbage collection
        lbl.pack(pady=6)

        # Confirm button
        ctk.CTkButton(
            top,
            text="Đã thanh toán",
            command=lambda: self._confirm_payment(top)
        ).pack(pady=6)
        self.Entering_Customer_Window.destroy()
        
    #4
    def _confirm_payment(self, top):
        # 1️⃣ Collect customer and employee information
        # NgayLap = date.today()
        
        NgayLap = datetime.now().strftime('%Y-%m-%d')

        for item in self.invoice_items:
            SoLuong = item['qty'] #quantity
            MaSP = item['id']
            self.db.insertBill(NgayLap, self.TenKhachHang, self.Sdt_KhachHang, self.TenNV_Nhap, MaSP, SoLuong)

        print(NgayLap, self.TenKhachHang, self.Sdt_KhachHang, self.TenNV_Nhap, MaSP, SoLuong)
        self.app.show_toast(self.frame, "Thanh toán thành ")
        self._clear_invoice()
        self._render_products()
        self.app.pages["Dashboard"].refresh_table_inDashboard()
        self.app.pages['History'].refresh_table_inHistory()
        top.destroy()
    
# ---------------------------------------------------
    @staticmethod
    def currency_format(x):
        try:
            return f"{int(x):,}"
        except Exception:
            return str(x)
        
   
        
        


#============GUI===================================================================
    def on_text_change(self,*args):
        #reset
        self._reset_render_products()

        #get data from db
        values = self.db.suggestions_products_in_sales_page(f"{self.search_var.get()}%")

        #insert into products section
        self._insert_Table(values)
        
    def _create_search_bar(self):
        #Find based on text changed event
        self.search_var = ctk.StringVar()
        self.search_var.trace_add("write", lambda *args: self.on_text_change())

        self.search_entry = ctk.CTkEntry(
            
            #Using text variables => can use place holder + get value
           self.frame_functional_buttons_search,
            placeholder_text="🔍 Search by product name...",textvariable=self.search_var,
            width=240,
            height=32,
            corner_radius=8,
            bg_color='red'
        )
        self.search_entry.pack(side="left", padx=(0, 8))
        

        sort_btn = ctk.CTkButton(
           self.frame_functional_buttons_search,
            text="Sort by",
            fg_color="#00B894",
            hover_color="#009970",
            corner_radius=6,
            width=80,
            command=self.sort_action
        )
        sort_btn.pack(side="left")

        columns =["Tên sản phẩm","Mã sản phẩm"]
        self.column_combo = ctk.CTkComboBox(
            self.frame_functional_buttons_search,
            values=columns,
            width=140,
            height=32,
            corner_radius=8
        )
        self.column_combo.pack(side= "left", padx= "8")
        self.columns ={
            "Tên sản phẩm" : "TenSP",
            "Mã sản phẩm" : "MaSP"
        }


#====================Sub pages=========================================
#Hiển thị Bảng nhập thông tin khách hàng
    def _enter_customers(self):
        if not self.invoice_items:
            messagebox.showinfo("Hoá đơn rỗng", "Vui lòng thêm sản phẩm trước khi thanh toán")
            return
        #chỉ cần : tên nhân viên (có sẵn trong db) - tên kh - sdt - ngày lập (current date)
        # ======= CREATE SUB FORM =======
        self.Entering_Customer_Window = ctk.CTkToplevel(self.frame)
        self.Entering_Customer_Window.title("Add New Product")
        self.Entering_Customer_Window.geometry("350x350")

        # Hiển thị form trên top và khóa main
        try:
            self.Entering_Customer_Window.lift()
            self.Entering_Customer_Window.attributes('-topmost', True)
            self.Entering_Customer_Window.after(200, lambda: self.Entering_Customer_Window.attributes('-topmost', False))
            self.Entering_Customer_Window.grab_set()
            self.Entering_Customer_Window.focus_force()
        except Exception:
            pass

        # ======= FRAME CHỨA NỘI DUNG =======
        frame_info = ctk.CTkFrame(self.Entering_Customer_Window, corner_radius=12, fg_color="#F4F4F4")
        frame_info.pack(fill="both", expand=True, padx=20, pady=20)

        # ======= ROW 0:Tên nhân viên - có sẵn trong db =======
        ctk.CTkLabel(frame_info, text="Nhân viên").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        Emp = ["Trần Thị B","Phạm Văn D","Nguyễn Văn G",]
        self.employees_combo = ctk.CTkComboBox(frame_info, values=Emp, width=160)
        self.employees_combo.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        # ======= ROW 1: Tên Khách Hàng  =======
        ctk.CTkLabel(frame_info, text="Tên Khách Hàng:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.entry_customers_name = ctk.CTkEntry(frame_info, width=160)
        self.entry_customers_name.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        # ======= ROW 2:+ SDT =======
        ctk.CTkLabel(frame_info, text="Số điện thoại:").grid(row=2, column=0, padx=10, pady=10, sticky="e")
        self.entry_SDT = ctk.CTkEntry(frame_info, width=160)
        self.entry_SDT.grid(row=2, column=1, padx=10, pady=10, sticky="w")

        
        # ======= ROW 3: Địa chỉ=======
        ctk.CTkLabel(frame_info, text="Địa chỉ khách hàng:").grid(row=3, column=0, padx=10, pady=10, sticky="e")
        self.entry_Address = ctk.CTkEntry(frame_info, width=160)
        self.entry_Address.grid(row=3, column=1, padx=10, pady=10)


        
        ctk.CTkButton(self.Entering_Customer_Window, text="Save", command = self._save_customer_info).pack(pady=(0,20))