# Rev B
* Move PMOS screw hole to not intersect with adjacent track. Change flood touching back of PMOS to the correct net (not GND).
* Change PMOS Zener diode to MELF from micro-MELF package.
* DNP C_feed from the feedback network on the DC-DC converter, as it causes instability at higher currents. Probably enough stray capacitance with current layout to feed forward as it is.
* Double output capacitance to 6x22uF to reduce ripple ad account for capacitance drop due to DC bias.
* Swap feedback resistor values so that R_fb2 = 15k Ohms.
