/*
 * sct.c
 *
 *  Created on: Oct 8, 2025
 *      Author: 228046
 */

#include "sct.h"
#include "main.h"

void sct_init(void)
{
	sct_led(0);
}

void sct_led(uint32_t value)
{
    // Odesíláme 32 bitů, od LSB po MSB
    for (uint8_t i = 0; i < 32; i++)
    {
        // Nastav SDI podle aktuálního bitu (LSB první)
        if (value & 1)
            HAL_GPIO_WritePin(SCT_SDI_GPIO_Port, SCT_SDI_Pin, 1);
        else
            HAL_GPIO_WritePin(SCT_SDI_GPIO_Port, SCT_SDI_Pin, 0);

        // Puls na CLK (zachytí bit do posuvného registru)
        HAL_GPIO_WritePin(SCT_CLK_GPIO_Port, SCT_CLK_Pin, 1);
        HAL_GPIO_WritePin(SCT_CLK_GPIO_Port, SCT_CLK_Pin, 0);

        // Posuneme hodnotu doprava, připravíme další bit
        value >>= 1;
    }

    // Puls na /LA (latch), aby se data přenesla do výstupního registru
    HAL_GPIO_WritePin(SCT_NLA_GPIO_Port, SCT_NLA_Pin, 1);
    HAL_GPIO_WritePin(SCT_NLA_GPIO_Port, SCT_NLA_Pin, 0);
}
