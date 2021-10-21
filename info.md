# Home Assistant sensor component for Windcentrale

[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg)](https://github.com/custom-components/hacs)
[![GitHub release (latest by date)](https://img.shields.io/github/v/release/jobvk/Home-Assistant-Windcentrale)](https://github.com/jobvk/Home-Assistant-Windcentrale/releases)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-Yes-brightgreen.svg)](https://github.com/jobvk/Home-Assistant-Sensor-Windcentrale/graphs/commit-activity)

[![Buy me a coffee](https://img.shields.io/static/v1.svg?label=Buy%20me%20a%20coffee&logo=buy%20me%20a%20coffee&logoColor=white&labelColor=blue&message=donate&color=Black)](https://www.buymeacoffee.com/jobvk)

Home Assistant component for the Windcentrale

The `Windcentrale` component is a Home Assistant component which lets you get sensor and news data from all wind turbines.

The official website https://www.windcentrale.nl

## Example

Below is an example of the sensors.

![image](https://user-images.githubusercontent.com/32730202/131559085-00470dae-f4d0-43b0-a082-395d63f29e76.png)

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

## License

[Apache License 2.0](https://github.com/jobvk/Home-Assistant-Windcentrale/blob/main/LICENSE)

## Say thank you

There is put a lot of work into making this repo and component available.
If you want to make donation as appreciation of my work, you can buy me a coffee. Thank you!

[![Buy me a coffee][buymeacoffee-shield]][buymeacoffee]

[buymeacoffee-shield]: https://www.buymeacoffee.com/assets/img/guidelines/download-assets-sm-2.svg
[buymeacoffee]: https://www.buymeacoffee.com/jobvk