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
To maximize trial period:
- Install **V17**, **V18**, and **V19** consecutively → 21 days each = **63 days** free trial.

> ⚠️ Each version must be installed separately and used one at a time.

### 🔐 License Activation
- On startup, activate **STEP7 Professional combo license** from trial prompt.

---

## 🔌 2. Hardware Connections & Network Configuration

### 🔋 Power and Ethernet Setup
- Power ON the **PLC** and **HMI**
- Use an Ethernet hub to connect PLC, HMI, and PC

### 🌐 IP Configuration
Assign static IPs in the same subnet:

| Device | IP Address      |
|--------|-----------------|
| PLC    | `192.168.0.1`   |
| HMI    | `192.168.0.2`   |
| PC     | `192.168.0.3`   |
| Subnet | `255.255.255.0` |

Set PC IP:
- Go to **Control Panel → Network → Adapter Settings**
- Right-click Ethernet → **Properties**
- IPv4 → Set manual IP

Set PLC IP using:
- TIA Portal → **Online → Accessible Devices** → Assign IP

---

## 🏗️ 3. PLC Programming in TIA Portal

### 📥 Upload Existing PLC Program
The PLC already contains the uploaded program:
- In TIA Portal, use **"Upload Station to PG/PC"** to bring the program into your project
- This retrieves ladder logic, device configuration, and tags

### ➕ Adding Devices
- Add the **S7-1214 DC/DC/DC PLC**
- Add plug-in modules as needed
- Add and configure the **HMI**

### 🧠 Logic Overview
- Ladder logic OB1 uses **NO contacts** mapped to bits for valve/pump control
- HMI uses **JavaScript scripting** under **Release Events** for button interactions:
  - Writes `True` to control tag
  - Resets other tags
  - Optionally updates status displays

---

## 🐍 4. Python Scripts

### `listener.py`: Connects PLC + Azure IoT Hub
- Uses **Snap7** to connect to PLC via IP `192.168.0.1`
- Subscribes to **Azure IoT Hub cloud-to-device messages**
- Writes values to specific memory bits in PLC

To run it:

```bash
pip install snap7 azure-iot-device
python listener.py
```

✅ Make sure:
- The PLC is on and reachable
- snap7.dll is present (on Windows)
- Your Azure IoT Hub credentials are valid

---

### `controller.py`: Remote Web UI + Azure Sender
- A **Flask web app** that lets you toggle valves/cases/pumps via a web UI
- On button press, sends JSON payload to **Azure IoT Hub** as a C2D message
- PLC receives message through the `listener.py` script

---

## 📦 5. Deploying `controller.py` using Render

### 🌐 What is Render?
Render.com is a free cloud platform to deploy Python apps publicly.

### 📝 requirements.txt
To deploy `controller.py`, include this file:

```txt
flask
azure-iot-device
```

### 🚀 Steps to Deploy:
1. Go to [https://render.com](https://render.com)
2. Click **New Web Service**
3. Link GitHub repo with `controller.py` and `requirements.txt`
4. Set:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python controller.py`
5. Once deployed, open your Render URL to control the system

---

## 🧪 Running the System (Full Workflow)

| Step | Action |
|------|--------|
| 1    | Power ON PLC + HMI and connect to network |
| 2    | Configure IPs and verify communication via `ping` |
| 3    | (Optional) Upload existing PLC program using TIA |
| 4    | Run `listener.py` locally |
| 5    | Open Render-hosted controller site |
| 6    | Click buttons to actuate valves or pumps remotely |

---

## 🛠️ Troubleshooting

| Issue                    | Fix |
|-------------------------|-----|
| Snap7 error             | Ensure `snap7.dll` is in the same directory (Windows) |
| IoT Hub connection fails | Recheck connection string format |
| Flask app crashes       | Use `flask run` and check error logs |
| Render doesn’t deploy   | Check logs; confirm `requirements.txt` and `start command` |

---

## 🧠 Summary

This system integrates:
- Siemens industrial hardware
- Secure cloud communication
- A local PLC listener
- A remote Flask web controller

It demonstrates a complete **digital twin pipeline** for real-world industrial automation and control.

---

## ⚡ XRcreate Integration

The `readwrite.py` script extends the system by directly integrating **XRcreate** with the PLC.  

### 🔗 How It Works
- **XRcreate** has its **own frontend** for device control.  
- Each device is linked to XRcreate using a **unique device string (`owndevicestring`)**, which can be generated by the **XRcreate admin panel**.  
- The `readwrite.py` script uses this string inside the Azure IoT Hub connection string to authenticate:  

```python
conn_str = "HostName=arcreate.azure-devices.net;DeviceId=(owndevicestring)"
```

### 🖥️ Where to Run
- `readwrite.py` **must run on the local PC** that is physically connected to the Siemens PLC.  
- This script listens for cloud-to-device (C2D) messages from XRcreate and writes them to the PLC memory using **Snap7**.  

### 🌐 Remote Control
- From any **remote PC**, XRcreate can be launched through its own frontend.  
- Once logged in, select the PLC device (registered with its device string).  
- Start the procedure named **`testing`** from XRcreate.  
- Commands from XRcreate are then transmitted via Azure IoT Hub → `readwrite.py` → PLC.  

### ⚙️ Programming Behavior
- XRcreate sends JSON commands like `{"case1": "true"}` or `{"pump1": "false"}`.  
- `readwrite.py` decodes these messages, maps them to the correct PLC memory bits (`M0.0`, `M3.0`, etc.), and updates the PLC in real-time.  
- After writing to the PLC, the script **echoes back the confirmation** to XRcreate, ensuring synchronized status between the PLC and the frontend.  

### ▶️ Running `readwrite.py`
To start the XRcreate → PLC bridge, run on the PC connected to the PLC:  

```bash
pip install snap7 azure-iot-device
python readwrite.py
```

✅ Requirements:  
- Siemens S7-1214 PLC powered ON and network-connected  
- Correct IP configured (`192.168.0.1` by default)  
- Valid XRcreate device string (`owndevicestring`) set in the script  
