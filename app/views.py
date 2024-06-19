import json
from django.shortcuts import render
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Q
from django.shortcuts import redirect, render
from datetime import datetime, timedelta, date
from .models import *
from .forms import CreateUserForm
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.views.decorators.cache import never_cache
# Create your views here.

def dangky(request):
    form = CreateUserForm()
    if request.method == "POST":
        form =CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Gán quyền Staff status cho người dùng mới
            user.is_staff = True
            user.save()
            # form.save()
            return redirect('dangnhap')
    context={'form': form}
    return render(request,'app/dangky.html',context)
def dangnhap(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == "POST":
        u = request.POST.get('username')
        p = request.POST.get('password')
        user = authenticate(request, username=u, password=p)
        
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, 'Your account is inactive. Please contact the admin.')
        else:
            messages.info(request, 'Username or password is not correct!')
           
    context={}    
    return render(request,'app/dangnhap.html',context)
def logoutPage(request):
    logout(request)
    return redirect("dangnhap")
def home(request):
    tinhs = Tinh.objects.all()
    tinh_data = Tinh.objects.annotate(num_hotels=Count('khachsan'))
    # Lấy hai hàng đầu hiển thị 2 ảnh
    top_2_tinhs = Tinh.objects.all()[:2]
    # Lấy hàng thứ hai hiển thị 3 ảnh kèm tên
    # second_tinh = Tinh.objects.all()[2]
    # top_3_tinhs = Tinh.objects.filter(id__gte=second_tinh.id)[:3]
    try:
        second_tinh = Tinh.objects.all()[2]
        top_3_tinhs = Tinh.objects.filter(id__gte=second_tinh.id)[:3]
    except IndexError:
        second_tinh = None
        top_3_tinhs = None

    context={'tinh_data': tinh_data, 'tinhs':tinhs,'top_2_tinhs':top_2_tinhs,'top_3_tinhs':top_3_tinhs} 
    return render(request,'app/home.html',context)
def search(request):
    if request.method=="POST":
        search= request.POST.get('tinh')
        tinh= Tinh.objects.filter(tentinh=search).first() # ten tinh
        if search !='':
            khachsans= KhachSan.objects.filter(tinh_id=tinh)
        else:
            khachsans=KhachSan.objects.all()
    context={'khachsans':khachsans,'search':search,'tinh':tinh,'search':search}
    return render(request,'app/search.html',context)
def ds(request): #view danh sách khách sạn theo tỉnh
    tinh_id = request.GET.get('tinh_id')
    tinh_name = request.GET.get('tinh_name')
   # Kiểm tra xem có tinh_id nào được truyền không
    if tinh_id is not None:
        khachsans = KhachSan.objects.filter(tinh_id=tinh_id)
    else:
        khachsans = KhachSan.objects.all()
    context={'khachsans':khachsans, 'tinh_id':tinh_id,'tinh_name':tinh_name}
    return render(request,'app/listkhachsan.html',context)
def ks(request):
    khachsan_id = request.GET.get('khachsan_id')
    khachsan = KhachSan.objects.get(pk=khachsan_id)
    listanhks =AnhKhachSan.objects.filter(khachsan=khachsan)
    khachsan_name = khachsan.tenkhachsan
    listphong = Phong.objects.filter(khachsan=khachsan)
    for phong in listphong:
         number_of_rooms = phong.soluong
         phong.range_soluong = range(phong.soluong+1)
    # Lấy giá của mỗi phòng từ cơ sở dữ liệu
    # Đây là một ví dụ đơn giản, bạn có thể thay đổi truy vấn để lấy giá cụ thể của mỗi phòng
    first_room = Phong.objects.first()
    price_per_room = first_room.giaphong if first_room else 0

    # Lấy giá của mỗi phòng từ cơ sở dữ liệu
    # Đây là một ví dụ đơn giản, bạn có thể thay đổi truy vấn để lấy giá cụ thể của mỗi phòng
    first_room = Phong.objects.first()
    price_per_room = first_room.giaphong
    tinh_name = khachsan.tinh.tentinh
    tinh_id = khachsan.tinh.id
    # lay_ngay_nhan = request.GET.get('ngay_nhan')
    # lay_ngay_tra = request.GET.get('ngay_tra')
    # check_in=''
    # check_out=''
    # if request.method=="POST":
    #     check_in= request.POST.get('check-in')
    #     check_out=request.POST.get('check-out')
    # # Kiểm tra và chuyển đổi ngày
    # phong_trong =[]
    # phongs = Phong.objects.filter(khachsan=khachsan_id)
    # if lay_ngay_nhan and lay_ngay_tra:
    #     # Chuyển đổi giá trị ngày từ chuỗi sang đối tượng datetime
    #     ngaynhan = datetime.fromisoformat(lay_ngay_nhan).date()
    #     ngaytra = datetime.fromisoformat(lay_ngay_tra).date()
    #     phong_trong = [phong for phong in phongs if phong.is_phong_trong_hien_tai(ngaynhan,ngaytra) is True]
    # for phong in phongs:
    #     anhs = AnhPhong.objects.filter(phong=phong)
    # danhgias= Danhgia.objects.filter(phong__khachsan=khachsan)
    # tiennghis = SapXepTN.objects.filter(phong=phongs.first())
    # diemtb_danhgia = khachsan.diem_trung_binh    
    # tendiem_tb= khachsan.get_danh_gia_tb
    # tong_danhgia=khachsan.sum_danh_gia
    # 'danhgias':danhgias,
    # 'tong_danhgia':tong_danhgia,
    # 'tendiem_tb':tendiem_tb,'diemtb_danhgia':diemtb_danhgia,'check_in':check_in,'check_out':check_out,'anhs':anhs,'phongs': phongs,'phong_trong':phong_trong, ,'tinh_name':tinh_name,'tinh_id':tinh_id
    context={'range': range,'numberOfRoomsFromServer': number_of_rooms, 'pricePerRoomFromServer': price_per_room,'khachsan':khachsan,'khachsan_id':khachsan_id, 'khachsan_name':khachsan_name,'listanhks':listanhks,'listphong':listphong,'tinh_name':tinh_name,'tinh_id':tinh_id}
    return render(request, 'app/khachsan.html', context)
def dondatphong(request):
    if request.user.is_authenticated:
        customer = request.user
        hoadons= HoaDon.objects.filter(user=customer)
        if request.method == 'POST':
            diem = request.POST.get("exampleRadios")
            binhluan = request.POST.get("binhluan")
            phong_id = request.POST.get("phong_id")  # Lấy phong_id từ biểu mẫu đánh giá
            hoadon = HoaDon.objects.get(chitiethoadon__phong_id=phong_id, user=customer)  # Lấy hóa đơn dựa trên phong_id
            danhgia = Danhgia.objects.create(user=customer, phong=hoadon.chitiethoadon_set.get(phong_id=phong_id).phong, diem=diem, binhluan=binhluan)
            return redirect('dondatphong')  # Chuyển hướng trở lại trang danh sách hóa đơn sau khi đánh giá
    else:
        hoadon =[]
        
    context ={'hoadons':hoadons}
    return render(request,'app/dondatphong.html', context)
@login_required(login_url='dangnhap')
def datphong(request):
    # if request.user.is_authenticated:
    #     if request.method == 'GET':           
    #         ngay_gio_nhan = request.GET.get("ngay_nhan")
    #         ngay_gio_tra = request.GET.get("ngay_tra")
    #         so_luong_nguoi = request.GET.get("so_luong_nguoi")
    #         phong_id = request.GET.get("phong_id")
    #         phong = Phong.objects.get(id= phong_id)
    #         ten_ks= phong.khachsan.tenkhachsan
    #         ten_tinh= phong.khachsan.tinh.tentinh
    #         tenphong = phong.loaiphong.tenloaiphong
    #         dongia=phong.giaphong
    #         ngay_gio_nhan_str = datetime.strptime(ngay_gio_nhan, "%Y-%m-%dT%H:%M")
    #         ngay_gio_tra_str = datetime.strptime(ngay_gio_tra, "%Y-%m-%dT%H:%M")
    #         so_dem= (ngay_gio_tra_str-ngay_gio_nhan_str).days
    #         total=so_dem*dongia
    #         anh_phong = Anh.objects.filter(phong=phong)    
    #         diemtb_danhgia = phong.khachsan.diem_trung_binh    
    #         tendiem_tb= phong.khachsan.get_danh_gia_tb
    #         tong_danhgia=phong.khachsan.sum_danh_gia
    #         tien_nghi_phong = SapXepTN.objects.filter(phong=phong).values('tiennghi__tentiennghi', 'tiennghi__icon')
    #         # Bây giờ bạn có thể truy cập từng giá trị như sau:
    #         tien_nghi_list = []
    #         for item in tien_nghi_phong:
    #             tentiennghi = item['tiennghi__tentiennghi']
    #             icon = item['tiennghi__icon']
    #             tien_nghi_list.append({'tentiennghi': tentiennghi, 'icon': icon})
    #         context ={'ten_tinh':ten_tinh,'so_luong_nguoi':so_luong_nguoi,
    #                   'ngay_gio_nhan':ngay_gio_nhan,'ngay_gio_tra': ngay_gio_tra,
    #                   'ten_ks': ten_ks,'so_dem':so_dem,
    #                   'total':total,'tenphong':tenphong,
    #                   'dongia':dongia,'anh_phong':anh_phong,'tien_nghi_list':tien_nghi_list,
    #                   'diemtb_danhgia':diemtb_danhgia,'tendiem_tb':tendiem_tb,'tong_danhgia':tong_danhgia}
            return render(request,'app/datphong.html')
    #     elif request.method=='POST':
    #         ngay_nhan = request.POST.get("ngay_nhan")
    #         ngay_tra = request.POST.get("ngay_tra")
    #         so_luong_dem = request.POST.get("so_luong_dem")
    #         phong_id = request.POST.get("phong_id")
    #         # Kiểm tra xem giá trị từ phiên đã tồn tại hay chưa
    #         phong = Phong.objects.get(id=phong_id)
    #         don_gia = phong.giaphong
    #         customer = request.user
    #         hoadon = HoaDon.objects.create(user=customer,trangthaihoanthanh="Chưa hoàn thành")
    #         chitiethoadon = ChiTietHoaDon.objects.create(phong=phong,hoadon=hoadon,ngay_gio_nhan=ngay_nhan,ngay_gio_tra=ngay_tra,soluong=so_luong_dem,dongia=don_gia)
    #         return redirect('dondatphong')
    #         # Lưu thay đổi vào cơ sở dữ liệu  
    # else:
    #     chitiethoadon=[]
    #     hoadon ={''}

def index(request):
    # Xác định ngày hiện tại
    today = datetime.now()

    # Tìm ngày thứ 2 gần nhất
    monday = today - timedelta(days=today.weekday())

    # Xác định ngày chủ nhật trong tuần
    sunday = monday + timedelta(days=6)

    # Kiểm tra nếu hôm nay là chủ nhật và nếu vậy, giảm đi 1 tuần
    if today.weekday() == 6:
        monday -= timedelta(days=7)
        sunday -= timedelta(days=7)

    group_name = 'khachhang'
    group = Group.objects.get(name=group_name)  # Lấy đối tượng nhóm từ tên
    users_count = User.objects.filter(
    Q(groups=group),
    Q(date_joined__gte=monday),
    Q(date_joined__lte=sunday)
    ).count()
    # ... (Các bước trước để tính số lượng người dùng trong tuần hiện tại)

    # Tính số lượng người dùng trong tuần trước
    last_monday = monday - timedelta(days=7)
    last_sunday = sunday - timedelta(days=7)

    last_week_users_count = User.objects.filter(
        Q(groups=group),
        Q(date_joined__gte=last_monday),
        Q(date_joined__lte=last_sunday)
    ).count()
    if last_week_users_count == 0:
    # Tránh chia cho 0
        percentage_change = 0
    else:
        percentage_change = ((users_count - last_week_users_count) / last_week_users_count) * 100
     # Lấy năm hiện tại
    current_year = datetime.now().year

    # Xác định quý hiện tại
    current_quarter = (datetime.now().month - 1) // 3 + 1
    # Lấy số lượng khách sạn hiện tại từ quý trước
    khach_san_hien_tai = KhachSan.objects.filter(
        ngay_them__year=current_year,
        ngay_them__quarter=current_quarter
    ).count()
    tinh_data = []
    tinh_list = Tinh.objects.all()
    for tinh in tinh_list:
        khachsan_count = KhachSan.objects.filter(tinh=tinh).count()
        phong_count = Phong.objects.filter(khachsan__tinh=tinh).count()
        tinh_data.append({
            'ten_tinh': tinh.tentinh,
            'so_luong_khach_san': khachsan_count,
            'tong_so_phong': phong_count
        })

    context = {'users_count':users_count,'percentage_change':percentage_change,'khach_san_hien_tai':khach_san_hien_tai, 'tinh_data': tinh_data}
    return render(request, 'admin/index.html', context)

def edit_profile(request):
    if request.method == 'POST':
        user = request.user
        
        # Lấy các giá trị từ POST request
        new_username = request.POST.get('username')
        new_email = request.POST.get('email')
        new_first_name = request.POST.get('first_name')
        new_last_name = request.POST.get('last_name')

        # Chỉ cập nhật thông tin nếu có sự thay đổi
        if new_username:
            user.username = new_username
        if new_email:
            user.email = new_email
        if new_first_name:
            user.first_name = new_first_name
        if new_last_name:
            user.last_name = new_last_name

        # Xử lý tải lên hình ảnh mới
        if 'avatar' in request.FILES:
            avatar = request.FILES['avatar']
            # Lưu hình ảnh vào hệ thống lưu trữ (ví dụ: media/uploads/)
            user.avatar = 'uploads/' + avatar.name
            default_storage.save(user.avatar, ContentFile(avatar.read()))

        user.save()
        return redirect('edit_profile')
    context ={'user':request.user}
    return render(request, 'pages/profile.html', context)
def dashboard(request):
    if request.user.is_authenticated:
        user = request.user
        danhgia_list = Danhgia.objects.filter(user=user)       
        hoadons= HoaDon.objects.filter(user=user)
        danhgia_hoadon = None
        if request.method == 'POST':
            diem = request.POST.get("exampleRadios")
            binhluan = request.POST.get("binhluan")
            phong_id = request.POST.get("phong_id")  # Lấy phong_id từ biểu mẫu đánh giá
            hoadon = HoaDon.objects.get(chitiethoadon__phong_id=phong_id, user=user)  # Lấy hóa đơn dựa trên phong_id
            danhgia_hoadon = Danhgia.objects.filter(user=user, phong=hoadon.chitiethoadon_set.get(phong_id=phong_id).phong)
            if not danhgia_hoadon:
                danhgia = Danhgia.objects.create(user=user, phong=hoadon.chitiethoadon_set.get(phong_id=phong_id).phong, diem=diem, binhluan=binhluan)
            else:
                pass
            return redirect('customer_dashboard')  # Chuyển hướng trở lại trang danh sách hóa đơn sau khi đánh giá
    else:
        hoadon =[]
    context = {
        'hoadons': hoadons,
        'danhgia_hoadon': danhgia_hoadon,
        'danhgia_list':danhgia_list,
    }
    
    return render(request, 'pages/dashboard.html', context)