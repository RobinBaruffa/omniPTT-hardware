# Topology Analysis

## Power Nets
- **+3.3V**: C1[10uF]-2, C16[100 nF]-2, C17[10uF]-2, C2[100nF]-2, C23[33 pF]-2, C25[100nF]-2, C6[10uF]-2, C8[10uF]-2, C9[100nF]-2, J1[3.3v]-1(Pin_1), R13[10k]-2, U1[FSC-BT1036C]-33(VDD), U6[TLV75533PDBVR]-5(OUT), U7[LMV321]-5(V+), U8[STM32G030F6P6TR]-4(VDDA/DDA)
- **+BATT**: C4[1uF]-1, R20[1]-2, R6[100]-2, SW3[MSK12C02]-1(1), TP3[+BATT_AFTER_SHUNT]-1(1), U2[TP4057]-3(BAT)
- **+BATT_AFTER_SWITCH**: C24[100nF]-2, C7[10uF]-2, R22[100K]-1, SW3[MSK12C02]-2(2), U6[TLV75533PDBVR]-1(IN), U6[TLV75533PDBVR]-3(EN)
- **-BATT**: C5[0.1uF]-1, TP6[-BATT]-1(1), U3[XB5352A]-2(GND), U5[S2B-PH-K-S(LF)(SN)]-1(1)
- **/+BATT_PRE_SHUNT**: R20[1]-1, TP1[+BATT_PRE_SHUNT]-1(1), TP47[+BATT_PRE_SHUNT]-1(1), U5[S2B-PH-K-S(LF)(SN)]-2(2)
- **5V_usb**: C3[1uF]-2, R2[1K]-1, U2[TP4057]-4(V_{CC}), USB1[TYPE-C 6P QT073]-A9(VBUS), USB1[TYPE-C 6P QT073]-B9(VBUS)
- **GND**: C1[10uF]-1, C10[33 pF]-2, C11[33 pF]-2, C14[1nF]-1, C15[1uF]-1, C16[100 nF]-1, C17[10uF]-1, C2[100nF]-1, C21[10uF]-1, C22[33 pF]-1, C23[33 pF]-1, C24[100nF]-1, C25[100nF]-1, C27[100nF]-1, C28[1nF]-2, C29[100nF]-2, C3[1uF]-1, C30[100nF]-2, C4[1uF]-2, C6[10uF]-1, C7[10uF]-1, C8[10uF]-1, C9[100nF]-1, D1[B LED]-1(K), D5[B LED]-1(K), J2[GND]-1(Pin_1), Q1[2N7002K]-2(S), R12[10k]-1, R16[100]-1, R17[470k]-1, R18[10K]-2, R21[150K]-2, R3[5.1k]-1, R4[5.1k]-1, R5[3.3K]-2, R9[10K]-2, RV2[1K]-3(3), SW2[RKB2SJG250SMTRLFS]-2(2), SW3[MSK12C02]-4(4), TP5[GND]-1(1), U1[FSC-BT1036C]-1(GND), U1[FSC-BT1036C]-22(GND), U1[FSC-BT1036C]-32(GND), U1[FSC-BT1036C]-50(GND), U1[FSC-BT1036C]-52(GND), U2[TP4057]-2(GND), U3[XB5352A]-4(VM), U3[XB5352A]-5(VM), U6[TLV75533PDBVR]-2(GND), U7[LMV321]-2(V-), U8[STM32G030F6P6TR]-5(VSSA/SSA), USB1[TYPE-C 6P QT073]-7(EH), USB1[TYPE-C 6P QT073]-A12(GND), USB1[TYPE-C 6P QT073]-B12(GND)

## Signal Nets
### Debug
- **Debug_gpio**: R19[1K]-2, U8[STM32G030F6P6TR]-10(PA3)
### FSC
- **FSC_LED**: R1[1K]-2, U1[FSC-BT1036C]-17(P2/LED)
### MIC0
- **MIC0_LN**: C15[1uF]-2, TP49[MIC0_LN]-1(1), U1[FSC-BT1036C]-44(MIC0_LN)
- **MIC0_LP**: C13[1uF]-2, TP38[MIC0_LP]-1(1), U1[FSC-BT1036C]-43(MIC0_LP)
- **MIC0_RN**: U1[FSC-BT1036C]-41(MIC0_RN)
- **MIC0_RP**: U1[FSC-BT1036C]-40(MIC0_RP)
### PTT
- **PTT_Trigger**: Q1[2N7002K]-1(G), R9[10K]-1, TP2[PTT_Trigger]-1(1), U8[STM32G030F6P6TR]-13(PA6)
### SPK
- **SPK_LN**: C19[1uF]-2, TP34[SPK_LN]-1(1), U1[FSC-BT1036C]-48(SPK_LN)
- **SPK_LP**: C18[1uF]-2, TP33[SPK_LP]-1(1), U1[FSC-BT1036C]-49(SPK_LP)
- **SPK_RN**: U1[FSC-BT1036C]-46(SPK_RN)
- **SPK_RP**: U1[FSC-BT1036C]-47(SPK_RP)
### Squelch
- **Squelch_detect**: C29[100nF]-1, D2[RB521S-30_C727120]-1(K), R17[470k]-2, TP44[Squelch_detect]-1(1), U8[STM32G030F6P6TR]-14(PA7)
### UART
- **UART_RX**: R23[Poka Yoke UART]-3, U1[FSC-BT1036C]-14(P1/UART_RX/DP)
- **UART_TX**: R23[Poka Yoke UART]-4, U1[FSC-BT1036C]-13(P0/UART_TX/DN)
### Other Signals
- **RESET**: C30[100nF]-1, J3[RESET]-1(Pin_1), U8[STM32G030F6P6TR]-6(NRST)
- **SWDCLK**: J4[SWDCLK]-1(Pin_1), R18[10K]-1, U8[STM32G030F6P6TR]-19(PA15/PA14-BOOT0)
- **SWDIO**: J5[SWDIO]-1(Pin_1), U8[STM32G030F6P6TR]-18(PA13)

## Local (Auto-named) Nets
- **Net-(C12-Pad1)**: C12[4.7uF]-1, TP20[SPK]-1(1), TP45[SPK]-1(1)
- **Net-(C13-Pad1)**: C13[1uF]-1, C14[1nF]-2, RV2[1K]-2(2)
- **Net-(C18-Pad1)**: C18[1uF]-1, R10[47k]-1
- **Net-(C19-Pad1)**: C19[1uF]-1, R11[47k]-1
- **Net-(C20-Pad1)**: C20[1uF]-1, R7[4.7k]-2
- **Net-(C20-Pad2)**: C20[1uF]-2, R16[100]-2, RV1[1K]-3(3)
- **Net-(C21-Pad2)**: C21[10uF]-2, C27[100nF]-2, R12[10k]-2, R13[10k]-1, R14[10k]-2
- **Net-(C22-Pad2) (via U7-4)**: C22[33 pF]-2, R15[10k]-2, R7[4.7k]-1, U7[LMV321]-4
- **Net-(C26-Pad1)**: C26[1uF]-1, RV1[1K]-2(2)
- **Net-(C26-Pad2)**: C26[1uF]-2, L1[BLM18KG601SN1D]-1(1)
- **Net-(C28-Pad1)**: C28[1nF]-1, L1[BLM18KG601SN1D]-2(2), TP50[MIC]-1(1), TP51[MIC]-1(1)
- **Net-(D1-A)**: D1[B LED]-2(A), R1[1K]-1
- **Net-(D2-A)**: C12[4.7uF]-2, D2[RB521S-30_C727120]-2(A), R8[8.2K]-2
- **Net-(D3-A)**: D3[R LED]-2(A), D4[G LED]-2(A), R2[1K]-2
- **Net-(D3-K) (via U2-~{CHRG})**: D3[R LED]-1(K), U2[TP4057]-1(~{CHRG})
- **Net-(D4-K) (via U2-STDBY)**: D4[G LED]-1(K), U2[TP4057]-5(STDBY)
- **Net-(D5-A)**: D5[B LED]-2(A), R19[1K]-1
- **Net-(Q1-D) (via Q1-D)**: Q1[2N7002K]-3(D), TP14[TRIGGER]-1(1), TP43[TRIGGER]-1(1)
- **Net-(R8-Pad1)**: R8[8.2K]-1, RV2[1K]-1(1)
- **Net-(U2-PROG) (via U2-PROG)**: R5[3.3K]-1, U2[TP4057]-6(PROG)
- **Net-(U3-VDD) (via U3-VDD)**: C5[0.1uF]-2, R6[100]-1, U3[XB5352A]-3(VDD)
- **Net-(U7-+) (via U7-+)**: C11[33 pF]-1, R10[47k]-2, R14[10k]-1, U7[LMV321]-1(+)
- **Net-(U7--) (via U7--)**: C10[33 pF]-1, R11[47k]-2, R15[10k]-1, U7[LMV321]-3(-)
- **Net-(U8-PA2) (via U8-PA2)**: R21[150K]-1, R22[100K]-2, U8[STM32G030F6P6TR]-9(PA2)
- **Net-(U8-PA4) (via U8-PA4)**: SW2[RKB2SJG250SMTRLFS]-3(3), U8[STM32G030F6P6TR]-11(PA4)
- **Net-(U8-PB3{slash}PB4{slash}PB5{slash}PB6) (via U8-PB3/PB4/PB5/PB6)**: R23[Poka Yoke UART]-2, U8[STM32G030F6P6TR]-20(PB3/PB4/PB5/PB6)
- **Net-(U8-PB7{slash}PB8) (via U8-PB7/PB8)**: R23[Poka Yoke UART]-1, U8[STM32G030F6P6TR]-1(PB7/PB8)
- **Net-(USB1-CC1) (via USB1-CC1)**: R4[5.1k]-2, USB1[TYPE-C 6P QT073]-A5(CC1)
- **Net-(USB1-CC2) (via USB1-CC2)**: R3[5.1k]-2, USB1[TYPE-C 6P QT073]-B5(CC2)

<details>
<summary>Unconnected Pins</summary>

- **unconnected-(RV1-Pad1)**: RV1[1K]-1(1)
- **unconnected-(SW2-Pad1)**: SW2[RKB2SJG250SMTRLFS]-1(1)
- **unconnected-(SW2-Pad4)**: SW2[RKB2SJG250SMTRLFS]-4(4)
- **unconnected-(SW3-Pad3)**: SW3[MSK12C02]-3(3)
- **unconnected-(U1-+5V-Pad39)**: U1[FSC-BT1036C]-39(+5V)
- **unconnected-(U1-3.3V_OUT-Pad31)**: U1[FSC-BT1036C]-31(3.3V_OUT)
- **unconnected-(U1-EXT_ANT-Pad51)**: U1[FSC-BT1036C]-51(EXT_ANT)
- **unconnected-(U1-I2S_MCLK-Pad9)**: U1[FSC-BT1036C]-9(I2S_MCLK)
- **unconnected-(U1-MIC_BIAS-Pad45)**: U1[FSC-BT1036C]-45(MIC_BIAS)
- **unconnected-(U1-NC-Pad10)**: U1[FSC-BT1036C]-10(NC)
- **unconnected-(U1-NC-Pad11)**: U1[FSC-BT1036C]-11(NC)
- **unconnected-(U1-NC-Pad12)**: U1[FSC-BT1036C]-12(NC)
- **unconnected-(U1-NC-Pad2)**: U1[FSC-BT1036C]-2(NC)
- **unconnected-(U1-NC-Pad23)**: U1[FSC-BT1036C]-23(NC)
- **unconnected-(U1-NC-Pad26)**: U1[FSC-BT1036C]-26(NC)
- **unconnected-(U1-NC-Pad29)**: U1[FSC-BT1036C]-29(NC)
- **unconnected-(U1-NC-Pad3)**: U1[FSC-BT1036C]-3(NC)
- **unconnected-(U1-NC-Pad30)**: U1[FSC-BT1036C]-30(NC)
- **unconnected-(U1-NC-Pad34)**: U1[FSC-BT1036C]-34(NC)
- **unconnected-(U1-NC-Pad35)**: U1[FSC-BT1036C]-35(NC)
- **unconnected-(U1-NC-Pad36)**: U1[FSC-BT1036C]-36(NC)
- **unconnected-(U1-NC-Pad42)**: U1[FSC-BT1036C]-42(NC)
- **unconnected-(U1-P0{slash}UART_TX{slash}DN-Pad38)**: U1[FSC-BT1036C]-38(P0/UART_TX/DN)
- **unconnected-(U1-P11{slash}ADC0-Pad18)**: U1[FSC-BT1036C]-18(P11/ADC0)
- **unconnected-(U1-P13-Pad21)**: U1[FSC-BT1036C]-21(P13)
- **unconnected-(U1-P1{slash}UART_RX{slash}DP-Pad37)**: U1[FSC-BT1036C]-37(P1/UART_RX/DP)
- **unconnected-(U1-P30{slash}I2S_BCLK-Pad4)**: U1[FSC-BT1036C]-4(P30/I2S_BCLK)
- **unconnected-(U1-P31{slash}I2S_WS-Pad7)**: U1[FSC-BT1036C]-7(P31/I2S_WS)
- **unconnected-(U1-P32{slash}I2S_DI-Pad5)**: U1[FSC-BT1036C]-5(P32/I2S_DI)
- **unconnected-(U1-P33{slash}{slash}I2S_DO-Pad6)**: U1[FSC-BT1036C]-6(P33//I2S_DO)
- **unconnected-(U1-P37{slash}ADC1-Pad19)**: U1[FSC-BT1036C]-19(P37/ADC1)
- **unconnected-(U1-P37{slash}ADC1-Pad20)**: U1[FSC-BT1036C]-20(P37/ADC1)
- **unconnected-(U1-P38{slash}I2C_SCL-Pad24)**: U1[FSC-BT1036C]-24(P38/I2C_SCL)
- **unconnected-(U1-P38{slash}I2C_SCL-Pad27)**: U1[FSC-BT1036C]-27(P38/I2C_SCL)
- **unconnected-(U1-P39{slash}I2C_SDA-Pad25)**: U1[FSC-BT1036C]-25(P39/I2C_SDA)
- **unconnected-(U1-P39{slash}I2C_SDA-Pad28)**: U1[FSC-BT1036C]-28(P39/I2C_SDA)
- **unconnected-(U1-P4{slash}UART_CTS-Pad15)**: U1[FSC-BT1036C]-15(P4/UART_CTS)
- **unconnected-(U1-P5{slash}UART_RTS-Pad16)**: U1[FSC-BT1036C]-16(P5/UART_RTS)
- **unconnected-(U1-RESET-Pad8)**: U1[FSC-BT1036C]-8(RESET)
- **unconnected-(U3-VT-Pad1)**: U3[XB5352A]-1(VT)
- **unconnected-(U6-NC-Pad4)**: U6[TLV75533PDBVR]-4(NC)
- **unconnected-(U8-PA0-Pad7)**: U8[STM32G030F6P6TR]-7(PA0)
- **unconnected-(U8-PA1-Pad8)**: U8[STM32G030F6P6TR]-8(PA1)
- **unconnected-(U8-PA11[PA9]-Pad16)**: U8[STM32G030F6P6TR]-16(PA11[PA9])
- **unconnected-(U8-PA12[PA10]-Pad17)**: U8[STM32G030F6P6TR]-17(PA12[PA10])
- **unconnected-(U8-PA5-Pad12)**: U8[STM32G030F6P6TR]-12(PA5)
- **unconnected-(U8-PB0{slash}PB1{slash}PB2{slash}PA8-Pad15)**: U8[STM32G030F6P6TR]-15(PB0/PB1/PB2/PA8)
- **unconnected-(U8-PB9{slash}PC14-OSC32_IN-Pad2)**: U8[STM32G030F6P6TR]-2(PB9/PC14-OSC32_IN)
- **unconnected-(U8-PC15-OSC32_OUT-Pad3)**: U8[STM32G030F6P6TR]-3(PC15-OSC32_OUT)

</details>