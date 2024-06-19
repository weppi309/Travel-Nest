function setdate(){
    const checkInDateInput = document.getElementById('check-in');
    const checkOutDateInput = document.getElementById('check-out');

    // Lấy ngày hiện tại
    const currentDate = new Date();
    const currentDateString = currentDate.toISOString().split('T')[0];

    // Đặt ngày đặt phòng là ngày hiện tại
    checkInDateInput.setAttribute('min', currentDateString);

    // Xử lý sự kiện thay đổi ngày đặt phòng
    checkInDateInput.addEventListener('change', () => {
        // Lấy ngày đặt phòng từ trường nhập
        const checkInDate = new Date(checkInDateInput.value);

        // Kiểm tra xem ngày đặt phòng có nằm trong quá khứ không
        if (checkInDate < currentDate) {
            alert('Ngày đặt phòng không được trong quá khứ');
            checkInDateInput.value = currentDateString;
        }

        // Cập nhật ngày trả phòng để đảm bảo sau ngày đặt phòng
        checkOutDateInput.setAttribute('min', checkInDateInput.value);
        // const checkOutMinDate = new Date(checkInDate);
        // checkOutMinDate.setDate(checkOutMinDate.getDate() + 1);
        // const checkOutMinDateString = checkOutMinDate.toISOString().split('T')[0];
        // checkOutDateInput.setAttribute('min', checkOutMinDateString);
    });

    // Xử lý sự kiện thay đổi ngày trả phòng
    checkOutDateInput.addEventListener('change', () => {
        // Lấy ngày trả phòng từ trường nhập
        const checkOutDate = new Date(checkOutDateInput.value);

        // Kiểm tra xem ngày trả phòng có nằm trong quá khứ không
        if (checkOutDate < currentDate) {
            alert('Ngày trả phòng không được trong quá khứ');
            checkOutDateInput.value = currentDateString;
        }
    });
}
function showSuggestions(input) {
    const inputField = document.getElementById("cityInput");
    const suggestionsList = document.getElementById("suggestions");
    suggestionsList.innerHTML = ""; // Xóa các gợi ý trước đó
  
    // Kiểm tra xem input có giá trị hay không
    if (input.value) {
      const userInput = input.value.toLowerCase();
  
      // Lấy danh sách các tỉnh từ Django context
      const tinhs = JSON.parse("{{ tinhs|escapejs }}");
  
      // Lọc các tỉnh mà bạn muốn gợi ý dựa trên dữ liệu từ máy chủ
      const suggestions = tinhs.filter(tinh => tinh.tentinh.toLowerCase().includes(userInput));
  
      suggestions.forEach(suggestion => {
        const suggestionElement = document.createElement("div");
        suggestionElement.textContent = suggestion.tentinh;
        suggestionElement.addEventListener("click", function() {
          inputField.value = suggestion.tentinh;
          suggestionsList.innerHTML = ""; // Xóa danh sách gợi ý sau khi người dùng chọn
        });
        suggestionsList.appendChild(suggestionElement);
      });
    }
  } 