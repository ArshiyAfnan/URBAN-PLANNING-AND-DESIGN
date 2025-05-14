
from flask import Flask, request, render_template_string

app = Flask(__name__)
feedback_list = []

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Urban Transportation Dashboard</title>
    <style>
        body { font-family: Arial; padding: 20px; background: #eef2f5; }
        h2, h3 { text-align: center; }
        form, .section { background: white; padding: 20px; margin-bottom: 30px; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1); width: 90%; max-width: 600px; margin-left: auto; margin-right: auto; }
        label { display: block; margin-top: 10px; }
        input, select, textarea { width: 100%; padding: 8px; margin-top: 5px; }
        input[type=submit] { margin-top: 15px; background: #007bff; color: white; border: none; border-radius: 4px; cursor: pointer; }
        .results, .error, .feedback-list { background: #fff; padding: 15px; border-radius: 8px; margin-top: 15px; }
    </style>
</head>
<body>

    <h2>Urban Planning and Design – Transportation</h2>

    <!-- Transport Efficiency Calculator -->
    <form method="post">
        <h3>1. Transport Efficiency Calculator</h3>
        <label>Number of Public Buses:</label>
        <input type="number" name="buses" required>

        <label>Average Bus Speed (km/h):</label>
        <input type="number" step="0.1" name="speed" required>

        <label>Congestion Level (%):</label>
        <input type="number" step="0.1" name="congestion" required>

        <input type="submit" name="action" value="Calculate Efficiency">
    </form>

    {% if travel_time is defined %}
    <div class="results">
        <p><strong>Estimated Travel Time (per 100 km):</strong> {{ travel_time }} hours</p>
        <p><strong>Estimated CO₂ Reduction:</strong> {{ co2_reduction }} tons/day</p>
    </div>
    {% elif error is defined %}
    <div class="error">
        <p style="color:red;">Error: {{ error }}</p>
    </div>
    {% endif %}

    <!-- Traffic Simulation Section -->
    <form method="post">
        <h3>2. Simulated Traffic Performance Report</h3>
        <label>Select Urban Area Type:</label>
        <select name="area_type">
            <option value="Residential">Residential</option>
            <option value="Commercial">Commercial</option>
            <option value="Mixed-use">Mixed-use</option>
        </select>
        <input type="submit" name="action" value="Generate Report">
    </form>

    {% if area_report is defined %}
    <div class="results">
        <p><strong>Traffic Performance for {{ area_type }} Zone:</strong></p>
        <ul>
            <li>Avg Speed: {{ area_report.speed }} km/h</li>
            <li>Congestion Level: {{ area_report.congestion }}%</li>
            <li>Public Transport Coverage: {{ area_report.coverage }}</li>
        </ul>
    </div>
    {% endif %}

    <!-- Feedback Form -->
    <form method="post">
        <h3>3. Submit Feedback</h3>
        <label>Your Name:</label>
        <input type="text" name="user">

        <label>Your Feedback:</label>
        <textarea name="feedback" rows="4"></textarea>

        <input type="submit" name="action" value="Submit Feedback">
    </form>

    {% if feedback_list %}
    <div class="feedback-list">
        <h4>Collected Feedback:</h4>
        <ul>
            {% for fb in feedback_list %}
            <li><strong>{{ fb.user }}</strong>: {{ fb.text }}</li>
            {% endfor %}
        </ul>
    </div>
    {% endif %}

</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def dashboard():
    travel_time = co2_reduction = area_type = area_report = error = None

    if request.method == 'POST':
        action = request.form.get("action")

        if action == "Calculate Efficiency":
            try:
                buses = int(request.form['buses'])
                speed = float(request.form['speed'])
                congestion = float(request.form['congestion'])

                if speed <= 0 or congestion >= 100:
                    raise ValueError("Speed must be > 0 and congestion < 100")

                travel_time = 100 / (speed * (1 - congestion / 100))
                co2_reduction = buses * 1.5
            except Exception as e:
                error = str(e)

        elif action == "Generate Report":
            area_type = request.form['area_type']
            report_data = {
                "Residential": {"speed": 35, "congestion": 40, "coverage": "Moderate"},
                "Commercial": {"speed": 20, "congestion": 70, "coverage": "High"},
                "Mixed-use": {"speed": 28, "congestion": 55, "coverage": "Moderate-High"}
            }
            area_report = report_data.get(area_type, {})

        elif action == "Submit Feedback":
            user = request.form.get("user", "Anonymous")
            feedback = request.form.get("feedback", "")
            if feedback.strip():
                feedback_list.append({"user": user.strip(), "text": feedback.strip()})

    return render_template_string(
        HTML_TEMPLATE,
        travel_time=round(travel_time, 2) if travel_time else None,
        co2_reduction=round(co2_reduction, 2) if co2_reduction else None,
        area_report=area_report,
        area_type=area_type,
        error=error,
        feedback_list=feedback_list
    )

if __name__ == '__main__':
    app.run(debug=True)
