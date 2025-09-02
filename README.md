# 💡 Siemens S7-1214 PLC + HMI + Azure IoT + Python Web Controller (Full Setup)

## 📌 Overview

This project demonstrates how to build a fully connected **Industrial IoT control system** using:

- ✅ **Siemens S7-1214 DC/DC/DC PLC** with 2 plug-in I/O modules
- ✅ **HMI (Human-Machine Interface)** integrated via TIA Portal v19
- ✅ **Python listener** to read/write PLC memory via Snap7
- ✅ **Azure IoT Hub** for cloud-based messaging
- ✅ **Flask-based web controller**, deployed on **Render**, for remote access

---

## 🧰 1. Installing & Setting Up TIA Portal V19

### 🔗 Download TIA Portal V19
- Link: [Siemens Support Portal](https://support.industry.siemens.com/cs/attachments/109820994/TIA_Portal_STEP7_Prof_Safety_WinCC_V19.iso)
- Requires a free **Siemens Account** – sign up and register as **educational use**.

### 💡 Trial License Strategy
TIA Portal v19 requires a license after 21 days. To extend this:
1. Install TIA Portal **V17** → use for 21 days
2. Then install **V18** → use for 21 days
3. Then install **V19** → use for 21 days
📆 **Total free time: 63 days**

> ⚠️ Ensure each version is installed in isolation and not overwritten.

### 🔐 License Activation
Upon launch:
- Activate **STEP7 Professional combo license**
- Follow on-screen prompts for activation.

---

## 🔌 2. Hardware Connections & Network Configuration

### 🔋 Powering the System
- Power ON the **S7-1214 PLC** using a 24V DC power supply.
- Power ON the **HMI Panel**.
- Connect **PLC**, **HMI**, and your **PC** to an **Ethernet hub/switch**.

### 🌐 Assigning IP Addresses (Same Subnet)
| Device | IP Address        |
|--------|-------------------|
| PLC    | `192.168.0.1`     |
| HMI    | `192.168.0.2`     |
| PC     | `192.168.0.3`     |
| Subnet | `255.255.255.0`   |

#### ✅ Set PC IP (Windows)
1. Go to **Control Panel → Network & Sharing Center**
2. Click **Change adapter settings**
3. Right-click on **Ethernet** → **Properties**
4. Select **IPv4** → **Properties**
5. Manually assign `192.168.0.3` and `255.255.255.0` as above
6. Open Command Prompt: run `ipconfig` to verify

#### ✅ Set PLC IP via TIA Portal
1. Open TIA Portal
2. Select **Online → Accessible Devices**
3. Search for the PLC
4. Set IP address to `192.168.0.1`

---

## 🏗️ 3. TIA Portal Project Setup

### 📥 Upload Existing PLC Program
The PLC already has a program uploaded. To view or modify it:
1. Open TIA Portal
2. Choose **Upload station to PG/PC**
3. The PLC workstation will now appear with its existing program

### ➕ Add Devices
- Add your **PLC** (S7-1214 DC/DC/DC)
- Add any **plug-in I/O modules**
- Add the **HMI device**

### 🧠 OB Logic & Programming

#### 🗂️ Organizational Block (OB1)
- Navigate to `Program Blocks → Main OB (OB1)`
- Ladder logic uses **NO contacts** (normally open) to map memory bits (for valve/pump control)

#### 🏷️ HMI Tags & JavaScript Events
- Go to `HMI > Screens > Events`
- Each button (e.g., "Open Valve", "Start Pump") has:
  - **Release Event**
  - JavaScript that:
    - Sets control bit to `True`
    - Resets others if needed
    - Updates status tags

> 🧠 The main logic is scripted in **HMI JavaScript events**, not just in ladder logic.

---

## 🐍 4. Python Scripts

### `listener.py`: Local Listener + PLC Writer
- Connects to the Siemens PLC via **Snap7**
- Listens for **cloud-to-device (C2D)** messages from **Azure IoT Hub**
- Parses each message (e.g., `{"case1": true}`)
- Converts it to a **memory bit write** on the PLC (e.g., `M0.0 = True`)

🧠 Uses a memory mapping like:
```python
"case1":  (0, 0),
"case2":  (0, 1),
...
"pump1":  (3, 0)
```

💾 Writes to PLC using:
```python
plc.mb_write(byte_index, 1, plc_data)
```

### `controller.py`: Web UI + Azure Sender
- Flask web app serving an HTML page with buttons for **15 cases + 2 pumps**
- Clicking a button sends a JSON message to **Azure IoT Hub**, e.g.:
  ```json
  {"pump2": true}
  ```
- This is received by `listener.py` and written to the PLC

🧠 Ensures **only one case is active** at a time

---

## 📦 5. Requirements.txt

Create a file `requirements.txt` with the following content:
```txt
Flask
azure-iot-hub
azure-iot-device
snap7
```

Install with:
```bash
pip install -r requirements.txt
```

---

## ☁️ 6. Hosting `controller.py` on Render

### 🔥 What is Render?
- Free cloud platform to deploy web apps
- Gives you a public HTTPS URL
- Simple GitHub integration

### 🛰️ Steps to Deploy:
1. Sign up at [https://render.com](https://render.com)
2. Click **New Web Service**
3. Connect your GitHub repo containing `controller.py`
4. Set:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python controller.py`
5. Visit your **public link** and use the UI to control the PLC

---

## 🚀 Running the Full System

| Step | Action |
|------|--------|
| 1.   | Power ON PLC and HMI |
| 2.   | Set IPs to same subnet |
| 3.   | Open TIA Portal and upload project (optional) |
| 4.   | Run `listener.py` locally |
| 5.   | Launch Render web UI |
| 6.   | Control valves and pumps remotely |

---

## 📞 Troubleshooting

| Problem | Solution |
|---------|----------|
| Snap7 errors | Make sure `snap7.dll` is present (Windows) |
| Can't reach PLC | Ensure IPs are correct and on same subnet |
| Azure errors | Verify IoT Hub connection strings |
| UI not loading | Check Flask logs or Render logs |

---

## 🧠 Final Notes

This system closes the loop from **industrial hardware to cloud** with a simple yet powerful Python + Azure + Siemens setup. It enables you to:

- 🔁 Remotely control actuators
- 📡 Bridge PLC → Cloud → Web
- 💬 Extend with sensor feedback, graphs, logging, and alerts
