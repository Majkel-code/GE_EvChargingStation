const connectAcButton = document.querySelector(".connect-page-button-ac");
const acPercentNumber = document.querySelector(".num-ac h2");
const CirclePercentAc = document.querySelector(".svg-ac-percent-show-display");

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
async function TakeBatteryLevelAc(){
  if (AcIsConnected){
    const request_display_percent = await fetch("http://127.0.0.1:5000/display_ac/BATTERY_LEVEL");
    let data = await request_display_percent.json();
    if (typeof(data) === "number"){
      AcBatteryLevel = data
      acPercentNumber.textContent = data;
      CirclePercentAc.style.strokeDashoffset = Math.floor(760 - (760 * data) / 100);
      let span = document.createElement("span");
      acPercentNumber.appendChild(span);
      span.innerText = "%";
      return true;
    }
  }
  else {
    return false;
  }

}

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

connectAcButton.addEventListener("click", () => {
  SendAcConncet();
});

startAcChargingButton.addEventListener("click", () =>{
  SendAcStart();
})

startCustomAcChargingButton.addEventListener("click", () => {
  PrepareCustomAcSession();
})

disconnectAcVehicleButton.addEventListener("click", () =>{
  SendAcDisconnect();
})

