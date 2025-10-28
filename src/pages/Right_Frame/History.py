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
from tkinter import messagebox
from datetime import datetime



class History:
    def __init__(self, parent, app,db):
        #main app
        self.app = app
        #connect db
        self.db = db

        #toggle button
        self.false = True  

        #columns 
        self.columns = {
            "Mã hoá đơn": "hd.MaHD",
            "Tên khách hàng": "hd.TenKH",
            "Tên sản phẩm": "sp.TenSP",
            "Số điện thoại": "hd.SDT"
        }

        #main app
        self.app = app

        # Frame chính
        self.frame = ctk.CTkFrame(parent, corner_radius=10,fg_color="#F4F4F4")
        self.frame.pack(fill="both", expand=True, padx=16, pady=16)

        # Tiêu đề
        self.title_frame = ctk.CTkFrame(self.frame, corner_radius=0,fg_color="#3CB251")
        self.title_frame.pack(fill="x",pady=(12, 0), padx=10)
        #expand true => causes the frame is stretching as much as possible

        ctk.CTkLabel(
            self.title_frame,
            text="Lịch sử giao dịch",
            font=ctk.CTkFont(family="Roboto",size=24, weight="bold"),
            text_color="white"
        ).pack(anchor='center', pady=8)


         # ===== SEARCH & FILTER BAR =====
        self.frame_functional_buttons_search = ctk.CTkFrame(
            self.frame,
            fg_color="transparent"
        )
        self.frame_functional_buttons_search.pack(fill="x", pady=(12, 0), padx=10)

        self._create_buttons()
        self._create_search_bar()

        # ===== TABLE SECTION =====
        self.frame_table = ctk.CTkScrollableFrame(
            self.frame,
            fg_color="transparent",
            corner_radius=8,height=300
        )
        self.frame_table.pack(fill="both", expand=True, pady=(12, 0))
        self._create_table()

   # ---------- Search / Filter Section / Buttons----------
    def _create_buttons(self):
       # Update
        self.btn_update_product = ctk.CTkButton(
            self.frame_functional_buttons_search,
            text="✏️ Sửa Hoá Đơn",
            fg_color="#FFC107",
            hover_color="#E0A800",
            corner_radius=6,
            width=140,
            command=self.open_update_receipt_page
        )   
        self.btn_update_product.pack(side="left") 

        #Delete
        self.btn_delete_product = ctk.CTkButton(
            self.frame_functional_buttons_search,     
            text="🗑️ Xoá hoá đơn",
            fg_color="#DC3545",
            hover_color="#C82333",
            corner_radius=6,
            width=140,
            command=self.open_delete_product_page
        )
        self.btn_delete_product.pack(side="left", padx=10)

          
    
    def _create_search_bar(self):
        self.column_combo = ctk.CTkComboBox(
           self.frame_functional_buttons_search,
            values=["Mã hoá đơn", "Tên khách hàng", "Tên sản phẩm", "Số điện thoại"],
            width=140,
            height=32,
            corner_radius=8
        )
        self.column_combo.pack(side="right", padx=6)

        

        self.search_entry = ctk.CTkEntry(
           self.frame_functional_buttons_search,
            placeholder_text="🔍 Search Receipt...",
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
            width=80,
            command=self.filter_action
           
        )
        filter_btn.pack(side="right", padx=6)

        sort_btn = ctk.CTkButton(
           self.frame_functional_buttons_search,
            text="Sort",
            fg_color="#00B894",
            hover_color="#009970",
            corner_radius=6,
            width=80,
            command=self.sort_action
        )
        sort_btn.pack(side="right", padx=6)


    # ---------- Table Section ----------
    
        
    def _create_table(self):

        #Style 

        # --- Khung chứa bảng ---> tự động giãn cột
        self.frame_table.grid_rowconfigure(0, weight=1)
        self.frame_table.grid_columnconfigure(0, weight=1)

        # --- Treeview thêm cột Mã sản phẩm ---
        self.history_Table = ttk.Treeview(
            self.frame_table,
            columns=("idHD", "idSP", "customer", "phone", "product", "quantity", "price", "total", "employee", "date"),
            show="headings",
            #Handle the shrink of table (especially TTkFrame with built-in scrollbar) 
            height=30,
        )

        # --- Khai báo tiêu đề cột ---
        self.history_Table.heading("idHD", text="Mã Hóa Đơn")
        self.history_Table.heading("idSP", text="Mã Sản Phẩm")
        self.history_Table.heading("customer", text="Tên Khách Hàng")
        self.history_Table.heading("phone", text="Số Điện Thoại")
        self.history_Table.heading("product", text="Tên Sản Phẩm")
        self.history_Table.heading("quantity", text="Số Lượng")
        self.history_Table.heading("price", text="Đơn Giá Bán")
        self.history_Table.heading("total", text="Thành Tiền")
        self.history_Table.heading("employee", text="Nhân Viên")
        self.history_Table.heading("date", text="Ngày Lập")

        # --- Cấu hình độ rộng và căn chỉnh ---
        self.history_Table.column("idHD", width=100, anchor="center")
        self.history_Table.column("idSP", width=100, anchor="center")
        self.history_Table.column("customer", width=150)
        self.history_Table.column("phone", width=120, anchor="center")
        self.history_Table.column("product", width=150)
        self.history_Table.column("quantity", width=80, anchor="center")
        self.history_Table.column("price", width=100, anchor="e")
        self.history_Table.column("total", width=100, anchor="e")
        self.history_Table.column("employee", width=120)
        self.history_Table.column("date", width=120, anchor="center")

        # --- Hiển thị bảng ---
        self.history_Table.grid(row=0, column=0, sticky="nsew")
        self.load_data()


   


#===============================Functionalities======================

#Interact with table
    def _insert_table(self,values):
        # Expecting: (MaHD, MaSP, TenKH, SDT, TenSP, SoLuong, DonGiaBan, ThanhTien, TenNV, NgayLap)
        for row in values:
            formatted_row = (
                row[0],  # MaHD
                row[1],  # MaSP
                row[2],  # TenKH
                row[3],  # SDT
                row[4],  # TenSP
                row[5],  # SoLuong
                f"{float(row[6]):,.0f} VND",
                f"{float(row[7]):,.0f} VND",
                row[8],  # TenNV
                str(row[9])  # NgayLap
            )
            self.history_Table.insert("", tk.END, values=formatted_row)

    def reset_table(self):
        for i in self.history_Table.get_children():
            self.history_Table.delete(i)

    def load_data(self):
        self.reset_table()
        values = self.db.get_sales_history()
        self._insert_table(values)
        
    
    def refresh_table_inHistory(self):
        self.load_data()
        print("Table refreshed!")


#Sort and Filter => Corresponding button 
    def sort_action(self):
        #Toggle button
        self.false = not self.false
        ascending = self.false

        #reset
        self.reset_table()
       
        #Get value from db
        values = self.db.sort_receipts_by_column(self.columns[self.column_combo.get()], ascending)
        # Expect: (MaHD, MaSP, TenKH, SDT, TenSP, SoLuong, DonGiaBan, ThanhTien, TenNV, NgayLap)

        #Insert into value (format by rows -> insert table)
        self._insert_table(values)

    def filter_action(self):
        
        #reset
        self.reset_table()
        
        #Get value from search entry 
        filter_value = self.search_entry.get()
         
        # add and get value from db
        values = self.db.filter_receipts(self.columns[self.column_combo.get()], f"{filter_value}%")

        #insert table
        self._insert_table(values)
    
    




#Select value from table -> focus
    def get_selected_product(self):
        selected_item = self.history_Table.focus()  # lấy item đang được chọn
        if not selected_item:
            messagebox.showinfo("Notice", "Please select a product to update.")
            return None

        values = self.history_Table.item(selected_item, "values")  # lấy giá trị từng cột
        return values  # Trả về tuple: 
    
#===============================Sub pages=============================

    def open_update_receipt_page(self):
        data = self.get_selected_product()
        if not data:
            return

        MaHD, MaSP,TenKH,SDT,TenSP, SoLuong,DonGiaBan,ThanhTien,TenNV,NgayLap = data

        

        # ======= CREATE SUB FORM =======
        update_receipt_window = ctk.CTkToplevel(self.frame)
        update_receipt_window.title("Add New Product")
        update_receipt_window.geometry("600x350")

        # Hiển thị form trên top và khóa main
        update_receipt_window.lift()
        update_receipt_window.attributes('-topmost', True)
        update_receipt_window.after(200, lambda: update_receipt_window.attributes('-topmost', False))
        update_receipt_window.grab_set()
        update_receipt_window.focus_force()

        # ======= FRAME CHỨA NỘI DUNG =======
        frame_info = ctk.CTkFrame(update_receipt_window, corner_radius=12, fg_color="#F4F4F4")
        frame_info.pack(fill="both", expand=True, padx=20, pady=20)

        # ======= CỘT 0-5: GRID CHUẨN =======
        frame_info.columnconfigure((0, 1, 4, 5), weight=1, uniform="col")

        # ======= ROW 0: Mã Hoá đơn (inactive) + Nhân viên =======
        ctk.CTkLabel(frame_info, text="Mã hoá đơn:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        entry_id = ctk.CTkEntry(frame_info, width=160)
        entry_id.insert(0, MaHD)
        entry_id.configure(state="disabled")  # không cho sửa ID
        entry_id.grid(row=0, column=1, padx=10, pady=10, sticky="w")



        ctk.CTkLabel(frame_info, text="Nhân viên").grid(row=0, column=4, padx=10, pady=10, sticky="e")
        Emp = ["Trần Thị B","Phạm Văn D","Nguyễn Văn G",]
        employees_combo = ctk.CTkComboBox(frame_info, values=Emp, width=160)
        employees_combo.set(TenNV)  # Mặc định chọn nhà cung cấp đầu tiên
        employees_combo.grid(row=0, column=5, padx=10, pady=10, sticky="w")

        # ======= ROW 1: Tên Khách Hàng + SDT =======
        ctk.CTkLabel(frame_info, text="Tên Khách Hàng:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
        entry_customers_name = ctk.CTkEntry(frame_info, width=160)
        entry_customers_name.insert(0, TenKH)
        entry_customers_name.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        ctk.CTkLabel(frame_info, text="Số điện thoại:").grid(row=1, column=4, padx=10, pady=10, sticky="e")
        entry_SDT = ctk.CTkEntry(frame_info, width=160)
        entry_SDT.insert(0, SDT)
        entry_SDT.grid(row=1, column=5, padx=10, pady=10, sticky="w")


        

        # ======= ROW 2:Tên sp (inactive) + SỐ LƯỢNG  mua+ =======
        ctk.CTkLabel(frame_info, text="Tên sản phẩm:").grid(row=2, column=0, padx=10, pady=10, sticky="e")
        entry_products_name = ctk.CTkEntry(frame_info, width=160)
        entry_products_name.insert(0, TenSP)
        entry_products_name.configure(state="disabled")  
        entry_products_name.grid(row=2, column=1, padx=10, pady=10, sticky="w")

        ctk.CTkLabel(frame_info, text="Số lượng mua:").grid(row=2, column=4, padx=10, pady=10, sticky="e")
        entry_SLM = ctk.CTkEntry(frame_info, width=160)
        entry_SLM.insert(0, SoLuong)
        entry_SLM.grid(row=2, column=5, padx=10, pady=10, sticky="w")

        
        # ======= ROW 3: Ma sp  + Ngay Lap=======
        ctk.CTkLabel(frame_info, text="Mã sản phẩm:").grid(row=4, column=0, padx=10, pady=10, sticky="e")
        entry_MaSP = ctk.CTkEntry(frame_info, width=160)
        entry_MaSP.insert(0, MaSP)
        entry_MaSP.configure(state="disabled")
        entry_MaSP.grid(row=4, column=1, padx=10, pady=10, sticky="w")

        ctk.CTkLabel(frame_info, text="Ngày lập (YYYY-MM-DD):").grid(row=3, column=4, padx=10, pady=10, sticky="e")
        entry_date = DateEntry(frame_info, width=17, date_pattern="yyyy-mm-dd")
        #from datetime import datetime
        try:
        # Chuyển đổi chuỗi từ SQL sang datetime
            current_date = datetime.strptime(NgayLap, "%Y-%m-%d")
        except:
             current_date = datetime.today()
        entry_date.set_date(current_date)
        entry_date.grid(row=3, column=5, padx=10, pady=10, sticky="w")

        
        # Nút Save
        def save_changes():
            # They are disabled - so no need to get them
            # new_mhd = entry_id.get()
            # new_id_product = entry_MaSP.get()

            new_customer_name = entry_customers_name.get()
            new_sdt = entry_SDT.get()
            new_employee = employees_combo.get()

            # new_product_name = entry_products_name.get()
            new_quantity = entry_SLM.get()

            #Price has vnd at last - need to remove it
            new_date = entry_date.get_date().strftime("%Y-%m-%d")
            

          
            self.db.updateBill(MaHD ,MaSP, new_date, new_quantity, new_customer_name, new_sdt, new_employee)
            messagebox.showinfo("Success", "Product updated successfully!")

            self.refresh_table_inHistory()  # cập nhật lại giao diện

            self.pages["Dashboard"].refresh_table_inDashboard()
            
            self.app.pages["Sales"].refresh_pages()
            self.app.show_toast(self.frame, "Receipt Updated successfully.")
        ctk.CTkButton(update_receipt_window, text="Save", command=save_changes).pack(pady=10)


    def open_delete_product_page(self):
      
        data = self.get_selected_product()
        if not data:
            return

        MaHD, MaSP,TenKH,SDT,TenSP, SoLuong,DonGiaBan,ThanhTien,TenNV,NgayLap = data

        #ask for confirmation
        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete bill of '{TenKH}' (Mã HD: {MaHD } + Mã SP: {MaSP})?")
        if confirm:
            self.db.deleteBill(MaHD,SoLuong,MaSP)
            self.pages["Dashboard"].refresh_table_inDashboard()
            messagebox.showinfo("Success", "Product deleted successfully!")
        else:
            messagebox.showinfo("Cancelled", "Product deletion cancelled.")

       
        self.refresh_table_inHistory()  # cập nhật lại giao diện
        self.app.pages["Dashboard"].refresh_cards()  # Cập nhật bảng trên Dashboard
        self.app.show_toast(self.frame, "Receipt deleted successfully.")
        
