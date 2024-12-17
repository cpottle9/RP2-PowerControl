from power_ctrl_2040 import PowerCtrl

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

