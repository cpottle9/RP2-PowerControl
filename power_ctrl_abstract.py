from machine import mem32

class PowerCtrlAbstract :

    __WAKE_EN0    = 0
    __WAKE_EN1    = 0
    __SLEEP_EN0   = 0
    __SLEEP_EN1   = 0
    
    __SAVE_SLEEP_EN0  = 0
    __SAVE_WAKE_EN0   = 0
    __SAVE_SLEEP_EN1  = 0
    __SAVE_WAKE_EN1   = 0

    def __combine_args(self, args) :
        mask0 = 0
        mask1 = 0
        for arg in args:
            if arg >= 32 :
                mask1 |= 1 << (arg - 32)
            else :
                mask0 |= 1 << arg
        return mask0, mask1
    
    # Disable specified hardware blocks while RP2 is sleeping.
    # If called with no arguments does nothing.

    def disable_while_sleeping(self, *args) :
        mask0, mask1 = self.__combine_args(args)
                
        mem32[self.__SLEEP_EN0] &= ~mask0
        mem32[self.__SLEEP_EN1] &= ~mask1
        
    # Enable specified hardware blocks while RP2 is sleeping.
    # If called with no arguments does nothing.
    #
    # Note: Not that useful.
    # Typically users disable given hardware blocks and leave it that way forever.
    
    def enable_while_sleeping(self, *args) :
        mask0, mask1 = self.__combine_args(args)
                
        mem32[self.__SLEEP_EN0] |= mask0
        mem32[self.__SLEEP_EN1] |= mask1
        
    # Disable all but the specified hardware blocks while RP2 is sleeping.
    # If called with no argumentss will disable all hardware blocks.

    def disable_while_sleeping_all_but(self, *args) :
        mask0, mask1 = self.__combine_args(args)

        mem32[self.__SLEEP_EN0] &= mask0
        mem32[self.__SLEEP_EN1] &= mask1

    # Disable specified hardware blocks while RP2 is
    # awake (at least one core running or DMA active),
    # If called with no arguments does nothing.

    def disable_while_awake(self, *args) :
        mask0, mask1 = self.__combine_args(args)

        mem32[self.__WAKE_EN0] &= ~mask0
        mem32[self.__WAKE_EN1] &= ~mask1
        
    # Enable specified hardware blocks while RP2 is
    # awake (at least one core running or DMA active),
    # If called with no arguments does nothing.
    #
    # Note: Useful if given hardware blocks are needed occasionally.

    def enable_while_awake(self, *args) :
        mask0, mask1 = self.__combine_args(args)

        mem32[self.__WAKE_EN0] |= mask0
        mem32[self.__WAKE_EN1] |= mask1
        
    # Disable all but the specified hardware blocks while RP2 is
    # awake(at least one core running or DMA active),
    # If called with no arguments  will disable all hardware blocks.

    def disable_while_awake_all_but(self, *args) :
        mask0, mask1 = self.__combine_args(args)
        
        mem32[self.__WAKE_EN0] &= mask0
        mem32[self.__WAKE_EN1] &= mask1

    def __str__(self) :

        return "wake_en0:  %08X wake_en1:  %08X\nsleep_en0: %08X sleep_en1: %08X" % (
            0xffffffff & mem32[self.__WAKE_EN0],
            0xffffffff & mem32[self.__WAKE_EN1],
            0xffffffff & mem32[self.__SLEEP_EN0],
            0xffffffff & mem32[self.__SLEEP_EN1]
        )
    #   Set RP2 wake_enX and sleep_enX registers to their default values
    def restore(self) :
        mem32[self.__SLEEP_EN0] = self.__SAVE_SLEEP_EN0
        mem32[self.__SLEEP_EN1] = self.__SAVE_SLEEP_EN1
        mem32[self.__WAKE_EN0]  = self.__SAVE_WAKE_EN0
        mem32[self.__WAKE_EN1]  = self.__SAVE_WAKE_EN1
            
