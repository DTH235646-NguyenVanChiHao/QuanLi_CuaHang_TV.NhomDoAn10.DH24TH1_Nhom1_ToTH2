import customtkinter as ctk

root = ctk.CTk()
root.geometry("600x300")

frame = ctk.CTkScrollableFrame(root)
frame.pack(fill="both", expand=True, padx=20, pady=20)

# Tiêu đề cột
headers = ["Product", "Price", "Quantity"]
for col, h in enumerate(headers):
    label = ctk.CTkLabel(frame, text=h, font=ctk.CTkFont(weight="bold"))
    label.grid(row=0, column=col, padx=10, pady=5, sticky="w")

# Dữ liệu
data = [
    ("Sữa tươi", "25,000", "30"),
    ("Cà phê hòa tan", "50,000", "12"),
    ("Bánh quy", "35,000", "45"),
    ("Nước ngọt", "20,000", "60"),
]

for r, row in enumerate(data, start=1):
    for c, value in enumerate(row):
        ctk.CTkLabel(frame, text=value).grid(row=r, column=c, padx=10, pady=5, sticky="w")

root.mainloop()
