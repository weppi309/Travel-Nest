const prevButton = document.getElementById("prev");
const nextButton = document.getElementById("next");
const imageList = document.querySelector(".image-list");

let currentIndex = 0;

prevButton.addEventListener("click", () => {
  currentIndex = Math.max(currentIndex - 1, 0);
  updateImageSlider();
});

nextButton.addEventListener("click", () => {
  currentIndex = Math.min(currentIndex + 1, imageList.children.length - 1);
  updateImageSlider();
});

function updateImageSlider() {
  const imageWidth = document.querySelector(".image-list img").clientWidth;
  const newPosition = -currentIndex * imageWidth;
  imageList.style.transform = `translateX(${newPosition}px)`;

  // Kiểm tra nút hiển thị
  prevButton.disabled = currentIndex === 0;
  nextButton.disabled = currentIndex === imageList.children.length - 1;
}

// Ban đầu vô hiệu hóa nút Prev
prevButton.disabled = true;

const prevButton2 = document.getElementById("prev2");
const nextButton2 = document.getElementById("next2");
const imageList2 = document.getElementById("image-list2");

let currentIndex2 = 0;

prevButton2.addEventListener("click", () => {
  currentIndex2 = Math.max(currentIndex2 - 1, 0);
  updateImageSlider2();
});

nextButton2.addEventListener("click", () => {
  currentIndex2 = Math.min(currentIndex2 + 1, imageList2.children.length - 1);
  updateImageSlider2();
});

function updateImageSlider2() {
  const itemWidth2 = imageList2.firstElementChild.clientWidth; // Kích thước của một phần
  const newPosition2 = -currentIndex2 * itemWidth2;
  imageList2.style.transform = `translateX(${newPosition2}px)`;

  // Kiểm tra nút hiển thị
  prevButton2.disabled = currentIndex2 === 0;
  nextButton2.disabled = currentIndex2 === imageList2.children.length - 1;
}

// Ban đầu vô hiệu hóa nút Prev2
prevButton2.disabled = true;

