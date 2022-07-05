// Open in dbdiagram.io

Table users {
  id int [pk, increment] // auto-increment
  login varchar
  password_hash varchar
  xgrow_key varchar
}

Table xgrow_units {
  xgrow_key varchar [pk, increment]
  pots pots
}

Ref: users.xgrow_key - xgrow_units.xgrow_key
Ref: air_sensor.xgrow_key - xgrow_units.xgrow_key


Table air_sensor {
  id int [pk, increment]
  xgrow_key varchar

  temperature float
  humidity float

  stats air_stats
}

Ref: air_sensor.stats > air_stats.id


Table air_stats {
  id int [pk, increment]

  timestamp timestamp
  temperature float
  humidity float
}

Ref: xgrow_units.xgrow_key > pots.id
Ref: xgrow_units.xgrow_key > fans.id
Ref: xgrow_units.xgrow_key > custom_devices.id

Table pots {
  id int [pk, increment]
  xgrow_key varchar
  index int
  active bool

  autoWatering bool
  humidity float
  minHumidity float
  maxHumidity float

  pumpWorking bool
  automaticWateringTime int
  pumpWorkingTimeLimit int
  wateringCycleTimeInHour int
  manualWateringTime int

  stats pot_stats
}

Ref: pots.stats > pot_stats.id


Table pot_stats {
  id int [pk, increment]

  timestamp timestamp
  humidity float
  pumpCurrentStatus bool
}

Table fans {
  id int [pk, increment]
  xgrow_key varchar
  index int
  active bool

  working bool
}

// grzałki,lampy
Table custom_devices {
  id int [pk, increment]
  xgrow_key varchar
  index int
  type varchar
  active bool
  working bool
  timer timer
  air_sensor_triggers air_sensor_triggers
}


Ref: custom_devices.timer - timers.id
Ref: custom_devices.air_sensor_triggers > air_sensor_triggers.id


Table timers {
  id int [pk, increment]
  xgrow_key varchar
  index int
  device_id int
  value float

  startTime datetime
  stopTime datetime
  lightCycle int
}

Table air_sensor_triggers {
  id int [pk, increment]
  xgrow_key varchar
  index int
  device_id int
  type varchr // TempMax, TempMin, HumMax, HumMin
  value float
}