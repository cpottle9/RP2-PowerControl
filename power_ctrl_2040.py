from micropython import const
from machine import mem32

from power_ctrl_abstract import PowerCtrlAbstract

class PowerCtrl(PowerCtrlAbstract) :
    EN0_CLK_SYS_SRAM3               = const(31)
    EN0_CLK_SYS_SRAM2               = const(30)
    EN0_CLK_SYS_SRAM1               = const(29)
    EN0_CLK_SYS_SRAM0               = const(28)
    
    EN0_CLK_SYS_SPI1                = const(27)
    EN0_CLK_PERI_SPI1               = const(26)
    EN0_CLK_SYS_SPI0                = const(25)
    EN0_CLK_PERI_SPI0               = const(24)
    
    EN0_CLK_SYS_SIO                 = const(23)
    EN0_CLK_SYS_RTC                 = const(22)
    EN0_CLK_RTC_RTC                 = const(21)
    EN0_CLK_SYS_ROSC                = const(20)

    EN0_CLK_SYS_ROM                 = const(19)
    EN0_CLK_SYS_RESETS              = const(18)
    EN0_CLK_SYS_PWM                 = const(17)
    EN0_CLK_SYS_PSM                 = const(16)
    
    EN0_CLK_SYS_PLL_USB             = const(15)
    EN0_CLK_SYS_PLL_SYS             = const(14)
    EN0_CLK_SYS_PIO1                = const(13)
    EN0_CLK_SYS_PIO0                = const(12)
    
    EN0_CLK_SYS_PADS                = const(11)
    EN0_CLK_SYS_VREG_AND_CHIP_RESET = const(10)
    EN0_CLK_SYS_JTAG                = const(9)
    EN0_CLK_SYS_IO                  = const(8)
    
    EN0_CLK_SYS_I2C1                = const(7)
    EN0_CLK_SYS_I2C0                = const(6)
    EN0_CLK_SYS_DMA                 = const(5)
    EN0_CLK_SYS_BUSFABRIC           = const(4)
    
    EN0_CLK_SYS_BUSCTRL             = const(3)
    EN0_CLK_SYS_ADC                 = const(2)
    EN0_CLK_ADC_ADC                 = const(1)
    EN0_CLK_SYS_CLOCKS              = const(0)


    # EN1 masks
    # value 32 > indicates EN1 bit

    EN1_CLK_SYS_XOSC                = const(32 + 14)
    EN1_CLK_SYS_XIP                 = const(32 + 13)
    EN1_CLK_SYS_WATCHDOG            = const(32 + 12)


    EN1_CLK_USB_USBCTRL             = const(32 + 11)
    EN1_CLK_SYS_USBCTRL             = const(32 + 10)
    EN1_CLK_SYS_UART1               = const(32 + 9)
    EN1_CLK_PERI_UART1              = const(32 + 8)
    
    EN1_CLK_SYS_UART0               = const(32 + 7)
    EN1_CLK_PERI_UART0              = const(32 + 6)
    EN1_CLK_SYS_TIMER               = const(32 + 5)
    EN1_CLK_SYS_TBMAN               = const(32 + 4)
    
    EN1_CLK_SYS_SYSINFO             = const(32 + 3)
    EN1_CLK_SYS_SYSCFG              = const(32 + 2)
    EN1_CLK_SYS_SRAM5               = const(32 + 1)
    EN1_CLK_SYS_SRAM4               = const(32 + 0)

    def __init__(self) :
        __CLOCK_BASE_2040 = const(0x40008000)

        self.__WAKE_EN0    = __CLOCK_BASE_2040+0xa0
        self.__WAKE_EN1    = __CLOCK_BASE_2040+0xa4
        self.__SLEEP_EN0   = __CLOCK_BASE_2040+0xa8
        self.__SLEEP_EN1   = __CLOCK_BASE_2040+0xac

        # default values for RP2040
        self.__SAVE_SLEEP_EN0 = 0xFFFFFFFF
        self.__SAVE_SLEEP_EN1 = 0x00007FFF
        self.__SAVE_WAKE_EN0  = 0xFFFFFFFF
        self.__SAVE_WAKE_EN1  = 0x00007FFF

    def __str__(self) :
        return "%s\n%s" % ("PowerCtrl for RP2040", super().__str__())
