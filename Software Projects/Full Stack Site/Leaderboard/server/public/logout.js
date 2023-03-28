const usernameChange = document.getElementById("useredit");
const emailChange = document.getElementById("emailedit");
const sidChange = document.getElementById("sidedit");
const passChange = document.getElementById("passedit");
const sess = document.getElementById("sessionid").innerHTML;
var hold;

function ValidateEmail(email) {
  let valid =
    /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/;

  if (email.match(valid)) {
    return true;
  } else {
    return false;
  }
}

function ValidateUser(user) {
  if (user.length > 2 && user.length < 21) {
    return true;
  } else {
    return false;
  }
}

async function checkUserDB(user) {
  let check = { checkuser: user };
  let valid = await fetch("/checkUsername", {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify(check),
  });
  counted = await valid.json();
  console.log(counted);
  if (counted != 0) {
    document.getElementById("userError").innerHTML = "Username in Use";
  } else {
    updateUser(user);
  }
}

async function checkEmailDB(e) {
  let check = { checkemail: e };
  let valid = await fetch("/checkEmail", {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify(check),
  });
  counted = await valid.json();
  console.log(counted);
  if (counted != 0) {
    document.getElementById("emailError").innerHTML = "Email in Use";
  } else {
    updateEmail(e);
  }
}

function server_request(url, data = {}, verb, callback) {
  return fetch(url, {
    credentials: "same-origin",
    method: verb,
    body: JSON.stringify(data),
    headers: { "Content-Type": "application/json" },
  })
    .then((response) => response.json())
    .then((response) => {
      if (callback) callback(response);
    })
    .catch((error) => console.error("Error:", error));
}

async function updateprofile(input) {
  const emailHolder = document.getElementById("em");
  const userHolder = document.getElementById("un");
  const sidHolder = document.getElementById("sid");
  data = { used: input };
  let userdata = await fetch("/getUserData", {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify(data),
  });
  hold = await userdata.json();

  emailHolder.innerHTML = `Email: ${hold[0]["email"]}`;
  userHolder.innerHTML = `Username: ${hold[0]["username"]}`;
  sidHolder.innerHTML = `Student ID: ${hold[0]["studentid"]}`;
}

async function whosLogged() {
  const sess = document.getElementById("sessionid").innerHTML;
  let data = { ssid: sess };
  let sessdata = await fetch("/whosLoggedIn", {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify(data),
  });
  hold = await sessdata.json();
  updateprofile(JSON.parse(hold[0]["session_data"])["username"]);
}

async function updateUser(input) {
  data = {
    userChangeTo: input,
    currentName: hold[0]["username"],
    sessionIden: sess,
  };
  const userHolder = document.getElementById("un");
  let userdata = await fetch("/updateUsername", {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify(data),
  });
  let info = await userdata.json();
  hold = info;
  usernameChange.style.visibility = "visible";
  userHolder.innerHTML = `Username: ${hold[0]["username"]}`;
}

async function updateEmail(input) {
  data = {
    emailChangeTo: input,
    currentEmail: hold[0]["email"],
  };
  const emailHolder = document.getElementById("em");
  let userdata = await fetch("/updateEmail", {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify(data),
  });
  let info = await userdata.json();
  hold = info;
  emailChange.style.visibility = "visible";
  emailHolder.innerHTML = `Email: ${hold[0]["email"]}`;
}

async function updateSID(input) {
  data = {
    sidChangeTo: input,
    currentsid: hold[0]["studentid"],
    currentE: hold[0]["email"],
    currentU: hold[0]["username"],
  };
  const sidHolder = document.getElementById("sid");
  let userdata = await fetch("/updateSID", {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify(data),
  });
  let info = await userdata.json();
  hold = info;
  sidChange.style.visibility = "visible";
  sidHolder.innerHTML = `Student ID: ${hold[0]["studentid"]}`;
}

async function updatePass(input) {
  data = {
    passChangeTo: input,
    currentS: hold[0]["studentid"],
    currentE: hold[0]["email"],
    currentU: hold[0]["username"],
  };
  const passHolder = document.getElementById("pa");
  await fetch("/updatePass", {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify(data),
  });
  passChange.style.visibility = "visible";
  passHolder.innerHTML = `Password: ******`;
}

document.addEventListener("DOMContentLoaded", () => {
  const emailHolder = document.getElementById("em");
  const userHolder = document.getElementById("un");
  const sidHolder = document.getElementById("sid");
  const paHolder = document.getElementById("pa");
  const logoutbtn = document.getElementById("logout");
  logoutbtn.addEventListener("click", (event) => {
    server_request("/logout", {}, "POST", (response) => {
      if (response.session_id == 0) {
        location.replace("/login");
      }
    });
  });
  whosLogged();
  usernameChange.addEventListener("click", (e) => {
    e.preventDefault();
    usernameChange.style.visibility = "hidden";
    userHolder.innerHTML = `Username: <form id="acceptuser"><input id="userChange" required><button type="submit">Confirm</button><button id="canceluser">Cancel</button></form>`;
    let accU = document.getElementById("acceptuser");
    let canU = document.getElementById("canceluser");
    let uu = document.getElementById("userChange");
    let captureUserErr = document.getElementById("userError");
    uu.addEventListener("input", (e) => {
      captureUserErr.innerHTML = "";
    });
    accU.addEventListener("submit", (e) => {
      e.preventDefault();
      let inputU = document.getElementById("userChange").value;
      if (ValidateUser(inputU)) {
        checkUserDB(inputU);
      } else {
        captureUserErr.innerHTML = "Invalid Username";
      }
    });
    canU.addEventListener("click", (e) => {
      e.preventDefault();
      usernameChange.style.visibility = "visible";
      userHolder.innerHTML = `Username: ${hold[0]["username"]}`;
      captureUserErr.innerHTML = "";
    });
  });

  emailChange.addEventListener("click", (e) => {
    e.preventDefault();
    emailChange.style.visibility = "hidden";
    emailHolder.innerHTML = `Email: <form id="acceptemail"><input id="emailChange" required><button type="submit">Confirm</button><button id="cancelemail">Cancel</button></form>`;
    let accE = document.getElementById("acceptemail");
    let canE = document.getElementById("cancelemail");
    let aa = document.getElementById("emailChange");
    let captureErr = document.getElementById("emailError");
    aa.addEventListener("input", (e) => {
      captureErr.innerHTML = "";
    });
    accE.addEventListener("submit", (e) => {
      e.preventDefault();
      let inputE = document.getElementById("emailChange").value;
      if (ValidateEmail(inputE)) {
        checkEmailDB(inputE);
      } else {
        captureErr.innerHTML = "Invalid Email";
      }
    });
    canE.addEventListener("click", (e) => {
      e.preventDefault();
      emailChange.style.visibility = "visible";
      emailHolder.innerHTML = `Email: ${hold[0]["email"]}`;
      captureErr.innerHTML = "";
    });
  });

  sidChange.addEventListener("click", (e) => {
    e.preventDefault();
    sidHolder.innerHTML = `Student ID: <form id="acceptsid"><input id="ssidInput" required><button type="submit">Confirm</button><button id="cancelsid">Cancel</button></form>`;
    sidChange.style.visibility = "hidden";
    let accS = document.getElementById("acceptsid");
    let canS = document.getElementById("cancelsid");
    accS.addEventListener("submit", (e) => {
      e.preventDefault();
      let inputS = document.getElementById("ssidInput").value;
      console.log(inputS);
      updateSID(inputS);
    });
    canS.addEventListener("click", (e) => {
      e.preventDefault();
      sidChange.style.visibility = "visible";
      sidHolder.innerHTML = `Student ID: ${hold[0]["studentid"]}`;
    });
  });

  passChange.addEventListener("click", (e) => {
    e.preventDefault();
    paHolder.innerHTML = `Password: <form id="acceptpa"><input id="paChange" required><button type="submit">Confirm</button><button id="cancelpa">Cancel</button></form>`;
    passChange.style.visibility = "hidden";
    let accP = document.getElementById("acceptpa");
    let canP = document.getElementById("cancelpa");
    accP.addEventListener("submit", (e) => {
      e.preventDefault();
      let inputP = document.getElementById("paChange").value;
      console.log(inputP);
      updatePass(inputP);
    });
    canP.addEventListener("click", (e) => {
      e.preventDefault();
      passChange.style.visibility = "visible";
      paHolder.innerHTML = `Password: ******`;
    });
  });
});
