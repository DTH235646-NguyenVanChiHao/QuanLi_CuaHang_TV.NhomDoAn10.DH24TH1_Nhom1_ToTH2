'''
Requirements
    


  - Has 2 button : Receipt for purchasing (Phiếu nhập) + bill (Hóa đơn)
  - Bill : customer info + TIME + products
  - Purchase : provider + time + products 


  - Table 
    -   Button add - upgrade - delete (create the box to tick and choose)
    -   Filter - Sort A-Z - Search (autofill + recommend)

    - Show the tables based bill or purchase
'''

import customtkinter as ctk
from tkinter import ttk
import tkinter as tk
from tkcalendar  import DateEntry
from tkinter import messagebox,simpledialog
from datetime import datetime


from src.config.db import DB

class History:
    def __init__(self, parent, app,db = DB('SQL Server', 'ADMIN-PC\\SQLEXPRESS', 'Quan_Li_TV')):
        #connect db
        self.db = db

        #toggle button
        self.false = True  

        #main
        print("Success - History")
        self.app = app

        # Frame chính
        self.frame = ctk.CTkFrame(parent, corner_radius=10,fg_color="#F4F4F4")
        self.frame.pack(fill="both", expand=True, padx=16, pady=16)

        # Tiêu đề
        ctk.CTkLabel(
            self.frame,
            text="Lịch sử giao dịch",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(anchor='w', pady=(12, 0), padx=10)
         # ===== SEARCH & FILTER BAR =====
        self.frame_functional_buttons_search = ctk.CTkFrame(
            self.frame,
            fg_color="transparent"
        )
        self.frame_functional_buttons_search.pack(fill="x", pady=(12, 0), padx=10)

        self._create_buttons()
        self._create_search_bar()

        # ===== TABLE SECTION =====
        self.frame_table = ctk.CTkFrame(
            self.frame,
            fg_color="transparent",
            corner_radius=8,height=300
        )
        self.frame_table.pack(fill="both", expand=True, pady=(12, 0), padx=10)

   
        self._create_table()

   # ---------- Search / Filter Section / Buttons----------
    def _create_buttons(self):
       
    
       
       

        self.btn_update_product = ctk.CTkButton(
            self.frame_functional_buttons_search,
            text="✏️ Update Receipt",
            fg_color="#FFC107",
            hover_color="#E0A800",
            corner_radius=6,
            width=140
        )   
        self.btn_update_product.pack(side="left") 

        self.btn_delete_product = ctk.CTkButton(
            self.frame_functional_buttons_search,     
            text="🗑️ Delete Receipt",
            fg_color="#DC3545",
            hover_color="#C82333",
            corner_radius=6,
            width=140
        )
        self.btn_delete_product.pack(side="left", padx=10)

          

    
    def on_text_change(self,*args,column):
        

        # I take % syntax here instead of src.config.db.py
        print("Text changed:", self.search_var.get())
        self.reset_table()

    
        
        
           

    def _create_search_bar(self):
        

        self.column_combo = ctk.CTkComboBox(
           self.frame_functional_buttons_search,
            values=["Mã sản phẩm", "Tên sản phẩm", "Nhà cung cấp"],
            width=140,
            height=32,
            corner_radius=8
        )
        self.column_combo.pack(side="right", padx=6)

        columns = {
            "Mã sản phẩm": "MaSP",
            "Tên sản phẩm": "TenSP",
            "Nhà cung cấp": "NhaCC"
        }

        #auto complete

        self.search_var = ctk.StringVar()
        self.search_var.trace_add("write", lambda *args: self.on_text_change(column=columns[self.column_combo.get()]))

        self.search_entry = ctk.CTkEntry(
           self.frame_functional_buttons_search,
            placeholder_text="🔍 Search Receipt...",textvariable=self.search_var,
            width=240,
            height=32,
            corner_radius=8
        )
        self.search_entry.pack(side="right", padx=6)

        filter_btn = ctk.CTkButton(
           self.frame_functional_buttons_search,
            text="Filter",
            fg_color="#007BFF",
            hover_color="#0056D2",
            corner_radius=6,
            width=80
           
        )
        filter_btn.pack(side="right", padx=6)

        sort_btn = ctk.CTkButton(
           self.frame_functional_buttons_search,
            text="Sort",
            fg_color="#00B894",
            hover_color="#009970",
            corner_radius=6,
            width=80
        )
        sort_btn.pack(side="right", padx=6)


    # ---------- Table Section ----------
    def sort_action(self,column= "MaSP", ):
        self.false = not self.false
        ascending = self.false
        self.reset_table()
       
        
        values = self.db.sort_products_by_column("MaSP",ascending)
        for row in values:
            # After get row from values => using tuple [(tuple of device 1) , (2) ,(3) ...]
            formatted_row = (
                row[0],  
                row[1],
                row[2],  
                f"{float(row[3]):,.0f} VND",  
                row[4],  
                str(row[5])  
            )
            self.history_Table.insert("", tk.END, values=formatted_row)
        


    def filter_action(self):
        columns = {
            "Mã sản phẩm": "MaSP",
            "Tên sản phẩm": "TenSP",
            "Nhà cung cấp": "NhaCC"
        }
        self.reset_table()
        
        
        filter_value = self.search_entry.get()
         
        values = self.db.filter_products(columns[self.column_combo.get()], filter_value)
        for row in values:
            # After get row from values => using tuple [(tuple of device 1) , (2) ,(3) ...]
            formatted_row = (
                row[0],  
                row[1],
                row[2],  
                f"{float(row[3]):,.0f} VND",  
                row[4],  
                str(row[5])  
            )
            self.history_Table.insert("", tk.END, values=formatted_row)
        


    def autofill_action(self):
        print("auto")

    def suggestion_action():
        print("suggestion")


    def _create_table(self):
         # Khung chứa bảng
        self.frame_table.grid_rowconfigure(0, weight=1)
        self.frame_table.grid_columnconfigure(0, weight=1)

        # Tạo Treeview
        self.history_Table = ttk.Treeview(
            self.frame_table,
            columns=("idHD", "idSP", "quantity", "price", "total", "date", "customer", "employee"),
            show="headings"
        )

        # --- Khai báo tiêu đề cột ---
        self.history_Table.heading("idHD", text="Mã Hoá Đơn")
        self.history_Table.heading("idSP", text="Mã Sản Phẩm")
        self.history_Table.heading("quantity", text="Số Lượng")
        self.history_Table.heading("price", text="Đơn Giá Bán")
        self.history_Table.heading("total", text="Thành Tiền")
        self.history_Table.heading("date", text="Ngày Mua")
        self.history_Table.heading("customer", text="Khách Hàng")
        self.history_Table.heading("employee", text="Nhân Viên")

        # --- Cấu hình độ rộng và căn chỉnh ---
        self.history_Table.column("idHD", width=100, anchor="center")
        self.history_Table.column("idSP", width=100, anchor="center")
        self.history_Table.column("quantity", width=100, anchor="center")
        self.history_Table.column("price", width=120, anchor="e")        # e = right align
        self.history_Table.column("total", width=120, anchor="e")
        self.history_Table.column("date", width=120, anchor="center")
        self.history_Table.column("customer", width=150)
        self.history_Table.column("employee", width=150)

        # Hiển thị bảng
        self.history_Table.grid(row=0, column=0, sticky="nsew")


         # Gọi ScrollBar
        self._create_scrollbar()

         # Hiển thị bảng và thanh cuộn
        self.history_Table.grid(row=0, column=0, sticky="nsew")

        self.load_data()


    def _create_scrollbar(self):
    # Scrollbar dọc
        scroll_y = ttk.Scrollbar(self.frame_table, orient="vertical", command=self.history_Table.yview)
        scroll_y.grid(row=0, column=1, sticky="ns")
        #ns is for north-south (top to bottom) direction

    # Scrollbar ngang
        scroll_x = ttk.Scrollbar(self.frame_table, orient="horizontal", command=self.history_Table.xview)
        scroll_x.grid(row=1, column=0, sticky="ew")
        #ew is for east-west (left to right) direction

    # Liên kết với Treeview
        self.history_Table.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)


#-----------------------Functionalities -----------------------------
    def reset_table(self):
        for i in self.history_Table.get_children():
            self.history_Table.delete(i)

    def load_data(self):
        
        self.reset_table()
      
        
        values = self.db.get_sales_history()
        for row in values:
            # After get row from values => using tuple [(tuple of device 1) , (2) ,(3) ...]
            formatted_row = (
                row[0],  
                row[1],
                row[2],  
                f"{float(row[3]):,.0f} VND",  
                row[4],  
                str(row[5])  
            )
            self.history_Table.insert("", tk.END, values=formatted_row)
        


    def refresh_table(self):
        self.load_data()
        print("Table refreshed!")

   

    


