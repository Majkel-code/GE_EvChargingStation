const numberInput = document.querySelector(".number-input");
const confirmSessionButton = document.querySelector(".confirm-session-button");
const numberButtons = document.querySelectorAll(".number-button");
const deleteButton = document.querySelector(".delete");


numberButtons.forEach((button) => {
  button.addEventListener("click", () => {
    if (numberInput.value.length < 3) {
      if (Number(numberInput.value + button.dataset.number) > 100){
        return
      }
      else {
        const percentNumber = numberInput.value + button.dataset.number;
        numberInput.value = percentNumber;
      }
    }
  });
});


deleteButton.addEventListener("click", () => {
  const percentNumber = numberInput.value.slice(0, -1);
  numberInput.value = "";
  numberInput.value = percentNumber;
  confirmSessionButton.classList.remove("show");
});

function CloseNumpadCustom(){
  NumpadCustomSession.classList.add("unactive-numeric-pad");
  numberInput.value = "";

}

async function SendCustomAcStart(){
  var requestOptions = {
    method: 'POST',
    redirect: 'follow'
  };
  const request_start = await fetch(`http://127.0.0.1:5000/charger/start_ac_${customPercentAc}`, requestOptions);
  if (request_start.ok) {
    CloseNumpadCustom();
    CheckChargingAc();
  }
}

async function SendCustomChademoStart(){
  var requestOptions = {
    method: 'POST',
    redirect: 'follow'
  };
  const request_start = await fetch(`http://127.0.0.1:5000/charger/start_chademo_${customPercentChademo}`, requestOptions);
  if (request_start.ok) {
    CloseNumpadCustom();
    CheckChargingAc();
  }
}


confirmSessionButton.addEventListener("click", ()=>{
  if (NumpadCustomSession.className.includes("ac-numpad")) {
    customPercentAc = Number(numberInput.value);
    SendCustomAcStart();
    NumpadCustomSession.classList.remove("ac-numpad");
  }
  if (NumpadCustomSession.className.includes("chademo-numpad")) {
    customPercentChademo = Number(numberInput.value);
    SendCustomChademoStart();
    NumpadCustomSession.classList.remove("chademo-numpad");
  }
})
