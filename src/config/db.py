#MSP1 is the default id of products
#MHD1 is the default id of receipts

import pyodbc

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

    def insertProducts(self, table_name, id, TenSP, SLConLai, SoTien, Nha_CC, NgayNhap):
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

   

# TEST
db = DB('SQL Server', 'ADMIN-PC\\SQLEXPRESS', 'Quan_Li_TV')

