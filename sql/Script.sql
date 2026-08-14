-- 1. tạo bảng
create table nhan_vien (
	id serial primary key,
	ten varchar(100),
	phongban varchar(100),
	tuoi integer,
	luong integer
);

-- 1.1 tạo thêm bảng phòng ban
create table phongbaninfor (
	tenphong varchar(100) primary key,
	truongphong varchar(100)
);


-- 2. thêm dữ liệu vào bảng
insert into nhan_vien (ten, phongban, tuoi, luong)
values 
	('an', 'sales', 20, 8000000),
	('binh', 'it', 22, 9000000),
	('chi', 'sales', 23, 7000000),
	('dung', 'it', 21, 3000000),
	('em', 'hr', 19,4000000);

-- 2.1 thêm dữ liệu vào bảng phòng ban
insert into phongbaninfor (tenphong, truongphong)
values 
	('sales', 'nam'),
	('it', 'lan'),
	('hr' , 'hoa');


-- 3. xem toàn bộ dữ liệu
select * from nhan_vien;

-- 4. chọn những người có lương lớn hơn  7 củ
select ten, luong from nhan_vien where luong > 7000000;

-- 5. in danh dách tên người có tiền lương từ thấp đến cao
select ten from nhan_vien order by tuoi asc;

-- 6. thử cái where 
select ten 
from nhan_vien
where phongban = 'it';

select phongban, avg(luong)
from nhan_vien
group by phongban
having avg(luong) > 8000000;

select phongban, count(*)
from nhan_vien
group by phongban;

-- dùng view để join 2 bảng lại
create view nv_pbinfor as 
select 
	nv.ten, 
	nv.phongban,
	nv.tuoi,
	nv.luong,
	pbinfor.truongphong
from nhan_vien as nv
join phongbaninfor as pbinfor
	on nv.phongban = pbinfor.tenphong;

select ten, truongphong 
from nv_pbinfor;

select nv_pbinfor.truongphong, count(*)
from nv_pbinfor
group by nv_pbinfor.truongphong;