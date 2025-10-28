# 🧩 Project Title: Electronic Devices Management System
# 📘 Overview

The Sales Management System is a full-stack desktop application designed to support small and medium-sized enterprises (SMEs) in managing their sales activities effectively. The program allows users to create, update, and track invoices, customers, and products through an intuitive graphical interface.

This project demonstrates my skills in Python (CTkinter) for GUI design, SQL Server for database management, and Object-Oriented Programming (OOP) for maintaining clean, scalable code.

## 🚀 Key Features



## 🧱 Technologies Used

## 📂 Project Structure
```bash
SalesManagementSystem/
│
├── src/
│   ├── pages/
│   │   ├── AddProduct.py
│   │   ├── UpdateProduct.py
│   │   ├── History.py
│   │   └── MainFrame.py
│   │
│   ├── database/
│   │   ├── connect.py
│   │   ├── create_tables.sql
│   │   └── query_samples.sql
│   │
│   └── assets/
│       └── icons/
│
├── README.md
└── main.py
```
## ⚙️ Installation
1. Prerequisites
 - Make sure you have installed the following tools
    - Python 3.10+
    - SQL Server 2019+
    - pip (Python package manager)

2. Clone the Repository
```bash
        git clone https://github.com/DTH235646-NguyenVanChiHao/QuanLi_CuaHang_TV.NhomDoAn10.DH24TH1_Nhom1_ToTH2.gitư
```

3. Install Required Libraries
```bash
pip install customtkinter pyodbc Pillow tkcalendar
```


4. Access Your SQL Server Workplace: 
   - Create database:  ***Quan_Li_TV***  
   - Run the script in: db_scripts/SQLQuery1.sql to create tables
   - Test and ensure your database can run the script

5. Access main.py, detect the following snippet and replace with your own credentials:
```python
self.db = DB (Driver , Server , 'Quan_Li_TV')
```
**Example:**
```bash
        Driver = SQL Server
        server = 'PC_name\\SQLEXPRESS'
        database = 'Quan_Li_TV'
```

6. Run the Application
```bash
python main.py
```

## 📊 Example Screenshots



## 🔍 Future Improvements



# 🧑‍💻 Author

Name: Chi Hao

Role: Junior Student at An Giang University

Email: hao_dth235646@student.agu.edu.vn

GitHub: [github.com/](https://github.com/DTH235646-NguyenVanChiHao)

# 📜 License

This project is released under the MIT License, allowing anyone to use, modify, and distribute it for educational or commercial purposes with proper attribution.  