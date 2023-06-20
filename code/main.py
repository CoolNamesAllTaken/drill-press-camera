import machine, neopixel
from machine import Pin, ADC
from utime import sleep
import math # for floor

PIXELS_PER_STRIP = 5
BYTES_PER_PIXEL = 4
U16_MAX = 2**16-1
ADC_DEADBAND = 0.05

np_left = neopixel.NeoPixel(machine.Pin(17), PIXELS_PER_STRIP, BYTES_PER_PIXEL)
np_right = neopixel.NeoPixel(machine.Pin(16), PIXELS_PER_STRIP, BYTES_PER_PIXEL)
adc_color_ctrl = ADC(Pin(27))
adc_brightness_ctrl = ADC(Pin(26))

def main():
    pin = Pin("LED", Pin.OUT)
    set_led_color((255,255,255,255))
    while True:
        color_ctrl = adc_color_ctrl.read_u16()/U16_MAX
        brightness_ctrl = adc_brightness_ctrl.read_u16()/U16_MAX
        
        # print(f"color_ctrl={color_ctrl:.2f}\tbrightness_ctrl={brightness_ctrl:.2f}")
        update_leds(color_ctrl, brightness_ctrl)
        pin.toggle()



def update_leds(color_ctrl, brightness_ctrl):
    """
    @brief Updates the illumination LEDs with the specified values.

    @param[in] color_ctrl Normalized color value (0-1.0).
    @param[in] brightness_ctrl Normalized brightness value (0-1.0).
    """

    color = (255, 255, 255, 255) # default to white if color_ctrl is below ADC_DEADBAND

    if color_ctrl > ADC_DEADBAND:
        color_ctrl = (color_ctrl-ADC_DEADBAND) / (1-ADC_DEADBAND) # re-normalize color control
        if (color_ctrl < (1/3)):
            # Blend R and B
            color = ((1-3*color_ctrl), 0.0, 3*color_ctrl, 0.0)
        elif (color_ctrl < (2/3)):
            # Blend G and B
            color = (0.0, (color_ctrl-(1/3))*3, (1-(color_ctrl-(1/3))*3), 0.0)
        else:
            # Blend R and G
            color = ((color_ctrl-(2/3))*3, (1-(color_ctrl-(2/3))*3), 0.0, 0.0)
        color = (255*color[0], 255*color[1], 255*color[2], 255*color[3])

    print(f"color_ctrl={color_ctrl:.2f}\tcolor=({color[0]:.2f},\t{color[1]:.2f},\t{color[2]:.2f},\t{color[3]:.2f})")
    if brightness_ctrl < ADC_DEADBAND:
            brightness_ctrl = 0.0

    set_led_color((math.floor(color[0]*brightness_ctrl),math.floor(color[1]*brightness_ctrl),math.floor(color[2]*brightness_ctrl),math.floor(color[3]*brightness_ctrl)))

def set_led_color(color):
    """
    @brief Sets the color of all neopixels.
    @param[in] color Four-element tuple with values [R,G,B,Y]
    """
    for i in range(PIXELS_PER_STRIP):
        np_left[i] = color
        np_right[i] = color
    np_left.write()
    np_right.write()

if __name__ == "__main__":
    main()