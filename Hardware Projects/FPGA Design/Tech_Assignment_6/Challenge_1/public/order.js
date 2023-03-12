const menuscreen = document.getElementById("menu");
const select = document.getElementById("menuitem");
const costupdate = document.getElementById("Cost");
const ordForm = document.getElementById("orderform");
const updater1 = document.getElementById("quantity");
const updater2 = document.getElementById("menuitem");
var loadMenu;

async function load() {
  await fetch("/loadMenu")
    .then((response) => {
      return response.json();
    })
    .then((json) => {
      loadMenu = json;
    });
  menuscreen.innerHTML = "";
  for (let ctr = 0; ctr < Object.keys(loadMenu).length; ctr++) {
    let menuBoard = document.createElement("div");
    menuBoard.classList.add("menuClass");
    menuBoard.innerHTML = `<div class="menuItemsClass">
          <p>Item ID: ${loadMenu[ctr]["item_id"]}</p>
          <p>Name: ${loadMenu[ctr]["name"]}</p>
          <p>Price: $${loadMenu[ctr]["price"]}</p>
        </div><br>`;
    menuscreen.appendChild(menuBoard);
  }
}

async function loadOptions() {
  await fetch("/loadMenu")
    .then((response) => {
      return response.json();
    })
    .then((json) => {
      loadMenu = json;
    });
  for (let ctr = 0; ctr < Object.keys(loadMenu).length; ctr++) {
    let options = document.createElement("option");
    options.value = loadMenu[ctr]["item_id"];
    options.text = loadMenu[ctr]["name"];
    select.appendChild(options);
  }
}

async function orderForm() {
  let itemID = select.value;
  let orderName = document.getElementById("customer").value;
  let orderQuantity = document.getElementById("quantity").value;
  let dict = { item_id: itemID, name: orderName, quantity: orderQuantity };
  await fetch(`/order`, {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify(dict),
  });
  load();
}

async function updateOrderCost() {
  await fetch("/loadMenu")
    .then((response) => {
      return response.json();
    })
    .then((json) => {
      loadMenu = json;
    });
  if (!select.value) {
    return;
  }
  let holder = Number(document.getElementById("quantity").value);
  for (let ctr = 0; ctr < Object.keys(loadMenu).length; ctr++) {
    if (select.value == loadMenu[ctr]["item_id"]) {
      item = loadMenu[ctr]["price"];
    }
  }
  let price = holder * item;
  costupdate.innerHTML = `Cost: $${price}`;
}

updater1.addEventListener("input", updateOrderCost);
updater2.addEventListener("input", updateOrderCost);
ordForm.addEventListener("submit", orderForm);
