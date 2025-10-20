'''
Requirements
  - Can show the notification after done:  show_toast(self.root, "Thanh toán thành công")
  - add log out button 
  - add avatar
'''

import customtkinter as ctk
from PIL import Image
from src.pages.Login.main import LoginPage

from src.pages.Right_Frame.Dashboard import Dashboard
from  src.pages.Right_Frame.History import History
from  src.pages.Right_Frame.Sales import Sales
from  src.pages.Right_Frame.Purchase import Purchase

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("POS Application")
        self.root.geometry("1280x660+0+0")

        #Logo + Name
        


          # Logo + Name container
        self.container_logo_name = ctk.CTkFrame(self.root, height=700, fg_color="#3CB251",corner_radius=0)
        self.container_logo_name.pack(fill="x", side="top")   # pack it first

        #Log
        my_image = ctk.CTkImage(light_image=Image.open("src/assets/heart.png"),
                                  
                                  size=(18, 18))
        #Name
        self.app_name_label = ctk.CTkLabel(
            self.container_logo_name,
            image=my_image,
            text="Orian Chi",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="white",compound="left",padx="10"
        )
        self.app_name_label.pack(side="left")

        # Container chính
        self.container = ctk.CTkFrame(self.root,fg_color = "#D8E0D9")
        self.container.pack(fill="both", expand=True)

        # Left navigation
        self.left_nav = ctk.CTkFrame(self.container, width=260, corner_radius=0,fg_color="#FFFFFF")
        self.left_nav.pack(side="left", fill="y")

        # Right content
        self.right_content = ctk.CTkFrame(self.container, corner_radius=0)
        self.right_content.pack(side="right", fill="both", expand=True)

        self._build_navbar()
        self._build_pages()

    def logout(self):
        self.frame.destroy()
        LoginPage(self.root, on_login_success=self._show_main_app)

    def _build_navbar(self):
        # Header
        header = ctk.CTkLabel(self.left_nav, text="POS System", font=ctk.CTkFont(size=16, weight="bold"))
        header.pack(pady=16)

        buttons = [
            ("Dashboard", lambda: self.show_page("Dashboard")),
            ("Sales", lambda: self.show_page("Sales")),
            ("History", lambda: self.show_page("History")),
            ("Log out",lambda: self.logout())
        ]

          #Chu to hon - dam hon

          #Transparent = opacity = 0
        for (text, cmd) in buttons:
            b = ctk.CTkButton(
                  self.left_nav,
                  text=text,
                 command=cmd,
                 fg_color="transparent",            # nền trong suốt = default is blue
                  text_color=["#8C8C8C", "#000000"], # chữ mờ -> đậm khi hover/nhấn
                 hover_color="#D9D9D9"              # nền sáng khi hover
                )
            b.pack(fill="x", padx=12, pady=6)

          #Them nut logout

    def _build_pages(self):
        self.pages = {}

        #This is objects 
        #this.pages.dashboard = new dashboard()
        #Don't use because python automatically invoke constructor (__init__)
        
        self.pages["Dashboard"] = Dashboard(self.right_content)
        self.pages["Sales"] = Sales(self.right_content, self)
        self.pages["Purchase"] = Purchase(self.right_content, self)
        self.pages["History"] = History(self.right_content, self)

        #Access frame (this is a properties of each classes)
        for page in self.pages.values():
            page.frame.place(relx=0, rely=0, relwidth=1, relheight=1)

    def show_page(self, name):
        page = self.pages.get(name)
        if page:
            #Tkraise will give priority to the page, which is invoked by button
            page.frame.tkraise()

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


def start_app():
    ctk.set_appearance_mode("System")  # "Light" hoặc "Dark"
    ctk.set_default_color_theme("blue")  # theme mặc định

    root = ctk.CTk()

    # def show_main():
    MainApp(root)
    #Pass show_main into login => success -> login + call show main, which is containing maiapp()
    # LoginPage(root, on_login_success=show_main)

    root.mainloop()


if __name__ == '__main__':
    start_app()
