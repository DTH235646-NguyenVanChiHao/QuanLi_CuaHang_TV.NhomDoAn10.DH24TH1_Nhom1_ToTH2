CREATE DATABASE Quan_Li_TV;
GO

USE Quan_Li_TV;
GO







CREATE TABLE HoaDon (
    MaHD VARCHAR(10) PRIMARY KEY,
    NgayLap DATE NOT NULL,
    ThanhTien DECIMAL(18,2) DEFAULT 0
);
GO

CREATE TABLE SanPham (
    MaSP VARCHAR(10) PRIMARY KEY,
    TenSP NVARCHAR(100) NOT NULL,
    SLConLai INT DEFAULT 0,
    SoTien DECIMAL(18,2) DEFAULT 0,
    NhaCC NVARCHAR(100) NOT NULL,
    NgayNhap DATE NOT NULL,
);
GO



CREATE TABLE ChiTietHoaDon (
    MaHD VARCHAR(10) NOT NULL,
    MaSP VARCHAR(10) NOT NULL,
    SoLuong INT NOT NULL,
    DonGiaBan DECIMAL(18,2) NOT NULL,
    NgayMua DATE DEFAULT GETDATE(),
    TenKH VARCHAR(10),
    SDT     VARCHAR(10),
    TenNV  VARCHAR(10),
    PRIMARY KEY (MaHD, MaSP),
    FOREIGN KEY (MaHD) REFERENCES HoaDon(MaHD),
    FOREIGN KEY (MaSP) REFERENCES SanPham(MaSP),
);
GO



---------- Insert

--Khong dung
--insert into SanPham (MaSP,TenSP,SLConLai,SoTien,NhaCC,NgayNhap) 
--values ("MSP1","TV Sony", 10,1000000,"Nha Cung Cap A", "12/9/2024")

--Properway 

INSERT INTO SanPham (MaSP, TenSP, SLConLai, SoTien, NhaCC, NgayNhap) 
VALUES 
('MSP2', N'TV Samsung 43 inch', 15, 8000000, N'Nhà Cung Cấp B', '2024-09-10'),
('MSP3', N'TV LG 65 inch', 5, 15000000, N'Nhà Cung Cấp C', '2024-09-08'),
('MSP4', N'TV TCL 32 inch', 20, 5000000, N'Nhà Cung Cấp A', '2024-09-05'),
('MSP5', N'TV Xiaomi 50 inch', 8, 7000000, N'Nhà Cung Cấp D', '2024-09-15');

INSERT INTO HoaDon (MaHD, NgayLap, ThanhTien)
VALUES 
('HD001', '2024-09-20', 15000000),
('HD002', '2024-09-21', 8000000),
('HD003', '2024-09-22', 22000000),
('HD004', '2024-09-23', 5000000),
('HD005', '2024-09-24', 14000000);

INSERT INTO ChiTietHoaDon (MaHD, MaSP, SoLuong, DonGiaBan, NgayMua, TenKH, SDT, TenNV)
VALUES 
('HD001', 'MSP3', 1, 15000000, '2024-09-20', N'Nguyễn Văn A', '0909123456', N'Trần Thị B'),
('HD001', 'MSP2', 1, 8000000, '2024-09-20', N'Nguyễn Văn A', '0909123456', N'Trần Thị B'),
('HD002', 'MSP2', 1, 8000000, '2024-09-21', N'Lê Thị C', '0918234567', N'Phạm Văn D'),
('HD003', 'MSP1', 2, 10000000, '2024-09-22', N'Hoàng Văn E', '0927345678', N'Trần Thị B'),
('HD003', 'MSP5', 1, 7000000, '2024-09-22', N'Hoàng Văn E', '0927345678', N'Trần Thị B'),
('HD004', 'MSP4', 1, 5000000, '2024-09-23', N'Phan Thị F', '0936456789', N'Nguyễn Văn G'),
('HD005', 'MSP1', 1, 10000000, '2024-09-24', N'Vũ Văn H', '0945567890', N'Phạm Văn D'),
('HD005', 'MSP5', 1, 7000000, '2024-09-24', N'Vũ Văn H', '0945567890', N'Phạm Văn D');
--
Select * from dbo.ChiTietHoaDon
Select * from dbo.HoaDon
Select * from dbo.SanPham


------Update types
ALTER TABLE ChiTietHoaDon
ALTER COLUMN TenKH Nvarchar(100) ;

ALTER TABLE ChiTietHoaDon
ALTER COLUMN TenNV Nvarchar(100) ;


------Update value
UPDATE SanPham 
SET SoTien = 12000000, SLConLai = 8 
WHERE MaSP = 'MSP1';

UPDATE ChiTietHoaDon 
SET TenKH = N'Nguyễn Văn Nam', SDT = '0912345678' 
WHERE MaHD = 'HD001' AND MaSP = 'MSP3'; 


UPDATE HoaDon 
SET ThanhTien = (
    SELECT SUM(SoLuong * DonGiaBan) 
    FROM ChiTietHoaDon 
    WHERE ChiTietHoaDon.MaHD = HoaDon.MaHD
)
WHERE MaHD = 'HD001';


------Delete value

DELETE FROM ChiTietHoaDon 
WHERE MaHD = 'HD001' AND MaSP = 'MSP2';


----Check length
-- Kiểm tra độ dài tối đa của các cột
SELECT 
    MAX(LEN(TenKH)) as MaxTenKH,
    MAX(LEN(TenNV)) as MaxTenNV,
    MAX(LEN(SDT)) as MaxSDT
FROM ChiTietHoaDon;



-- Advance selection 

SELECT * FROM HoaDon;
    
SELECT 
    MaHD AS 'Mã HĐ',
    FORMAT(NgayLap, 'dd/MM/yyyy') AS 'Ngày lập',
    FORMAT(ThanhTien, 'N0') AS 'Thành tiền'
FROM HoaDon;

-- Hiển thị hóa đơn và chi tiết hóa đơn
SELECT 
    hd.MaHD AS 'Mã HĐ',
    hd.NgayLap AS 'Ngày lập',
    cthd.MaSP AS 'Mã SP',
    cthd.SoLuong AS 'Số lượng',
    cthd.DonGiaBan AS 'Đơn giá bán',
    (cthd.SoLuong * cthd.DonGiaBan) AS 'Thành tiền',
    cthd.TenKH AS 'Tên KH',
    cthd.TenNV AS 'Tên NV'
FROM HoaDon hd
INNER JOIN ChiTietHoaDon cthd ON hd.MaHD = cthd.MaHD
ORDER BY hd.MaHD, cthd.MaSP;
