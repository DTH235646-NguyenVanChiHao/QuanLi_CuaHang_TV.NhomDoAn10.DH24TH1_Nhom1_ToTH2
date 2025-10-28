import customtkinter as ctk
from tkinter import ttk
import tkinter as tk
from tkcalendar  import DateEntry
from tkinter import messagebox,simpledialog
from datetime import datetime




#Weakness => call db everywhere 

#"#F4F4F4" => bg

#text_color="#333333"

#     fg_color="#FFFFFF",



class Dashboard:
    def __init__(self, parent,database,app):
        #connect db
        self.db = database
        
        #main app
        self.app=app
        #toggle button -> sort button
        self.false = False

        # Main Frame
        self.frame = ctk.CTkFrame(parent, corner_radius=12, fg_color="#F4F4F4")
        self.frame.pack(fill="both", expand=True, padx=16, pady=16)

        # ===== HEADER =====

        # Tiêu đề
        self.title_frame = ctk.CTkFrame(self.frame, corner_radius=0,fg_color="#3CB251")
        self.title_frame.pack(fill="x",pady=(12, 0), padx=10)
        #expand true => causes the frame is stretching as much as possible

        ctk.CTkLabel(
            self.title_frame,
            text="📊 Dashboard",
            font=ctk.CTkFont(family="Roboto",size=24, weight="bold"),
            text_color="white"
        ).pack(anchor='center', pady=8)
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
        self.frame_table = ctk.CTkScrollableFrame(
            self.frame,
            fg_color="transparent",
            corner_radius=8,height=300
        )
        self.frame_table.pack(fill="both", expand=True, pady=(12, 0))

   
        self._create_table()
        
#======================Build GUI================================

# ---------- Cards Section ----------
    def refresh_cards(self):
        for widget in self.cards_frame.winfo_children():
            widget.destroy()
        self._create_cards()

    def _create_cards(self):
        revuenue = self.db.total_revenue()
        orders = self.db.count_orders_today()
        lowstock = self.db.count_low_stock_products()

        # Use grid layout for even spacing
        self.cards_frame.columnconfigure((0, 1, 2), weight=1, uniform="a")

        self.card_revenue = self._card(self.cards_frame, "💰 Doanh thu hôm nay", f"{float(revuenue):,.0f} VND", 0)
        self.card_orders = self._card(self.cards_frame, "🧾 Đơn hàng hôm nay", f"{orders}", 1)
        self.card_lowstock = self._card(self.cards_frame, "⚠️ Sản phẩm sắp hết", f"{lowstock}", 2)

    def _card(self, parent, title, value, column):
        frame = ctk.CTkFrame(
            parent,
            fg_color="#FFFFFF",
            corner_radius=10,
            border_width=1,
            border_color="#E0E0E0"
        )
        frame.grid(row=0, column=column, padx=8, ipadx=4, ipady=6, sticky="nsew")

        #"nsew": Kéo giãn widget để nó lấp đầy toàn bộ ô (cả 4 hướng)

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

        #Create and add into variables
        return frame

# ---------- Search / Filter Section / Buttons----------
#Button
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

          
#Ideas: reset (table + card + ...) -> call db method (will return the value)
#       value in products => get row[i] -> format them +insert


#Search bar: onTextChange (event) + 
    def _create_search_bar(self):
        

        self.column_combo = ctk.CTkComboBox(
           self.frame_functional_buttons_search,
            values=["Mã sản phẩm", "Tên sản phẩm", "Nhà cung cấp"],
            width=140,
            height=32,
            corner_radius=8
        )
        self.column_combo.pack(side="right", padx=6)

        #Create this to add proper columns into database
        columns = {
            "Mã sản phẩm": "MaSP",
            "Tên sản phẩm": "TenSP",
            "Nhà cung cấp": "NhaCC"
        }

        #text on changed
        self.search_var = ctk.StringVar()
        #lambda for adding params 
        self.search_var.trace_add("write", lambda *args: self.on_text_change(column=columns[self.column_combo.get()]))

        self.search_entry = ctk.CTkEntry(
           self.frame_functional_buttons_search,
            placeholder_text="🔍 Search by product name...",textvariable=self.search_var,
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
            ,command=self.filter_action
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
         

         # Khung chứa bảng
         self.frame_table.grid_rowconfigure(0, weight=1)
         self.frame_table.grid_columnconfigure(0, weight=1)

         # Tạo Treeview
         self.devices_Table = ttk.Treeview(
             self.frame_table,
             columns=("id", "name", "quantity", "price", "provider", "date"),
             show="headings",

             #handle the shrink of table 
             height=30
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

        
         # Hiển thị bảng và thanh cuộn
         self.devices_Table.grid(row=0, column=0, sticky="nsew")
        
        #Hiển thị dữ liệu
         self.load_data()



#-----------------------Functionalities -----------------------------
    def reset_table(self):
        for i in self.devices_Table.get_children():
            self.devices_Table.delete(i)

    def insert_table(self,values):
         #Format + Insert
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
    
    #Reset -> get value from db -> format : row[i] -> insert
    def load_data(self):
        #Reset
        self.reset_table()

        #Get value from DB
        values = self.db.searchTable("SanPham")

        #Insert
        self.insert_table(values)
       

    def refresh_table_inDashboard(self):
        self.refresh_cards()
        self.load_data()
        print("Table refreshed!")


#Sub pages -> Add Product, Update Product, Delete Product
    def open_add_product_page(self):
        # ======= CREATE SUB FORM =======
        add_product_window = ctk.CTkToplevel(self.frame)
        add_product_window.title("Add New Product")
        add_product_window.geometry("800x350")

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
        entry_id.grid(row=0, column=1,pady=10, sticky="w")

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

        self.refresh_cards()
        def add_product_action():
           
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
                if not self.db.is_exist(MaSP):  # kiểm tra trực tiếp trong database
                    self.db.insertProducts(MaSP, TenSP, SLConLai, SoTien, Nha_CC, NgayNhap)
                    messagebox.showinfo("Success", "Product added successfully!")
                    #refresh sales
                    self.app.pages["Sales"].refresh_pages()
                    self.refresh_table_inDashboard()
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

        # ======= FOCUS =======
        entry_id.focus_force()
        self.refresh_cards()
    
     

        
        
        

    


    
   



#======================Functionalities==========================

#On changed value -> search section
    def on_text_change(self,*args,column):

        # TV% => start with TV
        # %TV  => END with TV
        # %TV%  => Anywhere has TV

        # I take % syntax here instead of src.config.db.py
        products = self.db.suggestions_product_names(column, f"%{self.search_var.get()}%")
        self.reset_table()

        #insert
        self.insert_table(products)

#Sort + Filter => corresponding buttons
    def sort_action(self,column= "MaSP", ):
        self.false = not self.false
        ascending = self.false
        self.reset_table()
        values = self.db.sort_products_by_column("MaSP",ascending)
        
        #
        self.insert_table(values)
        


    def filter_action(self):
        columns = {
            "Mã sản phẩm": "MaSP",
            "Tên sản phẩm": "TenSP",
            "Nhà cung cấp": "NhaCC"
        }
        self.reset_table()
        
        
        filter_value = self.search_entry.get()
         
        values = self.db.filter_products(columns[self.column_combo.get()], filter_value)
        
        #
        self.insert_table(values)

#Select the value on table => called: selected items
    def get_selected_product(self):
        selected_item = self.devices_Table.focus()  # lấy item đang được chọn
        if not selected_item:
            messagebox.showinfo("Notice", "Please select a product to update.")
            return None

        values = self.devices_Table.item(selected_item, "values" )  # lấy giá trị từng cột = values là option để lấy
        return values  # Trả về tuple: (MaSP, TenSP, SLConLai, SoTien, Nha_CC, NgayNhap)
    
#===========================Sub pages =====================
    def open_update_product_page(self):
       
        data = self.get_selected_product()
        if not data:
            return

        MaSP, TenSP, SLConLai, SoTien, Nha_CC, NgayNhap = data
    
        #so tien has vnd at last - need to remove it
        SoTien = int(''.join(filter(str.isdigit, SoTien)))

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
            self.db.updateProducts(MaSP, new_name, new_quantity, new_price, new_provider, new_date)
            messagebox.showinfo("Success", "Product updated successfully!")
            self.refresh_table_inDashboard()  # cập nhật lại giao diện
            self.app.pages["Sales"].refresh_pages()
            update_product_window.destroy()
            

        ctk.CTkButton(update_product_window, text="Save", command=save_changes).pack(pady=10)


    def open_delete_product_page(self):
      
        data = self.get_selected_product()
        if not data:
            return

        MaSP, TenSP, SLConLai, SoTien, Nha_CC, NgayNhap = data

        #ask for confirmation
        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete product '{TenSP}' (ID: {MaSP})?")
        if confirm:
            self.db.deleteProducts(MaSP)
            messagebox.showinfo("Success", "Product deleted successfully!")
            self.refresh_table_inDashboard()
            self.app.pages["Sales"].refresh_pages()
        else:
            messagebox.showinfo("Cancelled", "Product deletion cancelled.")

       
        self.refresh_table_inDashboard()  # cập nhật lại giao diện
    