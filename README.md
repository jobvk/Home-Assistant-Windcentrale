# Home Assistant sensor component for Windcentrale

[![hacs_badge](https://img.shields.io/badge/HACS-Default-blue.svg)](https://github.com/hacs/integration)
[![GitHub release (latest by date)](https://img.shields.io/github/v/release/jobvk/Home-Assistant-Windcentrale?label=Release)](https://github.com/jobvk/Home-Assistant-Windcentrale/releases)
![Downloads](https://img.shields.io/github/downloads/jobvk/Home-Assistant-Windcentrale/total?color=blue&label=Downloads)

[![Maintainer](https://img.shields.io/badge/Maintainer-jobvk-brightgreen.svg)](https://github.com/jobvk/)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-Yes-brightgreen.svg)](https://github.com/jobvk/Home-Assistant-Windcentrale/graphs/commit-activity)
[![Discord](https://img.shields.io/discord/1031889093296140309?color=brightgreen&label=Discord&logo=Discord&logoColor=white)](https://discord.gg/yHTjhJVdJa)

[![Github-sponsors](https://img.shields.io/badge/sponsor-30363D?style=flat&logo=GitHub-Sponsors&logoColor=#EA4AAA)](https://github.com/sponsors/jobvk?frequency=one-time)
[![](https://img.shields.io/badge/PayPal-00457C?style=flat&logo=paypal&logoColor=white)](https://paypal.me/jobvankoeveringe)
[![Buy me a coffee](https://img.shields.io/badge/-buy_me_a%C2%A0coffee-gray?logo=buy-me-a-coffee&color=orange)](https://www.buymeacoffee.com/jobvk)

Home Assistant component for the Windcentrale & Winddelen

The `Windcentrale` component is a Home Assistant component which lets you get sensor and news data from all wind turbines.

The official websites are https://www.windcentrale.nl and https://winddelen.nl

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
* [Contributors](#contributors)
* [Stargazers](#stargazers)
* [License](#license)
* [Disclaimer](#disclaimer)
* [Say thank you](#say-thank-you)

## Installation

### Installation through HACS

1. Ensure that [HACS](https://hacs.xyz/) is installed.
2. Click on the `+ Explore & download repositories`
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

Go to Settings and then Devices & Services, select Integrations and click on the `+ add integration`, select Windcentrale and configure the setup on the form.
Fill in your email address and password that you use for signing in to the website, and press submit.

![image](https://github.com/jobvk/Home-Assistant-Windcentrale/assets/32730202/30b7a02e-b5c5-45bf-8a16-ec325a441ed5)

### Options

Go to Settings and then Devices & Service, select Integrations and search for the integration `Windcentrale` and click on configure. Here you change if you want to show the wind trubine(s) on the map.

![image](https://user-images.githubusercontent.com/32730202/194356933-d5cae789-c919-4b07-a4d6-a9db4471ac17.png)

## Sensors

### Live

These sensors show live data from the wind turbine.

|ID|Type|Description|Unit of Measurement
|------------|------------|------------|------------|
| `sensor.name` | Int | The total amount of power you currently generate with the number of wind shares. | Watt (W)
| `sensor.name_energy` | Int | The energy that the wind turbine has produced this year. | Kilowatt-hour (kWh)
| `sensor.name_energy_prognoses_this_year` | Float | The percentage of how much the wind turbine should produce in a year. | Percentage (%)
| `sensor.name_energy_shares` | Float | The energy that your shares of the wind turbine has produced this year. | Kilowatt-hour (kWh)
| `sensor.name_hours_run_this_year` | Int | The number of hours the wind turbine has operated this year. | Hours (h)
| `sensor.name_hours_run_total` | Int | The number of hours the wind turbine has operated in total. | Hours (h)
| `sensor.name_last_update` | DateTime | Returns when the wind turbine last updated. | DateTime
| `sensor.name_power_per_share` | Int | The power per wind share that the wind turbine currently generates. | Watt (W)
| `sensor.name_power_percentage` | Int | The ability in percentage the wind turbine can generate power. | Percentage (%)
| `sensor.name_power_total` | Int | The total power that the wind turbine currently generates. | Kilowatt (kW)
| `binary_sensor.name_pulsating` | Bool | The wind turbine is at max power. | Boolean
| `sensor.name_revolutions_per_minute` | Float | The speed at which the blades of the wind turbine rotate. | Revolutions Per minute (RPM)
| `sensor.name_run_percentage` | Float | The percentage of the wind turbine is operational since the start date. | Percentage (%)
| `sensor.name_wind_direction` | String | The direction of the wind at the wind turbine. | Wind rose
| `sensor.name_wind_speed` | Int | The speed of the wind at the wind turbine. | Beaufort scale (BFT)

### History

These sensors show how much power the wind turbine has delivered over a certain time.
These sensors are not displaying live data. These senors are updated around noon the following day.

|ID|Type|Description|Unit of Measurement
|----------|------------|------------|------------|
| `sensor.name_production_year_total` | Int | The energy produced by the wind turbine total this year. | Kilowatt-hour (kWh)
| `sensor.name_production_month_total` | Int | The energy produced by the wind turbine total this month. | Kilowatt-hour (kWh)
| `sensor.name_production_week_total` | Int | The energy produced by the wind turbine total this week. | Kilowatt-hour (kWh)
| `sensor.name_production_year_shares` | Int | The energy produced by your shares of the wind turbine this year. | Kilowatt-hour (kWh)
| `sensor.name_production_month_shares` | Int | The energy produced by your shares of the wind turbine this month. | Kilowatt-hour (kWh)
| `sensor.name_production_week_shares` | Int | The energy produced by your shares of the wind turbine this week. | Kilowatt-hour (kWh)

### News

This sensor shows the latest news.

The value of `sensor.the_windcentrale_news` doesn't change because the news string is longer than 255 characters. There for the state is static and will always report `News`.

The attributes have no limit on characters there for I made a solution.

Create a markdown card with the following content: 
``` yaml
type: markdown
content: '{{ state_attr(''sensor.the_windcentrale_news'', ''News Item'') }}'
```

An example of what it should look like:

![image](https://user-images.githubusercontent.com/32730202/126724281-7634e278-093d-4ab9-bd04-5e73448b7d61.png)

### Example

Below is an example of the sensors.

![image](https://user-images.githubusercontent.com/32730202/195425402-9ecdb159-898e-4a13-a0a8-c406d5b3ccf8.png)

## Energy Management tab

To use of Energy Management tab you need to use the sensor `sensor.name_energy_shares` 

The sensor state_class is "total" and not "total_increasing" because of energy use of the wind turbine. If the wind turbine is not spinning the wind turbine can use more power than it produces. Found this on their site:

![image](https://user-images.githubusercontent.com/32730202/194364186-bf6ce362-11df-4471-9f1e-014b80835a3b.png)

But there is also a problem. The API uses live data for the power management tab. But for the graph on the official site has a small correction. But this means there is a difference between the graph of energy management tab and the official site. This also means that when the day is past, the total does not match the correct values. When I have found a solution I will certainly update it.

If you found a solution please contact me on [discord](https://discord.com/users/311908841459810316/) or start a [Discussion](https://github.com/jobvk/Home-Assistant-Windcentrale/discussions).

## Contributors
Special Thanks to all contributors
* [@vdheidenet](https://github.com/vdheidenet): Sharing his data for creating the signing in function
* [@rob-on-git](https://github.com/rob-on-git): For creating a formula for the run percentage sensor

## Stargazers
Thanks to everyone having starred my repo!

[![Stargazers repo roster for @jobvk/Home-Assistant-Windcentrale](https://git-lister.onrender.com/api/stars/jobvk/Home-Assistant-Windcentrale?limit=30)](https://github.com/jobvk/Home-Assistant-Windcentrale/stargazers)

## License
[Apache License 2.0](https://github.com/jobvk/Home-Assistant-Windcentrale/blob/main/LICENSE)

## Disclaimer
This integration is not developed, nor supported by the windcentrale company.

## Say thank you

There is put a lot of work into making this repo and component available.
If you want to make donation as appreciation of my work, you can buy me a coffee. Thank you!

[![Github-sponsors](https://img.shields.io/badge/sponsor-30363D?style=flat&logo=GitHub-Sponsors&logoColor=#EA4AAA)](https://github.com/sponsors/jobvk?frequency=one-time)
[![](https://img.shields.io/badge/PayPal-00457C?style=flat&logo=paypal&logoColor=white)](https://paypal.me/jobvankoeveringe)
[![Buy me a coffee](https://img.shields.io/badge/-buy_me_a%C2%A0coffee-gray?logo=buy-me-a-coffee&color=orange)](https://www.buymeacoffee.com/jobvk)
