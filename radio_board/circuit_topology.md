# Schematic Reference — BT-to-Radio PTT Adapter

> Single-PCB Bluetooth interface to a Kenwood-style ("K") two-way radio.
> An nRF52-based MCU (SKB369) supervises a Feasycom FSC-BT1036C BT audio
> module over UART; bidirectional audio is level-matched between the module
> and the radio; PTT is keyed by a low-side MOSFET. Li-ion powered, USB-C
> charged. This document is the canonical topology reference used as a
> preprompt for schematic debugging.

---

## 1. Power architecture

| Rail     | Source                              | Nominal         | Notes                          |
|----------|-------------------------------------|-----------------|--------------------------------|
| 5V_USB   | USB-C VBUS (USB1)                   | 5.0 V           | Only present when cable is in  |
| +BATT    | Li-ion cell via U5 → U3 protection  | 3.0 – 4.2 V     | Gated downstream by SW3        |
| +3.3V    | XC6206P332MR LDO (U6)               | 3.3 V           | Main logic / analog rail       |
| GND      | —                                   | 0 V             | Single ground                  |

Flow:

```
USB-C (VBUS) ─► 5V_USB ─► TP4057 (U2) ─► +BATT ◄─ Cell (U5) ─ XB5352A (U3)
                                                │
                                              SW3 ─► XC6206 (U6) ─► +3.3V
```

---

## 2. Complete BOM

### Active devices

| Ref    | Part                      | Function                              |
|--------|---------------------------|---------------------------------------|
| SKB369 | nRF52-based module        | Main MCU / system controller          |
| U1     | FSC-BT1036C               | BT audio + data module (Feasycom)     |
| U2     | TP4057                    | Single-cell Li-ion linear charger     |
| U3     | XB5352A                   | Single-cell Li-ion protection IC      |
| U6     | XC6206P332MR              | 3.3 V / 200 mA LDO                    |
| U7     | LMV321                    | Single rail-to-rail op-amp            |
| Q1     | 2N7002K                   | N-channel MOSFET (PTT low-side)       |
| D1     | Blue LED                  | FSC module status indicator           |
| G_LED  | Green LED                 | Charger `CHRG` indicator              |
| R_LED  | Red LED                   | Charger `STDBY` indicator             |

### Connectors & switches

| Ref   | Part                     | Function                              |
|-------|--------------------------|---------------------------------------|
| USB1  | USB-C 6-pin (TYPE-C 6P Q1073) | Charging input                   |
| U5    | SZB-PH-K-6(LF)(SN)       | Li-ion cell connector *("CHECK POLARITY")* |
| CN1   | HX JN1.27-2×5P ZZ H4.9   | Cortex-M 10-pin SWD header            |
| SW2   | Tactile switch, 4-pin    | User button → P0.27                   |
| SW3   | MSK-12C02 slide SPDT     | Main on/off between +BATT and LDO     |
| Probes| Single-row test header   | Debug test points (see §3.8)          |

### Passives

| Ref    | Value      | Role                                               |
|--------|------------|----------------------------------------------------|
| R0     | *(unclear)*| G_LED series current limit **← verify designator** |
| R1     | 1 kΩ       | D1 (FSC LED) series                                |
| R2     | 1 kΩ       | R_LED series current limit                         |
| R3     | 5.1 kΩ     | USB-C CC1 pulldown (UFP advertisement)             |
| R4     | 5.1 kΩ     | USB-C CC2 pulldown (UFP advertisement)             |
| R5     | 3.3 kΩ     | TP4057 `PROG` — sets charge current                |
| R6     | 100 Ω      | XB5352A VM/−BATT sense                             |
| R7     | 22 kΩ      | TX audio output series                             |
| R8     | 8.2 kΩ     | RX audio input series                              |
| R9     | 10 kΩ      | Q1 gate pulldown                                   |
| R10    | 10 kΩ      | Op-amp summing, SPK_LP leg                         |
| R11    | 10 kΩ      | Op-amp summing, SPK_LN leg                         |
| R12    | 10 kΩ      | Op-amp bias divider (top)                          |
| R13    | 10 kΩ      | Op-amp bias divider (bottom)                       |
| R14    | 10 kΩ      | Op-amp feedback                                    |
| R15    | 10 kΩ      | TX output load to GND                              |
| RV1    | 1 kΩ trim  | TX output level                                    |
| RV2    | 1 kΩ trim  | RX input level                                     |
| C1     | 10 µF      | U1 VDD bulk                                        |
| C2     | 100 nF     | U1 VDD HF                                          |
| C3     | 1 µF       | 5V_USB decoupling                                  |
| C4     | 1 µF       | TP4057 BAT output                                  |
| C5     | 0.1 µF     | XB5352A VM                                         |
| C6     | 1 µF       | U6 LDO input                                       |
| C7     | 1 µF       | +BATT bulk *("can be omitted if C4 is close")*     |
| C8/CB  | 10 µF      | SKB369 VCC bulk **← verify designator**            |
| C9     | 100 nF     | SKB369 VCC HF                                      |
| C12    | 4.7 µF     | RX input AC-coupling                               |
| C13    | 1 µF       | RX output AC-coupling to MIC0_LP                   |
| C14    | 1 nF       | RX RF shunt (wiper to GND)                         |
| C15    | *(n/a)*    | MIC0_LN AC termination to GND                      |
| C16    | 100 nF     | U7 supply HF                                       |
| C17    | 1 µF       | U7 supply bulk                                     |
| C18    | 1 µF       | TX input AC-coupling (SPK_LP)                      |
| C19    | 1 µF       | TX input AC-coupling (SPK_LN)                      |
| C20    | 1 µF       | TX output AC-coupling                              |
| C21    | 10 µF      | Op-amp bias-node bypass                            |

**Numbering gaps (no components on sheet):** C10, C11, U4.

---

## 3. Subsystems

### 3.1 MCU — SKB369 (nRF52 module)

- **Supply:** +3.3 V; decoupled by C9 (100 nF) ∥ C8/CB (10 µF).
- **User input:** SW2 between +3.3 V and P0.27 (uses internal pull-down or pull-up in MCU; no external divider).
- **Debug:** SWDIO (pin 23), SWDCLK (pin 24), RESET (pin 22) → CN1; RESET is also tied to U1 `RESET`.
- **UART to U1:** UART_TX (pin 12), UART_RX (pin 13).
- **PTT control:** P0.08 → Q1 gate.
- **Exposed to Probes:** P0.06, P0.07, P0.08, UART_TX, UART_RX.
- **Other nets present but unused on-sheet:** P0.25, P0.26, P0.28–P0.31, P0.09/NFC1, P0.10/NFC2, ANT.

### 3.2 BT module — FSC-BT1036C (U1)

- **Supply:** +3.3 V to VDD (pin 32); C1 (10 µF) ∥ C2 (100 nF); 3.3V_OUT (pin 31) exposed, unloaded.
- **UART #1 (to MCU):** UART_TX (p16), UART_RX (p17), UART_CTS (p18), UART_RTS (p19).
- **UART #2:** UART_TX_2 (p36), UART_RX_2 (p35) — broken out, unused.
- **I²S bus:** BCLK / DI / DO / WS / MCLK (p4–p8) — broken out, unused.
- **I²C:** I2C_SCL, I2C_SDA, I2C_SCL_2, I2C_SDA_2 (p27–p30) — broken out, unused.
- **ADC:** ADC0 (p10), ADC1 (p11) — broken out, unused.
- **GPIO broken out, unused:** P2/LED (p15), P13 (p21).
- **Analog audio OUT (differential stereo):** SPK_LP (p48), SPK_LN (p47), SPK_RP (p46), SPK_RN (p45). **Only L pair used downstream (§3.6).**
- **Analog audio IN:** MIC_BIAS (p44), MIC0_LN (p43), MIC0_LP (p42), MIC0_RN (p41), MIC0_RP (p40). **Only L pair used (§3.7). MIC_BIAS not used (AC-coupled input).**
- **Status LED:** FSC_LED (pin near p20) → R1 (1 kΩ) → D1 anode; D1 cathode → GND.
- **RESET:** tied to MCU RESET net.
- **EXT_ANT (p52):** exposed; module uses internal antenna by default.
- **Ground pins:** p1, p3, p22, p25, p26, and thermal pad — all tied to GND.

### 3.3 PTT driver

```
P0.08 ──┬──► Q1 gate
        │
        R9 (10 kΩ)
        │
       GND

Q1 drain  ──► K_CONNECTOR_PTT_TRIGGER_SLEEVE  (tip & sleeve labels tied)
Q1 source ──► GND
```

- Idle-safe: R9 holds the gate low while MCU is in reset.
- Asserting P0.08 high shorts PTT to ground.

### 3.4 SWD debug — CN1 (Cortex-M 10-pin)

| CN1 pin | Net    | CN1 pin | Net    |
|---------|--------|---------|--------|
| 1       | +3.3V  | 2       | SWDIO  |
| 3       | GND    | 4       | SWDCLK |
| 5       | GND    | 6       | —      |
| 7       | —      | 8       | —      |
| 9       | GND    | 10      | RESET  |

### 3.5 Power & charging

**USB-C input (USB1):**
- VBUS → 5V_USB; C3 (1 µF) decoupling.
- CC1 → R3 (5.1 kΩ) → GND; CC2 → R4 (5.1 kΩ) → GND — UFP (sink) advertisement.
- USB D+/D− not connected downstream on this sheet.

**Charger (U2 TP4057):**
- VCC ← 5V_USB.
- BAT → +BATT; C4 (1 µF) on BAT.
- PROG → R5 (3.3 kΩ) → GND — sets charge current.
- CHRG → G_LED cathode; G_LED anode → R0 → 5V_USB.
- STDBY → R_LED cathode; R_LED anode → R2 (1 kΩ) → 5V_USB.
- GND → GND.

**Protection (U3 XB5352A) + cell (U5):**
- Pack +BATT / −BATT from U5 (2-pin used; 6-pin housing).
- VM path: −BATT → R6 (100 Ω) → VM pin; C5 (0.1 µF) on VM.
- Handles over-charge, over-discharge, over-current, short-circuit.
- **Silkscreen / schematic note: "CHECK POLARITY"** on cell connector.

**Main switch (SW3):**
- SPDT slide (MSK-12C02) between +BATT and U6 VIN.

**LDO (U6 XC6206P332MR):**
- VIN ← switched +BATT; C6 (1 µF) input.
- VOUT → +3.3 V; C7 (1 µF) *"can be omitted if C4 is close"* (design note).

### 3.6 TX audio path — "Speaker voltage limiting"

Inverting summing amplifier collapsing stereo SPK_L± to mono, then attenuating to mic level.

```
SPK_LP ─┤├─ C18 (1µF) ─► R10 (10k) ─┐
                                     ├─► U7 inv input (pin 2)
SPK_LN ─┤├─ C19 (1µF) ─► R11 (10k) ─┘
                                        U7 out (pin 1) ─► RV1 (1k) ─┬─► R15 (10k) ─► GND
                                                                     │
                                                                     └─► R7 (22k) ─┤├─ C20 (1µF) ─► K_CONNECTOR_MIC_IN (tip + sleeve)

Bias (non-inv, pin 3):  +3.3V ─ R12 (10k) ─┬─ R13 (10k) ─ GND
                                            ├─► U7 pin 3
                                            └─► C21 (10µF) ─ GND

Feedback:  U7 pin 1 ─ R14 (10k) ─ U7 pin 2

Supply:    U7 pin 5 → +3.3V (∥ C16 100nF, C17 1µF to GND); U7 pin 4 → GND
```

### 3.7 RX audio path — "Mic voltage limiting"

Passive AC-coupled attenuator, radio speaker → BT module left mic.

```
K_CONNECTOR_SPK_OUT ─┤├─ C12 (4.7µF) ─► R8 (8.2k) ─┬─► RV2 (1k) top
                                                     │
                                                    C14 (1nF) ─ GND  (wiper-to-GND RF shunt)
                                                     │
                                   RV2 wiper ─┤├─ C13 (1µF) ─► MIC0_LP
                                   RV2 bottom ─► GND

MIC0_LN ─┤├─ C15 ─ GND                (cold side AC termination)
```

- **MIC_BIAS is not tied to this input** — module runs MIC0 in AC-coupled mode.

### 3.8 Probes / test points

Single-row header; signals exposed for bench instrumentation:

```
GND × 3, −BATT × 2, +BATT × 2, +3.3V,
UART_RX, UART_TX,
MIC0_LP, MIC0_LN, MIC0_RN, MIC0_RP, MIC_BIAS,
SPK_LP, SPK_LN, SPK_RP, SPK_RN,
FSC_LED, P0.08
```

---

## 4. Inter-block net map

| Net                              | Driver(s)        | Receiver(s)        | Notes                       |
|----------------------------------|------------------|---------------------|-----------------------------|
| UART_TX                          | SKB369 p12       | U1 p16              | Also to Probes              |
| UART_RX                          | U1 p17           | SKB369 p13          | Also to Probes              |
| RESET                            | SKB369 p22 / CN1 | U1 RESET            | Shared reset domain         |
| SWDIO                            | CN1 p2           | SKB369 p23          |                             |
| SWDCLK                           | CN1 p4           | SKB369 p24          |                             |
| P0.08                            | SKB369           | Q1 gate, Probes     | PTT control                 |
| FSC_LED                          | U1               | R1 → D1, Probes     |                             |
| SPK_LP / SPK_LN                  | U1 p48 / p47     | U7 inverting sum    | Also to Probes              |
| MIC0_LP / MIC0_LN                | U7 (via RV2/C13) | U1 p42 / p43        | Also to Probes              |
| K_CONNECTOR_MIC_IN               | TX path out      | (external K plug)   | Tip + sleeve                |
| K_CONNECTOR_SPK_OUT              | (external K plug)| RX path in          | Tip + sleeve                |
| K_CONNECTOR_PTT_TRIGGER_SLEEVE   | Q1 drain         | (external K plug)   | Tip + sleeve tied together  |
| 5V_USB                           | USB1 VBUS        | U2 VCC, charge LEDs | Decoupled by C3             |
| +BATT                            | U2 BAT / U5      | SW3, Probes         | Protected by U3             |
| +3.3V                            | U6 VOUT          | SKB369, U1, U7, CN1 | Global logic/analog rail    |

---

## 5. Unused / broken-out resources (for reference during debugging)

- **FSC-BT1036C:** UART #2, I²S, I²C (both), ADC0/1, P2/LED, P13, EXT_ANT, 3.3V_OUT.
- **SKB369:** P0.06, P0.07, P0.25, P0.26, P0.28–P0.31, P0.09/NFC1, P0.10/NFC2, ANT.
- **Stereo audio:** Only the L channel is wired on both TX and RX. Right-channel SPK/MIC pairs exit U1 but terminate only at the Probes header.

---

## 6. Known ambiguities / flags

1. **R0 designator** — the G_LED series resistor is readable as `R0` in the screenshot; verify against BOM/PCB.
2. **C8 vs CB** — the 10 µF bulk cap at SKB369 VCC; the label is ambiguous at current resolution.
3. **Numbering gaps:** C10, C11, U4 — not present on this sheet.
4. **"CHECK POLARITY"** warning on U5 cell connector — pinout of the JST-PH housing must be checked against the specific pack used.
5. **Design note on C7:** "Can be omitted if C4 is close" — acceptable only if C4 provides local bulk for U6 VIN.
6. **K-radio plug body** not drawn: only net labels `K_CONNECTOR_*` exit the sheet. Physical connector is on another sheet or mechanical-only.
7. **MIC_BIAS is unused** in the RX path; if the design intent was to bias an electret-style input, this is a candidate defect.
8. **Only L-channel audio routed** — confirm this is intentional (mono radio link) and not an unrouted net.
9. **SW2** has no visible external pull — assumes MCU internal pull is configured in firmware.
10. **R9 is a gate-to-source pull-down**, but there is no explicit gate series resistor on Q1; acceptable for a slow low-side switch but worth noting.

---

## 7. Topology summary (single diagram)

```
             ┌──────────────── USB-C (USB1) ────────────────┐
             │            R3,R4 = 5.1k CC pulldowns          │
             └─ VBUS ─► 5V_USB ─┬─► C3                       │
                                │                            │
                         ┌──────┴──────┐                     │
                         │  U2 TP4057  │── PROG ─ R5 (3.3k) ─┘
                         │  charger    │── CHRG ─ G_LED ─ R0 ─ 5V_USB
                         │             │── STDBY─ R_LED ─ R2 ─ 5V_USB
                         └──────┬──────┘
                                │ BAT
                            C4 ─┤
                                ▼
                    ┌─── +BATT ───────────────── Cell (U5) ── U3 XB5352A (C5, R6)
                    │
                   SW3 (slide)
                    │
                    ▼
                  U6 XC6206 LDO  ── C6 in / C7 out ──► +3.3V ──┐
                                                                │
                                                                ▼
  ┌───────────────────────────────────────────────────────────────────────────────┐
  │                                                                               │
  │  SKB369 (nRF52) ◄─── SWD ──► CN1                                              │
  │    │                                                                          │
  │    ├── UART_TX / UART_RX ──────────────► U1 FSC-BT1036C  (C1, C2)             │
  │    │                                        │                                 │
  │    │                                        ├── FSC_LED ─ R1 ─ D1 ─ GND       │
  │    │                                        │                                 │
  │    │                                        │  SPK_LP/LN ──► U7 LMV321        │
  │    │                                        │                (summing amp     │
  │    │                                        │                 + RV1/R7/R15    │
  │    │                                        │                 + C20) ──► K_MIC_IN
  │    │                                        │                                 │
  │    │                                        │  MIC0_LP/LN ◄── RV2 / R8 /      │
  │    │                                        │                 C12,C13,C14,C15 │
  │    │                                        │                ◄── K_SPK_OUT    │
  │    │                                        │                                 │
  │    │                              RESET ────┴── shared                        │
  │    │                                                                          │
  │    └── P0.08 ──► Q1 (2N7002K), R9 pulldown ──► K_PTT_TRIGGER                  │
  │                                                                               │
  └───────────────────────────────────────────────────────────────────────────────┘
```

**One-line function:** The MCU talks to the BT module over UART, keys PTT via a
low-side MOSFET, and the two audio directions pass through an op-amp
summing-attenuator (outbound) and an RC/trimmer network (inbound) between the
BT module and the Kenwood-style radio connector.
