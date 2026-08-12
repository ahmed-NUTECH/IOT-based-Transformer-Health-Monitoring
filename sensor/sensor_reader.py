# ==========================================================
# IoT-Based Distribution Transformer
# REAL SENSOR READER
#
# Raspberry Pi 4
#
# DS18B20  -> Temperature
# ADS1115 A1 -> MQ-2
# ADS1115 A2 -> ACS712-5A
# SH1106 OLED -> Display
#
# Output:
# Data/sensor.json
# ==========================================================

import time
import json
from datetime import datetime
from pathlib import Path

from smbus2 import SMBus

from luma.core.interface.serial import i2c
from luma.oled.device import sh1106

from PIL import Image, ImageDraw, ImageFont


# ==========================================================
# PROJECT PATH
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "Data"

SENSOR_FILE = DATA_DIR / "sensor.json"

DATA_DIR.mkdir(exist_ok=True)


# ==========================================================
# TRANSFORMER CONFIGURATION
# ==========================================================

TRANSFORMER_TYPE = "Distribution Transformer"

RATED_CURRENT = 5.0

# These are currently fixed/reference values.
# We do NOT have voltage/frequency/power-factor sensors
# in the hardware configuration you provided.

VOLTAGE = 230.0

FREQUENCY = 50.0

POWER_FACTOR = 0.96


# ==========================================================
# I2C CONFIGURATION
# ==========================================================

OLED_ADDRESS = 0x3C

ADS_ADDRESS = 0x48

I2C_BUS = 1

ADS_CHANNEL_SMOKE = 1

ADS_CHANNEL_CURRENT = 2


# ==========================================================
# ACS712 CONFIGURATION
# ==========================================================

# ACS712-5A sensitivity:
# approximately 185 mV/A

ACS712_SENSITIVITY = 0.185

ACS712_ZERO_CURRENT_VOLTAGE = 2.5


# ==========================================================
# ADS1115 SETUP
# ==========================================================

bus = SMBus(I2C_BUS)


# ==========================================================
# OLED SETUP
# ==========================================================

serial = i2c(
    port=I2C_BUS,
    address=OLED_ADDRESS
)

oled = sh1106(serial)

font = ImageFont.load_default()


def oled_display(lines):

    image = Image.new(
        "1",
        oled.size
    )

    draw = ImageDraw.Draw(image)

    y = 0

    for line in lines:

        draw.text(
            (0, y),
            str(line),
            font=font,
            fill=255
        )

        y += 12

    oled.display(image)


# ==========================================================
# DS18B20 TEMPERATURE
# ==========================================================

def read_temperature():

    sensors = list(
        Path("/sys/bus/w1/devices").glob("28-*")
    )

    if not sensors:

        raise RuntimeError(
            "DS18B20 sensor not found"
        )

    sensor_file = sensors[0] / "w1_slave"

    data = sensor_file.read_text().splitlines()

    if not data:

        raise RuntimeError(
            "DS18B20 returned no data"
        )

    if "YES" not in data[0]:

        raise RuntimeError(
            "DS18B20 CRC check failed"
        )

    if "t=" not in data[1]:

        raise RuntimeError(
            "Invalid DS18B20 temperature data"
        )

    temperature = int(
        data[1].split("t=")[1]
    ) / 1000.0

    return round(
        temperature,
        2
    )


# ==========================================================
# ADS1115
# ==========================================================

def read_ads(channel):

    if channel not in [0, 1, 2, 3]:

        raise ValueError(
            "ADS1115 channel must be 0-3"
        )

    config_reg = 0x01

    conversion_reg = 0x00

    mux = {
        0: 0x4000,
        1: 0x5000,
        2: 0x6000,
        3: 0x7000
    }

    config = (
        0x8000 |
        mux[channel] |
        0x0200 |
        0x0100 |
        0x00E0 |
        0x0003
    )

    bus.write_i2c_block_data(
        ADS_ADDRESS,
        config_reg,
        [
            (config >> 8) & 0xFF,
            config & 0xFF
        ]
    )

    time.sleep(0.01)

    data = bus.read_i2c_block_data(
        ADS_ADDRESS,
        conversion_reg,
        2
    )

    value = (
        (data[0] << 8)
        | data[1]
    )

    if value > 32767:

        value -= 65536

    voltage = (
        value * 4.096
    ) / 32768

    return round(
        voltage,
        3
    )


# ==========================================================
# MQ-2
# ==========================================================

def read_smoke_voltage():

    return read_ads(
        ADS_CHANNEL_SMOKE
    )


def smoke_status(smoke_voltage):

    # For now we use the voltage as a simple
    # threshold-based indicator.
    #
    # IMPORTANT:
    # MQ-2 requires calibration for meaningful
    # gas concentration measurements.

    if smoke_voltage >= 2.5:

        return "Smoke Detected"

    return "Safe"


# ==========================================================
# ACS712 CURRENT
# ==========================================================

def read_current():

    voltage = read_ads(
        ADS_CHANNEL_CURRENT
    )

    current = (
        voltage -
        ACS712_ZERO_CURRENT_VOLTAGE
    ) / ACS712_SENSITIVITY

    # Remove very small zero-current noise

    if abs(current) < 0.05:

        current = 0.0

    return round(
        abs(current),
        2
    )


# ==========================================================
# BUILD SENSOR DATA
# ==========================================================

def build_sensor_data():

    temperature = read_temperature()

    smoke_voltage = read_smoke_voltage()

    current = read_current()

    smoke = smoke_status(
        smoke_voltage
    )

    sensor_data = {

        "transformer_type":
            TRANSFORMER_TYPE,

        "temperature":
            temperature,

        "current":
            current,

        "rated_current":
            RATED_CURRENT,

        "voltage":
            VOLTAGE,

        "frequency":
            FREQUENCY,

        "power_factor":
            POWER_FACTOR,

        "smoke":
            smoke,

        "smoke_voltage":
            smoke_voltage,

        "time":
            datetime.now().strftime(
                "%d-%m-%Y %H:%M:%S"
            )

    }

    return sensor_data


# ==========================================================
# WRITE SENSOR JSON
# ==========================================================

def write_sensor_data(sensor_data):

    temporary_file = SENSOR_FILE.with_suffix(
        ".tmp"
    )

    with open(
        temporary_file,
        "w"
    ) as file:

        json.dump(
            sensor_data,
            file,
            indent=4
        )

    temporary_file.replace(
        SENSOR_FILE
    )


# ==========================================================
# MAIN
# ==========================================================

def main():

    print("=" * 60)

    print(
        "IoT TRANSFORMER SENSOR READER"
    )

    print(
        "REAL HARDWARE MODE"
    )

    print(
        "DS18B20 + ADS1115 + MQ-2 + ACS712"
    )

    print(
        "Sensor file:"
    )

    print(
        SENSOR_FILE
    )

    print("=" * 60)


    oled_display(
        [
            "Transformer",
            "Monitor",
            "",
            "Starting..."
        ]
    )

    time.sleep(2)


    while True:

        try:

            # ==========================================
            # READ REAL SENSORS
            # ==========================================

            sensor_data = build_sensor_data()


            # ==========================================
            # SAVE JSON
            # ==========================================

            write_sensor_data(
                sensor_data
            )


            # ==========================================
            # OLED
            # ==========================================

            oled_display(
                [
                    f"Temp: {sensor_data['temperature']} C",

                    f"Curr: {sensor_data['current']} A",

                    f"Smoke: {sensor_data['smoke']}",

                    f"MQ2: {sensor_data['smoke_voltage']} V"
                ]
            )


            # ==========================================
            # TERMINAL
            # ==========================================

            print("----------------------------------------")

            print(
                "Temperature:",
                sensor_data["temperature"],
                "C"
            )

            print(
                "Current:",
                sensor_data["current"],
                "A"
            )

            print(
                "MQ-2:",
                sensor_data["smoke_voltage"],
                "V"
            )

            print(
                "Smoke:",
                sensor_data["smoke"]
            )

            print(
                "JSON:",
                SENSOR_FILE
            )


            # ==========================================
            # WAIT
            # ==========================================

            time.sleep(2)


        except KeyboardInterrupt:

            print(
                "\nSensor reader stopped."
            )

            oled_display(
                [
                    "Transformer",
                    "Monitor",
                    "",
                    "Stopped"
                ]
            )

            break


        except Exception as error:

            print(
                "SENSOR ERROR:",
                error
            )

            oled_display(
                [
                    "Sensor Error",
                    "",
                    str(error)[:18]
                ]
            )

            time.sleep(2)


# ==========================================================
# START
# ==========================================================

if __name__ == "__main__":

    main()