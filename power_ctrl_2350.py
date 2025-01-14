from micropython import const
from power_ctrl_abstract import PowerCtrlAbstract

class PowerCtrl(PowerCtrlAbstract) :
    # Define register addresses

    # EN0 masks
    EN0_CLK_SYS_SIO                 = const(31)
    EN0_CLK_SYS_SHA256              = const(30)
    EN0_CLK_SYS_PSM                 = const(29)
    EN0_CLK_SYS_ROSC                = const(28)
    EN0_CLK_SYS_ROM                 = const(27)
    EN0_CLK_SYS_RESETS              = const(26)
    EN0_CLK_SYS_PWM                 = const(25)
    EN0_CLK_SYS_POWMAN              = const(24)
    EN0_CLK_REF_POWMAN              = const(23)
    EN0_CLK_SYS_PLL_USB             = const(22)
    EN0_CLK_SYS_PLL_SYS             = const(21)
    EN0_CLK_SYS_PIO2                = const(20)
    EN0_CLK_SYS_PIO1                = const(19)
    EN0_CLK_SYS_PIO0                = const(18)
    EN0_CLK_SYS_PADS                = const(17)
    EN0_CLK_SYS_OTP                 = const(16)
    EN0_CLK_REF_OTP                 = const(15)
    EN0_CLK_SYS_JTAG                = const(14)
    EN0_CLK_SYS_IO                  = const(13)
    EN0_CLK_SYS_I2C1                = const(12)
    EN0_CLK_SYS_I2C0                = const(11)
    EN0_CLK_SYS_HSTX                = const(10)
    EN0_CLK_HSTX                    = const(9)
    EN0_CLK_SYS_GLITCH_DETECTOR     = const(8)
    EN0_CLK_SYS_DMA                 = const(7)
    EN0_CLK_SYS_BUSFABRIC           = const(6)
    EN0_CLK_SYS_BUSCTRL             = const(5)
    EN0_CLK_SYS_BOOTRAM             = const(4)
    EN0_CLK_SYS_ADC                 = const(3)
    EN0_CLK_ADC                     = const(2)
    EN0_CLK_SYS_ACCESSCTRL          = const(1)
    EN0_CLK_SYS_CLOCKS              = const(0)

    #EN1 masks
    EN1_CLK_SYS_XOSC                = const(32 + 30)
    EN1_CLK_SYS_XIP                 = const(32 + 29)
    EN1_CLK_SYS_WATCHDOG            = const(32 + 28)
    EN1_CLK_USB                     = const(32 + 27)
    EN1_CLK_SYS_USBCTRL             = const(32 + 26)
    EN1_CLK_SYS_UART1               = const(32 + 25)
    EN1_CLK_PERI_UART1              = const(32 + 24)
    EN1_CLK_SYS_UART0               = const(32 + 23)
    EN1_CLK_PERI_UART0              = const(32 + 22)
    EN1_CLK_SYS_TRNG                = const(32 + 21)
    EN1_CLK_SYS_TIMER1              = const(32 + 20)
    EN1_CLK_SYS_TIMER0              = const(32 + 19)
    EN1_CLK_SYS_TICKS               = const(32 + 18)
    EN1_CLK_REF_TICKS               = const(32 + 17)
    EN1_CLK_SYS_TBMAN               = const(32 + 16)
    EN1_CLK_SYS_SYSINFO             = const(32 + 15)
    EN1_CLK_SYS_SYSCFG              = const(32 + 14)
    EN1_CLK_SYS_SRAM9               = const(32 + 13)
    EN1_CLK_SYS_SRAM8               = const(32 + 12)
    EN1_CLK_SYS_SRAM7               = const(32 + 11)
    EN1_CLK_SYS_SRAM6               = const(32 + 10)
    EN1_CLK_SYS_SRAM5               = const(32 + 9)
    EN1_CLK_SYS_SRAM4               = const(32 + 8)
    EN1_CLK_SYS_SRAM3               = const(32 + 7)
    EN1_CLK_SYS_SRAM2               = const(32 + 6)
    EN1_CLK_SYS_SRAM1               = const(32 + 5)
    EN1_CLK_SYS_SRAM0               = const(32 + 4)
    EN1_CLK_SYS_SPI1                = const(32 + 3)
    EN1_CLK_PERI_SPI1               = const(32 + 2)
    EN1_CLK_SYS_SPI0                = const(32 + 1)
    EN1_CLK_PERI_SPI0               = const(32 + 0)

    def __init__(self) :
       __CLOCK_BASE_2350  = const(0x40010000)
                               
       self.__WAKE_EN0    = __CLOCK_BASE_2350+0xac
       self.__WAKE_EN1    = __CLOCK_BASE_2350+0xb0
       self.__SLEEP_EN0   = __CLOCK_BASE_2350+0xb4
       self.__SLEEP_EN1   = __CLOCK_BASE_2350+0xb8

        # default values for RP2350
       self.__SAVE_SLEEP_EN0  = 0xffffffff;
       self.__SAVE_WAKE_EN0   = 0xffffffff;
       self.__SAVE_SLEEP_EN1  = 0x7fffffff;
       self.__SAVE_WAKE_EN1   = 0x7fffffff;

    def __repr__(self) :
        return "%s\n%s" % ("PowerCtrl for RP2350", super().__repr__())
