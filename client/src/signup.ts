const signupForm = document.getElementById("signup-form");

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