# Bot Farm 
Is a system to simulate behaviour of Air Quality Monitoring System  
Bot Farm consists of **Bots** and the number of bots is given by **config.json** file  

## To run Bot Farm start 
start_bot_farm.py script

## Bot
Bot is emulate single device with sensors  
The number of sensors is 1-8 and given by **config.json** file  
Types of sensors is given by **config.json** file  
Bot can measure air parameters with its sensors and send this values to server  


## Sensor
Sensor is emulate a device for measuring one parameter of air  
Avaliable parameters:
- Temperature;
- Humidity;
- Pressure;
- PM2.5;
- PM10;
- CO;
- SO2;
- NO2;
- O3;
- NH3;
- H2S;
- CO2

## Config.json
Is a dict with parameters for all bots and all sensors.

### High level structure:  
{"bots": [conf_bot_1, ..., conf_bot_n]} - high level structure of config  
  
### conf_bot_n

{  
  "email": email_address ,  
  "channel": channel_num,  
  "bot_name": bot_name,  
  "api_key": api_key,  
  "update_time": update_time,  
  "sensors": [sensor_1, ..., sensor_n]  
 }  


- "email" - **Required.** Email address of account thingspeak account where the bot was created
- "channel" - **Required.** Number of channel of bot on thingspeak service
- "bot_name" - **Required.** Name of the bot (channel) on thingspeak service
- "api_key" - **Required.** API key of the bot (channel) on thingspeak service
- "update_time" - **Optional.** How often measure air parameters. Default 300s.
- "sensors" - **Required.** A list of sensors configs

### sensor_n

{  
  sensor_name: {sensor_conf}  
}  

- sensor_name - **Required.** Nov avaliable: "Temperature", "Humidity", "Pressure", "PM2.5", "PM10", "CO", "SO2", "NO2", "O3", "NH3", "H2S", "CO2"  
  
### sensor_conf  

{  
  "field": field,  
  "min_val": min_val,  
  "max_val": max_val,  
  "tend": tend,  
  "start_value": start_value  
}  

- field - **Required.** Number of field of the channel on thingspeak account  
- min_val - **Optional.** Minimum measurement limit for the sensor. Default value depend on sensor type  
- max_val - **Optional.** Maximum measurement limit for the sensor. Default value depend on sensor type  
- tend - **Optional.** Tendency to change the measured value. Avaliable: "fast_decrease", "decrease", "normal", "increase", "fast_increase". Default - "normal". Tend changes every 8h  
- start_value - **Optional.** First measured value. Default value depend on sensor type  

## Example
```json
{  
  "bots": [  
    {  
      "email": "ecomoniot3@gmail.com",  
      "channel": "1",  
      "bot_name": "bot_1",  
      "api_key": "JP8A6VDLKRU2KQY6",  
      "update_time": "200",  
      "sensors": [  
        {  
          "temperature": {  
            "field": "field1",  
            "min_val": "-40",  
            "max_val": "50",  
            "tend": "normal",  
            "start_value": "25"  
          }  
        },  
        {  
          "humidity": {  
            "field": "field2",  
            "min_val": "0",  
            "max_val": "100",  
            "tend": "decrease",  
            "start_value": "25"  
          }  
        },  
        {  
          "pressure": {  
            "field": "field3"  
          }  
        },  
        {  
          "PM2.5": {  
            "field": "field4"  
          }  
        }  
      ]  
    }  
  ]  
}  
```
One bot with 4 sensors
