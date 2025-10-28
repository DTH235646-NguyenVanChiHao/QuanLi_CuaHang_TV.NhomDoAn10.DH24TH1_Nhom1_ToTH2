#MSP1 is the default id of products
#MHD1 is the default id of receipts

import pyodbc
from datetime import date

#Products -> the devices like Television - Headphone ...
#Bill -> customer will buy and pay. they can get the receipt after that
class DB:
    #auto connect
    def __init__(self, driver_name, server_name, db_name):
        self.connect(driver_name, server_name, db_name)

#========================Connection========================
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
        
#====================Search====================================
    def searchTable(self, table_name):
        try:
            self.cursor.execute(f"SELECT * FROM {table_name}")
            rows = self.cursor.fetchall()  # Lấy kết quả
            print("Search thanh cong")
            return rows  # Trả về kết quả
        except pyodbc.Error as ex:
            print(f"Lỗi: {ex}")
            return []
    
    #In sales => create the frame and show the value (not a table)
    def getItems_Products(self):
        query = f'''
            select MaSP,TenSP , DonGiaBan, SLConLai
            from SanPham
        '''
        try:
            self.cursor.execute(query)
            rows = self.cursor.fetchall()  # Lấy kết quả
            print("Search thanh cong")
            return rows  # Trả về kết quả
        except pyodbc.Error as ex:
            print(f"Lỗi: {ex}")
            return []
        
    #bill + detail bill + product => in history page
    def get_sales_history(self):
        query = """
            SELECT 
                hd.MaHD AS N'Mã HĐ',
                sp.MaSP AS N'Mã SP',
                hd.TenKH AS N'Tên khách hàng',
                hd.SDT AS N'Số điện thoại',
                sp.TenSP AS N'Tên sản phẩm',
                cthd.SoLuong AS N'Số lượng',
                sp.DonGiaBan AS N'Đơn giá bán',
                (cthd.SoLuong * sp.DonGiaBan) AS N'Thành tiền',
                hd.TenNVLap AS N'Tên nhân viên lập',
                hd.NgayLapHD AS N'Ngày lập hóa đơn'
            FROM HoaDon hd
            INNER JOIN ChiTietHoaDon cthd ON hd.MaHD = cthd.MaHD
            INNER JOIN SanPham sp ON cthd.MaSP = sp.MaSP;
        """
        try:
            
            self.cursor.execute(query)
            rows = self.cursor.fetchall()
            print("✅ Lấy lịch sử bán hàng thành công")
            return rows
        except pyodbc.Error as ex:
            print(f"❌ Lỗi khi truy vấn: {ex}")
            return []

#================================Additions=====================================
    def insertProducts(self,id, TenSP, SLConLai, DonGiaBan, Nha_CC, NgayNhap):
        try:
            self.cursor.execute("INSERT INTO SanPham VALUES (?, ?, ?, ?, ?, ?)",
                          (id, TenSP, SLConLai, DonGiaBan, Nha_CC, NgayNhap))
            self.conn.commit()
            print("Thêm sản phẩm thành công!")
        except pyodbc.Error as ex:
            print(f"Lỗi: {ex}")

    
    
    def insertBill(self, NgayLap, TenKhachHang, Sdt_KhachHang, TenNV_Nhap, MaSP, SoLuong):
        try:
            # 1. Thêm vào bảng HoaDon
            MaHD = self.generate_mahd()

            self.cursor.execute("""
                INSERT INTO HoaDon (MaHD, NgayLapHD, TenKH, SDT, TenNVLap)
                VALUES (?, ?, ?, ?, ?)
            """, (MaHD, NgayLap, TenKhachHang, Sdt_KhachHang, TenNV_Nhap))

            # 2. Thêm vào bảng ChiTietHoaDon
            self.cursor.execute("""
                INSERT INTO ChiTietHoaDon (MaHD, MaSP, SoLuong)
                VALUES (?, ?, ?)
            """, (MaHD, MaSP, SoLuong))
            
            #3 : update số lượng
            self.cursor.execute('''
                UPDATE SanPham 
                SET SLConLai = SLConLai - ?
                WHERE MaSP = ?
            ''',(SoLuong, MaSP))
            # 3. Lưu thay đổi
            self.conn.commit()
            print("✅ Thêm hóa đơn và chi tiết hóa đơn thành công!")
    
        except pyodbc.Error as ex:
            print(f"❌ Lỗi khi thêm hóa đơn: {ex}")

#==============================Update=============================================
    def updateProducts(self, id, TenSP, SLConLai, DonGiaBan, Nha_CC, NgayNhap):
        try:
            #Update all because you don't know where is changed
            self.cursor.execute("""
            UPDATE SanPham 
            SET TenSP = ?, SLConLai = ?, DonGiaBan = ?, NhaCC = ?, NgayNhap = ? 
            WHERE MaSP = ?
            """, (TenSP, SLConLai, DonGiaBan, Nha_CC, NgayNhap, id))
            self.conn.commit()
            print("Cập nhật sản phẩm thành công!")
        except pyodbc.Error as ex:
            print(f"Lỗi: {ex}")

    def updateBill(self, MaHD, MaSP, NgayLap, SoLuong, TenKhachHang, Sdt_KhachHang, TenNV_Nhap):
        try:
            # 1️ Lấy số lượng cũ trong bảng ChiTietHoaDon
            self.cursor.execute("""
            SELECT SoLuong FROM ChiTietHoaDon
            WHERE MaHD = ? AND MaSP = ?
            """, (MaHD, MaSP))
            old_qty_row = self.cursor.fetchone()
            old_qty = old_qty_row[0] if old_qty_row else 0

            # 2️ Tính chênh lệch
            SoLuong = int(SoLuong)  # ensure numeric type
            delta = SoLuong - int(old_qty)

            # Cập nhật bảng HoaDon
            self.cursor.execute("""
            UPDATE HoaDon 
                SET NgayLapHD = ?, 
                    TenKH = ?, 
                    SDT = ?, 
                    TenNVLap = ?
                WHERE MaHD = ?
            """, (NgayLap, TenKhachHang, Sdt_KhachHang, TenNV_Nhap, MaHD))

            # 2. Cập nhật bảng ChiTietHoaDon
            self.cursor.execute("""
                UPDATE ChiTietHoaDon 
                SET SoLuong = ?
                WHERE MaHD = ? AND MaSP = ?
            """, (SoLuong, MaHD, MaSP))

            #3 : update số lượng
            self.cursor.execute('''
                UPDATE SanPham 
                SET SLConLai = SLConLai - ?
                WHERE MaSP = ?
            ''',(delta, MaSP))
            self.conn.commit()
            print("Cập nhật hóa đơn thành công!")
        except pyodbc.Error as ex:
            print(f"Lỗi: {ex}")
#=====================================Delete======================================
    def deleteProducts(self, id):
        try:
            self.cursor.execute("DELETE FROM SanPham WHERE MaSP = ?", (id,))
            self.conn.commit()
            print("Xóa sản phẩm thành công!")
        except pyodbc.Error as ex:
            print(f"Lỗi: {ex}")

    def deleteBill(self, MaHD, SoLuong, MaSP=None):
        try:
            # Add masp to delete one products, otherwise delete all

            if MaSP is None:
                self.cursor.execute("DELETE FROM ChiTietHoaDon WHERE MaHD = ?", (MaHD,))
                self.cursor.execute("DELETE FROM HoaDon WHERE MaHD = ?", (MaHD,))
            else:
                self.cursor.execute("DELETE FROM ChiTietHoaDon WHERE MaHD = ? AND MaSP = ?", (MaHD, MaSP))

            #: update số lượng
            self.cursor.execute('''
                UPDATE SanPham 
                SET SLConLai = SLConLai + ?
                WHERE MaSP = ?
            ''',(SoLuong, MaSP))
            self.conn.commit()
            print("Xóa hóa đơn thành công!")
        except pyodbc.Error as ex:
            print(f"Lỗi: {ex}")
#=================================Helper function==========================================
#Explain here: check if product id exists in database
    def is_exist(self, id):
        self.cursor.execute("SELECT COUNT(*) FROM SanPham WHERE MaSP = ?", (id,))
        return self.cursor.fetchone()[0] > 0


#Automatically Generate the id of bills => ex: HD01 -> HD02
    def generate_mahd(self):
        try:
            self.cursor.execute("SELECT TOP 1 MaHD FROM HoaDon ORDER BY MaHD DESC")
            last_row = self.cursor.fetchone()

            if not last_row or not last_row[0]:
                return "HD01"
    
            last_mahd = last_row[0]
            num = int(last_mahd.replace("HD", ""))
            new_num = num + 1
            return f"HD{new_num:02d}"  # Ví dụ: HD005 → HD006
        
        #Dùng :02d, :03d, :05d, ... chỉ đặt độ dài tối thiểu, không giới hạn độ dài tối đa.
        #Nếu số vượt mức đó, Python vẫn hiển thị đầy đủ giá trị thật.
    
        except pyodbc.Error as ex:
            print(f"❌ Lỗi khi thêm hóa đơn: {ex}")

#for card    in dashboard
    def total_revenue(self):
        query = """
            SELECT 
                SUM(cthd.SoLuong * sp.DonGiaBan) AS TongDoanhThu
            FROM HoaDon hd
            INNER JOIN ChiTietHoaDon cthd ON hd.MaHD = cthd.MaHD
            INNER JOIN SanPham sp ON cthd.MaSP = sp.MaSP;
        """
        try:
            self.cursor.execute(query)
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
        query = "SELECT COUNT(*) FROM HoaDon WHERE CAST(NgayLapHD AS DATE) = ?"
        #cast is used to convert datetime to date only
        try:
            self.cursor.execute(query, (today_str,))
            count = self.cursor.fetchone()[0]
            print("Đếm đơn hàng hôm nay thành công!")
            return count
        except pyodbc.Error as ex:
            print(f"Lỗi: {ex}")
            return 0
        
    
    
#===============================Sort + FIlter================================
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
        
    def sort_receipts_by_column(self, column_name = "MaHD", ascending=True):
        
        order = "ASC" if ascending else "DESC"
        query = f'''
            SELECT 
                hd.MaHD AS "Mã HĐ",
                sp.MaSP AS "Mã SP",
                hd.TenKH AS "Tên KH",
                hd.SDT AS "Số điện thoại",
                sp.TenSP AS "Tên sản phẩm",
                cthd.SoLuong AS "Số lượng",
                sp.DonGiaBan AS "Đơn giá bán",
                (cthd.SoLuong * sp.DonGiaBan) AS "Thành tiền",
                hd.TenNVLap AS "Tên NV",
                hd.NgayLapHD AS "Ngày lập"
            FROM HoaDon hd
            INNER JOIN ChiTietHoaDon cthd ON hd.MaHD = cthd.MaHD
            INNER JOIN SanPham sp ON cthd.MaSP = sp.MaSP
            ORDER BY {column_name} {order}
        '''
        try:
            self.cursor.execute(query)
            rows = self.cursor.fetchall()
            print(f"Sắp xếp hóa đơn theo {column_name} thành công!")
            return rows
        except pyodbc.Error as ex:
            print(f"Lỗi: {ex}")
            return []

    def sort_products_in_sales_pages(self, column_name = "MaSP", ascending=True):
        order = "ASC" if ascending else "DESC"
        query = f"SELECT MaSP,TenSP , DonGiaBan, SLConLai FROM SanPham ORDER BY {column_name} {order}"
        try:
            self.cursor.execute(query)
            rows = self.cursor.fetchall()
            print(f"Sắp xếp sản phẩm theo {column_name} thành công!")
            return rows
        except pyodbc.Error as ex:
            print(f"Lỗi: {ex}")
            return []
#=============================Filter + suggestion (on changed value)========================  
#Products
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

#Bill -> Sales page + History
    def suggestions_products_in_sales_page(self, filter_value):
        query = f"SELECT MaSP,TenSP , DonGiaBan, SLConLai FROM SanPham WHERE TenSP LIKE ?"
        try:
            #here is a wildcard search
            self.cursor.execute(query, (filter_value,))
            rows = self.cursor.fetchall()
            print(f"Lọc sản phẩm theo TenSP = {filter_value} thành công!")
            return rows
        except pyodbc.Error as ex:
            print(f"Lỗi: {ex}")
            return []
        
    def filter_receipts(self, column_name, filter_value):
        query = f"""
        SELECT 
            hd.MaHD AS N'Mã HĐ',
            sp.MaSP AS N'Mã SP',
            hd.TenKH AS N'Tên khách hàng',
            hd.SDT AS N'Số điện thoại',
            sp.TenSP AS N'Tên sản phẩm',
            cthd.SoLuong AS N'Số lượng',
            sp.DonGiaBan AS N'Đơn giá bán',
            (cthd.SoLuong * sp.DonGiaBan) AS N'Thành tiền',
            hd.TenNVLap AS N'Tên nhân viên lập',
            hd.NgayLapHD AS N'Ngày lập hóa đơn'
        FROM HoaDon hd
        INNER JOIN ChiTietHoaDon cthd ON hd.MaHD = cthd.MaHD
        INNER JOIN SanPham sp ON cthd.MaSP = sp.MaSP
        WHERE {column_name} LIKE ?
        """

        #why using ''' instead of "" => to write multi-line query
        try:
            self.cursor.execute(query, (filter_value,))
            rows = self.cursor.fetchall()
            print(f"Lọc sản phẩm theo {column_name} = {filter_value} thành công!")
            return rows
        except pyodbc.Error as ex:
            print(f"Lỗi: {ex}")
            return []
#==================Close==================================    
    def close(self):
        self.conn.close()
        print("Connection closed.")

    
        
    
        
        
    
   

# TEST
db = DB('SQL Server', 'ADMIN-PC\\SQLEXPRESS', 'Quan_Li_TV')

