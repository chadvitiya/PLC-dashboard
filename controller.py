from flask import Flask, render_template_string, request, redirect
from azure.iot.hub import IoTHubRegistryManager
import json

# Azure IoT Hub connection (service credentials)
connection_str = "HostName=advitiya-iothub.azure-devices.net;SharedAccessKeyName=iothubowner;SharedAccessKey=fV4KGKqo7EpeHtpduYnEVsgVjvf6wZqR2AIoTEOU/R4="
device_id = "PLC"
registry_manager = IoTHubRegistryManager(connection_str)

app = Flask(__name__)

case_keys = [f"case{i}" for i in range(1, 16)]
case_states = {key: False for key in case_keys}
pump_states = {"pump1": False, "pump2": False}

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>PLC Control Panel</title>
    <script>
        function disableOtherCases(activeKey) {
            const buttons = document.querySelectorAll('button[name="case"]');
            buttons.forEach((btn) => {
                if (btn.value !== activeKey) {
                    btn.disabled = true;
                }
            });
        }
        function handleCaseClick(key) {
            const isActive = document.getElementById(key).dataset.active === 'true';
            if (!isActive) {
                disableOtherCases(key);
            }
        }
    </script>
</head>
<body style="text-align: center; padding-top: 50px;">
    <h2>Remote Control Panel: Cases 1–15</h2>
    <form method="POST">
        {% set any_case_on = false %}
        {% for key in case_keys %}
            {% if states[key] %}
                {% set any_case_on = true %}
            {% endif %}
        {% endfor %}
        {% for key in case_keys %}
            <button 
                id="{{key}}" 
                name="case" 
                value="{{key}}" 
                data-active="{{ 'true' if states[key] else 'false' }}" 
                onclick="handleCaseClick('{{key}}')" 
                style="padding: 15px; margin: 5px; font-size: 16px; background-color: {{ 'green' if states[key] else 'red' }}; color: white;"
                {% if any_case_on and not states[key] %}disabled{% endif %}>
                {{ key|capitalize }} ({{ 'ON' if states[key] else 'OFF' }})
            </button>
        {% endfor %}

        <br><br>
        <h2>Pumps</h2>
        <button name="pump" value="pump1" style="padding: 15px; margin: 5px; font-size: 16px; background-color: {{ 'green' if pump_states['pump1'] else 'red' }}; color: white;">
            Pump 1 ({{ 'ON' if pump_states['pump1'] else 'OFF' }})
        </button>
        <button name="pump" value="pump2" style="padding: 15px; margin: 5px; font-size: 16px; background-color: {{ 'green' if pump_states['pump2'] else 'red' }}; color: white;">
            Pump 2 ({{ 'ON' if pump_states['pump2'] else 'OFF' }})
        </button>
    </form>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def control():
    if request.method == 'POST':
        case_clicked = request.form.get('case')
        pump_clicked = request.form.get('pump')

        if case_clicked:
            # Toggle selected case, turn others off
            was_on = case_states[case_clicked]
            for key in case_states:
                case_states[key] = False
            case_states[case_clicked] = not was_on
            payload = {case_clicked: case_states[case_clicked]}

        elif pump_clicked:
            pump_states[pump_clicked] = not pump_states[pump_clicked]
            payload = {pump_clicked: pump_states[pump_clicked]}

        message = json.dumps(payload)
        registry_manager.send_c2d_message(device_id, message)
        print(f"Sent: {payload}")
        return redirect('/')

    return render_template_string(HTML, case_keys=case_keys, states=case_states, pump_states=pump_states)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
