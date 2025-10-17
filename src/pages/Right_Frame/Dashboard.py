'''
Requirements

  - Enhance 3 cards to show the total revenue - the total orders - the low stock 
  - Add the frame to contain
      - frame 
        -   Button add - upgrade - delete (create the box to tick and choose)
        -   Filter - Sort A-Z - Search (autofill + recommend)

      - Table of products:  => change based on the frames above
'''

import customtkinter as ctk

class Dashboard:
    def __init__(self, parent):

        # Frame chính của Dashboard
        self.frame = ctk.CTkFrame(parent, corner_radius=10)
        self.frame.pack(fill="both", expand=True, padx=12, pady=12)

        # Header
        header = ctk.CTkLabel(self.frame, text="Dashboard", font=ctk.CTkFont(size=18, weight="bold"))
        header.pack(anchor="w")

        # Card thống kê nhanh
        cards = ctk.CTkFrame(self.frame, fg_color="transparent")
        cards.pack(fill="x", pady=10)

        self.card_revenue = self._card(cards, "Tổng doanh thu hôm nay", "0")
        self.card_orders = self._card(cards, "Số đơn bán hôm nay", "0")
        self.card_lowstock = self._card(cards, "Sản phẩm sắp hết (<10)", "0")

       #Table

        

    def _card(self, parent, title, value):
        """ Tạo 1 thẻ thống kê nhỏ """
        card = ctk.CTkFrame(parent, corner_radius=8)
        card.pack(side='left', padx=6)

        ctk.CTkLabel(card, text=title, font=ctk.CTkFont(size=12, weight="bold")).pack(pady=(4, 2))
        lbl_val = ctk.CTkLabel(card, text=value, font=ctk.CTkFont(size=14))
        lbl_val.pack(pady=(0, 4))

        return lbl_val
