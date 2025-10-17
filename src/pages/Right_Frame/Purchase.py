'''
Requirements
 - Can add the items into the table below 
 - Can save the table into mssql + change the history + increase the number of products currently+ cards in dashboard
'''


import customtkinter as ctk

class Purchase:
    def __init__(self, parent, app):
        print("Success - purchase")

        self.app = app

        # Frame chính
        self.frame = ctk.CTkFrame(parent, corner_radius=10)
        self.frame.pack(fill="both", expand=True, padx=16, pady=16)

        # Tiêu đề
        ctk.CTkLabel(
            self.frame,
            text="Nhập hàng",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(anchor='w')

        # Top bar
        top = ctk.CTkFrame(self.frame, fg_color="transparent")
        top.pack(fill='x', pady=8)

        # Nhà cung cấp
        ctk.CTkLabel(top, text="Nhà cung cấp").pack(side='left', padx=4)
        self.supplier_var = ctk.StringVar(value="Nhà cung cấp A")
        ctk.CTkOptionMenu(
            top,
            variable=self.supplier_var,
            values=["Nhà cung cấp A", "Nhà cung cấp B"],
            width=160
        ).pack(side='left', padx=6)

        # Tìm sản phẩm
        ctk.CTkLabel(top, text="Tìm sản phẩm:").pack(side='left', padx=8)
        self.psearch = ctk.CTkEntry(top, placeholder_text="Nhập tên sản phẩm...")
        self.psearch.pack(side='left', padx=4)

        ctk.CTkButton(
            top,
            text="Thêm vào phiếu",
            command=self._add_item_mock  # tạm thời mock
        ).pack(side='left', padx=6)

        # Danh sách sản phẩm (thay Listbox bằng Textbox để đồng bộ giao diện)
        self.items = []
        self.items_list = ctk.CTkTextbox(
            self.frame,
            height=250,
            font=ctk.CTkFont(size=13),
            wrap="none"
        )
        self.items_list.pack(fill='both', expand=True, pady=8)

        # Khu vực nút và tổng tiền
        btns = ctk.CTkFrame(self.frame, fg_color="transparent")
        btns.pack(pady=6)

        ctk.CTkButton(btns, text="Lưu phiếu nhập", command=self._save_mock).pack(side='left', padx=6)
        self.total_lbl = ctk.CTkLabel(self.frame, text="Tổng: 0 VNĐ", font=ctk.CTkFont(size=14, weight="bold"))
        self.total_lbl.pack(pady=6)

    # --------- MOCK FUNCTION (thay vì logic thực tế) ----------
    def _add_item_mock(self):
        name = self.psearch.get().strip() or "Sản phẩm A"
        qty = 2
        price = 50000
        total = qty * price
        self.items.append({'name': name, 'qty': qty, 'price': price, 'total': total})
        self._refresh()

    def _refresh(self):
        self.items_list.delete("1.0", "end")
        total = 0
        for it in self.items:
            line = f"{it['name']} | SL: {it['qty']} | ĐG: {it['price']:,} VNĐ | TT: {it['total']:,} VNĐ\n"
            self.items_list.insert("end", line)
            total += it['total']
        self.total_lbl.configure(text=f"Tổng: {total:,} VNĐ")

    def _save_mock(self):
        if not self.items:
            ctk.CTkMessagebox(title="Rỗng", message="Phiếu nhập rỗng", icon="info")
            return
        # Thông báo dạng toast
        self.app.show_toast(self.app.root, "Lưu phiếu nhập thành công")
        self.items = []
        self._refresh()
