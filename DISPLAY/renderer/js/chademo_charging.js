const connectChademoButton = document.querySelector(".connect-page-button-chademo");
const ChademoPercentNumber = document.querySelector(".num-chademo h2");
const CirclePercentChademo = document.querySelector(".svg-chademo-percent-show-display");

const startCustomChademoChargingButton = document.querySelector(".start-custom-page-button-chademo");
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
    const request_display_percent = await fetch("http://127.0.0.1:5000/display_chademo/BATTERY_LEVEL");
    let data = await request_display_percent.json();
    if (typeof(data) === "number") {
      ChademoBatteryLevel = data
      ChademoPercentNumber.textContent = ChademoBatteryLevel;
      CirclePercentChademo.style.strokeDashoffset = Math.floor(760 - (760 * data) / 100);
      let span = document.createElement("span");
      ChademoPercentNumber.appendChild(span);
      span.innerText = "%";
      return true;
    }
    else {
      SetDisconnectStatusChademo();
    }
  }
  else {
    return false;
  }

}

function SetConnectChademo(){
  ChademoIsConnected = true;
  TakeBatteryLevelChademo();
  connectChademoButton.classList.add("unactive-chademo-button");
  startChademoChargingButton.classList.remove("unactive-chademo-button");
  startCustomChademoChargingButton.classList.remove("unactive-chademo-button");
  disconnectChademoVehicleButton.classList.remove("unactive-chademo-button");
  ChargingCompleteChademo("start");
}

async function SendConncetChademo(){

  var requestOptions = {
    method: 'POST',
    redirect: 'follow'
  };
  const request_connect = await fetch("http://127.0.0.1:5000/vehicle_chademo/connect", requestOptions);
  if (request_connect.ok) {
    SetConnectChademo();
  }
}

function SetDisconnectStatusChademo(){
  connectChademoButton.classList.remove("unactive-chademo-button");
  disconnectChademoVehicleButton.classList.add("unactive-chademo-button");
  startChademoChargingButton.classList.add("unactive-chademo-button");
  startCustomChademoChargingButton.classList.add("unactive-chademo-button");
  ChademoPercentNumber.textContent = "--";
  CirclePercentChademo.style.strokeDashoffset = null;
  let span = document.createElement("span");
  ChademoPercentNumber.appendChild(span);
  span.innerText = "%"
  ChademoIsConnected = false;
  ChademoBatteryLevel = 0;
  ChargingCompleteChademo("disconnect");
}

async function SendDisconnectChademo(){
  var requestOptions = {
    method: 'POST',
    redirect: 'follow'
  };
  const request_connect = await fetch("http://127.0.0.1:5000/vehicle_chademo/disconnect", requestOptions);
  if (request_connect.ok) {
    SetDisconnectStatusChademo();
    customPercentChademo = 0
  }
}

let customPercentChademo = 0
async function CheckChargingChademo(){
  startChademoChargingButton.classList.add("unactive-chademo-button");
  disconnectChademoVehicleButton.classList.remove("unactive-chademo-button");
  startCustomChademoChargingButton.classList.add("unactive-chademo-button")
  ChargingCompleteChademo("ongoing")
  while (ChademoBatteryLevel < customPercentChademo && ChademoIsConnected == true){
    await sleep(1000);
    TakeBatteryLevelChademo();
  };
  if (ChademoIsConnected == true){
    ChargingCompleteChademo("complete");
  }
  else {
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
    customPercentChademo = 100
    CheckChargingChademo();

  }
}

function PrepareCustomChademoSession(){
  NumpadCustomSession.classList.remove("unactive-numeric-pad")
  NumpadCustomSession.classList.add("chademo-numpad")
}

connectChademoButton.addEventListener("click", () => {
  SendConncetChademo();
});

startChademoChargingButton.addEventListener("click", () =>{
  SendStartChademo();
})

startCustomChademoChargingButton.addEventListener("click", () => {
  PrepareCustomChademoSession();
})

disconnectChademoVehicleButton.addEventListener("click", () =>{
  SendDisconnectChademo();
})

