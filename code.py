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
        #give 3 seconds to let sensor sit on display
        time.sleep(3)
        
        #evaluate average luminance, ideally measures black level
        #TODO: need to determine effective sampling rate. ALS-PT19 rise/fall time is .11 and .22 ms respectively (idk what that means)
        start_calibration_timestamp = time.monotonic()
        initial_sensorvalue = 0.0
        n = 0
        while (time.monotonic() - start_calibration_timestamp <= 3.0):
            initial_sensorvalue += light_sensor.value
            n += 1
        initial_sensorvalue = initial_sensorvalue / n

        average_latency = 0.0
        num_runs = 50
        num_miss = 0
        
        for i in range(num_runs):
            start_test_timestamp = time.monotonic()
            mouse.press(Mouse.LEFT_BUTTON)
            time.sleep(0.01)
            mouse.release(Mouse.LEFT_BUTTON)
            #gtg2% question mark?
            #might need to clamp sampling frequency
            while (time.monotonic() - start_test_timestamp <= 0.25 and light_sensor.value <= initial_sensorvalue + 0.02 * initial_sensorvalue):
                continue
            latency = (time.monotonic() - start_test_timestamp) * 1000
            if latency >= 0.25:
                #ignore
                num_miss += 1
                continue
            else:
                average_latency += latency
            time.sleep(0.5)
        
        print("Average latency over all runs:")
        print(average_latency / (num_runs - num_miss)
    else:
        led.value = True
    
