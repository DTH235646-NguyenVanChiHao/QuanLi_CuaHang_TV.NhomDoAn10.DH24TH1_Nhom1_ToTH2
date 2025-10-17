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

class History:
    def __init__(self, parent, app):
        print("Success - History")
        self.app = app

        # Frame chính
        self.frame = ctk.CTkFrame(parent, corner_radius=10)
        self.frame.pack(fill="both", expand=True, padx=16, pady=16)

        # Tiêu đề
        ctk.CTkLabel(
            self.frame,
            text="Lịch sử giao dịch",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(anchor='w')

        # Tabs khu vực lựa chọn loại giao dịch
        tabs = ctk.CTkFrame(self.frame, fg_color="transparent")
        tabs.pack(fill='x', pady=8)

        ctk.CTkButton(
            tabs,
            text="Hoá đơn bán",
            command=lambda: self._load('sales'),
            width=140
        ).pack(side='left', padx=6)

        ctk.CTkButton(
            tabs,
            text="Phiếu nhập",
            command=lambda: self._load('purchases'),
            width=140
        ).pack(side='left', padx=6)

        # Danh sách giao dịch
        self.listbox = ctk.CTkTextbox(
            self.frame,
            height=400,
            font=ctk.CTkFont(size=13),
            wrap="none"   # không xuống dòng tự động
        )
        self.listbox.pack(fill='both', expand=True, pady=8)

        # Mặc định load sales
        self._load('sales')

    def _load(self, mode):
        # Xoá nội dung cũ
        self.listbox.delete("1.0", "end")

        # Dữ liệu mẫu
        if mode == 'sales':
            for i in range(1, 8):
                self.listbox.insert(
                    "end",
                    f"HD{i:03d} | 10:3{i} | Khách hàng A | {i*100000:,} VNĐ | ✅ Đã thanh toán\n"
                )
        else:
            for i in range(1, 6):
                self.listbox.insert(
                    "end",
                    f"PN{i:03d} | 09:2{i} | NCC B | {i*150000:,} VNĐ | 📦 Đã nhập\n"
                )
