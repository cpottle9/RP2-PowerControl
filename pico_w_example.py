from machine import Timer, Pin, lightsleep
from time import sleep_ms, ticks_ms, ticks_diff

from power_ctrl_2040 import PowerCtrl

pwr = PowerCtrl()

pwr.disable_while_sleeping_all_but(
    # TIMER is required so time.sleep_ms and Timer  work
    pwr.EN1_CLK_SYS_TIMER,
    #USB enabled so I can debug from REPL or thonny
    pwr.EN1_CLK_USB_USBCTRL,
    pwr.EN1_CLK_SYS_USBCTRL,
    pwr.EN0_CLK_SYS_PLL_USB
    # everything else is disabled while sleeping.
)

pwr.disable_while_awake(
    # These are blocks I know I don't need for this trivial application
    # Quick note: DMA is used to talk to the WIFI chip.
    # On PICO W the system LED is connected to the WIFI chip.
    pwr.EN0_CLK_SYS_SPI1,
    pwr.EN0_CLK_PERI_SPI1,
    pwr.EN0_CLK_SYS_SPI0,
    pwr.EN0_CLK_PERI_SPI0,
    pwr.EN0_CLK_SYS_I2C1,
    pwr.EN0_CLK_SYS_I2C0,
    pwr.EN0_CLK_SYS_PWM,
    pwr.EN0_CLK_SYS_PIO0,
    pwr.EN0_CLK_SYS_PADS,
    pwr.EN0_CLK_SYS_JTAG,
    pwr.EN0_CLK_SYS_ADC,
    pwr.EN0_CLK_ADC_ADC,
    pwr.EN1_CLK_SYS_UART1,
    pwr.EN1_CLK_PERI_UART1,
    pwr.EN1_CLK_SYS_UART0,
    pwr.EN1_CLK_PERI_UART0,
    pwr.EN1_CLK_SYS_WATCHDOG,
    pwr.EN1_CLK_SYS_TBMAN
)

print(pwr)

led = Pin("LED", Pin.OUT)
led.value(False)

count=0

def led_toggle(arg) :
    global count, t
    count = count + 1
    if count > 5 :
        t.deinit()
    led.toggle()
    
t=Timer(mode=Timer.PERIODIC, callback=led_toggle, freq=1)

tick_before = ticks_ms()
sleep_ms(10000)
tick_after = ticks_ms()

t.deinit()
sleep_ms(1000)
led.value(False)

print('slept: ', ticks_diff(tick_after, tick_before), ' ms')
print('count: ', count)

pwr.restore()

