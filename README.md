# GE_EvChargingStation
## _Green Energy_
<img width="400" alt="GE_EvChargingStationLOGO" src="https://github.com/Majkel-code/GE_EvChargingStation/assets/13604347/0617e712-5bf6-4836-8762-9cb22fd5d621">



GE_EvChargingStation is a charger and vehicle simulator.

- Run Server
- Connect vehicle
- Observe how charging flow is going

## Features

- Editing Charger settings
- Editiong Vehicle settings
- Run charge session for one or two outlets
- See console logs or preview output in dedicated display

GE_EvChargingStation is a lightweight charge station and vehicle simulator
where you can check charging flow, connectivity types and base "know how" it's work.

> Because electric vehicles are more efficient in converting energy to power cars and trucks,
> electricity across the board is cleaner and cheaper as a fuel for vehicles,
> even when that electricity comes from the dirtiest grid.


## Tech

GE_EvChargingStation uses a number of open source technologies to work properly:

- [FastApi] - FastAPI is a modern, fast (high-performance), web framework
- [Python] -  >= 3.11

## Installation

GE_EvChargingStation requires [Python](https://www.python.org/) v3.11+ to run.

Install the requirements.txt.

```sh
cd GE_EvChargingStation
pip3 install -r ./requirements.txt
```

## Development

Want to contribute? Great!
GE_EvChargingStation have two possibility to be used.
##### 1. Open your favorite Terminal and run these commands.

First Tab:

```sh
python3 ./server.py
```

Second Tab: (optional)
Thats it! In second tab you can send curl's or use for it  [Postman](https://www.postman.com/)

```sh
curl http://127.0.0.1:5000/is_alive
```
That's should return you "is_alive" state and in console with server, you will see code 200 if everything is fine.
Full list of curl's is placed on end of this READ.ME

#### Curl's list
##### Server
```sh
curl http://127.0.0.1:5000/is_alive # check server is alive
```
##### Charger
```sh
curl http://127.0.0.1:5000/charger/all # take all settings
```
```sh
curl http://127.0.0.1:5000/charger/<key> # return specific key
```
```sh
curl --location --request PUT 'http://127.0.0.1:5000/charger/' \
--header 'Content-Type: application/json' \
--data '{
  "key": "key",
  "value": value
}'
# change some value | key need to be str | value should be int/float or str but for non numeric value
# Example:
  "key": "EFFECTIVE_CHARGING_CAP",
  "value": 80
```
```sh
curl --location --request POST 'http://127.0.0.1:5000/charger/start_chademo'
# start charging to 100% CHADEMO protocol
```
```sh
curl --location --request POST 'http://127.0.0.1:5000/charger/start_ac'
# start charging to 100% AC protocol
```
```sh
curl --location --request POST 'http://127.0.0.1:5000/charger/start_chademo_<num>'
# start charging but into the specific battery level | example: start_chademo_80
```
```sh
curl --location --request POST 'http://127.0.0.1:5000/charger/start_ac_80'
# start charging but into the specific battery level | example: start_ac_80
```
```sh
curl --location 'http://127.0.0.1:5000/charger/outlets' # Shows which outlet are using for now
```

##### Vehicle AC/CHADEMO
```sh
curl --location --request POST 'http://127.0.0.1:5000/vehicle_ac/connect'
# connect vehicle using AC outlet
curl --location --request POST 'http://127.0.0.1:5000/vehicle_chademo/connect'
# connect vehicle using CHADEMO outlet
```
```sh
curl --location --request POST 'http://127.0.0.1:5000/vehicle_ac/disconnect'
# disconnect vehicle connected to AC outlet
curl --location --request POST 'http://127.0.0.1:5000/vehicle_chademo/disconnect'
# disconnect vehicle connected to CHADEMO outlet
```
```sh
curl --location 'http://127.0.0.1:5000/vehicle_ac/all'
# take all vehicle settings when connected to AC outlet
curl --location 'http://127.0.0.1:5000/vehicle_chademo/all'
# take all vehicle settings when connected to CHADEMO outlet
```
```sh
curl --location 'http://127.0.0.1:5000/vehicle_ac/<key>'
# take specific setting value AC vehicle
curl --location 'http://127.0.0.1:5000/vehicle_chademo/<key>'
# take specific setting value CHADEMO vehicle
```
```sh
curl --location --request PUT 'http://127.0.0.1:5000/vehicle_ac/' \
--header 'Content-Type: application/json' \
--data '{
  "key": "BATTERY_LEVEL",
  "value": 70
}'
# change some value in AC vehicle
# key need to be str | value should be int/float or str but for non numeric value
# Example:
  "key": "BATTERY_LEVEL",
  "value": 50
```
```sh
curl --location --request PUT 'http://127.0.0.1:5000/vehicle_chademo/' \
--header 'Content-Type: application/json' \
--data '{
  "key": "BATTERY_LEVEL",
  "value": 70
}'
# change some value in CHADEMO vehicle
# key need to be str | value should be int/float or str but for non numeric value
# Example:
  "key": "BATTERY_LEVEL",
  "value": 50
```
# TODO
#### 2. Run it on external machine (linux) with dedicated display
## License

MIT

**Free Software, Hell Yeah!**

