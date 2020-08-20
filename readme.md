# Australian Securities Exchange Portfolio Sensor
[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg?style=for-the-badge)](https://github.com/custom-components/hacs)
[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge)](https://github.com/custom-components/hacs)

_Creates a sensor for Home Assistant for your ASX share portfolio_


## Lovelace Examples

![Example of the entities in Lovelace](https://github.com/simonhq/asx_portfolio/blob/master/asx_portfolio_entities.PNG)

![An Entity has the share information](https://github.com/simonhq/asx_portfolio/blob/master/asx_portfolio_entity.PNG)

## Installation

This app is best installed using [HACS](https://github.com/custom-components/hacs), so that you can easily track and download updates.

Alternatively, you can download the `asx_portfolio` directory from inside the `apps` directory here to your local `apps` directory, then add the configuration to enable the `asx_portfolio` module.

## How it works

The [ASX](https://www.asx.com.au/) site provides this information in JSON format, this just makes the information available as sensors in HA.

This information is only daily information, showing the latest close data, and other relevant information about a stock, it does not provide actual trading information.

As this is non time critical sensor, it only gets the information on a set time schedule, once per day at 5.12am before the opening of the market. 

### To Run Manually

You will need to create an input_boolean entity to watch for when to update the sensor. When this `input_boolean` is turned on, whether manually or by another automation you create, the scraping process will be run to create/update the sensor.

## AppDaemon Libraries

Please add the following packages to your appdaemon 4 configuration on the supervisor page of the add-on.

``` yaml
system_packages: []
python_packages: []
init_commands: []
```

No specific packages are required for this app.

## App configuration

In the apps.yaml file in the appdaemon/apps directory - 

```yaml
asx_sensor:
  module: asx_portfolio
  class: Get_ASX_portfolio_info
  PORT_NAME: "low_risk_inv"
  TICKER: "CBA:10,TLS:30,BHP:15"
  TICK_FLAG: "input_boolean.check_asx_portfolio_info"
```

key | optional | type | default | description
-- | -- | -- | -- | --
`module` | False | string | | `asx_portfolio`
`class` | False | string | | `Get_ASX_portfolio_info`
`PORT_NAME` | False | string | | the name to append to this portfolio
`TICKER` | False | string | | The comma separated symbols for each of the stocks you are interested in, with the number of stocks you own separated by a : e.g. CBA:10 is 10 shares of Commonwealth Bank
`TICK_FLAG` | False | string | | The name of the flag in HA for triggering this sensor update - e.g. input_boolean.check_asx_portfolio_info

## Sensors Created

This version will create a sensor for each stock you provide named based upon the port_name above

* sensor.asx_portfolio_{PORT_NAME}

## Issues/Feature Requests

Please log any issues or feature requests in this GitHub repository for me to review.