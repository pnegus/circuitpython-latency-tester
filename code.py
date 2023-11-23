# Write your code here :-)
import board
import digitalio
from digitalio import DigitalInOut, Direction, Pull
from analogio import AnalogIn
import time
from adafruit_hid.mouse import Mouse
import usb_hid

light_sensor = AnalogIn(board.D11)
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

btn = DigitalInOut(board.BUTTON)
btn.direction = Direction.INPUT
btn.pull = Pull.UP

mouse = Mouse(usb_hid.devices)

while True:
    if not btn.value:
        led.value = False
        start_calibration_timestamp = time.monotonic()
        
        #rudimentary calibration
        initial_sensorvalue = 0.0
        n = 0
        largest = 0
        while (time.monotonic() - start_calibration_timestamp <= 3.0):
            initial_sensorvalue += light_sensor.value
            largest = max(largest, light_sensor.value)
            n += 1
        initial_sensorvalue = initial_sensorvalue / n
        max_deviation = largest - initial_sensorvalue
        print("Max calibration deviation: ")
        print(max_deviation)
        
        average_latency = 0.0
        num_runs = 100
        
        for i in range(num_runs):
            start_test_timestamp = time.monotonic()
            mouse.press(Mouse.LEFT_BUTTON)
            time.sleep(0.01)
            mouse.release(Mouse.LEFT_BUTTON)
            while (time.monotonic() - start_test_timestamp <= 0.5 and light_sensor.value <= initial_sensorvalue + max_deviation * 1.25):
                continue;
            latency = (time.monotonic() - start_test_timestamp) * 1000
            average_latency += latency
            time.sleep(0.5)
        
        print("Average latency over all runs:")
        print(average_latency / num_runs)
    else:
        led.value = True
    
