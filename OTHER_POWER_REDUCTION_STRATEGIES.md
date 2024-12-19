# Things to consider to reduce power use on Raspberry PI PICO projects

Before you make use of the code in this repository you should consider the following:

* If you need extremely low power consider a hardware solution.
There are several board vendor that provide a capability to completely power down the PICO.
For example, I use the [PIMORONI Badger W](https://shop.pimoroni.com/products/badger-2040-w?variant=40514062188627).
My application makes use of the e-ink display if you don't need it look for other hardware solutions online.
It has a small timer chip on board that can be programmed to power down the entire PICO board and wake it up at a specified time.
* If you have a PICO W or other board with WIFI you can save significant power by turning off the WIFI chip when you don't need it.
For the PICO W I use:
```
    from network import WLAN, STA_IF
    from rp2 import country
    rp2.country("CA") # I'm in Canada
    wlan = WLAN(STA_IF)
    wlan.disconnect()
    wlan.active(False)
    wlan.deinit()
    wlan = None
```
Note: On PICO W the system LED is connected to the WIFI chip.
Accessing the LED will power up the WIFI chip.
Other GPIO pins connect through the WIFI chip their names begin with "WL_" accessing them will power up the WIFI chip.
* When you have to use WIFI you can reduce power using wlan.config().
I use ```wlan.config(pm = 0xa11c81)``` but your mileage may vary.
You could also use ```wlan.config(pm=wlan.PM_POWERSAVE)``` from the micropython manual.
There are resources online.
* If you have external devices that consume power consider shutting them down before a long sleep.
For example, my Badger W project uses an [mcp9808](https://www.adafruit.com/product/1782) I2C temperature sensor I bought from Adafruit.
It has a low power mode which consumes only 2 microamps compared to 400 microamps in operating mode.
I only need to read the sensor once per minute so I keep it in low power mode most of the time.
* Don't use the second core unless you _really_ need to. The second core will consume more power.