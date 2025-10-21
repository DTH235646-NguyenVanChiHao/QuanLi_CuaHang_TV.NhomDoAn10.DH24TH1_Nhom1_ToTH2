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

        except pyodbc.Error as ex:
    
            print(ex)

        # def insertProducts(id, TenSP,SLConLai,SoTien,Nha_CC,NgayNhap):

        # def insertBill(id,NgayNhap, ThanhTien , SoLuong , DonGia,NgayMua, TenKhachHang,Sdt_KhachHang,TenNV_Nhap)
        
        # def updateProducts(id, TenSP,SLConLai,SoTien,Nha_CC,NgayNhap):
        # def updateBill(id,NgayNhap, ThanhTien , SoLuong , DonGia,NgayMua, TenKhachHang,Sdt_KhachHang,TenNV_Nhap)

        # def deleteProducts(id, TenSP,SLConLai,SoTien,Nha_CC,NgayNhap):
        # def deleteBill(id,NgayNhap, ThanhTien , SoLuong , DonGia,NgayMua, TenKhachHang,Sdt_KhachHang,TenNV_Nhap)

# Ví dụ sử dụng:
db = DB('SQL Server', 'ADMIN-PC\\SQLEXPRESS', 'Quan_Li_TV')


#f -> format : pass the arguments
#{driver} => {sql server} ; {{ }} = { }
# 
# Do đó, khi viết ADMIN-PC\SQLEXPRESS, Python sẽ hiểu \S là lỗi.
# → Cần viết ADMIN-PC\\SQLEXPRESS để giữ đúng ký tự \. 