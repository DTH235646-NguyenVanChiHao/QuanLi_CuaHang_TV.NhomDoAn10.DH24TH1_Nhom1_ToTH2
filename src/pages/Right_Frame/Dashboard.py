import customtkinter as ctk
from tkinter import ttk

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

        # ===== CARDS SECTION =====
        self.cards_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        self.cards_frame.pack(fill="x", pady=10)

        self._create_cards()

        # ===== SEARCH & FILTER BAR =====
        self._create_search_bar()

        # ===== TABLE SECTION =====
        self.frame_table = ctk.CTkFrame(
            self.frame,
            fg_color="#FFFFFF",
            corner_radius=8
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

    # ---------- Search / Filter Section ----------
    def _create_search_bar(self):
        self.frame_search = ctk.CTkFrame(
            self.frame,
            fg_color="#FFFFFF",
            corner_radius=8
        )
        self.frame_search.pack(fill="x", pady=12, padx=6, ipady=6)

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
      # Dùng treeview của Tkinter
      devices_Table = ttk.Treeview(self.frame_table, columns=("id", "name", "quantity","price"), show="headings")
      devices_Table.pack(fill="both", expand=True)

      devices_Table.heading("id", text="Mã sản phẩm")
      devices_Table.heading("name", text="Tên sản phẩm")
      devices_Table.heading("quantity",text="Số lượng còn lại")
      devices_Table.heading("price", text="Giá sản phẩm")

      devices_Table.column("id", width=80, anchor="center")
      devices_Table.column("name", width=200)

      #call load_
      
    #   def load_value():
        

    

