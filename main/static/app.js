const sign_in_btn = document.querySelector("#sign-in-btn");
const sign_up_btn = document.querySelector("#sign-up-btn");
const container = document.querySelector(".container");

let pathname = window.location.pathname;
if (pathname == "/accounts/signup/"){
  console.log(container.classList)
  // container.classList.add("sign-up-mode");
  container.className = "container sign-up-mode";
}

sign_up_btn.addEventListener("click", () => {
  container.classList.add("sign-up-mode");
});

sign_in_btn.addEventListener("click", () => {
  container.classList.remove("sign-up-mode");
});
