import customtkinter as ctk
from tkinter import ttk
import tkinter as tk
from tkcalendar  import DateEntry
from tkinter import messagebox,simpledialog
from datetime import datetime


#Weakness => call db everywhere 

from src.config.db import DB

class Dashboard:
    def __init__(self, parent):
        #connect db
        
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
       
    
        self.btn_add_product = ctk.CTkButton(
            self.frame_functional_buttons_search,
            text="➕ Add Product",
            fg_color="#28A745",
            hover_color="#1E7E34",
            corner_radius=6,
            width=120,
            command=self.open_add_product_page
        )
        self.btn_add_product.pack(side="left", pady=12)

        self.btn_update_product = ctk.CTkButton(
            self.frame_functional_buttons_search,
            text="✏️ Update Product",
            fg_color="#FFC107",
            hover_color="#E0A800",
            corner_radius=6,
            width=140,
            command=self.open_update_product_page
        )   
        self.btn_update_product.pack(side="left", padx=6, pady=12) 

        self.btn_delete_product = ctk.CTkButton(
            self.frame_functional_buttons_search,     
            text="🗑️ Delete Product",
            fg_color="#DC3545",
            hover_color="#C82333",
            corner_radius=6,
            width=140,
            command=self.open_delete_product_page
        )
        self.btn_delete_product.pack(side="left", pady=12)

          



    def _create_search_bar(self):
        

        search_entry = ctk.CTkEntry(
           self.frame_functional_buttons_search,
            placeholder_text="🔍 Search by product name...",
            width=240,
            height=32,
            corner_radius=8
        )
        search_entry.pack(side="right", padx=6)

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
        

        
        #db.insertProducts(MaSP, TenSP, SLConLai, SoTien, Nha_CC, NgayNhap)
        
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

#Sub pages -> Add Product, Update Product, Delete Product
    def open_add_product_page(self):
        # ======= CREATE SUB FORM =======
        add_product_window = ctk.CTkToplevel(self.frame)
        add_product_window.title("Add New Product")
        add_product_window.geometry("600x350")

        # Hiển thị form trên top và khóa main
        add_product_window.lift()
        add_product_window.attributes('-topmost', True)
        add_product_window.after(200, lambda: add_product_window.attributes('-topmost', False))
        add_product_window.grab_set()
        add_product_window.focus_force()

        # ======= FRAME CHỨA NỘI DUNG =======
        frame_info = ctk.CTkFrame(add_product_window, corner_radius=12, fg_color="#F4F4F4")
        frame_info.pack(fill="both", expand=True, padx=20, pady=20)

        # ======= CỘT 0-5: GRID CHUẨN =======
        frame_info.columnconfigure((0, 1, 4, 5), weight=1, uniform="col")

        # ======= ROW 0: MÃ SP + NHÀ CC =======
        ctk.CTkLabel(frame_info, text="Mã sản phẩm:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        entry_id = ctk.CTkEntry(frame_info, width=160)
        entry_id.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        ctk.CTkLabel(frame_info, text="Nhà cung cấp:").grid(row=0, column=4, padx=10, pady=10, sticky="e")
        Providers = ["Samsung", "LG", "Sony", "Panasonic", "Toshiba", "Sharp", "Philips", "Hisense", "Vizio", "Insignia"]
        entry_provider = ctk.CTkComboBox(frame_info, values=Providers, width=160)
        entry_provider.grid(row=0, column=5, padx=10, pady=10, sticky="w")

        # ======= ROW 1: TÊN SP + NGÀY NHẬP =======
        ctk.CTkLabel(frame_info, text="Tên sản phẩm:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
        entry_name = ctk.CTkEntry(frame_info, width=160)
        entry_name.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        ctk.CTkLabel(frame_info, text="Ngày nhập (YYYY-MM-DD):").grid(row=1, column=4, padx=10, pady=10, sticky="e")
        entry_date = DateEntry(frame_info, width=17, date_pattern="yyyy-mm-dd")
        entry_date.grid(row=1, column=5, padx=10, pady=10, sticky="w")

        # ======= ROW 2: SỐ LƯỢNG =======
        ctk.CTkLabel(frame_info, text="Số lượng nhập:").grid(row=2, column=0, padx=10, pady=10, sticky="e")
        entry_quantity = ctk.CTkEntry(frame_info, width=160)
        entry_quantity.grid(row=2, column=1, padx=10, pady=10, sticky="w")

        # ======= ROW 3: GIÁ =======
        ctk.CTkLabel(frame_info, text="Giá sản phẩm:").grid(row=3, column=0, padx=10, pady=10, sticky="e")
        entry_price = ctk.CTkEntry(frame_info, width=160)
        entry_price.grid(row=3, column=1, padx=10, pady=10, sticky="w")

       

        


        
        def add_product_action():
            db = DB('SQL Server', 'ADMIN-PC\\SQLEXPRESS', 'Quan_Li_TV')
            if not all([entry_id.get(), entry_name.get(), entry_quantity.get(), entry_price.get(), entry_provider.get(), entry_date.get()]):
                messagebox.showinfo(title="Error", message="Please fill in all fields.")
                return

            MaSP = entry_id.get()
            TenSP = entry_name.get()
            SLConLai = entry_quantity.get()
            SoTien = entry_price.get()
            Nha_CC = entry_provider.get()
            NgayNhap = entry_date.get()

            # Lặp đến khi có ID hợp lệ
            while True:
                if not db.is_exist(MaSP):  # kiểm tra trực tiếp trong database
                    db.insertProducts(MaSP, TenSP, SLConLai, SoTien, Nha_CC, NgayNhap)
                    messagebox.showinfo("Success", "Product added successfully!")
                    db.conn.close()
                    break
                else:
                    messagebox.showinfo("Error", f"Product ID '{MaSP}' already exists.")
                    MaSP = simpledialog.askstring("Duplicate ID", "Please enter a new Product ID:")
                    add_product_window.destroy()
                    if MaSP is None:  # user bấm Cancel
                        return

                
            
                

         # ======= NÚT ADD =======
        btn_add = ctk.CTkButton(frame_info,
                                text="Add Product",
                                fg_color="#28A745",
                                hover_color="#1E7E34",
                                corner_radius=6,
                                width=180,command=add_product_action)
        btn_add.grid(row=4, column=0, columnspan=6, pady=20)

        # ======= FOCUS VÀ MAINLOOP =======
        entry_id.focus_force()
        

        # add_product_window.mainloop()

        
        
        

    def open_update_product_page(self):
        db = DB('SQL Server', 'ADMIN-PC\\SQLEXPRESS', 'Quan_Li_TV')
        data = self.get_selected_product()
        if not data:
            return

        MaSP, TenSP, SLConLai, SoTien, Nha_CC, NgayNhap = data

        # ======= CREATE SUB FORM =======
        update_product_window = ctk.CTkToplevel(self.frame)
        update_product_window.title("Add New Product")
        update_product_window.geometry("600x350")

        # Hiển thị form trên top và khóa main
        update_product_window.lift()
        update_product_window.attributes('-topmost', True)
        update_product_window.after(200, lambda: update_product_window.attributes('-topmost', False))
        update_product_window.grab_set()
        update_product_window.focus_force()

        # ======= FRAME CHỨA NỘI DUNG =======
        frame_info = ctk.CTkFrame(update_product_window, corner_radius=12, fg_color="#F4F4F4")
        frame_info.pack(fill="both", expand=True, padx=20, pady=20)

        # ======= CỘT 0-5: GRID CHUẨN =======
        frame_info.columnconfigure((0, 1, 4, 5), weight=1, uniform="col")

        # ======= ROW 0: MÃ SP + NHÀ CC =======
        ctk.CTkLabel(frame_info, text="Mã sản phẩm:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        entry_id = ctk.CTkEntry(frame_info, width=160)
        entry_id.insert(0, MaSP)
        entry_id.configure(state="disabled")  # không cho sửa ID
        entry_id.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        ctk.CTkLabel(frame_info, text="Nhà cung cấp:").grid(row=0, column=4, padx=10, pady=10, sticky="e")
        Providers = ["Samsung", "LG", "Sony", "Panasonic", "Toshiba", "Sharp", "Philips", "Hisense", "Vizio", "Insignia"]
        provider_combo = ctk.CTkComboBox(frame_info, values=Providers, width=160)
        provider_combo.set(Nha_CC)
        provider_combo.grid(row=0, column=5, padx=10, pady=10, sticky="w")

        # ======= ROW 1: TÊN SP + NGÀY NHẬP =======
        ctk.CTkLabel(frame_info, text="Tên sản phẩm:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
        entry_name = ctk.CTkEntry(frame_info, width=160)
        entry_name.insert(0, TenSP)
        entry_name.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        ctk.CTkLabel(frame_info, text="Ngày nhập (YYYY-MM-DD):").grid(row=1, column=4, padx=10, pady=10, sticky="e")
        entry_date = DateEntry(frame_info, width=17, date_pattern="yyyy-mm-dd")

        #from datetime import datetime
        try:
        # Chuyển đổi chuỗi từ SQL sang datetime
            current_date = datetime.strptime(NgayNhap, "%Y-%m-%d")
        except:
             current_date = datetime.today()
        entry_date.set_date(current_date)
        entry_date.grid(row=1, column=5, padx=10, pady=10, sticky="w")

        # ======= ROW 2: SỐ LƯỢNG =======
        ctk.CTkLabel(frame_info, text="Số lượng nhập:").grid(row=2, column=0, padx=10, pady=10, sticky="e")
        entry_quantity = ctk.CTkEntry(frame_info, width=160)
        entry_quantity.insert(0, SLConLai)
        entry_quantity.grid(row=2, column=1, padx=10, pady=10, sticky="w")

        # ======= ROW 3: GIÁ =======
        ctk.CTkLabel(frame_info, text="Giá sản phẩm:").grid(row=3, column=0, padx=10, pady=10, sticky="e")
        entry_price = ctk.CTkEntry(frame_info, width=160)
        entry_price.insert(0, SoTien)
        entry_price.grid(row=3, column=1, padx=10, pady=10, sticky="w")


    

       

        # Nút Save
        def save_changes():
            new_name = entry_name.get()
            new_quantity = entry_quantity.get()
            new_price = entry_price.get()
            new_provider = provider_combo.get()
            new_date = entry_date.get()

             # Gọi DB update
            db.updateProducts(MaSP, new_name, new_quantity, new_price, new_provider, new_date)
            messagebox.showinfo("Success", "Product updated successfully!")
            update_product_window.destroy()
            db.conn.close()
            self.refresh_table()  # cập nhật lại giao diện

        ctk.CTkButton(update_product_window, text="Save", command=save_changes).pack(pady=10)


    def open_delete_product_page(self):
        db = DB('SQL Server', 'ADMIN-PC\\SQLEXPRESS', 'Quan_Li_TV')
        data = self.get_selected_product()
        if not data:
            return

        MaSP, TenSP, SLConLai, SoTien, Nha_CC, NgayNhap = data

        #ask for confirmation
        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete product '{TenSP}' (ID: {MaSP})?")
        if confirm:
            db.deleteProducts(MaSP)
            messagebox.showinfo("Success", "Product deleted successfully!")
        else:
            messagebox.showinfo("Cancelled", "Product deletion cancelled.")

        db.conn.close()
        self.refresh_table()  # cập nhật lại giao diện


    
    def get_selected_product(self):
        selected_item = self.devices_Table.focus()  # lấy item đang được chọn
        if not selected_item:
            messagebox.showinfo("Notice", "Please select a product to update.")
            return None

        values = self.devices_Table.item(selected_item, "values")  # lấy giá trị từng cột
        return values  # Trả về tuple: (MaSP, TenSP, SLConLai, SoTien, Nha_CC, NgayNhap)

