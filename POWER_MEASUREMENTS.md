# Power measurements
The power measurements presented here were measure powering the PICO boards over USB using a FNB58 USB Tester bought on Amazon. It has a resolution of 0.01 milliamps.
Manuals for the device are available online in github here [fnb58-archive](https://github.com/Rhomboid/fnb58-archive).

When doing a test there is a considerable amount of noise due to how the PICO power converter works.
Current draw varies by about 0.3 milliamps.
The numbers I report are my eye-ball of the average.

Except where/if noted, all measurements were done running micropython 1.23.0.

I recently received a new Raspberry PI PICO and PICO W.
My earlier data for PICO W was a board with an I2C temperature monitor connected.
I retested with the new PICO and PICO W (with nothing connected).
Interestingly, now in some tests the PICO W appears to use a little less power than the PICO.

## Raspberry PI PICO W

For all measurements reported here the CYW43439 WIFI chip is powered down.
This is the case on power up.
Enabling WIFI or accessing hardware connected to the WIFI chip will power it up and significantly increase power consumption.
This includes the board LED.

The following table reports power usage in milli-amps.

|Test                  |CPU 125 Mhz(default) | CPU 64 Mhz   | CPU 18 Mhz   |
|----------------------|---------------------|--------------|--------------|
| busy wait            | 20.94               | 14.09        | 7.76         |
| normal sleep_ms      | 18.35               | 12.81        | 7.44         |
| always safe sleep_ms | 17.03               | 12.09        | 7.29         |
| timer+USB sleep_ms   |  8.69               |  7.47        | 5.85         |
| timer only sleep_ms  |  6.36               |  5.54        | 4.19         |
| lightsleep           |  1.29               |  1.29        | 1.29         |

Note: lightsleep always reduce the system clock to 12 Mhz. That is why results are the same for all clocks speeds.

## Raspberry PI PICO

The following table reports power usage in milli-amps.

|Test                  |CPU 125 Mhz(default) | CPU 64 Mhz   | CPU 18 Mhz   |
|----------------------|---------------------|--------------|--------------|
| busy wait            | 21.24               | 14.45        | 7.83         |
| normal sleep_ms      | 18.80               | 13.00        | 7.45         |
| always safe sleep_ms | 17.30               | 12.36        | 7.25         |
| timer+USB sleep_ms   |  8.70               |  7.43        | 5.72         |
| timer only sleep_ms  |  6.68               |  5.50        | 3.98         |
| lightsleep           |  1.29               |  1.29        | 1.29         |


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

freq(64*1000*1000)

lightsleep(15000)

freq(125*1000*1000)
```