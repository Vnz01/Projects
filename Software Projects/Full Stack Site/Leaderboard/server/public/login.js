function ValidateEmail(email) {
  let valid =
    /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/;

  if (email.match(valid)) {
    return true;
  } else {
    return false;
  }
}

async function signin() {
  let emailoruser = document.getElementById("loginUser").value;
  let pass = document.getElementById("loginPass").value;
  const data = { username: emailoruser, password: pass };
  await fetch("/login", {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify(data),
  })
    .then((response) => response.json())
    .then((response) => {
      const loginForm = document.querySelector("#login");
      if (response.session_id == 0) {
        setFormMessage(
          loginForm,
          "error",
          "Invalid username/password combination"
        );
      }
      if (response.session_id != 0) {
        document.cookie = "session_id=" + response.session_id + "; path=/";
        setFormMessage(loginForm, "success", "Login Successful");
        location.replace("/profile");
      }
    })
    .catch((error) => console.error("Error:", error));
}

async function signup() {
  const createAccountForm = document.querySelector("#createAccount");
  let user = document.getElementById("signupUsername").value;
  let student = document.getElementById("signupStudentID").value;
  let e = document.getElementById("signupEmail").value;
  let pass = document.getElementById("signupPass").value;
  let passConfirmed = document.getElementById("signupPassConfirmed").value;

  ValidateEmail(e);

  if (pass == passConfirmed && user.length > 2 && ValidateEmail(e)) {
    let dict = { Username: user, StudentID: student, Email: e, Password: pass };
    let check = { checkuser: user, checkemail: e };
    let valid = await fetch("/check", {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify(check),
    });
    counted = await valid.json();
    if (counted == 0) {
      await fetch("/signup", {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify(dict),
      });
      setFormMessage(createAccountForm, "Success", "Account Created");
      location.replace("/login");
    } else {
      setFormMessage(createAccountForm, "error", "Email/User in Use");
    }
  }
}

async function reset() {
  const resetPass = document.querySelector("#resetPassword");
  let resetE = document.getElementById("resetEmail").value;
  let resetID = document.getElementById("resetStudentID").value;
  let newpass = document.getElementById("resetPass").value;
  let dict = { Email: resetE, StudentID: resetID, Password: newpass };
  let check = { checkID: resetID, checkE: resetE };
  let valid = await fetch("/checkReset", {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify(check),
  });
  counted = await valid.json();
  console.log(counted);
  if (counted != 0) {
    await fetch("/reset", {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify(dict),
    });
    setFormMessage(resetPass, "Success", "Password Reset");
    location.replace("/login");
  } else {
    setFormMessage(resetPass, "error", "Email not Found");
  }
}

function setFormMessage(formElement, type, message) {
  const messageElement = formElement.querySelector(".form__message");

  messageElement.textContent = message;
  messageElement.classList.remove(
    "form__message--success",
    "form__message--error"
  );
  messageElement.classList.add(`form__message--${type}`);
}

function setInputError(inputElement, message) {
  inputElement.classList.add("form__input--error");
  inputElement.parentElement.querySelector(
    ".form__input-error-message"
  ).textContent = message;
}

function clearInputError(inputElement) {
  inputElement.classList.remove("form__input--error");
  inputElement.parentElement.querySelector(
    ".form__input-error-message"
  ).textContent = "";
}

document.addEventListener("DOMContentLoaded", () => {
  const loginForm = document.querySelector("#login");
  const createAccountForm = document.querySelector("#createAccount");
  const resetPass = document.querySelector("#resetPassword");

  document
    .querySelector("#linkCreateAccount")
    .addEventListener("click", (e) => {
      e.preventDefault();
      loginForm.classList.add("form--hidden");
      createAccountForm.classList.remove("form--hidden");
    });

  document.querySelector("#linkLogin").addEventListener("click", (e) => {
    e.preventDefault();
    loginForm.classList.remove("form--hidden");
    createAccountForm.classList.add("form--hidden");
  });

  document.querySelector("#linkReset").addEventListener("click", (e) => {
    e.preventDefault();
    loginForm.classList.add("form--hidden");
    resetPass.classList.remove("form--hidden");
  });

  document.querySelector("#cancelReset").addEventListener("click", (e) => {
    e.preventDefault();
    loginForm.classList.remove("form--hidden");
    resetPass.classList.add("form--hidden");
  });

  document.querySelectorAll(".form__input").forEach((inputElement) => {
    inputElement.addEventListener("blur", (e) => {
      if (
        e.target.id === "signupUsername" &&
        e.target.value.length > 0 &&
        e.target.value.length < 3
      ) {
        setInputError(
          inputElement,
          "Username must be at least 3 characters in length"
        );
      }

      let pp = document.getElementById("signupPass").value;
      let ppc = document.getElementById("signupPassConfirmed").value;

      if (e.target.id === "signupPassConfirmed" && pp != ppc) {
        setInputError(inputElement, "Passwords don't match");
      }

      let ee = document.getElementById("signupEmail").value;

      let check = ValidateEmail(ee);

      if (e.target.id === "signupEmail" && !check) {
        setInputError(inputElement, "Invalid Email");
      }
    });

    inputElement.addEventListener("input", (e) => {
      clearInputError(inputElement);
    });
  });

  loginForm.addEventListener("submit", (e) => {
    e.preventDefault();
    signin();
  });

  createAccountForm.addEventListener("submit", (e) => {
    e.preventDefault();
    signup();
  });

  resetPass.addEventListener("submit", (e) => {
    e.preventDefault();
    reset();
  });
});
