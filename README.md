# 🌞🌙 Sun and Moon Apparent Motion Calculator

A Python-based tool to calculate and visualize the **apparent motion of the Sun and the Moon**, based on user-specified or current date and location (latitude). This project was originally developed for an academic final project in *Programming with Python* (Dec 2023), and it combines astronomy, geometry, and basic lunar calendar principles into an interactive terminal program with visual output.

## ✨ Features

- 📍 **Location-aware** calculations (based on latitude)  
- 🌅 Compute **sunrise/sunset time**, **solar elevation at noon**, **solar azimuth**  
- 🌕 Estimate **moonrise/moonset time**, **flood/ebb tide time**, and **moon phase**  
- 🌓 Plot **approximate moon phase diagram** using `matplotlib`  
- 📁 Export results to a local **CSV file**, with proper headers and formatting  
- 🌐 Supports **Gregorian and Lunar calendars** (via `zhdate`)

## ⚠️ Assumptions & Limitations

- The Earth is treated as a **perfect sphere**  
- **Atmospheric refraction** is ignored for simplicity  
- Moon motion is approximated **without geographical coordinates** (geometric simplification)  
- Resulting times are **local times**, not UTC  

These choices make the tool educational and accessible, but introduce small deviations (e.g. sunrise time may differ from real-world values by a few minutes).

## 📸 Sample Output

```
Date:                  04/22/2025  
Latitude:              40° 44' 0.0" N  
Solar declination:     11° 24' 51.0" N  
Sunrise time:          05:59:42  
Sunset time:           19:40:17  
Solar elevation at noon:   61.44°  
...  
Moonrise time:         15:27:00  
Moon phase:            Waxing Gibbous  
```

## 📦 Dependencies

- Python ≥ 3.8  
- [`zhdate`](https://pypi.org/project/zhdate/)  
- `matplotlib`  
- Standard libraries: `csv`, `datetime`, `math`

Install dependencies via:

```bash
pip install zhdate matplotlib
```

## 🚀 How to Run

```bash
python SMAMC.py
```

Follow the on-screen prompts to either use the current date or input a custom one. Make sure to provide a valid `.csv` file path to save your results.

---

Feel free to fork this repo, explore the code, and modify it to suit your needs — whether it's for **education** or just out of **astronomy curiosity** 🌌
