import customtkinter as ctk
from tkinter import ttk
import tkinter as tk

from src.config.db import DB

class Dashboard:
    def __init__(self, parent):
        # Main Frame
        self.frame = ctk.CTkFrame(parent, corner_radius=12, fg_color="#F4F4F4")
        self.frame.pack(fill="both", expand=True, padx=16, pady=16)

        # ===== HEADER =====
        header = ctk.CTkLabel(
            self.frame,
            text="📊 Dashboard",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color="#333333"
        )
        header.pack(anchor="w", pady=(0, 12), padx=6)
        #w is for west (left) alignment

        # ===== CARDS SECTION =====
        self.cards_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        self.cards_frame.pack(fill="x", pady=10)

        self._create_cards()

        # ===== SEARCH & FILTER BAR =====
        self.frame_functional_buttons_search = ctk.CTkFrame(
            self.frame,
            fg_color="transparent"
        )
        self.frame_functional_buttons_search.pack(fill="x")

        self._create_buttons()
        self._create_search_bar()

        # ===== TABLE SECTION =====
        self.frame_table = ctk.CTkFrame(
            self.frame,
            fg_color="transparent",
            corner_radius=8,height=300
        )
        self.frame_table.pack(fill="both", expand=True, pady=(12, 0), padx=6)

   
        self._create_table()
        

    # ---------- Cards Section ----------
    def _create_cards(self):
        # Use grid layout for even spacing
        self.cards_frame.columnconfigure((0, 1, 2), weight=1, uniform="a")

        self.card_revenue = self._card(self.cards_frame, "💰 Doanh thu hôm nay", "12,300,000 ₫", 0)
        self.card_orders = self._card(self.cards_frame, "🧾 Đơn hàng hôm nay", "35", 1)
        self.card_lowstock = self._card(self.cards_frame, "⚠️ Sản phẩm sắp hết", "4", 2)

    def _card(self, parent, title, value, column):
        frame = ctk.CTkFrame(
            parent,
            fg_color="#FFFFFF",
            corner_radius=10,
            border_width=1,
            border_color="#E0E0E0"
        )
        frame.grid(row=0, column=column, padx=8, ipadx=4, ipady=6, sticky="nsew")

        title_label = ctk.CTkLabel(
            frame,
            text=title,
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#555555",
            anchor="w"
        )
        title_label.pack(anchor="w", padx=12, pady=(6, 2))

        value_label = ctk.CTkLabel(
            frame,
            text=value,
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#007BFF",
            anchor="w"
        )
        value_label.pack(anchor="w", padx=12, pady=(0, 6))

        return frame

    # ---------- Search / Filter Section / Buttons----------
    def _create_buttons(self):
        self.frame_buttons = ctk.CTkFrame(
            self.frame_functional_buttons_search,
            fg_color="transparent",
            corner_radius=8
        )
        self.frame_buttons.pack(side='left', pady=12, padx=(0, 6), ipady=6)
    
        self.btn_add_product = ctk.CTkButton(
            self.frame_buttons,
            text="➕ Add Product",
            fg_color="#28A745",
            hover_color="#1E7E34",
            corner_radius=6,
            width=120
        )
        self.btn_add_product.pack(side="left", padx=6, pady=12)

        self.btn_update_product = ctk.CTkButton(
            self.frame_buttons,
            text="✏️ Update Product",
            fg_color="#FFC107",
            hover_color="#E0A800",
            corner_radius=6,
            width=140
        )   

        self.btn_delete_product = ctk.CTkButton(
            self.frame_buttons,     
            text="🗑️ Delete Product",
            fg_color="#DC3545",
            hover_color="#C82333",
            corner_radius=6,
            width=140
        )
        self.btn_delete_product.pack(side="left", padx=6, pady=12)

          



    def _create_search_bar(self):
        self.frame_search = ctk.CTkFrame(
            self.frame_functional_buttons_search,
            fg_color="transparent",
            corner_radius=8
        )
        self.frame_search.pack(side="right", pady=12, padx=(6, 0), ipady=6)

        search_entry = ctk.CTkEntry(
            self.frame_search,
            placeholder_text="🔍 Search by product name...",
            width=240,
            height=32,
            corner_radius=8
        )
        search_entry.pack(side="left", padx=10)

        filter_btn = ctk.CTkButton(
            self.frame_search,
            text="Filter",
            fg_color="#007BFF",
            hover_color="#0056D2",
            corner_radius=6,
            width=80
        )
        filter_btn.pack(side="left", padx=6)

        sort_btn = ctk.CTkButton(
            self.frame_search,
            text="Sort",
            fg_color="#00B894",
            hover_color="#009970",
            corner_radius=6,
            width=80
        )
        sort_btn.pack(side="left", padx=6)

    def _create_table(self):
         # Khung chứa bảng
         self.frame_table.grid_rowconfigure(0, weight=1)
         self.frame_table.grid_columnconfigure(0, weight=1)

         # Tạo Treeview
         self.devices_Table = ttk.Treeview(
             self.frame_table,
             columns=("id", "name", "quantity", "price", "provider", "date"),
             show="headings"
            )

    # Khai báo tiêu đề cột
         self.devices_Table.heading("id", text="Mã sản phẩm")
         self.devices_Table.heading("name", text="Tên sản phẩm")
         self.devices_Table.heading("quantity", text="Số lượng còn lại")
         self.devices_Table.heading("price", text="Giá sản phẩm")
         self.devices_Table.heading("provider", text="Nhà cung cấp")
         self.devices_Table.heading("date", text="Ngày nhập")

            # Cấu hình độ rộng cột
         self.devices_Table.column("id", width=100, anchor="center")
         self.devices_Table.column("name", width=180)
         self.devices_Table.column("quantity", width=140, anchor="center")
         self.devices_Table.column("price", width=140, anchor="e")
         self.devices_Table.column("provider", width=160)
         self.devices_Table.column("date", width=120, anchor="center")

         # Gọi ScrollBar
         self._create_scrollbar()

         # Hiển thị bảng và thanh cuộn
         self.devices_Table.grid(row=0, column=0, sticky="nsew")

         self.load_data()


    def _create_scrollbar(self):
    # Scrollbar dọc
        scroll_y = ttk.Scrollbar(self.frame_table, orient="vertical", command=self.devices_Table.yview)
        scroll_y.grid(row=0, column=1, sticky="ns")
        #ns is for north-south (top to bottom) direction

    # Scrollbar ngang
        scroll_x = ttk.Scrollbar(self.frame_table, orient="horizontal", command=self.devices_Table.xview)
        scroll_x.grid(row=1, column=0, sticky="ew")
        #ew is for east-west (left to right) direction

    # Liên kết với Treeview
        self.devices_Table.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)


#-----------------------Functionalities -----------------------------
    def load_data(self):
        for i in self.devices_Table.get_children():
            self.devices_Table.delete(i)

        db = DB('SQL Server', 'ADMIN-PC\\SQLEXPRESS', 'Quan_Li_TV')
        
        values = db.searchTable("SanPham")
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
            self.devices_Table.insert("", tk.END, values=formatted_row)
        
        db.conn.close()

    def refresh_table(self):
        self.load_data()
        print("Table refreshed!")

    def insert_product(self, MaSP, TenSP, SLConLai, SoTien, Nha_CC, NgayNhap):
        

        db = DB('SQL Server', 'ADMIN-PC\\SQLEXPRESS', 'Quan_Li_TV')
        db.insertProducts(MaSP, TenSP, SLConLai, SoTien, Nha_CC, NgayNhap)
        db.conn.close()
        self.refresh_table()

    def update_product(self, id, TenSP, SLConLai, SoTien, Nha_CC, NgayNhap):
        db = DB('SQL Server', 'ADMIN-PC\\SQLEXPRESS', 'Quan_Li_TV')
        db.updateProducts(id, TenSP, SLConLai, SoTien, Nha_CC, NgayNhap)
        db.conn.close()
        self.refresh_table()

    def delete_product(self, id):
        db = DB('SQL Server', 'ADMIN-PC\\SQLEXPRESS', 'Quan_Li_TV')
        db.deleteProducts(id)
        db.conn.close()
        self.refresh_table()


        

    

