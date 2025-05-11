let chademo_is_ongoing = false
let ac_is_ongoing = false

async function CheckStatus(){
  const request_status = await fetch("http://127.0.0.1:5000/charger/outlets");
  let used_outlets = await request_status.json();
  if (request_status.ok) {
    if( used_outlets["data"]["parameters"]["CHADEMO"] !== "Not used"){
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
    if(used_outlets["data"]["parameters"]["AC"] !== "Not used") {
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
    if ( used_outlets["data"]["parameters"]["CHADEMO"] === "Not used"){
      SetDisconnectStatusChademo();
    }
    if (used_outlets["data"]["parameters"]["AC"] === "Not used"){
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
