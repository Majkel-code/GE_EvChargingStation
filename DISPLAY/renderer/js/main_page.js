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
  if (!NumpadCustomSession.className.includes("unactive-numeric-pad")){
    CloseNumpadCustom();
  }
  else {
    preparationDisplay.classList.remove('active');
  }
}
closeChargingDisplayBtn.addEventListener("click", function() {
  closeChargingDisplay();
})

document.querySelector(".start").addEventListener("click", () =>{
  ChargingPreparationDisplay();
})


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
