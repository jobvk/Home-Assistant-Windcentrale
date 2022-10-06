# Home Assistant sensor component for Windcentrale

[![hacs_badge](https://img.shields.io/badge/HACS-Default-blue.svg)](https://github.com/hacs/integration)
[![GitHub release (latest by date)](https://img.shields.io/github/v/release/jobvk/Home-Assistant-Windcentrale)](https://github.com/jobvk/Home-Assistant-Windcentrale/releases)
[![GitHub](https://img.shields.io/badge/license-Apache-blue)](LICENSE)

[![Maintenance](https://img.shields.io/badge/Maintained%3F-Yes-brightgreen.svg)](https://github.com/jobvk/Home-Assistant-Windcentrale/graphs/commit-activity)
[![Maintainer](https://img.shields.io/badge/Maintainer-jobvk-brightgreen.svg)](https://github.com/jobvk/)
[![](https://dcbadge.vercel.app/api/shield/311908841459810316?style=flat&theme=default-inverted)](https://discordapp.com/users/311908841459810316/)

[![Buy me a coffee](https://img.shields.io/static/v1.svg?label=Buy%20me%20a%20coffee&logo=buy%20me%20a%20coffee&logoColor=white&labelColor=orange&message=donate&color=Black)](https://www.buymeacoffee.com/jobvk)

Home Assistant component for the Windcentrale

The `Windcentrale` component is a Home Assistant component which lets you get sensor and news data from all wind turbines.

The official website https://www.windcentrale.nl

## Example

Below is an example of the sensors.

<img src="https://user-images.githubusercontent.com/32730202/194361335-60f094cd-480e-4d7e-9c12-c9c9d538037e.png" width="668" height="541">

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

Are not available at this time

<!--
These sensors show how much power the wind turbine has delivered over a certain time.

|ID|Type|Description|Decimals|Unit of Measurement
|----------|------------|------------|------------|------------|
| `sensor.name_day_production` | Int | The amount of power deliverd by the wind turbine this day. | 1 | Watt-hour (Wh)
| `sensor.name_week_production` | Int | The amount of power deliverd by the wind turbine last 7 days. | 1 | Kilowatt-hour (kWh)
| `sensor.name_month_production` | Int | The amount of power deliverd by the wind turbine this month. | 2 | Kilowatt-hour (kWh)
| `sensor.name_year_production` | Int | The amount of power deliverd by the wind turbine this year. | 3 | Megawatt-hour (MWh)
| `sensor.name_total_production` | Int | The amount of power deliverd by the wind turbine all time. | 3 | Megawatt-hour (MWh)
 -->

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
