# 🧩 Project Title: Electronic Devices Management System
# 📘 Overview

The Sales Management System is a full-stack desktop application designed to support small and medium-sized enterprises (SMEs) in managing their sales activities effectively. The program allows users to create, update, and track invoices, customers, and products through an intuitive graphical interface.

This project demonstrates my skills in Python (CTkinter) for GUI design, SQL Server for database management, and Object-Oriented Programming (OOP) for maintaining clean, scalable code.

## 🚀 Key Features
- I completely divide the whole program into smaller, which is called modules. The tiny modules alongside OOP design helps my program more reusable and less complex 

- Being likely to connect to database: Addition - Update - Delete. 

- In sales page, the program can add the products into the receipt and conduct calculate the sum of receipt

## 🧱 Technologies Used
- Python + Tkinter + Customtkinter

## 📂 Project Structure
```bash
CHIHIAO_DTH235646_DH24TH1/
│
├── db_scripts/
│   └── SQLQuery1.sql
│
├── src/
│   ├── assets/
│   │   └── heart.png
│   │
│   ├── config/
│   │   └── db.py
│   │
│   ├── pages/
│   │   ├── Login/
│   │   │   └── main.py
│   │   │
│   │   ├── Right_Frame/
│   │   │   ├── Dashboard.py
│   │   │   ├── History.py
│   │   │   └── Sales.py
│   │
│   └── main.py
│
├── README.md
└── studies.txt

```
## ⚙️ Installation
**1. Prerequisites**

- Make sure you have installed the following tools:
    - Python 3.10+
    - SQL Server 2019+
    - pip (Python package manager)

**2. Clone the Repository**

```bash
git clone https://github.com/DTH235646-NguyenVanChiHao/QuanLi_CuaHang_TV.NhomDoAn10.DH24TH1_Nhom1_ToTH2.gitư
```

**3. Install Required Libraries**

```bash
pip install customtkinter pyodbc Pillow tkcalendar
```
**4. Access Your SQL Server Workplace:**
   - Create database:  ***Quan_Li_TV***  
   - Run the script in: db_scripts/SQLQuery1.sql to create tables
   - Test and ensure your database can run the script

**5. Access main.py, detect the following snippet and replace with your own credentials:**

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
Dashboard page: [] 

History page: [] 

Sales page: []

Login page: []


## 🔍 Future Improvements
- In any entry_search_data, I'd would like to add autofill or get suggestions when you enter any words 

- Create Purchase Page to add multiple products and save into database

- Authorize the employees 

- Create Employee table - Consumers Table - Purchase Table


# 🧑‍💻 Author

Name: Nguyen Van Chi Hao

Role: Junior Student at An Giang University

Email: hao_dth235646@student.agu.edu.vn

GitHub: [github.com/](https://github.com/DTH235646-NguyenVanChiHao)

# 📜 License

This project is released under the MIT License, allowing anyone to use, modify, and distribute it for educational or commercial purposes with proper attribution.  
