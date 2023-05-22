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

## Example

Below is an example of the sensors.

![image](https://user-images.githubusercontent.com/32730202/195425402-9ecdb159-898e-4a13-a0a8-c406d5b3ccf8.png)

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

## License

[Apache License 2.0](https://github.com/jobvk/Home-Assistant-Windcentrale/blob/main/LICENSE)

## Say thank you

There is put a lot of work into making this repo and component available.
If you want to make donation as appreciation of my work, you can buy me a coffee. Thank you!

[![Buy me a coffee][buymeacoffee-shield]][buymeacoffee]

[buymeacoffee-shield]: https://www.buymeacoffee.com/assets/img/guidelines/download-assets-sm-2.svg
[buymeacoffee]: https://www.buymeacoffee.com/jobvk
