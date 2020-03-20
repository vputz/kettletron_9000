import time
import board
from adafruit_onewire.bus import OneWireBus
from adafruit_ds18x20 import DS18X20
from simple_pid import PID

# ds18b20 code is from https://learn.adafruit.com/using-ds18b20-temperature-sensor-with-circuitpython/circuitpython
# D4 is top, D3 is bottom, https://learn.adafruit.com/adafruit-pyportal/pinouts
ow_bus = OneWireBus(board.D4)
ds18 = DS18X20(ow_bus, ow_bus.scan()[0])
ds18.resolution = 12

# We'll just set these here; it would be better to read them
# from a file and / or store the settings with some sort of GUI


def f_from_c(c: float) -> float:
    "Convert centigrade to fahrenheit for primitive countries"
    return (c*9.0/5.0)+32


pid = PID(Kp=5.0,  # Proportional constant
          Ki=0.1,  # Integral constant
          Kd=0.1,  # derivative constant
          setpoint=73.0,  # temp this is trying to set
          sample_time=1.0,  # update the output every second
          output_limits=(0, 100)  # 0 = full off, 100 = full on
          )


while True:
    try:
        # time.sleep(0.1*5)
        value = f_from_c(ds18.temperature)  # read_temperature()
        power = pid(value)
        print("Temp: ",value, ", Pwr: ", power)
    except RuntimeError as e:
        print("Some error occured, retrying! -", e)
