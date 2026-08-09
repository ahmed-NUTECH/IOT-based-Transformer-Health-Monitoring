# ==========================================================
# IoT-Based Distribution Transformer
# Sensor Reader - Simulation Mode
#
# Raspberry Pi 4
# DS18B20 + ACS712 + MQ-2
#
# CURRENTLY:
# Hardware is not connected.
# This file simulates sensor readings and automatically
# updates Data/sensor.json.
#
# LATER:
# Replace the simulated sensor functions with the actual
# Raspberry Pi GPIO / ADC sensor code.
# ==========================================================

import os
import json
import time
import random
from datetime import datetime


# ==========================================================
# PROJECT PATH
# ==========================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

DATA_DIR = os.path.join(
    BASE_DIR,
    "Data"
)

SENSOR_FILE = os.path.join(
    DATA_DIR,
    "sensor.json"
)


# ==========================================================
# CREATE DATA FOLDER
# ==========================================================

os.makedirs(
    DATA_DIR,
    exist_ok=True
)


# ==========================================================
# TRANSFORMER SETTINGS
# ==========================================================

TRANSFORMER_TYPE = "Distribution Transformer"

RATED_CURRENT = 5

VOLTAGE = 230

FREQUENCY = 50

POWER_FACTOR = 0.96


# ==========================================================
# SIMULATED DS18B20
# ==========================================================

def read_temperature():

    """
    Simulates DS18B20 temperature.

    Later this function will read the
    real DS18B20 sensor connected to Raspberry Pi.
    """

    temperature = random.uniform(
        20,
        65
    )

    return round(
        temperature,
        1
    )


# ==========================================================
# SIMULATED ACS712
# ==========================================================

def read_current():

    """
    Simulates ACS712 current.

    Later this function will read ACS712
    through an ADC such as ADS1115/MCP3008.
    """

    current = random.uniform(
        1,
        6
    )

    return round(
        current,
        2
    )


# ==========================================================
# SIMULATED MQ-2
# ==========================================================

def read_smoke():

    """
    Simulates MQ-2 smoke detection.

    Returns:
        Safe
        Smoke Detected
    """

    # Mostly Safe during normal operation

    random_value = random.random()

    if random_value < 0.90:

        return "Safe"

    else:

        return "Smoke Detected"


# ==========================================================
# VOLTAGE
# ==========================================================

def read_voltage():

    """
    Currently using the expected transformer voltage.

    Later this can be replaced by an actual
    voltage measurement system.
    """

    return VOLTAGE


# ==========================================================
# FREQUENCY
# ==========================================================

def read_frequency():

    return FREQUENCY


# ==========================================================
# POWER FACTOR
# ==========================================================

def read_power_factor():

    return POWER_FACTOR


# ==========================================================
# BUILD SENSOR DATA
# ==========================================================

def build_sensor_data():

    temperature = read_temperature()

    current = read_current()

    voltage = read_voltage()

    frequency = read_frequency()

    power_factor = read_power_factor()

    smoke = read_smoke()


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
            voltage,

        "frequency":
            frequency,

        "power_factor":
            power_factor,

        "smoke":
            smoke,

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

    try:

        with open(
            SENSOR_FILE,
            "w"
        ) as file:

            json.dump(
                sensor_data,
                file,
                indent=4
            )

        print(
            "Sensor data updated:"
        )

        print(
            sensor_data
        )

    except Exception as error:

        print(
            "ERROR writing sensor.json:"
        )

        print(
            error
        )


# ==========================================================
# MAIN SENSOR LOOP
# ==========================================================

def main():

    print("=" * 60)

    print(
        "IoT TRANSFORMER SENSOR READER"
    )

    print(
        "SIMULATION MODE"
    )

    print(
        "Hardware is not connected."
    )

    print(
        "Updating sensor.json automatically..."
    )

    print(
        "Sensor file:"
    )

    print(
        SENSOR_FILE
    )

    print("=" * 60)


    while True:

        try:

            # ==========================================
            # READ SENSORS
            # ==========================================

            sensor_data = build_sensor_data()


            # ==========================================
            # WRITE DATA
            # ==========================================

            write_sensor_data(
                sensor_data
            )


            # ==========================================
            # WAIT
            # ==========================================

            time.sleep(2)


        except KeyboardInterrupt:

            print(
                "\nSensor reader stopped."
            )

            break


        except Exception as error:

            print(
                "Sensor reader error:"
            )

            print(
                error
            )

            time.sleep(2)


# ==========================================================
# START
# ==========================================================

if __name__ == "__main__":

    main()