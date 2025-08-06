![Logo](https://github.com/kriptos1970/simple_cooler_heater_pid/raw/main/assets/logo.png)
# Simple Cooler Heater PID Controller

> This **fork** of the original [simple_pid_controller](https://github.com/bvweerd/simple_pid_controller) enhances its functionality by adding support for a **Cooling Mode** and the ability to select a custom **output entity**.  
>  
> The Simple PID Controller is a Home Assistant integration that provides real-time PID control with a user-friendly interface for tuning and diagnostics.

---

### Cooling Mode

- In **Cooling Mode**, the PID output is **inverted**, allowing the controller to regulate systems where **decreasing** the control variable is needed  
  (e.g., turning on a fan to reduce temperature), rather than increasing it as in heating mode.

- ✅ The new feature is fully compatible with the existing configuration.

- Introduces a **UI switch** (`cooling_mode`) to toggle between heating and cooling behavior **dynamically**.

---

### Use Cases

This enhancement is especially useful for scenarios such as:  
- Active cooling of enclosures  
- Temperature-regulated fan control  
- Other inverse-response systems


---

## 📚 Table of Contents
- [Features](#features)
- [Installation](#installation)
  - [HACS (Recommended)](#hacs-recommended)
  - [Manual Installation](#manual-installation)
  - [Removal Instructions](#removal-instructions) 
- [Configuration](#configuration)
- [Entities Overview](#entities-overview)
- [PID Tuning Guide](#pid-tuning-guide)
  - [Manual Tuning](#1-manual-trial--error)
  - [Ziegler–Nichols Method](#2-zieglernichols-method)
- [More details and extended documentation](#extended-documentation)
- [Example PID Graph](#example-pid-graph)
- [Support & Development](#support--development)
- [Service Actions](#service-actions)


---

## ✨ Features

- **Live PID tuning** via Number entities.
- **Diagnostics** for P, I, and D terms (optional).
- **Switch** to toggle auto mode and proportional-on-measurement.
- **Configurable** output limits, setpoint, and sample time.

### Included Entities

| Platform | Entity                    | Purpose                                 |
|----------|---------------------------|-----------------------------------------|
| Sensor   | `PID Output`              | Current controller output as percentage |
| Sensor   | `PID P Contribution`      | Proportional term value (diagnostic)    |
| Sensor   | `PID I Contribution`      | Integral term value (diagnostic)        |
| Sensor   | `PID D Contribution`      | Derivative term value (diagnostic)      |
| Number   | `Kp`, `Ki`, `Kd`          | PID gain parameters                     |
| Number   | `Setpoint`                | Desired target value                    |
| Number   | `Output Min` / `Max`      | Controller output limits                |
| Number   | `Sample Time`             | PID evaluation interval                 |
| Switch   | `Auto Mode`               | Toggle automatic control                |
| Switch   | `Proportional on Measurement` | Change proportional mode         |
| Switch   | `Windup Protection`       | Toggle windup protection                |
| Switch   | `Cooler mode`             | Toggle cooler mode                      |


> 💡 All entities are editable via the UI in **Settings > Devices & Services > [Your Controller] > Options**.

---

## 🔧 Installation

### HACS (Recommended)

1. In Home Assistant UI, navigate to **HACS > Integrations**
2. Click the three-dot menu (⋮) and select **Custom repositories**
3. Add:
   ```text
   https://github.com/kriptos1970/simple_cooler_heater_pid
   ```
   Select **Integration** as type
4. Search for **Simple PID Controller** and install
5. Restart Home Assistant

### Manual Installation

1. Download or clone this repository
2. Copy `simple_cooler_heater_pid` to `/config/custom_components/`
3. Restart Home Assistant

### Removal Instructions 
To remove the Simple PID Controller, navigate to **Settings > Devices & Services**, select **Simple PID Controller**, and click **Delete**. If installed manually, delete the `custom_components/simple_cooler_heater_pid` directory and restart Home Assistant.

---

## ⚙️ Configuration
The controller is configured through the UI using the Config Flow {% term config_flow %}.

1. Go to **Settings > Devices & Services**
2. Click **Add Integration** and choose **Simple PID Controller**
3. Enter:
   - **Name**: e.g., "Heater Controller"
   - **Sensor Entity**: e.g., `sensor.living_room_temperature`
4. Submit and finish setup

**Default Range:**  
The controller’s setpoint range defaults to **0.0 – 100.0**. To customize this range, select the integration in **Settings > Devices & Services**, click **Options**, adjust **Range Min** and **Range Max**, and save.

---

## 📊 Entities Overview

| Platform | Entity Suffix                 | Description                                        |
|----------|-------------------------------|----------------------------------------------------|
| Sensor   | `PID Output`                  | Current controller output (%).                     |
| Sensor   | `PID P/I/D Contribution`      | Diagnostic terms. Disabled by default.             |
| Number   | `Kp`, `Ki`, `Kd`              | PID gains.                                         |
| Number   | `Setpoint`                    | Desired system target.                             |
| Number   | `Output Min` / `Output Max`   | Min/max control limits.                            |
| Number   | `Sample Time`                 | PID evaluation rate in seconds.                    |
| Switch   | `Auto Mode`                   | Enable/disable PID automation.                     |
| Switch   | `Proportional on Measurement` | Use measurement instead of error for P term.       |
| Switch   | `Windup Protection`           | Toggle windup protection                           |
| Switch   | `Cooler mode`                 | Toggle cooler mode                                 |

---

## 🎯 PID Tuning Guide

A PID controller continuously corrects the difference between a **setpoint** and **measured value** using:

- **P (Proportional)**: reacts to present error
- **I (Integral)**: compensates for past error
- **D (Derivative)**: predicts future error trends

<details>
<summary><strong>1. Manual (Trial & Error)</strong></summary>

1. Set `Ki` and `Kd` to 0
2. Start with small `Kp` (e.g., 1.0)
3. Increase `Kp` until oscillations appear
4. Halve that `Kp` value
5. Increase `Ki` to reduce steady-state error
6. Add `Kd` to smooth out oscillations

</details>

<details>
<summary><strong>2. Ziegler–Nichols Method</strong></summary>

1. Set `Ki = 0`, `Kd = 0`, increase `Kp` until sustained oscillations
2. Measure:
   - **Ku** = critical gain
   - **Pu** = oscillation period
3. Apply:
   - `Kp = 0.6 × Ku`
   - `Ki = 1.2 × Ku / Pu`
   - `Kd = 0.075 × Ku × Pu`

</details>

---

### How it works in practice

1. **Initialization**  
   - On startup (or when options change), we set up a single `sample_time` value (in seconds).  
   - We register a periodic callback with Home Assistant’s scheduler (`async_track_time_interval` or `DataUpdateCoordinator`) using that same `sample_time`.  

2. **Coordinator Tick**  
   - Every `sample_time` seconds, Home Assistant’s scheduler invokes our update method.  
   - We immediately read the current process variable (e.g. temperature sensor) and pass it to the PID logic.

3. **PID Logic & Output**  
   - The PID algorithm calculates the Proportional, Integral, and Derivative terms and writes the result to your target entity (e.g. a heater or set-point).

4. **Adjusting Sample Time**
   - Changing `sample_time` in your integration options takes effect at the end of the current interval—no Home Assistant restart is required.  
   - On the next tick, the coordinator will use the new interval.

---

## 📚 Extended documentation

The integration is based on simple-pid [https://pypi.org/project/simple-pid/](https://pypi.org/project/simple-pid/)

Read the user guide here: [https://simple-pid.readthedocs.io/en/latest/user_guide.html#user-guide](https://simple-pid.readthedocs.io/en/latest/user_guide.html#user-guide)

---

## 📈 Example PID Graph

Here's an example output showing the controller responding to a setpoint:

![Example PID Output](assets/pid_example_graph.png)

---

## 🛠️ Support & Development

- **GitHub Repository**: [https://github.com/kriptos1970/simple_cooler_heater_pid](https://github.com/kriptos1970/simple_cooler_heater_pid)
- **Issues & Bugs**: [Report here](https://github.com/kriptos1970/simple_cooler_heater_pid/issues)

---

## 🔧 Service Actions 
This Integration does **not** expose any custom services. All interactions are performed via UI-based entities.


