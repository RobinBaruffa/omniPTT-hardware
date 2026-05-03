# Detailed Wiring Description

## 1. Host MCU — SKB369

**Module pinout (net → pin):**
- Pin 1 → GND
- Pin 2 (VCC) → +3.3 V
- Pin 3 → P0.25 (unused, exposed)
- Pin 4 → P0.26 (unused)
- Pin 5 → P0.27 → SW2 pins 3–4
- Pin 6 → P0.28, Pin 7 → P0.29, Pin 8 → P0.30, Pin 9 → P0.31 (unused)
- Pin 10 → P0.10/NFC2 (unused)
- Pin 11 (P0.02) → **UART_TX** (to U1 pin 14, UART_RX)
- Pin 12 (P0.03) → **UART_RX** (from U1 pin 13, UART_TX)
- Pin 13 (P0.06) → probe P0.06
- Pin 14 (P0.07) → probe P0.07
- Pin 15 (P0.08) → **PTT drive** (Q1 gate / R9 / probe)
- Pin 16 (P0.09/NFC1) → unused
- Pins 17–21 (P0.16…P0.19) → unused
- Pin 22 (P0.21/RESET) → **RESET net** (to CN1 pin 10 and to U1 pin 8)
- Pin 23 → SWDIO (to CN1 pin 2)
- Pin 24 → SWDCLK (to CN1 pin 4)
- Pin 25 → ANT (internal antenna, unconnected externally)

**Passives:**
- **SW2** (tactile button): pins 1–2 to +3.3 V; pins 3–4 to P0.27. When released, P0.27 floats (needs internal pull-down) ; when pressed, P0.27 is pulled to +3.3 V.
- **C8 (10 µF)** and **C9 (100 nF)**: both connected between pin 2 (VCC/+3.3 V) and GND, placed close to the module for bulk + HF decoupling.

---

## 2. Bluetooth Module — U1 (FSC-BT1036C)

**Power pins:**
- Pin 32 (VDD) → +3.3 V rail; decoupled by **C1 (10 µF)** and **C2 (100 nF)**, each tied between VDD and GND.
- Pin 38 → **+5 V** (from +5V_usb, direct).
- Pin 31 (3.3V_OUT) → brought out but not loaded on this sheet.
- GND pins 1, 22, 50, 52 → GND plane.

**UART link to SKB369:**
- Pin 13 (UART_TX) → UART_RX of SKB369.
- Pin 14 (UART_RX) ← UART_TX of SKB369.
- Pins 15 (CTS), 16 (RTS) → brought out but not wired to the MCU (floating/reserved).
- Pins 36, 37 → alternate UART_RX_2 / UART_TX_2 brought out but unused.

**Audio pins:**
- Pins 48 (SPK_LN), 49 (SPK_LP) → differential output to TX audio stage (U7 inputs).
- Pins 43 (MIC0_LP), 44 (MIC0_LN) → differential input from RX audio stage.
- Pins 39, 40 (MIC0_RP/RN), 46, 47 (SPK_RP/RN), 45 (MIC_BIAS) → broken out to probe header only.
- Pin 45 (MIC_BIAS) → probe only (not used because the RX path uses AC coupling to GND, not an electret mic).

**Other I/O (all probe-exposed or unused):**
- Pins 4–7, 9 (I²S bus) → unused.
- Pins 24, 26, 27, 28 (I²C) → unused.
- Pin 8 (RESET) → tied to the common RESET net (shared with SKB369/CN1).
- Pin 17 (P2/LED) → **FSC_LED** probe.
- P2  → drives **B_LED** indicator via **R1 (1 kΩ)** in series with **D1**, cathode to GND.
- Pin 19/20 (ADC1) → unused.
- Pin 51 → EXT_ANT (module-internal antenna path).

---

## 3. PTT Switching Stage — Q1

- **Q1 (2N7002K) gate** ← P0.08 from SKB369 pin 15.
- **R9 (10 kΩ)** between gate and GND → pull-down that guarantees Q1 is OFF during MCU reset or Hi-Z state.
- **Source** → GND.
- **Drain** → K_CONNECTOR_PTT_TRIGGER_SLEEVE (sleeve of the radio's PTT jack). When P0.08 is driven high, Q1 shorts the sleeve to GND, keying the radio.

---

## 4. Power & Charging

### 4.1 USB-C input (USB1 QT073)
- Pins A9/B9 (VBUS) → **+5V_usb** net.
- Pins A12/B12, EH (shield) → GND.
- Pin A5 (CC1) → GND via **R3 (5.1 kΩ)** → declares the board as a USB-C sink (UFP, 5 V default).
- Pin B5 (CC2) → GND via **R4 (5.1 kΩ)** → same role for orientation-independent insertion.

### 4.2 Li-ion charger (U2 TP4057)
- Pin 4 (Vcc) ← +5V_usb; local decouple **C3 (1 µF)** to GND.
- Pin 3 (BAT) → **+BATT** net; bulk cap **C4 (1 µF)** to GND.
- Pin 2 (GND) → GND.
- Pin 6 (PROG) → GND via **R5 (3.3 kΩ)** → sets charge current (≈300 mA for TP4057).
- Pin 1 (CHRG) → cathode of **D3 (R_LED)**; anode of D3 → series with **R2 (1 kΩ)** to +5V_usb → red "charging" indicator (lights while U2 sinks CHRG low).
- Pin 5 (STDBY) → cathode of **D2 (G_LED)**; anode of D2 shares the same R2 path (or a mirror) to +5V_usb → green "charge-complete" indicator.

### 4.3 Battery and protection (U3 XB5352A, U5)
- **U5 (PH-2 connector)**: pin 1 → +BATT (battery +), pin 2 → –BATT (battery –).
- U3 sits between the raw cell and the system:
  - VDD → cell +, VM → cell –, 
  - Power-FETs internal to U3 open –BATT during over-current / over-discharge / over-charge events.
  - **C5 (0.1 µF)** between VDD and VM → local supply decoupling for the protection IC.
  - **R6 (100 Ω)** between VDD pin and +BATT rail → VDD sense resistor (standard XB5352A reference schematic).

### 4.4 Main switch (SW3 MSK12C02)
- Slide switch inserted in the +BATT rail feeding U6's input; when OFF, U6 is starved and the whole +3.3 V rail collapses (U1, SKB369, U7, CN1 all lose power).

### 4.5 3.3 V LDO (U6 TLV75533PDBVR)
- Pin IN ← switched +BATT (from SW3).
- Pin EN → tied to IN (always enabled when battery is switched on).
- Pin GND → GND.
- Pin OUT → **+3.3 V** system rail.
- Pin NC → left floating.
- Output decoupling: **C6 (10 µF)** and **C25 (100 nF)** from OUT to GND.
- Input decoupling: **C7 (10 µF)** and **C24 (100 nF)** from IN to GND.

---

## 5. TX Audio Stage — "Speaker voltage limiting" (BT → radio MIC)

5. TX Audio Stage — "Speaker voltage limiting" (as drawn)

Mid-rail bias (U7 pin1 reference):

    R12 (10k) left → GND, right → bias node
    R13 (10k) left → bias node, right → +3.3V
    C21 (10µF) between bias node and GND
    bias node → U7 pin1 (+)

Non-inverting input – U7 pin1:

    SPK_LP → C18 (1µF) → R10 (10k) → pin1
    SPK_LN → C19 (1µF) → R11 (10k) → pin1
    C11 (33pF) pin1 → GND
    R14 (10k) top → bias node, bottom → open in the drawing (in your original text it went to the – input)

Inverting input – U7 pin3:

    C10 (33pF) pin3 → GND
    R15 (10k) pin3 ↔ U7 pin4 (output) → this is now the only feedback = unity-gain follower

Supply:

    U7 pin5 (V+) → +3.3V, decoupled by C16 (100nF), C17 (10µF), and C23 (33pF) all to GND
    U7 pin2 (V–) → GND

Output path:

    U7 pin4 → C22 (33pF) → GND
    U7 pin4 → R7 (4.7k) → C20 (1µF) → node X
    node X → R16 (100) → GND
    node X → RV1 pin3, RV1 pin1 tied back to pin3 (so RV1 = 0–1k rheostat)
    RV1 wiper (pin2) → K_CONNECTOR_MIC_IN

---

## 6. RX Audio Stage — "Mic voltage limiting" (radio SPK → BT MIC)

Purely passive attenuator and AC-coupler.

**Signal path (radio speaker → U1 MIC0_LP):**
- K_CONNECTOR_SPK_OUT → **C12 (4.7 µF)** (AC-coupling, blocks DC from the radio's speaker stage)
- → **R8 (8.2 kΩ)** (series attenuator element)
- → **RV2 (1 kΩ)** trimmer (top of track)
- RV2 wiper → **C14 (1 nF)** to GND (shunt cap forming an RC low-pass with R8/RV2)
- Wiper → **C13 (1 µF)** → **MIC0_LP** (U1 pin 43).

**Differential ground return:**
- **MIC0_LN** (U1 pin 44) → **C15 (1 µF)** → GND → AC-grounds the negative mic input, making U1 see the signal as pseudo-differential against its internal mic-bias reference.

---

## 7. SWD Debug Connector — CN1 (JN1.27 2×5 P)

- Pin 1 → +3.3 V
- Pin 2 → SWDIO (to SKB369 pin 23)
- Pin 3 → not connected (key/no-pin)
- Pin 4 → SWDCLK (to SKB369 pin 24)
- Pin 5 → GND
- Pin 6, 8 → not connected
- Pin 7 → (cut pin — standard Cortex-M 10-pin keying)
- Pin 9 → GND
- Pin 10 → RESET (to SKB369 pin 22 and U1 pin 8)

No series resistors, no level shifters → debugger drives the target rail directly.

---

## 8. Probe Header

A bank of 2-pin headers, each wiring one named net to a test pad on the opposite side: GND ×3, –BATT ×2, +BATT ×2, +3.3 V ×2, UART_TX, UART_RX, MIC0_LP, MIC0_LN, MIC0_RN, MIC0_RP, MIC_BIAS, SPK_LP, SPK_LN, SPK_RP, SPK_RN, FSC_LED, P0.08. No passives — pure break-outs for oscilloscope/logic-analyzer access.

---

## 9. Cross-Subsystem Nets (summary)

- **+3.3 V rail:** feeds SKB369 pin 2, U1 pin 32 (via C1/C2), U7 pin 5 (via C16/C17), CN1 pin 1, R13 (mid-rail gen).
- **+5V_usb:** feeds U2 pin 4 (via C3)
- **+BATT:** from U2 pin 3 / U3 output (via R6), through SW3, into U6 IN (via C6/C25).
- **GND:** global return; every decoupling cap, every op-amp V–, every Q1 source, every USB shield pin, every protection-IC return lands here.
- **RESET:** common to SKB369 pin 22, U1 pin 8, CN1 pin 10 — debugger resets both the MCU and the BT module simultaneously.
- **UART_TX/UART_RX:** the only runtime control channel between SKB369 and U1.
- **P0.08:** single-purpose line, MCU → Q1 gate only.