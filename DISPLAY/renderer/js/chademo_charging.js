const connectChademoButton = document.querySelector(".connect-page-button-chademo");
const CirclePercentChademo = document.querySelector(".svg-chademo-percent-show-display");

const CircleChademoDivInformation = document.querySelector(".percent-chademo");

const ChademoCircleRegularInformation = document.querySelector(".regular-info-chademo");
const ChademoPercentNumber = document.querySelector(".num-chademo h2");

const ChademoCircleMoreInformation = document.querySelector(".more_chademo_info");
const chademoPercentNumberMore = document.querySelector(".more_chademo_info h2");
const KwPerMinCircleInfoChademo = document.querySelector(".more_chademo_info-kw-min");
const ChargedKwCircleInfoChademo = document.querySelector(".more_chademo_info-charged-kw");

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
let ChademoKwPerMin = 0
let ChademoChargedKw = 0
async function TakeBatteryLevelChademo(){
  if (ChademoIsConnected){
    const request_display_percent = await fetch("http://127.0.0.1:5000/display_chademo/charging_chademo");
    let data = await request_display_percent.json();
    if (typeof(data["BATTERY_LEVEL"]) === "number") {
      ChademoBatteryLevel = data["BATTERY_LEVEL"];
      ChademoKwPerMin = data["CHADEMO_KW_PER_MIN"];
      ChademoChargedKw = data["CHARGED_KW"];
      ChademoPercentNumber.textContent = ChademoBatteryLevel;
      chademoPercentNumberMore.textContent = ChademoBatteryLevel;
      CirclePercentChademo.style.strokeDashoffset = Math.floor(760 - (760 * ChademoBatteryLevel) / 100);
      FillMoreInfoChademo();
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

function FillMoreInfoChademo(){
  let span_info = document.createElement("span");
  ChademoPercentNumber.appendChild(span_info);
  span_info.innerText = "%";

  let span_more_info = document.createElement("span");
  chademoPercentNumberMore.appendChild(span_more_info);
  span_more_info.innerText = "%";
  KwPerMinCircleInfoChademo.textContent = ChademoKwPerMin.toFixed(4);
  ChargedKwCircleInfoChademo.textContent = ChademoChargedKw.toFixed(4);
}

function ChangeInfoStageChademo(){
  if (ChademoCircleMoreInformation.className.includes("unactive_info_chademo")){
    ChademoCircleMoreInformation.classList.remove("unactive_info_chademo");
    ChademoCircleRegularInformation.classList.add("unactive_info_chademo");
  }
  else if (ChademoCircleRegularInformation.className.includes("unactive_info_chademo")){
    ChademoCircleMoreInformation.classList.add("unactive_info_chademo");
    ChademoCircleRegularInformation.classList.remove("unactive_info_chademo");
  }
}

CircleChademoDivInformation.addEventListener("click", ()=>{
  ChangeInfoStageChademo();
})


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
  chademoPercentNumberMore.textContent = "--";
  KwPerMinCircleInfoChademo.textContent = 0.0;
  ChargedKwCircleInfoChademo.textContent = 0.0;
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
