#MSP1 is the default id of products
#MHD1 is the default id of receipts

import pyodbc
from datetime import date

class DB:
    def __init__(self, driver_name, server_name, db_name):
        self.connect(driver_name, server_name, db_name)

    def connect(self, driver, server, database_name):
        try:
            connection = pyodbc.connect(
                f"DRIVER={{{driver}}};"
                f"SERVER={server};"
                f"DATABASE={database_name};"
                "Trusted_Connection=yes;"
            )
           
            print("Connected to database successfully!")
            self.conn = connection  # Lưu connection để dùng sau này
            self.cursor = self.conn.cursor()

        except pyodbc.Error as ex:
            print(ex)
        

    def searchTable(self, table_name):
        try:
            self.cursor.execute(f"SELECT * FROM {table_name}")
            rows = self.cursor.fetchall()  # Lấy kết quả
            print("Search thanh cong")
            return rows  # Trả về kết quả
        except pyodbc.Error as ex:
            print(f"Lỗi: {ex}")
            return []
        
    def get_sales_history(self):
        try:
            query = """
                SELECT 
                    hd.MaHD,
                    hd.NgayLap,
                    sp.TenSP,
                    cthd.SoLuong,
                    cthd.DonGia,
                    cthd.ThanhTien,
                    hd.TongTien
                FROM HoaDon AS hd
                INNER JOIN ChiTietHoaDon AS cthd ON hd.MaHD = cthd.MaHD
                INNER JOIN SanPham AS sp ON sp.MaSP = cthd.MaSP
                ORDER BY hd.NgayLap DESC
            """
            self.cursor.execute(query)
            rows = self.cursor.fetchall()
            print("✅ Lấy lịch sử bán hàng thành công")
            return rows
        except pyodbc.Error as ex:
            print(f"❌ Lỗi khi truy vấn: {ex}")
            return []


    def insertProducts(self,id, TenSP, SLConLai, SoTien, Nha_CC, NgayNhap):
        try:
            self.cursor.execute("INSERT INTO SanPham VALUES (?, ?, ?, ?, ?, ?)",
                          (id, TenSP, SLConLai, SoTien, Nha_CC, NgayNhap))
            self.conn.commit()
            print("Thêm sản phẩm thành công!")
        except pyodbc.Error as ex:
            print(f"Lỗi: {ex}")

    def insertBill(self, MaHD, MaSP, NgayLap, ThanhTien, SoLuong, DonGia, NgayMua, TenKhachHang, Sdt_KhachHang, TenNV_Nhap):
        try:
            # Thêm vào bảng HoaDon
            self.cursor.execute("INSERT INTO HoaDon VALUES (?, ?, ?)",
                          (MaHD, NgayLap, ThanhTien))
        
            # Thêm vào bảng ChiTietHoaDon
            self.cursor.execute("INSERT INTO ChiTietHoaDon (MaHD, MaSP, SoLuong, DonGiaBan, NgayMua, TenKH, SDT, TenNV) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                          (MaHD, MaSP, SoLuong, DonGia, NgayMua, TenKhachHang, Sdt_KhachHang, TenNV_Nhap))
        
            self.conn.commit()
            print("Thêm hóa đơn thành công!")
        except pyodbc.Error as ex:
            print(f"Lỗi: {ex}")

    def updateProducts(self, id, TenSP, SLConLai, SoTien, Nha_CC, NgayNhap):
        try:
            self.cursor.execute("""
            UPDATE SanPham 
            SET TenSP = ?, SLConLai = ?, SoTien = ?, NhaCC = ?, NgayNhap = ? 
            WHERE MaSP = ?
            """, (TenSP, SLConLai, SoTien, Nha_CC, NgayNhap, id))
            self.conn.commit()
            print("Cập nhật sản phẩm thành công!")
        except pyodbc.Error as ex:
            print(f"Lỗi: {ex}")

    def updateBill(self, MaHD, MaSP, NgayLap, ThanhTien, SoLuong, DonGia, NgayMua, TenKhachHang, Sdt_KhachHang, TenNV_Nhap):
        try:
            # Cập nhật bảng HoaDon
            self.cursor.execute("""
            UPDATE HoaDon 
            SET NgayLap = ?, ThanhTien = ? 
            WHERE MaHD = ?
            """, (NgayLap, ThanhTien, MaHD))
        
            # Cập nhật bảng ChiTietHoaDon
            self.cursor.execute("""
            UPDATE ChiTietHoaDon 
            SET SoLuong = ?, DonGiaBan = ?, NgayMua = ?, TenKH = ?, SDT = ?, TenNV = ? 
            WHERE MaHD = ? AND MaSP = ?
            """, (SoLuong, DonGia, NgayMua, TenKhachHang, Sdt_KhachHang, TenNV_Nhap, MaHD, MaSP))
        
            self.conn.commit()
            print("Cập nhật hóa đơn thành công!")
        except pyodbc.Error as ex:
            print(f"Lỗi: {ex}")

    def deleteProducts(self, id):
        try:
            self.cursor.execute("DELETE FROM SanPham WHERE MaSP = ?", (id,))
            self.conn.commit()
            print("Xóa sản phẩm thành công!")
        except pyodbc.Error as ex:
            print(f"Lỗi: {ex}")

    def deleteBill(self, MaHD, MaSP=None):
        try:
            # Add masp to delete one products, otherwise delete all
            if MaSP is None:
                self.cursor.execute("DELETE FROM ChiTietHoaDon WHERE MaHD = ?", (MaHD,))
                self.cursor.execute("DELETE FROM HoaDon WHERE MaHD = ?", (MaHD,))
            else:
                self.cursor.execute("DELETE FROM ChiTietHoaDon WHERE MaHD = ? AND MaSP = ?", (MaHD, MaSP))
    
            self.conn.commit()
            print("Xóa hóa đơn thành công!")
        except pyodbc.Error as ex:
            print(f"Lỗi: {ex}")

#Explain here: check if product id exists in database
    def is_exist(self, id):
        self.cursor.execute("SELECT COUNT(*) FROM SanPham WHERE MaSP = ?", (id,))
        return self.cursor.fetchone()[0] > 0
    
    def sort_products_by_column(self, column_name = "MaSP", ascending=True):
        order = "ASC" if ascending else "DESC"
        query = f"SELECT * FROM SanPham ORDER BY {column_name} {order}"
        try:
            self.cursor.execute(query)
            rows = self.cursor.fetchall()
            print(f"Sắp xếp sản phẩm theo {column_name} thành công!")
            return rows
        except pyodbc.Error as ex:
            print(f"Lỗi: {ex}")
            return []

    def filter_products(self, column_name, filter_value):
        query = f"SELECT * FROM SanPham WHERE {column_name} = ?"
        try:
            self.cursor.execute(query, (filter_value,))
            rows = self.cursor.fetchall()
            print(f"Lọc sản phẩm theo {column_name} = {filter_value} thành công!")
            return rows
        except pyodbc.Error as ex:
            print(f"Lỗi: {ex}")
            return []
    def suggestions_product_names(self,column_name, filter_value):
        query = f"SELECT * FROM SanPham WHERE {column_name} LIKE ?"
        try:
            #here is a wildcard search
            self.cursor.execute(query, (filter_value,))
            rows = self.cursor.fetchall()
            print(f"Lọc sản phẩm theo {column_name} = {filter_value} thành công!")
            return rows
        except pyodbc.Error as ex:
            print(f"Lỗi: {ex}")
            return []

    #for card    
    def total_revenue(self):
        try:
            self.cursor.execute("SELECT SUM(ThanhTien) FROM HoaDon")
            total = self.cursor.fetchone()[0]
            print("Tính tổng doanh thu thành công!")
            #
            return total if total is not None else 0
        except pyodbc.Error as ex:
            print(f"Lỗi: {ex}")
            return 0
        
    def count_low_stock_products(self,sap_het_san_pham = 10):
        query = "SELECT COUNT(*) FROM SanPham WHERE SLConLai <= ?"
        try:
            self.cursor.execute(query, (sap_het_san_pham,))
            count = self.cursor.fetchone()[0]
            print("Đếm sản phẩm sắp hết thành công!")
            return count
        except pyodbc.Error as ex:
            print(f"Lỗi: {ex}")
            return 0
    
    def count_orders_today(self):
        #today = ngaylap -> get day == date 
        today_str = date.today().strftime('%Y-%m-%d')
        query = "SELECT COUNT(*) FROM HoaDon WHERE CAST(NgayLap AS DATE) = ?"
        #cast is used to convert datetime to date only
        try:
            self.cursor.execute(query, (today_str,))
            count = self.cursor.fetchone()[0]
            print("Đếm đơn hàng hôm nay thành công!")
            return count
        except pyodbc.Error as ex:
            print(f"Lỗi: {ex}")
            return 0
        
    
    def close(self):
        self.conn.close()
        print("Connection closed.")
        
    
        
        
    
   

# TEST
db = DB('SQL Server', 'ADMIN-PC\\SQLEXPRESS', 'Quan_Li_TV')

