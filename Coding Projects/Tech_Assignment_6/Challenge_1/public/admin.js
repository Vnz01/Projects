const menuscreen = document.getElementById("menu");
const orderscreen = document.getElementById("orderstatus");
const addForm = document.getElementById("add");
const delForm = document.getElementById("remove");
const editForm = document.getElementById("edit");

async function load() {
  await fetch("/loadMenu")
    .then((response) => {
      return response.json();
    })
    .then((json) => {
      loadMenu = json;
    });
  var loadMenu;
  menuscreen.innerHTML = "";
  for (let ctr = 0; ctr < Object.keys(loadMenu).length; ctr++) {
    let menuBoard = document.createElement("div");
    menuBoard.classList.add("menuClass");
    menuBoard.innerHTML = `<div class="menuItemsClass" >
          <p>Item ID: ${loadMenu[ctr]["item_id"]}</p>
          <p>Name: ${loadMenu[ctr]["name"]}</p>
          <p>Price: $${loadMenu[ctr]["price"]}</p>
        </div><br>`;
    menuscreen.appendChild(menuBoard);
  }
  loadOrders();
}

async function edit() {
  let editid = document.getElementById("editid").value;
  let editname = document.getElementById("editname").value;
  let editcost = document.getElementById("editcost").value;
  let dict = { id: editid, name: editname, price: editcost };
  await fetch(`/editMenu`, {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify(dict),
  });
  load();
}

async function remove() {
  let removeid = document.getElementById("removeid").value;
  let dict = { id: removeid };
  await fetch(`/deleteMenu`, {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify(dict),
  });
  load();
}

async function add() {
  let nameItem = document.getElementById("addname").value;
  let costItem = document.getElementById("addcost").value;
  let dict = {
    name: nameItem,
    price: costItem,
  };
  await fetch("/addMenu", {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify(dict),
  });
  load();
}

async function loadOrders() {
  await fetch("/loadOrder")
    .then((response) => {
      return response.json();
    })
    .then((json) => {
      loadOrder = json;
    });
  var loadOrder;
  orderscreen.innerHTML = "";
  for (let ctr = 0; ctr < Object.keys(loadOrder).length; ctr++) {
    let orderBoard = document.createElement("div");
    orderBoard.classList.add("orderClass");
    let colorselector;
    if (loadOrder[ctr]["status"] == "Pending") {
      colorselector = "yellow";
    } else {
      colorselector = "lightgreen";
    }
    orderBoard.innerHTML = `<div 
    class="orderItemsClass">
          <p>${loadOrder[ctr]["customer"]}</p>
          <p>${loadOrder[ctr]["name"]}</p>
          <p>${loadOrder[ctr]["quantity"]}</p>
          <button style="background-color: ${colorselector}" onclick="pendingBtn(${ctr})" id="Btn${ctr}">${loadOrder[ctr]["status"]}</button>
        </div><br>`;
    orderscreen.appendChild(orderBoard);
  }
}

async function pendingBtn(count) {
  let btnC = document.getElementById(`Btn${count}`);
  let state;
  if (btnC.innerHTML == "Pending") {
    btnC.style.background = "lightgreen";
    btnC.innerHTML = "Complete";
    state = "Complete";
  } else if (btnC.innerHTML == "Complete") {
    btnC.style.background = "Yellow";
    btnC.innerHTML = "Pending";
    state = "Pending";
  }
  let dict = {
    order_id: (count + 1).toString(),
    status: state,
  };
  await fetch("/status", {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify(dict),
  });
}

async function clearOrders() {
  await fetch("/clear");
  loadOrders();
}

addForm.addEventListener("submit", add);
delForm.addEventListener("submit", remove);
editForm.addEventListener("submit", edit);
