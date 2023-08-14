# EF_PWM32
A dual channel 32-bit PWM generator with a clock divider.
## Description
The PWM module is capable of producing two PWM signals on pwmA and pwmB ports. The PWM signals are generated out of a 32-bit counter which is compared to the values cmpA and cmpB. The counter has two modes of operation:
- Mode 1 (Up/Down counting): from 0 to load then back to 0
<img src="docs/_static/up-down.png" alt= “”>
- Mode 0 (Up counting): from 0 to load 
<img src="docs/_static/up.png" alt= “”>

There 6 events (e0 to e5) while in mode 1. Four of these 6 events are available in mode 0. Each of the PWM ports can be configured to perform different actions at each one of the events. The actions are:
- Change to high
- Change to low
- Toggle

## Clocking
There is a clock divider that can divide the system clock by 2, 4, 8 or 16. the output of this clock divider is used to clock the counter.


## Ports
<img src="docs//_static/ef_pwm32.svg" alt= “” width="70%" height="70%">

| Port name  | Direction | Size   | Description |
| ---------- | --------- | ------ | ----------- |
| clk        | input     | 1       | Clock            |
| rst_n      | input     | 1       | Active low reset            |
| pwmA| output| 1|PWM Channel A out pins|
| pwmB| output| 1|PWM Channel B out pins|
| cmpA| input| 32|Channel A Compare |
| cmpB| input| 32|Channel B Compare |
| load| input| 32|Counter load value|
| clkdiv  |  input| 4  | Clock Divider:<br> - 0001 /2<br> - 0010 /4<br> - 0100 /8<br> - 1000 /16  |
| cntr_mode|input|1|  1 - up/down <br> 0 - Down|
|enA|input|1| Channel A enable|
|enB|input|1| Channel B enable|
|en|input|1| PWM enable|
|invA|input|1| Invert channel A|
|invB|input|1| Invert channel B|
|pwmA_e0a|input|2| Action<sup>*</sup> for channel counter A reaching 0|
|pwmA_e1a|input|2| Action<sup>*</sup> for channel counter A matching cmpA going up|
|pwmA_e2a|input|2| Action<sup>*</sup> for channel counter A matching cmpB going up|
|pwmA_e3a|input|2| Action<sup>*</sup> for channel counter A matching load|
|pwmA_e4a|input|2| Action<sup>*</sup> for channel counter A matching cmpB going down|
|pwmA_e5a|input|2| Action<sup>*</sup> for channel counter A matching cmpA going down|
|pwmB_e0a|input|2| Action<sup>*</sup> for channel counter B reaching 0|
|pwmB_e1a|input|2| Action<sup>*</sup> for channel counter B matching cmpA going up|
|pwmB_e2a|input|2| Action<sup>*</sup> for channel counter B matching cmpB going up|
|pwmB_e3a|input|2| Action<sup>*</sup> for channel counter B matching load|
|pwmB_e4a|input|2| Action<sup>*</sup> for channel counter B matching cmpB going down|
|pwmB_e5a|input|2| Action<sup>*</sup> for channel counter B matching cmpA going down|

<sup>*</sup>00:none, 01:high, 10:low, 11:invert

## Bus Wrappers
AHB-Lite, APB and WB bus wrappers are provided.

### I/O Registers
| Register  | Size | Mode   | Offset | Reset Value |Description |
| ---------- | --------- | ------ | -- | ----| ----- |
| CMPA | 32 | RW | 0x00 | 0x00000000 | Compare A Register |
| CMPB | 32 | RW | 0x04 | 0x00000000 | Compare B Register |
| TOP | 32 | RW | 0x08 | 0x00000000 | Top Register |
| CLKDIV | 4 | RW | 0x0C | 0x00000000 | Clock Divider:<br> - 0001 /2<br> - 0010 /4<br> - 0100 /8<br> - 1000 /16 |
| CONTROL | 6 | RW | 0x10 | 0x00000000 | TControl Register: <br> - 0 : PWM Enable<br> - 1 : Channel A Enable<br> - 2 : Channel B enable<br> - 3 : Channel A Inversion<br> - 4 : Channel B Inversion<br> - 5: PWM counter mode (1:up/down, 0:Down)|
| GENA | 12 | RW | 0x14 | 0x00000000 | Gen A Register |
| GENB | 12 | RW | 0x18 | 0x00000000 | Gen B Register |

