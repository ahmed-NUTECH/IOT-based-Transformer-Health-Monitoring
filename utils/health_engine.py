# ==================================================
# IoT-Based Distribution Transformer
# Condition Monitoring System
# HEALTH ENGINE
# ==================================================

import os
import json

# ==================================================
# FILE PATH
# ==================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

SENSOR_FILE = os.path.join(
    BASE_DIR,
    "Data",
    "sensor.json"
)

# ==================================================
# TRANSFORMER LIMITS
# ==================================================

TRANSFORMER_LIMITS = {

    "Distribution Transformer": {
        "temp_warning": 60,
        "temp_critical": 80
    },

    "Power Transformer": {
        "temp_warning": 65,
        "temp_critical": 90
    },

    "Step-Up Transformer": {
        "temp_warning": 65,
        "temp_critical": 90
    },

    "Step-Down Transformer": {
        "temp_warning": 60,
        "temp_critical": 80
    },

    "Single Phase Transformer": {
        "temp_warning": 55,
        "temp_critical": 75
    },

    "Three Phase Transformer": {
        "temp_warning": 65,
        "temp_critical": 85
    }

}

# ==================================================
# LOAD SENSOR DATA
# ==================================================

def load_sensor_data():

    try:

        with open(SENSOR_FILE, "r") as file:
            return json.load(file)

    except Exception:

        return {
            "transformer_type": "Distribution Transformer",
            "temperature": 0,
            "current": 0,
            "rated_current": 4.8,
            "voltage": 230,
            "frequency": 50,
            "power_factor": 1.0,
            "smoke": "Safe"
        }

# ==================================================
# HEALTH ENGINE
# ==================================================

def calculate_health(data=None):

    if data is None:
        data = load_sensor_data()

    transformer = data.get(
        "transformer_type",
        "Distribution Transformer"
    )

    limits = TRANSFORMER_LIMITS.get(
        transformer,
        TRANSFORMER_LIMITS["Distribution Transformer"]
    )

    temperature = float(data.get("temperature", 0))
    current = float(data.get("current", 0))
    rated_current = float(data.get("rated_current", 5))
    voltage = float(data.get("voltage", 230))
    frequency = float(data.get("frequency", 50))
    power_factor = float(data.get("power_factor", 1))
    smoke = str(data.get("smoke", "Safe")).lower()

    if rated_current <= 0:
        rated_current = 5

    loading = (current / rated_current) * 100

    health = "Healthy"
    reasons = []

    # ==========================================
    # TEMPERATURE
    # ==========================================

    if temperature >= limits["temp_critical"]:

        health = "Critical"

        reasons.append(
            "Critical transformer temperature detected."
        )

    elif temperature >= limits["temp_warning"]:

        health = "Warning"

        reasons.append(
            "Transformer temperature is above the normal operating range."
        )

    # ==========================================
    # CURRENT
    # ==========================================

    if loading >= 120:

        health = "Critical"

        reasons.append(
            f"Transformer overloaded ({loading:.1f}% loading)."
        )

    elif loading >= 100:

        if health != "Critical":
            health = "Warning"

        reasons.append(
            f"Transformer current is above the rated limit ({loading:.1f}% loading)."
        )

    # ==========================================
    # VOLTAGE
    # ==========================================

    if voltage < 210 or voltage > 250:

        health = "Critical"

        reasons.append(
            "Voltage outside safe operating range."
        )

    elif voltage < 220 or voltage > 240:

        if health != "Critical":
            health = "Warning"

        reasons.append(
            "Voltage variation detected."
        )

    # ==========================================
    # FREQUENCY
    # ==========================================

    if frequency < 49 or frequency > 51:

        health = "Critical"

        reasons.append(
            "Frequency outside safe operating range."
        )

    elif frequency < 49.5 or frequency > 50.5:

        if health != "Critical":
            health = "Warning"

        reasons.append(
            "Frequency deviation detected."
        )

    # ==========================================
    # POWER FACTOR
    # ==========================================

    if power_factor < 0.80:

        health = "Critical"

        reasons.append(
            "Very low power factor."
        )

    elif power_factor < 0.90:

        if health != "Critical":
            health = "Warning"

        reasons.append(
            "Power factor below recommended value."
        )

    # ==========================================
    # SMOKE
    # ==========================================

    if smoke in ["critical", "danger", "detected"]:

        health = "Critical"

        reasons.append(
            "Smoke detected. Possible transformer fault."
        )

    elif smoke in ["warning"]:

        if health != "Critical":
            health = "Warning"

        reasons.append(
            "Smoke warning detected."
        )

    # ==========================================
    # RISK
    # ==========================================

    if health == "Healthy":

        risk = "Low Risk"

        actions = [
            "Continue normal transformer operation.",
            "Perform routine inspection.",
            "Monitor sensor values."
        ]

    elif health == "Warning":

        risk = "Medium Risk"

        actions = [
            "Schedule preventive maintenance.",
            "Inspect transformer cooling.",
            "Reduce loading if necessary."
        ]

    else:

        risk = "High Risk"

        actions = [
            "Reduce transformer loading immediately.",
            "Inspect transformer condition.",
            "Check insulation and cooling system."
        ]

    return {
        **data,

        "loading_percentage": round(
            loading,
            2
        ),

        "health": health,

        "reason": (
            " ".join(reasons)
            if reasons
            else
            "Transformer operating normally."
        ),

        "risk_assessment": risk,

        "recommended_actions": actions
    }