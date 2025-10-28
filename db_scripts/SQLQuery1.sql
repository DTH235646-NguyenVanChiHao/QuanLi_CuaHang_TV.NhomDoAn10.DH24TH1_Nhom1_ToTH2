CREATE DATABASE Quan_Li_TV;
GO

USE Quan_Li_TV;
GO









CREATE TABLE SanPham (
    MaSP VARCHAR(10) PRIMARY KEY,
    TenSP NVARCHAR(100) NOT NULL,
    SLConLai INT DEFAULT 0,
    DonGiaBan DECIMAL(18,2) DEFAULT 0,
    NhaCC NVARCHAR(100) NOT NULL,
    NgayNhap DATE NOT NULL,
);
GO



CREATE TABLE HoaDon (
    MaHD VARCHAR(10) PRIMARY KEY,
    NgayLapHD DATE NOT NULL,
    TenKH NVARCHAR(100),
    SDT     VARCHAR(10),
    TenNVLap  NVARCHAR(100),
);
GO

--- Delete: DonGiaBan -> của sản phẩm
CREATE TABLE ChiTietHoaDon (
    MaHD VARCHAR(10) NOT NULL,
    MaSP VARCHAR(10) NOT NULL , --- Take: don gia ban (Sotien) + 
    SoLuong INT NOT NULL,

  ---Thanh tien = soluong * don gia ban
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

INSERT INTO SanPham (MaSP, TenSP, SLConLai, DonGiaBan, NhaCC, NgayNhap)
VALUES
('SP01', N'Tivi Samsung 43 inch', 10, 8000000, N'Công ty Samsung Việt Nam', '2025-09-01'),
('SP02', N'Laptop Dell Inspiron 15', 5, 15000000, N'Công ty Dell Việt Nam', '2025-08-20'),
('SP03', N'Điện thoại iPhone 15', 8, 28000000, N'Công ty Apple Việt Nam', '2025-09-15'),
('SP04', N'Tai nghe Bluetooth Sony', 20, 1500000, N'Công ty Sony Việt Nam', '2025-09-10'),
('SP05', N'Máy lạnh LG Inverter 1.5HP', 6, 12000000, N'Công ty LG Việt Nam', '2025-08-25');


INSERT INTO HoaDon (MaHD, NgayLapHD, TenKH, SDT, TenNVLap)
VALUES
('HD01', '2025-09-25', N'Nguyễn Văn Nam', '0905123456', N'Trần Quốc Quang'),
('HD02', '2025-09-26', N'Lê Thị Linh', '0906789123', N'Nguyễn Thành Phúc'),
('HD03', '2025-09-27', N'Phạm Anh Huy', '0912345678', N'Võ Thị Thảo'),
('HD04', '2025-09-28', N'Hoàng Thị Trinh', '0934567890', N'Phạm Văn Hưng'),
('HD05', '2025-09-29', N'Đặng Minh Tuấn', '0923456789', N'Lê Thị Lan');


INSERT INTO ChiTietHoaDon (MaHD, MaSP, SoLuong)
VALUES
('HD01', 'SP03', 1), -- iPhone 15
('HD01', 'SP04', 2), -- Tai nghe Sony

('HD02', 'SP01', 1), -- Tivi Samsung
('HD02', 'SP04', 1), -- Tai nghe Sony

('HD03', 'SP02', 1), -- Laptop Dell

('HD04', 'SP05', 1), -- Máy lạnh LG
('HD04', 'SP04', 2), -- Tai nghe Sony

('HD05', 'SP01', 1), -- Tivi Samsung
('HD05', 'SP02', 1); -- Laptop Dell


--
Select * from dbo.ChiTietHoaDon
Select * from dbo.HoaDon
Select * from dbo.SanPham

SELECT TOP 1 MaHD FROM HoaDon ORDER BY MaHD DESC

------Update types
ALTER TABLE HoaDon
ALTER COLUMN TenKH Nvarchar(100) ;

ALTER TABLE HoaDon
ALTER COLUMN TenNVLap Nvarchar(100) ;


------Update value
UPDATE SanPham 
SET DonGiaBan = 12000000, SLConLai = 8 
WHERE MaSP = 'MSP1';

UPDATE HoaDon
SET TenKH = N'Nguyễn Văn Nam', SDT = '0912345678' 
WHERE MaHD = 'HD001'

-------Delete column
ALTER TABLE HoaDon
DROP COLUMN ThanhTien;

-------delete column with constraints
EXEC sp_helpconstraint 'HoaDon';
ALTER TABLE HoaDon DROP CONSTRAINT DF__HoaDon__ThanhTie__49C3F6B7;

------Delete value

DELETE FROM ChiTietHoaDon 
WHERE MaHD = 'HD001' AND MaSP = 'MSP2';


----Check length
-- Kiểm tra độ dài tối đa của các cột
SELECT 
    MAX(LEN(TenKH)) as MaxTenKH,
    MAX(LEN(TenNVLap)) as MaxTenNV,
    MAX(LEN(SDT)) as MaxSDT
FROM HoaDon;



-- Advance selection 

SELECT * FROM HoaDon;
    

-- Hiển thị thông tin hóa đơn cùng chi tiết sản phẩm
SELECT 
    hd.MaHD AS N'Mã HĐ',
    sp.MaSP as 'Mã sản phẩm',
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





-- Tổng doanh thu từ tất cả hóa đơn
SELECT 
    SUM(cthd.SoLuong * sp.DonGiaBan) AS TongDoanhThu
FROM HoaDon hd
INNER JOIN ChiTietHoaDon cthd ON hd.MaHD = cthd.MaHD
INNER JOIN SanPham sp ON cthd.MaSP = sp.MaSP;
        SELECT 
            SUM(cthd.SoLuong * cthd.DonGiaBan) AS TongDoanhThu
        FROM HoaDon hd
        INNER JOIN ChiTietHoaDon cthd ON hd.MaHD = cthd.MaHD
        INNER JOIN SanPham sp ON cthd.MaSP = sp.MaSP;


-- Tổng số hóa đơn được lập trong ngày cụ thể
SELECT COUNT(*) AS TongSoHoaDon
FROM HoaDon
WHERE CAST(NgayLapHD AS DATE) = '2024-09-20';

update dbo.HoaDon
set TenKH = 'Chí Hào',
    SDT = '012345678'
where mahd = 'HD01'


---
select MaSP,TenSP , DonGiaBan, SLConLai
from dbo.SanPham as sp
order by TenSP
asc

SELECT MaSP,TenSP , DonGiaBan, SLConLai 
FROM SanPham WHERE TenSP LIKE 'T%'


UPDATE SanPham 
SET SLConLai = SLConLai - 1
WHERE MaSP = 'SP01'

select *
from SanPham

select *
from HoaDon