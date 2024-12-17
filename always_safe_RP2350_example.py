from power_ctrl_2350 import PowerCtrl

pwr = PowerCtrl()

# It is always safe to turn off XIP and SRAM when sleeping.
pwr.disable_while_sleeping(
    pwr.EN1_CLK_SYS_XIP,
    pwr.EN1_CLK_SYS_SRAM9,
    pwr.EN1_CLK_SYS_SRAM8,
    pwr.EN1_CLK_SYS_SRAM7,
    pwr.EN1_CLK_SYS_SRAM6,
    pwr.EN1_CLK_SYS_SRAM5,
    pwr.EN1_CLK_SYS_SRAM4,
    pwr.EN1_CLK_SYS_SRAM3,
    pwr.EN1_CLK_SYS_SRAM2,
    pwr.EN1_CLK_SYS_SRAM1,
    pwr.EN1_CLK_SYS_SRAM0

)

