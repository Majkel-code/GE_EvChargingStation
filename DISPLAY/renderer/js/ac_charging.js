const connectAcButton = document.querySelector(".connect-page-button-ac");
const CirclePercentAc = document.querySelector(".svg-ac-percent-show-display");

const CircleAcDivInformation = document.querySelector(".percent-ac")

const AcCircleRegularInformation = document.querySelector(".regular-info-ac");
const acPercentNumber = document.querySelector(".regular-info-ac h2");

const AcCircleMoreInformation = document.querySelector(".more_ac_info");
const acPercentNumberMore = document.querySelector(".more_ac_info h2");
const KwPerMinCircleInfo = document.querySelector(".more_ac_info-kw-min");
const ChargedKwCircleInfo = document.querySelector(".more_ac_info-charged-kw");

const startCustomAcChargingButton = document.querySelector(".start-custom-page-button-ac");
const startAcChargingButton = document.querySelector(".start-page-button-ac");
const disconnectAcVehicleButton = document.querySelector(".disconnect-page-button-ac");

let AcIsConnected = false;

function ChargingCompleteAc(create_remove){
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
let AcKwPerMin = 0
let AcChargedKw = 0
async function TakeBatteryLevelAc(){
  if (AcIsConnected){
    const request_display_percent = await fetch("http://127.0.0.1:5000/display_ac/charging_ac");
    let data = await request_display_percent.json()
    console.log(data["BATTERY_LEVEL"])
    if (typeof(data["BATTERY_LEVEL"]) === "number"){
      AcBatteryLevel = data["BATTERY_LEVEL"];
      AcKwPerMin = data["AC_KW_PER_MIN"];
      AcChargedKw = data["CHARGED_KW"];
      acPercentNumber.textContent = AcBatteryLevel;
      acPercentNumberMore.textContent = AcBatteryLevel;
      CirclePercentAc.style.strokeDashoffset = Math.floor(760 - (760 * AcBatteryLevel) / 100);
      FillMoreInfoAc();
      return true;
    }
  }
  else {
    return false;
  }
}
function FillMoreInfoAc(){
  let span_info_ac = document.createElement("span");
  acPercentNumber.appendChild(span_info_ac);
  span_info_ac.innerText = "%";

  let span_more_info_ac = document.createElement("span");
  acPercentNumberMore.appendChild(span_more_info_ac);
  span_more_info_ac.innerText = "%";
  KwPerMinCircleInfo.textContent = AcKwPerMin.toFixed(4);
  ChargedKwCircleInfo.textContent = AcChargedKw.toFixed(4);
}


function ChangeInfoStageAc(){
  if (AcCircleMoreInformation.className.includes("unactive_info_ac")){
    AcCircleMoreInformation.classList.remove("unactive_info_ac");
    AcCircleRegularInformation.classList.add("unactive_info_ac");
  }
  else if (AcCircleRegularInformation.className.includes("unactive_info_ac")){
    AcCircleMoreInformation.classList.add("unactive_info_ac");
    AcCircleRegularInformation.classList.remove("unactive_info_ac");
  }
}

CircleAcDivInformation.addEventListener("pointerup", ()=>{
  ChangeInfoStageAc();
})

function SetConnectAc(){
  AcIsConnected = true;
  TakeBatteryLevelAc();
  connectAcButton.classList.add("unactive-ac-button");
  startAcChargingButton.classList.remove("unactive-ac-button");
  startCustomAcChargingButton.classList.remove("unactive-ac-button");
  disconnectAcVehicleButton.classList.remove("unactive-ac-button")
  ChargingCompleteAc("start");
}

async function SendAcConncet(){

  var requestOptions = {
    method: 'POST',
    redirect: 'follow'
  };
  const request_connect = await fetch("http://127.0.0.1:5000/vehicle_ac/connect", requestOptions);
  if (request_connect.ok) {
    SetConnectAc();
  }
}

function SetDisconnectStatusAc(){
  connectAcButton.classList.remove("unactive-ac-button");
  disconnectAcVehicleButton.classList.add("unactive-ac-button");
  startAcChargingButton.classList.add("unactive-ac-button");
  startCustomAcChargingButton.classList.add("unactive-ac-button");
  acPercentNumber.textContent = "--";
  acPercentNumberMore.textContent = "--";
  KwPerMinCircleInfo.textContent = 0.0;
  ChargedKwCircleInfo.textContent = 0.0;
  CirclePercentAc.style.strokeDashoffset = null;
  let span = document.createElement("span");
  acPercentNumber.appendChild(span);
  span.innerText = "%"
  AcIsConnected = false;
  ChargingCompleteAc("disconnect");
}

async function SendAcDisconnect(){
  var requestOptions = {
    method: 'POST',
    redirect: 'follow'
  };
  const request_connect = await fetch("http://127.0.0.1:5000/vehicle_ac/disconnect", requestOptions);
  if (request_connect.ok) {
    SetDisconnectStatusAc();
    customPercentAc = 0
  }
}

let customPercentAc = 0
async function CheckChargingAc(){
  startAcChargingButton.classList.add("unactive-ac-button");
  startCustomAcChargingButton.classList.add("unactive-ac-button")
  disconnectAcVehicleButton.classList.remove("unactive-ac-button");
  ChargingCompleteAc("ongoing")
  while (AcBatteryLevel < customPercentAc && AcIsConnected == true){
    await sleep(1000);
    TakeBatteryLevelAc();
  };
  if (AcIsConnected == true){
    ChargingCompleteAc("complete");
  }
  else {
    ChargingCompleteAc("disconnect");
  }
}

async function SendAcStart(){
  var requestOptions = {
    method: 'POST',
    redirect: 'follow'
  };
  const request_start = await fetch("http://127.0.0.1:5000/charger/start_ac", requestOptions);
  if (request_start.ok) {
    customPercentAc = 100
    CheckChargingAc();
  }
}

const NumpadCustomSession = document.querySelector(".numpad-custom-session")
function PrepareCustomAcSession(){
  NumpadCustomSession.classList.remove("unactive-numeric-pad")
  NumpadCustomSession.classList.add("ac-numpad")
}

connectAcButton.addEventListener("pointerup", () => {
  SendAcConncet();
});

startAcChargingButton.addEventListener("pointerup", () =>{
  SendAcStart();
})

startCustomAcChargingButton.addEventListener("pointerup", () => {
  PrepareCustomAcSession();
})

disconnectAcVehicleButton.addEventListener("pointerup", () =>{
  SendAcDisconnect();
})
