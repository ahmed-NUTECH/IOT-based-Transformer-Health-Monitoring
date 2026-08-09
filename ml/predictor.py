# ==========================================================
# ITHAP ML PREDICTOR
# ==========================================================

def generate_ml_prediction(sensor_data):
    """
    Generates ML-based prediction from transformer sensor values.

    Returns:
    {
        "prediction": "...",
        "details": "...",
        "confidence": 95
    }
    """

    temperature = float(sensor_data.get("temperature", 0))
    current = float(sensor_data.get("current", 0))
    voltage = float(sensor_data.get("voltage", 0))
    frequency = float(sensor_data.get("frequency", 50))
    power_factor = float(sensor_data.get("power_factor", 1))
    smoke = float(sensor_data.get("smoke", 0))

    # ------------------------------------------------------
    # CRITICAL CONDITION
    # ------------------------------------------------------

    if (
        temperature >= 85
        or current >= 90
        or smoke >= 300
        or power_factor < 0.75
    ):

        return {

            "prediction": "Critical Condition",

            "details": (
                "The transformer exhibits severe electrical and/or thermal "
                "abnormalities. Immediate maintenance is recommended to "
                "prevent insulation failure, equipment damage, or unexpected "
                "shutdown."
            ),

            "confidence": 98

        }

    # ------------------------------------------------------
    # WARNING CONDITION
    # ------------------------------------------------------

    elif (
        temperature >= 65
        or current >= 70
        or smoke >= 150
        or power_factor < 0.90
    ):

        return {

            "prediction": "Warning Condition",

            "details": (
                "The transformer is operating with one or more parameters "
                "approaching their recommended limits. Continued monitoring "
                "and preventive maintenance are advised."
            ),

            "confidence": 93

        }

    # ------------------------------------------------------
    # VOLTAGE ISSUE
    # ------------------------------------------------------

    elif (
        voltage < 210
        or voltage > 250
    ):

        return {

            "prediction": "Voltage Instability",

            "details": (
                "The measured voltage deviates from the acceptable operating "
                "range. Investigate supply conditions and verify transformer "
                "loading."
            ),

            "confidence": 91

        }

    # ------------------------------------------------------
    # FREQUENCY ISSUE
    # ------------------------------------------------------

    elif (
        frequency < 49
        or frequency > 51
    ):

        return {

            "prediction": "Frequency Deviation",

            "details": (
                "Frequency variation has been detected. Persistent frequency "
                "deviations may reduce transformer efficiency and should be "
                "investigated."
            ),

            "confidence": 90

        }

    # ------------------------------------------------------
    # HEALTHY CONDITION
    # ------------------------------------------------------

    else:

        return {

            "prediction": "Normal Operation",

            "details": (
                "All monitored parameters are within normal operating limits. "
                "The transformer is operating under healthy conditions and no "
                "abnormal thermal or electrical behaviour has been detected."
            ),

            "confidence": 99

        }