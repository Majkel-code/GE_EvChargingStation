const buttons = document.querySelectorAll(".btn");
const container = document.querySelector(".container");

const cssButton = document.querySelector(".btn.ac");
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


// const changeSettingsPage = document.querySelector(".custom-settings-setter-page");
// const closeChangeSettingsPageBtn = document.querySelector(".close-custom-settings-display");

// function CustomSettingsSetterPage() {
//   changeSettingsPage.classList.add('active');
// }

// function closeChangeSettingsPage() {
//   changeSettingsPage.classList.remove('active');
// }

// document.querySelector(".custom").addEventListener("click", () =>{
//   CustomSettingsSetterPage();
// })

// closeChangeSettingsPageBtn.addEventListener("click", () =>{
//   closeChangeSettingsPage();
// })
// _______________________________

// HELP DISPLAY
function closeHelpDisplay() {
  let = helpMessage = document.querySelectorAll(".help-message p");
  helpMessage.forEach(element => {
    element.textContent = "";
    element.style.margin = "0px";
  });

  helpDisplay.classList.remove('active');
}

function showMessage(title, first_p_message, second_p_message = null, third_p_message = null) {
  let helpTitle = document.querySelector(".help-title");
  let = helpMessage = document.querySelectorAll(".help-message p");
  helpTitle.textContent = title;
  helpMessage[0].textContent = first_p_message;
  helpMessage[1].textContent = second_p_message;
  helpMessage[2].textContent = third_p_message;
  helpDisplay.classList.add('active');
}

closeHelpButton.addEventListener("click", function() {
  closeHelpDisplay();
})

cssButton.addEventListener("click", () => {
  showMessage("AC", "From a technical point of view, the process of charging an electric car with this type of charger is less effective than when using a DC station. The key issue is the fact that we do not charge the batteries directly with alternating current, but along the way it must be 'rectified' by the built-in charger. This is one of the main disadvantages of AC charging because converters limit its power.");
});

chademoButton.addEventListener("click", () => {
  let chademo_title = "CHADEMO"
  let = chademo_message = "CHADEMO is a standard for charging electric cars with direct current - DC. It is used by the so-called fast chargers, characterized by much greater power, which in turn ensures a much shorter charging time for the battery in an electric car."
  showMessage(chademo_title, chademo_message);
});

enButton.addEventListener("click", () => {
  showMessage("EN", "Maybe it will have translate method to use in charger");
});

helpButton.addEventListener("click", () => {
  let help_title = "HELP";
  let help_first_p_message = "GE_EvChargingStation is a lightweight charge station and vehicle simulator where you can check charging flow, connectivity types and base 'know how' it's work.";
  let help_second_p_message = "When you click 'START' button on the middle of the screen you will see, new display. Here you can choose charging method between AC and DC or use both at the same time. In this display, vehicle settings will be read by a simulator and prepare charger for simulate charging flow.";
  let help_third_p_message = "TO DO!!!"
  showMessage(help_title, help_first_p_message, help_second_p_message, help_third_p_message);

});

// _______________________________


const connectAcButton = document.querySelector(".connect-page-button-ac");
const acPercentNumber = document.querySelector(".num-ac h2");
const CirclePercentAc = document.querySelector(".svg-ac-percent-show-display");

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
    else {

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
  }
}

async function CheckChargingAc(){
  startAcChargingButton.classList.add("unactive-ac-button");
  disconnectAcVehicleButton.classList.remove("unactive-ac-button");
  ChargingCompleteAc("ongoing")
  while (AcBatteryLevel < 100 && AcIsConnected == true){
    await sleep(2000);
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
    CheckChargingAc();
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
  }
}

async function CheckChargingChademo(){

  startChademoChargingButton.classList.add("unactive-chademo-button");
  disconnectChademoVehicleButton.classList.remove("unactive-chademo-button");
  ChargingCompleteChademo("ongoing")
  while (ChademoBatteryLevel < 100 && ChademoIsConnected == true){
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
    CheckChargingChademo();

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



// _______________________________

let chademo_is_ongoing = false
let ac_is_ongoing = false

async function CheckStatus(){
  const request_status = await fetch("http://127.0.0.1:5000/charger/outlets");
  let used_outlets = await request_status.json();
  if (request_status.ok) {
    if( used_outlets["CHADEMO"] !== "Not used"){
      if (!ChademoIsConnected){
        ChargingPreparationDisplay();
        SetConnectChademo();
      }
      else{
        const request_energy_ongoing_chademo = await fetch("http://127.0.0.1:5000/charger/energy_ongoing_chademo");
        let request_energy_ongoing_chademo_data = await request_energy_ongoing_chademo.json();
        if (request_energy_ongoing_chademo.ok){
          console.log(request_energy_ongoing_chademo_data);
          if (request_energy_ongoing_chademo_data === true){
            chademo_is_ongoing = true;
            CheckChargingChademo();
          }
        }
      }
    }
    if(used_outlets["AC"] !== "Not used") {
      if (!AcIsConnected){
        ChargingPreparationDisplay();
        SetConnectAc();
      }
      else{
        const request_energy_ongoing_ac = await fetch("http://127.0.0.1:5000/charger/energy_ongoing_ac");
        let request_energy_ongoing_ac_data = await request_energy_ongoing_ac.json();
        if (request_energy_ongoing_ac.ok){
          console.log(request_energy_ongoing_ac_data);
          if (request_energy_ongoing_ac_data === true){
            ac_is_ongoing = true;
            CheckChargingAc();
          }
        }
      }
    }
    if ( used_outlets["CHADEMO"] === "Not used"){
      SetDisconnectStatusChademo();
    }
    if (used_outlets["AC"] === "Not used"){
      SetDisconnectStatusAc();
    }
  }
}
const loop = async () => {
  let sleep_ms = 5000;
  while (true) {
    await sleep(sleep_ms);
    if (ChademoBatteryLevel > 0 || AcBatteryLevel > 0) {
      sleep_ms = 10000;
    }

    if (true){
      CheckStatus();
    }
    if (!AcIsConnected){
      ac_is_ongoing = false;
    }
    if (!ChademoIsConnected){
      chademo_is_ongoing = false;
    }
  }

}
loop()
