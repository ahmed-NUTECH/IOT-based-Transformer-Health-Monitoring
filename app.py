# ==================================================
# IoT-Based Distribution Transformer
# Condition Monitoring System
#
# Developed By
# Muhammad Ahmed Khokhar
# Muhiba Shakeel
# Kiran Batool
# ==================================================

from flask import (
    Flask,
    render_template,
    jsonify,
    send_file
)

import os
import io
import csv
import json

from datetime import datetime

# ==================================================
# HEALTH ENGINE
# ==================================================

from utils.health_engine import (
    calculate_health,
    TRANSFORMER_LIMITS
)

# ==================================================
# AI ENGINE
# ==================================================

from utils.ai_engine import (
    generate_complete_report,
    generate_ml_prediction
)

# ==================================================
# REPORTLAB
# ==================================================

from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import (
    getSampleStyleSheet
)

from reportlab.lib.pagesizes import A4
from reportlab.lib.enums import TA_CENTER
from reportlab.lib import colors

# ==================================================
# FLASK CONFIGURATION
# ==================================================

app = Flask(__name__)

# ==================================================
# PROJECT PATHS
# ==================================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

DATA_DIR = os.path.join(
    BASE_DIR,
    "Data"
)

SENSOR_FILE = os.path.join(
    DATA_DIR,
    "sensor.json"
)

HISTORY_FILE = os.path.join(
    DATA_DIR,
    "history.json"
)

# ==================================================
# GLOBAL REPORT STORAGE
# ==================================================

latest_report = None
# ==================================================
# LOAD SENSOR DATA
# ==================================================

def load_sensor_data():

    try:

        with open(SENSOR_FILE, "r") as file:

            return json.load(file)

    except Exception as e:

        print("Sensor Load Error:", e)

        return {

            "transformer_type": "Distribution Transformer",

            "temperature": 0,

            "current": 0,

            "rated_current": 1,

            "voltage": 230,

            "frequency": 50,

            "power_factor": 1.0,

            "smoke": "Safe",

            "health": "Healthy",

            "reason": "Transformer operating normally.",

            "risk_assessment": "Low Risk",

            "recommended_actions": [

                "Continue normal operation.",

                "Perform routine inspection.",

                "Monitor sensor values."

            ]

        }
# ==================================================
# LOAD HISTORY
# ==================================================

def load_history():

    try:

        with open(HISTORY_FILE, "r") as file:

            return json.load(file)

    except:

        return []
# ==================================================
# SAVE HISTORY
# ==================================================

def save_history(sensor_data):

    history = load_history()

    sensor_data["time"] = datetime.now().strftime(
        "%d-%m-%Y %H:%M:%S"
    )

    history.append(sensor_data)

    history = history[-100:]

    with open(HISTORY_FILE, "w") as file:

        json.dump(
            history,
            file,
            indent=4
        )
# ==================================================
# HISTORY STATISTICS
# ==================================================

def history_statistics():

    history = load_history()

    if len(history) == 0:

        return {

            "max_temperature": 0,

            "avg_temperature": 0,

            "max_current": 0,

            "avg_current": 0

        }

    temperatures = [

        float(item.get("temperature", 0))

        for item in history

    ]

    currents = [

        float(item.get("current", 0))

        for item in history

    ]

    return {

        "max_temperature": max(temperatures),

        "avg_temperature": round(

            sum(temperatures) / len(temperatures),

            2

        ),

        "max_current": max(currents),

        "avg_current": round(

            sum(currents) / len(currents),

            2

        )

    }
# ==================================================
# BUILD COMPLETE REPORT
# ==================================================

def build_complete_report():

    global latest_report

    sensor_data = calculate_health()

    transformer_type = sensor_data.get(

        "transformer_type",

        "Distribution Transformer"

    )

    ai_report = generate_complete_report(

        sensor_data,

        transformer_type,

        sensor_data

    )

    ml_prediction = generate_ml_prediction(

        sensor_data

    )

    latest_report = {

        "sensor_data": sensor_data,

        "health": sensor_data,

        "ai_report": ai_report,

        "ml_prediction": ml_prediction,

        "statistics": history_statistics(),

        "generated_time": datetime.now().strftime(

            "%d-%m-%Y %H:%M:%S"

        )

    }

    return latest_report
# ==================================================
# HOME
# ==================================================

@app.route("/")
def home():

    return render_template(

        "index.html",

        active_page="home"

    )


# ==================================================
# LIVE DASHBOARD
# ==================================================

@app.route("/dashboard")
def dashboard():

    return render_template(

        "dashboard.html",

        active_page="dashboard"

    )


# ==================================================
# HEALTH PAGE
# ==================================================

@app.route("/health")
def health():

    return render_template(

        "health.html",

        active_page="health"

    )


# ==================================================
# ALERT PAGE
# ==================================================

@app.route("/alerts")
def alerts():

    return render_template(

        "alerts.html",

        active_page="alerts"

    )


# ==================================================
# CONTROL PANEL
# ==================================================

@app.route("/control")
def control():

    return render_template(

        "control.html",

        active_page="control"

    )


# ==================================================
# REPORT PAGE
# ==================================================

@app.route("/report")
def report():

    return render_template(

        "report.html",

        active_page="report"

    )


# ==================================================
# ABOUT PAGE
# ==================================================

@app.route("/about")
def about():

    return render_template(

        "about.html"

    )

# ==================================================
# LIVE SENSOR DATA API
# ==================================================

@app.route("/api/sensor-data")
def api_sensor_data():

    try:

        # ------------------------------------------
        # LOAD CURRENT SENSOR.JSON
        # ------------------------------------------

        sensor_data = load_sensor_data()

        print("====================================")
        print("SENSOR FILE:")
        print(SENSOR_FILE)
        print("CURRENT DATA:")
        print(sensor_data)
        print("====================================")


        # ------------------------------------------
        # CALCULATE HEALTH
        # ------------------------------------------

        health_result = calculate_health()


        # ------------------------------------------
        # ADD HEALTH INFORMATION
        # ------------------------------------------

        sensor_data["health"] = health_result.get(
            "health",
            "Healthy"
        )

        sensor_data["reason"] = health_result.get(
            "reason",
            ""
        )

        sensor_data["risk_assessment"] = health_result.get(
            "risk_assessment",
            "Low Risk"
        )

        sensor_data["recommended_actions"] = health_result.get(
            "recommended_actions",
            []
        )


        # ------------------------------------------
        # SAVE HISTORY
        # ------------------------------------------

        save_history(
            sensor_data.copy()
        )


        # ------------------------------------------
        # RETURN JSON
        # ------------------------------------------

        return jsonify(sensor_data)


    except Exception as e:

        print(
            "SENSOR API ERROR:",
            str(e)
        )

        return jsonify({

            "status": "error",

            "message": str(e)

        }), 500

# ==================================================
# GENERATE COMPLETE REPORT
# ==================================================

@app.route("/api/generate-report")
def generate_report():

    try:

        report = build_complete_report()

        return jsonify({

            "status": "success",

            "report": report

        })

    except Exception as e:

        return jsonify({

            "status": "error",

            "message": str(e)

        }), 500


# ==================================================
# CURRENT REPORT
# ==================================================

@app.route("/api/current-report")
def current_report():

    global latest_report

    if latest_report is None:

        latest_report = build_complete_report()

    return jsonify({

        "status": "success",

        "report": latest_report

    })


# ==================================================
# ALERT API
# ==================================================

@app.route("/api/alerts")
def api_alerts():

    sensor = calculate_health()

    alerts = []

    if sensor["health"] == "Warning":

        alerts.append({

            "time":
            datetime.now().strftime("%H:%M:%S"),

            "message":
            sensor["reason"],

            "status":
            "Warning"

        })

    elif sensor["health"] == "Critical":

        alerts.append({

            "time":
            datetime.now().strftime("%H:%M:%S"),

            "message":
            sensor["reason"],

            "status":
            "Critical"

        })

    return jsonify(alerts)
# ==================================================
# EXPORT REPORT AS CSV
# ==================================================

@app.route("/api/export-csv")
def export_csv():

    try:

        report = build_complete_report()

        sensor = report["sensor_data"]

        output = io.StringIO()

        writer = csv.writer(output)

        writer.writerow(["Parameter", "Value"])

        writer.writerow(["Transformer Type",
                         sensor["transformer_type"]])

        writer.writerow(["Temperature",
                         sensor["temperature"]])

        writer.writerow(["Current",
                         sensor["current"]])

        writer.writerow(["Rated Current",
                         sensor["rated_current"]])

        writer.writerow(["Loading %",
                         sensor["loading_percentage"]])

        writer.writerow(["Voltage",
                         sensor["voltage"]])

        writer.writerow(["Frequency",
                         sensor["frequency"]])

        writer.writerow(["Power Factor",
                         sensor["power_factor"]])

        writer.writerow(["Smoke",
                         sensor["smoke"]])

        writer.writerow(["Health",
                         sensor["health"]])

        writer.writerow(["Reason",
                         sensor["reason"]])

        writer.writerow(["Risk",
                         sensor["risk_assessment"]])

        writer.writerow([

            "Recommended Actions",

            " | ".join(sensor["recommended_actions"])

        ])

        memory = io.BytesIO()

        memory.write(

            output.getvalue().encode("utf-8")

        )

        memory.seek(0)

        return send_file(

            memory,

            mimetype="text/csv",

            as_attachment=True,

            download_name="Transformer_Report.csv"

        )

    except Exception as e:

        return jsonify({

            "status": "error",

            "message": str(e)

        }), 500
# ==================================================
# PDF STYLES
# ==================================================

def pdf_styles():

    styles = getSampleStyleSheet()

    title = styles["Heading1"]

    title.alignment = TA_CENTER

    title.textColor = colors.HexColor("#183153")

    heading = styles["Heading2"]

    heading.textColor = colors.HexColor("#3EB489")

    body = styles["BodyText"]

    body.leading = 22

    return title, heading, body
# ==================================================
# REPORT HEADER
# ==================================================

def add_report_header(story, title):

    story.append(

        Paragraph(

            "National University of Technology (NUTECH)",

            title

        )

    )

    story.append(

        Paragraph(

            "Department of Electrical Engineering",

            getSampleStyleSheet()["Heading2"]

        )

    )

    story.append(

        Spacer(1, 15)

    )

    story.append(

        Paragraph(

            "<b>IoT-Based Distribution Transformer Condition Monitoring System</b>",

            getSampleStyleSheet()["Title"]

        )

    )

    story.append(

        Spacer(1, 20)

    )
# ==================================================
# REPORT INFORMATION TABLE
# ==================================================

def report_information(sensor):

    table = [

        [

            "Report ID",

            "ITHAP-" + datetime.now().strftime("%Y%m%d%H%M")

        ],

        [

            "Generated",

            datetime.now().strftime("%d-%m-%Y %H:%M")

        ],

        [

            "Transformer",

            sensor["transformer_type"]

        ],

        [

            "Health",

            sensor["health"]

        ]

    ]

    t = Table(

        table,

        colWidths=[170, 260]

    )

    t.setStyle(

        TableStyle([

            ("GRID", (0,0), (-1,-1), 1, colors.grey),

            ("BACKGROUND", (0,0), (0,-1),

             colors.HexColor("#183153")),

            ("TEXTCOLOR", (0,0), (0,-1),

             colors.white),

            ("BOTTOMPADDING", (0,0), (-1,-1), 8)

        ])

    )

    return t
# ==================================================
# SENSOR TABLE
# ==================================================

def sensor_table(sensor):

    rows = [

        ["Parameter","Value"],

        ["Temperature",

         f"{sensor['temperature']} °C"],

        ["Current",

         f"{sensor['current']} A"],

        ["Rated Current",

         f"{sensor['rated_current']} A"],

        ["Loading",

         f"{sensor['loading_percentage']} %"],

        ["Voltage",

         f"{sensor['voltage']} V"],

        ["Frequency",

         f"{sensor['frequency']} Hz"],

        ["Power Factor",

         sensor["power_factor"]],

        ["Smoke",

         sensor["smoke"]],

        ["Health",

         sensor["health"]],

        ["Risk",

         sensor["risk_assessment"]]

    ]

    t = Table(

        rows,

        colWidths=[180,220]

    )

    t.setStyle(

        TableStyle([

            ("GRID",(0,0),(-1,-1),1,colors.black),

            ("BACKGROUND",(0,0),(-1,0),

             colors.HexColor("#183153")),

            ("TEXTCOLOR",(0,0),(-1,0),

             colors.white),

            ("BACKGROUND",(0,1),(0,-1),

             colors.lightgrey)

        ])

    )

    return t
# ==================================================
# HISTORY STATISTICS TABLE
# ==================================================

def statistics_table(stats):

    rows = [

        ["Statistic","Value"],

        ["Maximum Temperature",

         f"{stats['max_temperature']} °C"],

        ["Average Temperature",

         f"{stats['avg_temperature']} °C"],

        ["Maximum Current",

         f"{stats['max_current']} A"],

        ["Average Current",

         f"{stats['avg_current']} A"]

    ]

    t = Table(

        rows,

        colWidths=[220,180]

    )

    t.setStyle(

        TableStyle([

            ("GRID",(0,0),(-1,-1),1,colors.black),

            ("BACKGROUND",(0,0),(-1,0),

             colors.HexColor("#3EB489")),

            ("TEXTCOLOR",(0,0),(-1,0),

             colors.white)

        ])

    )

    return t
# ==================================================
# AI SUMMARY
# ==================================================

def ai_summary(ai_report, ml_prediction):

    return f"""

    <b>AI Condition :</b><br/>

    {ai_report['condition']}<br/><br/>

    <b>Prediction :</b><br/>

    {ai_report['prediction']}<br/><br/>

    <b>Risk :</b><br/>

    {ai_report['risk']}<br/><br/>

    <b>Machine Learning :</b><br/>

    {ml_prediction['prediction']}<br/><br/>

    <b>Failure Probability :</b><br/>

    {ml_prediction['failure_probability']}<br/><br/>

    <b>Remaining Life :</b><br/>

    {ml_prediction['remaining_life']}

    """
# ==================================================
# GENERATE PDF REPORT
# ==================================================

def generate_pdf_report():

    report = build_complete_report()

    sensor = report["sensor_data"]

    stats = report["statistics"]

    ai = report["ai_report"]

    ml = report["ml_prediction"]

    buffer = io.BytesIO()

    document = SimpleDocTemplate(

        buffer,

        pagesize=A4,

        rightMargin=30,

        leftMargin=30,

        topMargin=30,

        bottomMargin=30

    )

    story = []

    title, heading, body = pdf_styles()

    # ===========================================
    # HEADER
    # ===========================================

    add_report_header(
        story,
        title
    )

    story.append(

        report_information(sensor)

    )

    story.append(

        Spacer(1, 20)

    )

    # ===========================================
    # EXECUTIVE SUMMARY
    # ===========================================

    story.append(

        Paragraph(

            "Executive Summary",

            heading

        )

    )

    summary = f"""

    This report has been automatically generated by the

    <b>IoT-Based Distribution Transformer
    Condition Monitoring System</b>.

    The monitoring platform continuously measures
    transformer temperature,
    load current,
    operating voltage,
    system frequency,
    power factor,
    and smoke level.

    Artificial Intelligence evaluates these
    measurements to determine transformer health,
    while Machine Learning predicts future
    operating behaviour.

    <br/><br/>

    <b>Current Transformer Health:</b>

    {sensor["health"]}

    <br/><br/>

    <b>Risk Assessment:</b>

    {sensor["risk_assessment"]}

    <br/><br/>

    <b>Reason:</b>

    {sensor["reason"]}

    """

    story.append(

        Paragraph(

            summary,

            body

        )

    )

    story.append(

        Spacer(1, 20)

    )

    # ===========================================
    # LIVE SENSOR INFORMATION
    # ===========================================

    story.append(

        Paragraph(

            "Live Sensor Measurements",

            heading

        )

    )

    story.append(

        sensor_table(sensor)

    )

    story.append(

        Spacer(1, 20)

    )

    # ===========================================
    # HISTORICAL STATISTICS
    # ===========================================

    story.append(

        Paragraph(

            "Historical Statistics",

            heading

        )

    )

    story.append(

        statistics_table(stats)

    )

    story.append(

        Spacer(1, 20)

    )

    # ===========================================
    # HEALTH ANALYSIS
    # ===========================================

    story.append(

        Paragraph(

            "Health Analysis",

            heading

        )

    )

    analysis = f"""

    The transformer health engine evaluates
    electrical and environmental conditions
    using multiple operating parameters.

    <br/><br/>

    Temperature :
    <b>{sensor["temperature"]} °C</b>

    <br/><br/>

    Current :
    <b>{sensor["current"]} A</b>

    <br/><br/>

    Rated Current :
    <b>{sensor["rated_current"]} A</b>

    <br/><br/>

    Transformer Loading :
    <b>{sensor["loading_percentage"]}%</b>

    <br/><br/>

    Voltage :
    <b>{sensor["voltage"]} V</b>

    <br/><br/>

    Frequency :
    <b>{sensor["frequency"]} Hz</b>

    <br/><br/>

    Power Factor :
    <b>{sensor["power_factor"]}</b>

    <br/><br/>

    Smoke Status :
    <b>{sensor["smoke"]}</b>

    <br/><br/>

    Overall Health :
    <b>{sensor["health"]}</b>

    """

    story.append(

        Paragraph(

            analysis,

            body

        )

    )

    story.append(

        Spacer(1, 20)

    )
    # ===========================================
    # AI ANALYSIS
    # ===========================================

    story.append(

        Paragraph(

            "Artificial Intelligence Analysis",

            heading

        )

    )

    story.append(

        Paragraph(

            ai_summary(

                ai,

                ml

            ),

            body

        )

    )

    story.append(

        Spacer(1,20)

    )

    # ===========================================
    # HEALTH ASSESSMENT
    # ===========================================

    story.append(

        Paragraph(

            "Health Assessment",

            heading

        )

    )

    health_text = f"""

    The transformer condition has been evaluated
    using multiple electrical and environmental
    parameters.

    Temperature, current loading, operating
    voltage, frequency, power factor and smoke
    level were analysed simultaneously.

    <br/><br/>

    <b>Overall Health:</b>

    {sensor["health"]}

    <br/><br/>

    <b>Risk Assessment:</b>

    {sensor["risk_assessment"]}

    <br/><br/>

    <b>Reason:</b>

    {sensor["reason"]}

    """

    story.append(

        Paragraph(

            health_text,

            body

        )

    )

    story.append(

        Spacer(1,20)

    )

    # ===========================================
    # RECOMMENDED ACTIONS
    # ===========================================

    story.append(

        Paragraph(

            "Recommended Actions",

            heading

        )

    )

    recommendations = "<br/><br/>".join(

        sensor["recommended_actions"]

    )

    story.append(

        Paragraph(

            recommendations,

            body

        )

    )

    story.append(

        Spacer(1,20)

    )

    # ===========================================
    # MACHINE LEARNING
    # ===========================================

    story.append(

        Paragraph(

            "Machine Learning Prediction",

            heading

        )

    )

    ml_text = f"""

    <b>Prediction</b><br/><br/>

    {ml["prediction"]}

    <br/><br/>

    <b>Failure Probability</b><br/><br/>

    {ml["failure_probability"]}

    <br/><br/>

    <b>Remaining Life</b><br/><br/>

    {ml["remaining_life"]}

    """

    story.append(

        Paragraph(

            ml_text,

            body

        )

    )

    story.append(

        Spacer(1,20)

    )

    # ===========================================
    # FINAL CONCLUSION
    # ===========================================

    story.append(

        Paragraph(

            "Final Conclusion",

            heading

        )

    )

    conclusion = f"""

    The Intelligent Transformer Health
    Analytics Platform successfully evaluated
    transformer operating condition using
    IoT sensors together with Artificial
    Intelligence and Machine Learning.

    <br/><br/>

    <b>Overall Health :</b>

    {sensor["health"]}

    <br/><br/>

    <b>Risk Level :</b>

    {sensor["risk_assessment"]}

    <br/><br/>

    Continuous monitoring improves transformer
    reliability, reduces maintenance cost,
    minimizes unexpected outages and enables
    predictive maintenance.

    """

    story.append(

        Paragraph(

            conclusion,

            body

        )

    )

    story.append(

        Spacer(1,20)

    )

    # ===========================================
    # DEVELOPED BY
    # ===========================================

    story.append(

        Paragraph(

            "Developed By",

            heading

        )

    )

    developers = """

    Muhammad Ahmed Khokhar

    <br/><br/>

    Muhiba Shakeel

    <br/><br/>

    Kiran Batool

    """

    story.append(

        Paragraph(

            developers,

            body

        )

    )

    story.append(

        Spacer(1,15)

    )

    story.append(

        Paragraph(

            "Department of Electrical Engineering<br/>"

            "National University of Technology (NUTECH)<br/>"

            "Islamabad, Pakistan",

            getSampleStyleSheet()["Italic"]

        )

    )

    story.append(

        Spacer(1,25)

    )

    # ===========================================
    # FOOTER
    # ===========================================

    story.append(

        Paragraph(

            "<b>***** END OF TRANSFORMER CONDITION REPORT *****</b>",

            title

        )

    )

    # ===========================================
    # BUILD PDF
    # ===========================================

    document.build(

        story

    )

    buffer.seek(0)

    return buffer
# ==================================================
# DOWNLOAD PDF REPORT
# ==================================================

@app.route("/download-report")
def download_report():

    try:

        pdf = generate_pdf_report()

        return send_file(

            pdf,

            mimetype="application/pdf",

            as_attachment=True,

            download_name="Transformer_Condition_Report.pdf"

        )

    except Exception as e:

        return jsonify({

            "status": "error",

            "message": str(e)

        }), 500


# ==================================================
# APPLICATION INFORMATION
# ==================================================

@app.route("/api/info")
def application_info():

    return jsonify({

        "project": "IoT-Based Distribution Transformer Condition Monitoring System",

        "university": "National University of Technology (NUTECH)",

        "department": "Department of Electrical Engineering",

        "developers": [

            "Muhammad Ahmed Khokhar",

            "Muhiba Shakeel",

            "Kiran Batool"

        ],

        "version": "2.0",

        "status": "Running"

    })


# ==================================================
# HEALTH CHECK
# ==================================================

@app.route("/api/health-check")
def health_check():

    return jsonify({

        "status": "OK",

        "server_time": datetime.now().strftime(

            "%d-%m-%Y %H:%M:%S"

        )

    })


# ==================================================
# START FLASK SERVER
# ==================================================

if __name__ == "__main__":


     app.run(

         host="0.0.0.0",
         port=5000
        )
#    app.run(

 #       host="127.0.0.1",

   #     port=5000,

    #    debug=True

     #)
###