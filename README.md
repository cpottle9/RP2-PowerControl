# Power Control for RP2 processors

## Important notes
**With micropython version  1.24.0 or 1.25 preview versions do not use machine.lightsleep() with this code.
Always use time.sleep_ms() or equivalent.
machine.lightsleep() will set registers SLEEP_EN0 and SLEEP_EN1 to the power on value when it returns.**

**This repository contains support for power control on RP2040 and RP2350.
I recently acquired an PICO2 and did some testing.
I do not see any power reduction while sleeping after calling API's disable_while_sleeping() and disable_while_sleeping_all_but().
There is an issue with the pico-sdk on RP2350, time.sleep_ms() and equivalents are effectively busy wait loops.
The problem details are captured in issue https://github.com/raspberrypi/pico-sdk/issues/1812.
The pico-sdk issue is actively being worked and should be fixed in the 1.25.0 preview builds on a week or two.**

## Why not use machine.lightsleep

Yes, rather than using this code you could just use machine.lightsleep.
While machine.lightsleep is running the RP2040 power consumption is very low.

lightsleep has issues on RP2040 and RP2350.
The exact issues you see will depend on which version of micropython you are using.

Fundamentally, lightsleep turns of almost all peripheral blocks and if you need one of those blocks active while sleeping you can't use it.
In micropython version 1.23.0 the USB block would be unusable after a lightsleep.
That was resolved in 1.24.0.

You can not use lightsleep for instance if you want to wakeup due to an interrupt generated from a button press.

## What this code does
This micropython code can be used to modify the RP2040 or RP2350 Power Control registers.
This can reduce power consumed both:
* while the chip is awake (at least one core is running or DMA is active),
* while the chip is sleeping.

Reducing power consumption is of value only if your application is running from battery.
If your board is powered from household AC power these capabilities have no value.

Most micropython applications running on RP2040 or RP2350 only use one core.
The core stops running(sleep) executing time.sleep() or time.sleep_ms().
Many device libraries you might use these functions.
Micropython internal code also does the equivalent in C.
Many applications on micropython spend considerable time sleeping.

For details on these register look at the respective data sheets 
[2040 Data Sheet](https://datasheets.raspberrypi.com/rp2040/rp2040-datasheet.pdf) section 2.11 or
[2350 Data Sheet](https://datasheets.raspberrypi.com/rp2350/rp2350-datasheet.pdf) section 6.5.
Look specifically at the SLEEP_EN0, SLEEP_EN1, WAKE_EN0, and WAKE_EN1 registers.

Power reduction is acheived by disabling clocks to specific hardware blocks.

If there are hardware blocks you do not need at all you can disable them completely.
For example if your application does not use SPI you can completely the SPI blocks.

There are several hardware blocks which can always safely be disabled while sleeping.
They are only needed while awake:
* SRAM - SRAM contents are preserved while disabled. There a total of 6 SRAM blocks on RP2040 and 10 SRAM blocks on the RP2350.
* XIP  - eXecute In Place cache also preserved while disabled.

Depending on your application some hardware blocks need to be enabled both while awake and asleep.
For instance, in order to debug using REPL or thonny USB blocks must be enabled at all times.

**If you disable a block that your application needs the RP2 processor may stop responding.
If that happens while coding using REPL or thonny you will need a hard reset by unplugging the USB cable and plugging it back in.**
## Files

* README.md - this file.
* power_ctrl_abstract.py - common code used for both rp2040 and rp2350
* power_ctrl_2040.py - RP2040 specific code
* power_ctrl_2350.py - RP2350 specific code
* always_safe_RP2040_example.py - contans a trivial example disabling a few blocks for the RP2040.
* always_safe_RP2350_example.py - contans a trivial example disabling a few blocks for the RP2350.
* pico_w_example.py - An example for the PICO_W. Only uses a single core, the system LED, and hardware timer.
Everything not needed is disabled.
A few other blocks are turned on when awake because the system LED is connected to the CYW43 wifi chip.
If this example was run on a PICO more blocks could be disabled when awake.
* OTHER_POWER_REDUCTION_STRATEGIES.md - Other ways to reduce power to consider before using This code.
* POWER_MEASUREMENTS.md - Contains power measurements I made using a USB power tester. Compares power reduction using my code in different ways and using lightsleep.

## How to use

Using thonny or another method you need to copy power_ctrl_abstract.py and either power_ctrl_2040.py or power_ctrl_2350.py to your board.

In your app import the appropriate file for your RP2 type and create an instance of PowerCtrl.
For an RP2040 you would do:
```
from power_ctrl_2040 import PowerCtrl
pwr = PowerCtrl()
```
Then there are two functions you can use to disable hardware blocks while sleeping.
* pwr.disable_while_sleeping() - arguments to this function are hardware blocks you want disabled when sleeping.
Hardware blocks you do not list are unchanged.
You can call this function more than once.
Note: If the argument is empty list no changes are made.

```
pwr.disable_while_sleeping(
    pwr.EN0_CLK_SYS_SRAM3,
    pwr.EN0_CLK_SYS_SRAM2,
    pwr.EN0_CLK_SYS_SRAM1,
    pwr.EN0_CLK_SYS_SRAM0,
    pwr.EN1_CLK_SYS_XIP,
    pwr.EN1_CLK_SYS_SRAM5,
    pwr.EN1_CLK_SYS_SRAM4
)
```
* pwr.disable_while_sleeping_all_but() - arguments to this function are hardware blocks you want enabled when sleeping.
All blocks you did not list will be disabled.
Note: If the argument is empty list all blocks will be disabled.

```
# While sleeping I only need TIMER and USB
pwr.disable_while_sleeping_all_but(
    pwr.EN1_CLK_SYS_TIMER,
    pwr.EN1_CLK_USB_USBCTRL,
    pwr.EN1_CLK_SYS_USBCTRL,
    pwr.EN0_CLK_SYS_PLL_USB
)
```
* pwr.enable_while_sleeping() - arguments to this function are hardware blocks you want enabled when sleeping.
Hardware blocks you do not list are unchanged.
You can call this function more than once.
Note: If the argument is empty list no changes are made.
This function is not that useful. Included for testing.
```
pwr.enable_while_sleeping(
    pwr.EN0_CLK_SYS_SPI1,
    pwr.EN0_CLK_PERI_SPI
)

```

There are two similar functions to disable hardware blocks while sleeping:
* pwr.disable_while_awake() - arguments to this function are hardware blocks you want disabled when sleeping.
Hardware blocks you do not list are unchanged.
Note: If the argument is empty list no changes are made.

```
# Not using SPI power them down.
pwr.disable_while_awake(
    pwr.EN0_CLK_SYS_SPI1,
    pwr.EN0_CLK_PERI_SPI1,
    pwr.EN0_CLK_SYS_SPI0,
    pwr.EN0_CLK_PERI_SPI0
)
```
* pwr.disable_while_awake_all_but() - arguments to this function are hardware blocks you want enabled when awake.
All blocks you did not list will be disabled.
Note: If the argument is empty list all blocks will be disabled.
```
# When awake everything powered down but I2C.
# YOU DON'T WANT TO DO THIS.
pwr.disable_while_awake_all_but(
    pwr.EN0_CLK_SYS_I2C1,
    pwr.EN0_CLK_SYS_I2C0
)
```
* pwr.enable_while_awake() - arguments to this function are hardware blocks you want enabled when awake.
Hardware blocks you do not list are unchanged.
You can call this function more than once.
Note: If the argument is empty list no changes are made.
This function is useful when there is a hardware block you only need occasionally.
```
pwr.enable_while_awake(
    pwr.EN0_CLK_SYS_SPI1,
    pwr.EN0_CLK_PERI_SPI
)

```

The values specified in argument list are constants defined in the PowerCtrl object.
You can read the source code or do ```help(PowerCtrl)```.
The names are a match for the bit positions in the RP2 register documented in the data sheet.s

Lastly, you can print the pwr object.

```
>>>print(pwr)

PowerCtrl for RP2040
wake_en0:  F0FDE539 wake_en1:  00006C2F
sleep_en0: 00008000 sleep_en1: 00000C20
```

It displays the current contents of the four registers in hexadecimal.

## Examples

* always_safe_RP2040_example.py - a tiny example that disables XIP and SRAM on RP2040. It is always safe to power these down when sleeping.  
* always_safe_RP2350_example.py - a tiny example that disables XIP and SRAM on RP2350.  It is always safe to power these down when sleeping.  
* pico_w_example.py - simple code running on PICO W. Toggles the system LED using a Timer. On a regular PICO more hardware could be disabled while awake.
