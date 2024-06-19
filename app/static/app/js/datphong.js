$(document).ready(function () {
    $(".datphong").click(function () {
        var ngayNhan = document.getElementById("check-in").value;
        var ngayTra = document.getElementById("check-out").value;
        var soLuongNguoi = document.getElementById("guestCountButton").textContent;
        // var phongid = $(this).data("phong");
        var url="/datphong/?ngay_nhan=" + ngayNhan + "&ngay_tra=" + ngayTra + "&so_luong_nguoi=" + soLuongNguoi ;
        window.location.href = url;
    });
});