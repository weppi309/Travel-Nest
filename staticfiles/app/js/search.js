
// Lấy trường input theo ID
const checkInInput = document.getElementById('check-in');
const checkOutInput = document.getElementById('check-out');

// Tạo một đối tượng Date đại diện cho ngày hiện tại
const currentDate = new Date();

// Tạo một đối tượng Date đại diện cho ngày mai
const tomorrow = new Date();
tomorrow.setDate(currentDate.getDate() + 1);

// Định dạng ngày hiện tại thành chuỗi ISO 8601
const year = currentDate.getFullYear();
const month = String(currentDate.getMonth() + 1).padStart(2, '0'); // Tháng bắt đầu từ 0
const day = String(currentDate.getDate()).padStart(2, '0');
const hours = '00';
const minutes = '00';

const currentDatetime = `${year}-${month}-${day}T${hours}:${minutes}`;

// Định dạng ngày mai thành chuỗi ISO 8601
const tomorrowYear = tomorrow.getFullYear();
const tomorrowMonth = String(tomorrow.getMonth() + 1).padStart(2, '0');
const tomorrowDay = String(tomorrow.getDate()).padStart(2, '0');

const tomorrowDatetime = `${tomorrowYear}-${tomorrowMonth}-${tomorrowDay}T${hours}:${minutes}`;

// Đặt giá trị của trường input Ngày đặt phòng thành ngày hiện tại
checkInInput.value = currentDatetime;

// Đặt giá trị của trường input Ngày trả phòng thành ngày mai
checkOutInput.value = tomorrowDatetime;

document.addEventListener("DOMContentLoaded", function () {
    const guestCountButton = document.getElementById("guestCountButton");
    // const guestCountDropdown = document.getElementById("guestCountDropdown");

    guestCountButton.addEventListener("click", () => {
        document.getElementById("guestCountDropdown").style.display = "block";
    });
  });
  function incrementValue(type) {
    var inputElement = document.getElementById(type + "Count");
    var count = parseInt(inputElement.value, 10);
    count++;
    inputElement.value = count;
    updateGuestCount();
  }

  function decrementValue(type) {
    var inputElement = document.getElementById(type + "Count");
    var count = parseInt(inputElement.value, 10);
    if (count > 0) {
      count--;
      inputElement.value = count;
      updateGuestCount();
    }
  }
  function updateGuestCount() {
    var adultCount = parseInt(document.getElementById('adultCount').value, 10);
    var childCount = parseInt(document.getElementById('childCount').value, 10);
    var roomCount = parseInt(document.getElementById('roomCount').value, 10);

    var totalCount = adultCount + childCount;
    var guestCountButton = document.getElementById('guestCountButton');
    guestCountButton.textContent = totalCount + " khách, " + roomCount + " phòng";
  }
  document.addEventListener("DOMContentLoaded", function () {
    var doneButton = document.getElementById('doneButton');
    doneButton.addEventListener("click", () => {
        updateGuestCount();
        document.getElementById("guestCountDropdown").style.display = "none";
    });
  });


  // let searchClicked = false;
  // document.getElementById("timkiem").addEventListener("submit", (event) => {
  //     if (!searchClicked) {
  //         event.preventDefault(); // Ngăn chặn việc submit form nếu nút tìm kiếm chưa được nhấn
  //     }
  //     // Thực hiện xử lý form khác ở đây nếu cần
  // });





 
// function redirectToHotelList() {
//     var destination = document.getElementById("tinh").value;
//     var checkIn = document.getElementById("check-in").value;
//     var checkOut = document.getElementById("check-out").value;
//     var guestCount = document.getElementById("guestCountButton").textContent; // Lấy giá trị số khách từ button

//     // Tạo URL với các tham số truy vấn
//     var url = "{% url 'ds'%}?tinh=" + tinh + "&checkIn=" + checkIn + "&checkOut=" + checkOut + "&guestCount=" + guestCount;

//     // Chuyển hướng đến trang tiếp theo
//     window.location.href = url;
//   }