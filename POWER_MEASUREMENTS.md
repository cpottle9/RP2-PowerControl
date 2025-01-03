# Power measurements
The power measurements presented here were measure powering the PICO boards over USB using a FNB58 USB Tester bought on Amazon. It has a resolution of 0.01 milliamps.
Manuals for the device are available online in github here [fnb58-archive](https://github.com/Rhomboid/fnb58-archive).

When doing a test there is a considerable amount of noise due to how the PICO power converter works.
Current draw varies by about 0.3 milliamps.
The numbers I report are my eye-ball of the average.

Except where/if noted, all measurements were done running micropython 1.23.0.

Currently I only have Raspberry PI PICO W. I ordered a regular PICO and PICO 1.
Once they arrive I will include data for them.

## Raspberry PI PICO W

For all measurements reported here the CYW43439 WIFI chip is powered down.
This is the case on power up.
Enabling WIFI or accessing hardware connected to the WIFI chip will power it up and significantly increase power consumption.
This includes the board LED.

The following table reports power usage in milli-amps.

|Test                  |CPU 125 Mhz(default) | CPU 64 Mhz   | CPU 18 Mhz   |
|----------------------|---------------------|--------------|--------------|
| busy wait            | 22.02               | 14.62        | 8.16         |
| normal sleep_ms      | 18.64               | 13.01        | 7.61         |
| always safe sleep_ms | 17.23               | 12.49        | 7.36         |
| timer+USB sleep_ms   |  9.13               |  7.83        | 5.86         |
| timer only sleep_ms  |  6.55               |  5.87        | 4.10         |
| lightsleep           |  1.51               |  1.51        | 1.51         |

Note: lightsleep always reduce the system clock to 12 Mhz. That is why results are the same for all clocks speeds.

**Busy wait code**
```
# Busy wait 15 seconds
from time import ticks_ms, ticks_diff
from machine import freq

start = ticks_ms()
end = start

freq(64*1000*1000)

while ticks_diff(end, start) < 15000 :
    end = ticks_ms()

freq(125*1000*1000)
```
**sleep_ms code**
```
#  sleep_ms 15 seconds
from time import sleep_ms
from machine import freq

start = ticks_ms()
end = start

freq(64*1000*1000)

sleep_ms(15000)

freq(125*1000*1000)
```
**Use PowerCtrl to turn off SRAM and XIP while sleeping**
```
# Safe Power Ctrl sleep 15 seconds
from power_ctrl_2040 import PowerCtrl
from machine import freq
from time import sleep_ms
pwr = PowerCtrl()

# It is always safe to turn off XIP and SRAM when sleeping.
pwr.disable_while_sleeping(
    pwr.EN0_CLK_SYS_SRAM3,
    pwr.EN0_CLK_SYS_SRAM2,
    pwr.EN0_CLK_SYS_SRAM1,
    pwr.EN0_CLK_SYS_SRAM0,
    pwr.EN1_CLK_SYS_XIP,
    pwr.EN1_CLK_SYS_SRAM5,
    pwr.EN1_CLK_SYS_SRAM4
)

freq(64*1000*1000)

sleep_ms(15000)

freq(125*1000*1000)

pwr.restore()
```
**Use PowerCtrl to turn off everything but the timer and USB while sleeping**
```
from machine import freq
from time import sleep_ms
from power_ctrl_2040 import PowerCtrl

pwr = PowerCtrl()

pwr.disable_while_sleeping_all_but(
    pwr.EN1_CLK_SYS_TIMER,
    pwr.EN1_CLK_USB_USBCTRL,
    pwr.EN1_CLK_SYS_USBCTRL,
    pwr.EN0_CLK_SYS_PLL_USB
)

freq(64*1000*1000)

sleep_ms(15000)

freq(125*1000*1000)

pwr.restore()
```
**Use PowerCtrl to turn off everything but the timer while sleeping**
This roughly equivalent to what lightsleep does in micropython version 1.23.0.
Except, lightsleep also turns off the two clock PLLs which save about 3 milli-amps.
```
from machine import freq
from time import sleep_ms
from power_ctrl_2040 import PowerCtrl

pwr = PowerCtrl()

pwr.disable_while_sleeping_all_but(
    pwr.EN1_CLK_SYS_TIMER
)

freq(64*1000*1000)

sleep_ms(15000)

freq(125*1000*1000)

pwr.restore()
```

**Use lightsleep**
Note, running micropython 1.23.0 USB will not recover after lightsleep completes.
You will need to power cycle the PICO to recover.
```
from machine import freq, lightsleep
from power_ctrl_2040 import PowerCtrl

pwr = PowerCtrl()

pwr.disable_while_sleeping_all_but(
    pwr.EN1_CLK_SYS_TIMER
)

freq(64*1000*1000)

lightsleep(15000)

freq(125*1000*1000)

pwr.restore()
```