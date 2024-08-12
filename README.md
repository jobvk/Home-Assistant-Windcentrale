# Home Assistant sensor component for Windcentrale

[![hacs_badge](https://img.shields.io/badge/HACS-Default-blue.svg)](https://github.com/hacs/integration)
[![GitHub release (latest by date)](https://img.shields.io/github/v/release/jobvk/Home-Assistant-Windcentrale?label=Release)](https://github.com/jobvk/Home-Assistant-Windcentrale/releases)
![Downloads](https://img.shields.io/github/downloads/jobvk/Home-Assistant-Windcentrale/total?color=blue&label=Downloads)

[![Maintainer](https://img.shields.io/badge/Maintainer-jobvk-brightgreen.svg)](https://github.com/jobvk/)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-Yes-brightgreen.svg)](https://github.com/jobvk/Home-Assistant-Windcentrale/graphs/commit-activity)

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
  * [History](#history)
  * [News](#news)
* [Button](#button)
* [Example](#example)
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

### History

These sensors show how much power the wind turbine has delivered over a certain time.
These sensors are not displaying live data. These sensors are updated around noon the following day.

|ID|Type|Description|Unit of Measurement|
|----------|------------|------------|------------|
| `sensor.name_production_year_total` | Int | The energy produced by the wind turbine total this year. | Kilowatt-hour (kWh) |
| `sensor.name_production_month_total` | Int | The energy produced by the wind turbine total this month. | Kilowatt-hour (kWh) |
| `sensor.name_production_week_total` | Int | The energy produced by the wind turbine total this week. | Kilowatt-hour (kWh) |
| `sensor.name_production_day_total` | Int | The energy produced by the wind turbine total 1 or 2 days ago. | Kilowatt-hour (kWh) |
| `sensor.name_production_year_shares` | Int | The energy produced by your shares of the wind turbine this year. | Kilowatt-hour (kWh) |
| `sensor.name_production_month_shares` | Int | The energy produced by your shares of the wind turbine this month. | Kilowatt-hour (kWh) |
| `sensor.name_production_week_shares` | Int | The energy produced by your shares of the wind turbine this week. | Kilowatt-hour (kWh) |
| `sensor.name_production_day_shares` | Int | The energy produced by your shares of the wind turbine 1 or 2 days ago. | Kilowatt-hour (kWh) |

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

## Button

This button `button.the_windcentrale_update_wind_shares` updates your shares. The reason this a button and doesn't update automatically is because your shares doesn't change that often.

### Example

Below is an example of the sensors.

![image](https://github.com/jobvk/Home-Assistant-Windcentrale/assets/32730202/cb7c24e9-d27f-4c06-9c29-9d36a3393b6d)

## Contributors
Special Thanks to all contributors
* [@vdheidenet](https://github.com/vdheidenet): for sharing his data on multiple windshares in different windturbines [#10](https://github.com/jobvk/Home-Assistant-Windcentrale/issues/10)

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