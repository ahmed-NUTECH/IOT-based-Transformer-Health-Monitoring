# ==================================================
# AI TRANSFORMER REPORT ENGINE
# ==================================================

def generate_complete_report(sensor_data, transformer_type, health_result):

    # -----------------------------------
    # Convert all values to numeric
    # -----------------------------------

    temperature = float(sensor_data.get("temperature", 0))
    current = float(sensor_data.get("current", 0))
    voltage = float(sensor_data.get("voltage", 0))
    frequency = float(sensor_data.get("frequency", 0))
    power_factor = float(sensor_data.get("power_factor", 0))
    smoke = str(sensor_data.get("smoke","Safe")).lower()

    health = health_result.get(
        "health",
        "Healthy"
    )

    # -----------------------------------
    # Condition Analysis
    # -----------------------------------

    if health == "Critical":

        condition = "Critical operating condition"

        prediction = (
            "Transformer operation shows abnormal "
            "parameters requiring immediate inspection."
        )

        explanation = (
            "One or more monitored parameters have "
            "exceeded safe operating limits. "
            "Thermal or electrical stress may damage "
            "transformer components."
        )

        risk = "High Risk"

        actions = [
            "Inspect transformer immediately.",
            "Check cooling system and insulation condition.",
            "Reduce load if necessary.",
            "Perform detailed maintenance inspection."
        ]

    elif health == "Warning":

        condition = "Warning operating condition"

        prediction = (
            "Transformer parameters indicate early "
            "signs of abnormal behaviour."
        )

        explanation = (
            "Some parameters are approaching "
            "recommended operating limits."
        )

        risk = "Medium Risk"

        actions = [
            "Monitor transformer continuously.",
            "Inspect temperature and loading.",
            "Schedule preventive maintenance."
        ]

    else:

        condition = "Healthy operating condition"

        prediction = (
            "All monitored parameters are within "
            "normal operating limits."
        )

        explanation = (
            "The transformer parameters are within "
            "acceptable operating limits. "
            "No abnormal thermal or electrical "
            "behaviour has been detected."
        )

        risk = "Low Risk"

        actions = [
            "Continue normal transformer operation.",
            "Perform routine inspection as scheduled.",
            "Maintain regular monitoring."
        ]

    return {

        "transformer_type": transformer_type,

        "condition": condition,

        "prediction": prediction,

        "explanation": explanation,

        "risk": risk,

        "actions": actions,

        "parameters": {

            "Temperature": temperature,
            "Current": current,
            "Voltage": voltage,
            "Frequency": frequency,
            "Power Factor": power_factor,
            "Smoke": smoke

        }

    }


# ==================================================
# ML PREDICTION FUNCTION
# ==================================================

def generate_ml_prediction(sensor_data):

    # -----------------------------------
    # Convert strings to float
    # -----------------------------------

    temperature = float(sensor_data.get("temperature", 0))
    current = float(sensor_data.get("current", 0))
    smoke = str(sensor_data.get("smoke","Safe"))

    # -----------------------------------
    # Prediction Logic
    # -----------------------------------

    if temperature >= 80 or current >= 100 or smoke >= "danger":

        return {

            "prediction": "Critical condition expected",

            "failure_probability": "High",

            "remaining_life": "Immediate inspection required"

        }

    elif temperature >= 60 or current >= 80 or smoke >= "warning":

        return {

            "prediction": "Degradation detected",

            "failure_probability": "Medium",

            "remaining_life": "Maintenance recommended"

        }

    else:

        return {

            "prediction": "Normal operation",

            "failure_probability": "Low",

            "remaining_life": "Transformer operating normally"

        }