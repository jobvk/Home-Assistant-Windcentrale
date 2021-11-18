# Home Assistant sensor component for Windcentrale

[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg)](https://github.com/custom-components/hacs)
[![GitHub release (latest by date)](https://img.shields.io/github/v/release/jobvk/Home-Assistant-Windcentrale)](https://github.com/jobvk/Home-Assistant-Windcentrale/releases)
[![GitHub](https://img.shields.io/badge/license-Apache-blue)](LICENSE)

[![Maintenance](https://img.shields.io/badge/Maintained%3F-Yes-brightgreen.svg)](https://github.com/jobvk/Home-Assistant-Windcentrale/graphs/commit-activity)
[![Maintainer](https://img.shields.io/badge/Maintainer-jobvk-brightgreen.svg)](https://github.com/jobvk/)
[![Ask Me Anything !](https://img.shields.io/badge/Ask%20me-anything-orange.svg)](https://discord.gg/T3tK4Jsquc)
[![Discord](https://img.shields.io/discord/882015341520244786?color=%09%237289DA)](https://discord.gg/T3tK4Jsquc)

[![Buy me a coffee](https://img.shields.io/static/v1.svg?label=Buy%20me%20a%20coffee&logo=buy%20me%20a%20coffee&logoColor=white&labelColor=blue&message=donate&color=Black)](https://www.buymeacoffee.com/jobvk)

Home Assistant component for the Windcentrale

The `Windcentrale` component is a Home Assistant component which lets you get sensor and news data from all wind turbines.

The official website https://www.windcentrale.nl

## Table of Contents

* [Installation](#installation)
  * [Installation through HACS](#installation-through-hacs)
  * [Manual Installation](#manual-installation)
* [Configuration](#configuration)
  * [Set Up](#set-up)
  * [Options](#options)
* [Sensors](#sensors)
  * [Live](#live)
  * [History](#history)
  * [News](#news)
* [Example](#example)
* [Energy Management tab](#energy-management-tab)
* [ToDo](#todo)
* [License](#license)
* [Disclaimer](#disclaimer)
* [Say thank you](#say-thank-you)

## Installation

### Installation through HACS

1. Ensure that [HACS](https://hacs.xyz/) is installed.
2. Click on the `+ Explore & add repositories`
3. Search for "Windcentrale" and install the integration.
4. Restart your instance.

### Manual Installation

1. Download the `windcentrale.zip` file from the
   [latest release](https://github.com/jobvk/Home-Assistant-Windcentrale/releases/latest).
2. Unpack the release and copy the files into the `custom_components/windcentrale` directory.
3. Restart your instance.

## Configuration

### Set Up

The Windcentrale component can be configured by config flow.

Go to Configuration and then Integrations, click on the `+ add integration`, select Windcentrale and configure the options on the form.
Fill in the amount of wind shares you own of the specific wind turbine(s). If you don't own wind shares of the other wind turbines, leave them on zero.

![image](https://user-images.githubusercontent.com/32730202/130699745-bb21526a-4cd2-4304-b62a-22329296149a.png)

### Options

Go to Configuration and then Integrations, search for the integration `Windcentrale` and click on configure. Here you can enable and disable sensors and adjust the interval of the sensors.

![image](https://user-images.githubusercontent.com/32730202/130699869-7ca11929-d521-442e-ba4b-8dc6c967d109.png)

## Sensors

### Live

These sensors show live data from the wind turbine.

|ID|Type|Description|Unit of Measurement
|------------|------------|------------|------------|
| `sensor.name` | Int | The total amount of power you currently generate with the number of wind shares. | Watt (W)
| `sensor.name_current_power` | Int | The ability in percentage the wind turbine can generate power. | Percentage (%)
| `sensor.name_hours_run_this_year` | Int | The number of hours that the windturbine has been running this year. | Hours (h)
| `sensor.name_kwh` | Int | The amount of engery production by the windturbine this year. | Kilowatt-hour (kWh)
| `sensor.name_last_updated` | DateTime | Returns when the windturbine last updated. | DateTime
| `sensor.name_power_production_per_share` | Int | The power per wind share that the windturbine currently generates. | Watt (W)
| `sensor.name_power_production_total` | Int | The total power that the windturbine currently generates. | Kilowatt (kW)
| `binary_sensor.name_pulsating` | Int | The windturbine is at max power. | Boolean
| `sensor.name_revolutions_per_minute` | Int | The speed at which the blades of the windturbine rotate. | Revolutions Per minute (RPM)
| `sensor.name_run_percentage` | Int | The percentage of the wind turbine is operational since the start date. | Percentage (%)
| `sensor.name_wind_direction` | String | The direction of the wind at the windturbine. | Wind rose
| `sensor.name_wind_speed` | Int | The speed of the wind at the windturbine. | Beaufort scale (BFT)

### History

These sensors show how much power the wind turbine has delivered over a certain time.

|ID|Type|Description|Decimals|Unit of Measurement
|----------|------------|------------|------------|------------|
| `sensor.name_day_production` | Int | The amount of power deliverd by the wind turbine this day. | 1 | Watt-hour (Wh)
| `sensor.name_week_production` | Int | The amount of power deliverd by the wind turbine last 7 days. | 1 | Kilowatt-hour (kWh)
| `sensor.name_month_production` | Int | The amount of power deliverd by the wind turbine this month. | 2 | Kilowatt-hour (kWh)
| `sensor.name_year_production` | Int | The amount of power deliverd by the wind turbine this year. | 3 | Megawatt-hour (MWh)
| `sensor.name_total_production` | Int | The amount of power deliverd by the wind turbine all time. | 3 | Megawatt-hour (MWh)

### News

This sensor shows the latest news.

The value of `sensor.the_windcentrale_news` doesn't change because the news string is longer than 255 characters. There for the state is static and will always report `News`.

The attributes have no limit on characters there for I made a solution.

Create a markdown card with the following content: 
```
type: markdown
content: '{{ state_attr(''sensor.the_windcentrale_news'', ''News Item'') }}'
```

An example of what it should look like:

![image](https://user-images.githubusercontent.com/32730202/126724281-7634e278-093d-4ab9-bd04-5e73448b7d61.png)

### Example

Below is an example of the sensors.

![image](https://user-images.githubusercontent.com/32730202/131559255-c2e7cd9f-6951-47be-9ae7-fd65dd8a5f85.png)

## Energy Management tab

To use of Energy Management tab you need to use the sensor `sensor.name_day_production` 

The sensor state_class is "total" and not "total_increasing" because of energy use of the windturbine. If the windturbine is not spinning the windturbine can use more power than it produces. Found this on their site:

![image](https://user-images.githubusercontent.com/32730202/140643066-aa6679d9-82de-4316-8627-3339c1475b67.png)

But there is also one problem. The API of the production history updates every couple of minutes. But 5 minutes after the hour/day has passed they change some data. I haven't found a solution for this yet. But this means there is a difference between the graph of Home Assistant energy management tab and the original app. This also means that when the day is over, the total will not align with the correct values. When I have found a solution I will certainly update it.

If you found a solution please contact me on [discord](https://discord.com/invite/T3tK4Jsquc) or make a pull request.

Home Assistant

![image](https://user-images.githubusercontent.com/32730202/140643312-0836568f-5acf-4369-a135-9a6b7a6629ac.png)

Windcentrale app

![image](https://user-images.githubusercontent.com/32730202/140643292-7ea72af5-0846-4c2a-8ffb-5ce837486b6e.png)

## ToDo

* Report right state after restart
* Change setup manually to setup with credentials login (Help wanted) [#10](https://github.com/jobvk/Home-Assistant-Windcentrale/issues/10)

## License
[Apache License 2.0](https://github.com/jobvk/Home-Assistant-Windcentrale/blob/main/LICENSE)

## Disclaimer
This integration is not developed, nor supported by the windcentrale company.

## Say thank you

There is put a lot of work into making this repo and component available.
If you want to make donation as appreciation of my work, you can buy me a coffee. Thank you!

[![Buy me a coffee][buymeacoffee-shield]][buymeacoffee]

[buymeacoffee-shield]: https://www.buymeacoffee.com/assets/img/guidelines/download-assets-sm-2.svg
[buymeacoffee]: https://www.buymeacoffee.com/jobvk