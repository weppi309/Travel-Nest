// Lấy địa chỉ từ thẻ HTML có id="diachi"
var address = document.getElementById('diachi').textContent;

// Tạo bản đồ và thêm vào thẻ có id="map"
var map = L.map("map").setView([0, 0], 16);

// Sử dụng dịch vụ OpenStreetMap
L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    maxZoom: 19,
}).addTo(map);

// Sử dụng Nominatim Geocoding để lấy tọa độ từ địa chỉ
var nominatimUrl = "https://nominatim.openstreetmap.org/search?format=json&limit=1&q=" + encodeURI(address);

fetch(nominatimUrl)
  .then(function(response) {
    return response.json();
  })
  .then(function(data) {
    var result = data[0];
    if (result && result.lat && result.lon) {
      var latLng = [result.lat, result.lon];
      L.marker(latLng).addTo(map);
      map.setView(latLng, 16);
    } else {
      console.log("Không tìm thấy tọa độ.");
    }
  });