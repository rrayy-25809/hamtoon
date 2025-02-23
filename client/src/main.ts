import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.bundle.min.js';
import './navbar';

document.addEventListener("DOMContentLoaded", () => {
    const loginForm = document.getElementById("login-form");
    const signupForm = document.getElementById("signup-form");
  
    if (loginForm) {
      loginForm.addEventListener("submit", async (event) => {
        event.preventDefault();
        const formData = new FormData(loginForm as HTMLFormElement);
        const response = await fetch("/login", {
          method: "POST",
          body: formData,
        });
        if (response.ok) {
          window.location.href = "/";
        } else {
          alert("로그인 실패");
        }
      });
    }
  
    if (signupForm) {
      signupForm.addEventListener("submit", async (event) => {
        event.preventDefault();
        const formData = new FormData(signupForm as HTMLFormElement);
        const response = await fetch("/signup", {
          method: "POST",
          body: formData,
        });
        if (response.ok) {
          window.location.href = "/login";
        } else {
          alert("회원가입 실패");
        }
      });
    }
  });