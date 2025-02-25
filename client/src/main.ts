import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.bundle.min.js';
import * as navbar from './navbar';
import * as detect from './page_detect';

navbar.loadNavbar(detect);

if (detect.is_login()) {
  const loginForm = document.getElementById("login-form") as HTMLFormElement;
  loginForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    const formData = new FormData(loginForm);
    const response = await fetch("/login", {
      method: "POST",
      body: formData,
    });
    if (response.ok) {
      //window.location.href = "/";
    } else {
      alert("로그인 실패");
    }
  });
}

if (detect.is_signup()) {
  const signupForm = document.getElementById("signup-form") as HTMLFormElement;
  signupForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    const formData = new FormData(signupForm);
    const response = await fetch("/signup", {
      method: "POST",
      body: formData,
    });
    if (response.ok) {
      //window.location.href = "/login";
    } else {
      alert("회원가입 실패");
    }
  });
}