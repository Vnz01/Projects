const overlay = document.querySelector(".overlay");
const btn1OpenModal = document.getElementById("show1");
const btn2OpenModal = document.getElementById("show2");
const btn3OpenModal = document.getElementById("show3");
const btn1CloseModal = document.getElementById("close1");
const btn2CloseModal = document.getElementById("close2");
const btn3CloseModal = document.getElementById("close3");
const modal1 = document.querySelector(".modal1");
const modal2 = document.querySelector(".modal2");
const modal3 = document.querySelector(".modal3");

const openModal1 = function () {
  if (modal1.classList.contains("hidden")) {
    modal1.classList.remove("hidden");
    overlay.classList.remove("hidden");
  }
};
const openModal2 = function () {
  if (modal2.classList.contains("hidden")) {
    modal2.classList.remove("hidden");
    overlay.classList.remove("hidden");
  }
};
const openModal3 = function () {
  if (modal3.classList.contains("hidden")) {
    modal3.classList.remove("hidden");
    overlay.classList.remove("hidden");
  }
};
const closeModal1 = function () {
  if (!modal1.classList.contains("hidden")) {
    modal1.classList.add("hidden");
    overlay.classList.add("hidden");
  }
};
const closeModal2 = function () {
  if (!modal2.classList.contains("hidden")) {
    modal2.classList.add("hidden");
    overlay.classList.add("hidden");
  }
};
const closeModal3 = function () {
  if (!modal3.classList.contains("hidden")) {
    modal3.classList.add("hidden");
    overlay.classList.add("hidden");
  }
};
btn1OpenModal.addEventListener("click", openModal1);
btn2OpenModal.addEventListener("click", openModal2);
btn3OpenModal.addEventListener("click", openModal3);
btn1CloseModal.addEventListener("click", closeModal1);
btn2CloseModal.addEventListener("click", closeModal2);
btn3CloseModal.addEventListener("click", closeModal3);

overlay.addEventListener("click", () => {
  closeModal1();
  closeModal2();
  closeModal3();
});

document.addEventListener("keydown", function (e) {
  if (e.key === "Escape" && !modal1.classList.contains("hidden")) {
    closeModal1();
  }
  if (e.key === "Escape" && !modal2.classList.contains("hidden")) {
    closeModal2();
  }
  if (e.key === "Escape" && !modal3.classList.contains("hidden")) {
    closeModal3();
  }
});
