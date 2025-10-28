'''
Requirements
  - Can show the notification after done:  show_toast(self.root, "Thanh toán thành công")
  - add log out button 
  - add avatar

  bd: "#D8E0D9"
  main_widgets: 
'''


import customtkinter as ctk
from tkinter import ttk
from PIL import Image
from tkinter import messagebox
import os 


#Pages
from src.pages.Login.main import LoginPage
from src.pages.Right_Frame.Dashboard import Dashboard
from  src.pages.Right_Frame.History import History
from  src.pages.Right_Frame.Sales import Sales

from src.config.db import DB

# ----- My weakness -------
# from  src.pages.Right_Frame.Purchase import Purchase

class MainApp:

  
    # self.db = DB('SQL Server', 'ADMIN-PC\\SQLEXPRESS', 'Quan_Li_TV')
    def __init__(self, root):

        #connect db 
        self.db = DB('SQL Server', 'ADMIN-PC\\SQLEXPRESS', 'Quan_Li_TV')

        
        #set style treeview
        self.TreeView_Style()
        #root = window app 
        self.root = root
        self.root.title("POS Application")
        self.root.geometry("1280x660+0+0") # 0 0 -> Điểm xuất khi bắt đầu app (top - left)

        # Khi người dùng đóng cửa sổ, đóng DB trước khi thoát
        self.root.protocol("WM_DELETE_WINDOW", lambda: closing_app(self.root, self.db))
        #Logo + Name
        


          # Logo + Name container
        self.container_logo_name = ctk.CTkFrame(self.root, height=700, fg_color="#3CB251",corner_radius=0)
        self.container_logo_name.pack(fill="x", side="top")   # pack it first
        self._build_info_sections()

        # Container chính
        self.container = ctk.CTkFrame(self.root,fg_color = "#D8E0D9")
        self.container.pack(fill="both", expand=True)

        # Left navigation
        self.left_nav = ctk.CTkFrame(self.container, width=260, corner_radius=0,fg_color="#2D3748")
        self.left_nav.pack(side="left", fill="y")
        self._build_navbar()

        # Right content
        self.right_content = ctk.CTkFrame(self.container, corner_radius=0)
        self.right_content.pack(side="right", fill="both", expand=True)
        self._build_pages()



       
#Main background = 
#Main text color
#Main 
   

    

    



#=========================GUI================================================
##Set style
    def TreeView_Style(self):
        #set style
         style = ttk.Style()
         style.configure("Treeview", font=("Arial", 12))          # Phóng to chữ trong bảng
         style.configure("Treeview.Heading", font=("Arial", 13, "bold"))  # Phóng to tiêu đề cột
##Build Nav
    def _build_navbar(self):
        # This will be create the blank => for visual
        header = ctk.CTkLabel(self.left_nav, text="", font=ctk.CTkFont(size=32, weight="bold"))
        header.pack(pady=16)

        buttons = [
            ("Dashboard", lambda: self._show_page("Dashboard")),
            ("Sales", lambda: self._show_page("Sales")),
            ("History", lambda: self._show_page("History")),
            #Cannot log out
            ("Log out",lambda : self._logout())
        ]

          #Chu to hon - dam hon

          #Transparent = opacity = 0
        for (text, cmd) in buttons:
            b = ctk.CTkButton(
                  self.left_nav,
                  text=text,
                 command=cmd,
                 
                 corner_radius=0,
                 fg_color="transparent",            # nền trong suốt = default is blue
                  text_color="#DCDADA", # chữ mờ -> đậm khi hover/nhấn
                 hover_color="#FCF7F7" ,
                              font=('Roboto', 20)             # nền sáng khi hover
                )
            b.pack(fill="x", pady = 30)
##Build Images
    def _build_info_sections(self):
        #Log
        my_image = ctk.CTkImage(light_image=Image.open("src/assets/heart.png"),
                                  size=(18, 18))
        
        # Avatar
        avatar_image = ctk.CTkImage(light_image=Image.open("src/assets/heart.png"), size=(36, 36))
        self.avatar_label = ctk.CTkLabel(
            self.container_logo_name,
            image=avatar_image,
            text="",
            corner_radius=100
        )
        self.avatar_label.image = avatar_image  # giữ tham chiếu tránh bị xóa bộ nhớ
        self.avatar_label.pack(side="right", padx=20)

        #Name
        self.app_name_label = ctk.CTkLabel(
            self.container_logo_name,
            image=my_image,
            text="Orian Chi",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="white",compound="left",padx="10"
        )
        self.app_name_label.pack(side="left")

#=========================Functionalities===================================
# _method = protected => only parent + its children
# _ _method = private  => only its own class

##Build Pages 
    def _build_pages(self):
        self.pages = {}

        #This is objects 
        #this.pages.dashboard = new dashboard()
        #Don't use because python automatically invoke constructor (__init__)
        
        self.pages["Dashboard"] = Dashboard(self.right_content,self.db,self)
        self.pages["Sales"] = Sales(self.right_content, self,self.db)
        self.pages["History"] = History(self.right_content, self,self.db)

        #Access frame (this is a properties of each classes)
        for page in self.pages.values():
            page.frame.place(relx=0, rely=0, relwidth=1, relheight=1)

    def _show_page(self, name):
        page = self.pages.get(name)
        if page:
            #Tkraise will give priority to the page, which is invoked by button
            page.frame.tkraise()
##Log off
    def _logout(self):
        if messagebox.askokcancel("Log out", "Do you want to log out?"):
            try:
                self.db.close()  # đóng kết nối hiện tại
            except Exception as e:
                print(f"Error closing DB: {e}")

        # Xóa các frame hiện có
        for widget in self.root.winfo_children():
            widget.destroy()

        # Quay lại trang Login
        LoginPage(self.root, on_login_success=lambda: MainApp(self.root))
#==========================static==========================================
    @staticmethod
    def show_toast(master, text, duration=2000):
        toast = ctk.CTkToplevel(master)
        toast.overrideredirect(True)
        toast.attributes("-topmost", True)

        label = ctk.CTkLabel(toast, text=text, fg_color="#333", text_color="white", corner_radius=8, padx=10, pady=6)
        label.pack()

        master.update_idletasks()
        x = master.winfo_x() + master.winfo_width() - toast.winfo_reqwidth() - 20
        y = master.winfo_y() + master.winfo_height() - toast.winfo_reqheight() - 40
        toast.geometry(f"+{x}+{y}")

        master.after(duration, toast.destroy)


#=======================End MainApp class====================================
#======================Start Up The Application =============================


def closing_app(root,db): #Log out
    if messagebox.askokcancel("Exit", "Do you want to exit the application?"):
        try:
            db.close()  # ✅ Đóng kết nối
        except Exception as e:
            print(f"Error closing DB: {e}")
        root.destroy()  # ✅ Thoát ứng dụng

def start_app():#Log in
    ctk.set_appearance_mode("System")  # "Light" hoặc "Dark"
    ctk.set_default_color_theme("blue")  # theme mặc định

    root = ctk.CTk()

    def show_main():
        main =   MainApp(root)

    #Pass show_main into login => success -> login + call show main, which is containing mainapp()
    LoginPage(root, on_login_success=show_main)
    root.mainloop()

if __name__ == '__main__':
    start_app()
