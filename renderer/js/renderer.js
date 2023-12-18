// Definicja zmiennych
// Definicja zmiennych
const buttons = document.querySelectorAll(".btn");
const container = document.querySelector(".container");

const cssButton = document.querySelector(".btn.css");
const chademoButton = document.querySelector(".btn.chademo");

const enButton = document.querySelector(".btn.en.right-btn");
const helpButton = document.querySelector(".btn.help.right-btn");

const helpDisplay = document.querySelector(".help-display");
const closeHelpButton = document.querySelector(".close-help-display ");

const infoMessage = document.querySelector(".info-message p");

const preparationDisplay = document.querySelector(".charging-page");
const closeChargingDisplayBtn = document.querySelector(".close-charging-display");


  function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

// CHARGING DISPLAY
function ChargingPreparationDisplay() {
  preparationDisplay.classList.add('active');
}

function closeChargingDisplay() {
  preparationDisplay.classList.remove('active');
}
closeChargingDisplayBtn.addEventListener("click", function() {
  closeChargingDisplay();
})

document.querySelector(".start").addEventListener("click", () =>{
  ChargingPreparationDisplay();
})
// _______________________________

// HELP DISPLAY
function closeHelpDisplay() {
  let = helpMessage = document.querySelector(".help-message");
  helpMessage.textContent = "";
  helpDisplay.classList.remove('active');
}

function showMessage(title, message) {
  let helpTitle = document.querySelector(".help-title");
  let = helpMessage = document.querySelector(".help-message");
  helpTitle.textContent = title;
  helpMessage.textContent = message;
  helpDisplay.classList.add('active');
}

closeHelpButton.addEventListener("click", function() {
  closeHelpDisplay();
})

cssButton.addEventListener("click", () => {
  showMessage("CSS", "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.");
});

chademoButton.addEventListener("click", () => {
  showMessage("CHADEMO", "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.");
});

enButton.addEventListener("click", () => {
  showMessage("EN", "Maybe it will have translate method to use in charger");
});

helpButton.addEventListener("click", () => {
  showMessage("HELP", "GE_EvChargingStation is a lightweight charge station and vehicle simulator where you can check charging flow, connectivity types and base 'know how' it's work.");
});

// _______________________________


const connectAcButton = document.querySelector(".connect-page-button-ac");
const acPercentNumber = document.querySelector(".num-ac h2");
const CirclePercentAc = document.querySelector(".svg-ac-percent-show-display");

const startAcChargingButton = document.querySelector(".start-page-button-ac");
const disconnectAcVehicleButton = document.querySelector(".disconnect-page-button-ac");

let AcIsConnected = false;

function ChargingComplete(create_remove){
  const ChargingStatusMessage = document.querySelector(".card-one h4");
  if (create_remove == "complete") {
    ChargingStatusMessage.textContent = "CHARGING COMPLETE"
  }
  else if (create_remove == "disconnect") {
    ChargingStatusMessage.textContent = "WAITING FOR CONNECT..."
  }
  else if ( create_remove == "ongoing"){
    ChargingStatusMessage.textContent = "CHARGE ONGOING"
  }
  else if (create_remove == "start"){
    ChargingStatusMessage.textContent = "WAITING FOR START..."
  }
}


let AcBatteryLevel = 0
async function TakeAcBatteryLevel(){
  if (AcIsConnected){
    const request_display_percent = await fetch("http://127.0.0.1:5000/vehicle_ac/BATTERY_LEVEL");
    let data = await request_display_percent.json();
    AcBatteryLevel = data
    acPercentNumber.textContent = data;
    CirclePercentAc.style.strokeDashoffset = Math.floor(760 - (760 * data) / 100);
    let span = document.createElement("span");
    acPercentNumber.appendChild(span);
    span.innerText = "%";
    return true;
  }
  else {
    return false;
  }

}


async function SendAcConncet(){

  var requestOptions = {
    method: 'POST',
    redirect: 'follow'
  };
  const request_connect = await fetch("http://127.0.0.1:5000/vehicle_ac/connect", requestOptions);
  if (request_connect.ok) {
    AcIsConnected = true;
    TakeAcBatteryLevel();
    connectAcButton.classList.add("unactive-ac-button");
    startAcChargingButton.classList.remove("unactive-ac-button");
    ChargingComplete("start");
  }
}

async function SendAcDisconnect(){
  var requestOptions = {
    method: 'POST',
    redirect: 'follow'
  };
  const request_connect = await fetch("http://127.0.0.1:5000/vehicle_ac/disconnect", requestOptions);
  if (request_connect.ok) {
    // TakeAcBatteryLevel();
    connectAcButton.classList.remove("unactive-ac-button");
    disconnectAcVehicleButton.classList.add("unactive-ac-button");
    acPercentNumber.textContent = "--";
    CirclePercentAc.style.strokeDashoffset = null;
    let span = document.createElement("span");
    acPercentNumber.appendChild(span);
    span.innerText = "%"
    AcIsConnected = false;
    ChargingComplete("disconnect");
  }
}


async function SendAcStart(){
  var requestOptions = {
    method: 'POST',
    redirect: 'follow'
  };
  const request_start = await fetch("http://127.0.0.1:5000/charger/start_ac", requestOptions);
  if (request_start.ok) {
    startAcChargingButton.classList.add("unactive-ac-button");
    disconnectAcVehicleButton.classList.remove("unactive-ac-button");
    ChargingComplete("ongoing")
    while (AcBatteryLevel < 100 && AcIsConnected == true){
      await sleep(2000);
      TakeAcBatteryLevel();
    };
    if (AcIsConnected == true){
      ChargingComplete("complete");
    }
    else {
      ChargingComplete("disconnect");
    }
  }

}

connectAcButton.addEventListener("click", () => {
  SendAcConncet();
});

startAcChargingButton.addEventListener("click", () =>{
  SendAcStart();
})

disconnectAcVehicleButton.addEventListener("click", () =>{
  SendAcDisconnect();
})



// CHADEMO CHARGING

const connectChademoButton = document.querySelector(".connect-page-button-chademo");
const ChademoPercentNumber = document.querySelector(".num-chademo h2");
const CirclePercentChademo = document.querySelector(".svg-chademo-percent-show-display");

const startChademoChargingButton = document.querySelector(".start-page-button-chademo");
const disconnectChademoVehicleButton = document.querySelector(".disconnect-page-button-chademo");

let ChademoIsConnected = false;

function ChargingCompleteChademo(create_remove){
  const ChargingStatusMessage = document.querySelector(".card-two h4");
  if (create_remove == "complete") {
    ChargingStatusMessage.textContent = "CHARGING COMPLETE"
  }
  else if (create_remove == "disconnect") {
    ChargingStatusMessage.textContent = "WAITING FOR CONNECT..."
  }
  else if ( create_remove == "ongoing"){
    ChargingStatusMessage.textContent = "CHARGE ONGOING"
  }
  else if (create_remove == "start"){
    ChargingStatusMessage.textContent = "WAITING FOR START..."
  }
}


let ChademoBatteryLevel = 0
async function TakeBatteryLevelChademo(){
  if (ChademoIsConnected){
    const request_display_percent = await fetch("http://127.0.0.1:5000/vehicle_chademo/BATTERY_LEVEL");
    let data = await request_display_percent.json();
    ChademoBatteryLevel = data
    ChademoPercentNumber.textContent = data;
    CirclePercentChademo.style.strokeDashoffset = Math.floor(760 - (760 * data) / 100);
    let span = document.createElement("span");
    ChademoPercentNumber.appendChild(span);
    span.innerText = "%";
    return true;
  }
  else {
    return false;
  }

}


async function SendConncetChademo(){

  var requestOptions = {
    method: 'POST',
    redirect: 'follow'
  };
  const request_connect = await fetch("http://127.0.0.1:5000/vehicle_chademo/connect", requestOptions);
  if (request_connect.ok) {
    ChademoIsConnected = true;
    TakeBatteryLevelChademo();
    connectChademoButton.classList.add("unactive-chademo-button");
    startChademoChargingButton.classList.remove("unactive-chademo-button");
    ChargingCompleteChademo("start");
  }
}

async function SendDisconnectChademo(){
  var requestOptions = {
    method: 'POST',
    redirect: 'follow'
  };
  const request_connect = await fetch("http://127.0.0.1:5000/vehicle_chademo/disconnect", requestOptions);
  if (request_connect.ok) {
    // TakeAcBatteryLevel();
    connectChademoButton.classList.remove("unactive-chademo-button");
    disconnectChademoVehicleButton.classList.add("unactive-chademo-button");
    ChademoPercentNumber.textContent = "--";
    CirclePercentChademo.style.strokeDashoffset = null;
    let span = document.createElement("span");
    ChademoPercentNumber.appendChild(span);
    span.innerText = "%"
    ChademoIsConnected = false;
    ChargingCompleteChademo("disconnect");
  }
}


async function SendStartChademo(){
  var requestOptions = {
    method: 'POST',
    redirect: 'follow'
  };
  const request_start = await fetch("http://127.0.0.1:5000/charger/start_chademo", requestOptions);
  if (request_start.ok) {
    startChademoChargingButton.classList.add("unactive-chademo-button");
    disconnectChademoVehicleButton.classList.remove("unactive-chademo-button");
    ChargingCompleteChademo("ongoing")
    while (ChademoBatteryLevel < 100 && ChademoIsConnected == true){
      await sleep(2000);
      TakeBatteryLevelChademo();
    };
    if (ChademoIsConnected == true){
      ChargingCompleteChademo("complete");
    }
    else {
      ChargingCompleteChademo("disconnect");
    }
  }

}

connectChademoButton.addEventListener("click", () => {
  SendConncetChademo();
});

startChademoChargingButton.addEventListener("click", () =>{
  SendStartChademo();
})

disconnectChademoVehicleButton.addEventListener("click", () =>{
  SendDisconnectChademo();
})

