# 🌴 AI Travel Recommendation System

An AI-powered web application that recommends travel destinations across Sri Lanka based on user preferences. The system analyzes curated travel data to suggest the best places to visit, helping users plan their perfect trip with ease.

---

## Key Features 🚀

- **AI-Powered Recommendations** — Suggests destinations tailored to user preferences using data-driven logic.
- **Sri Lanka Travel Dataset** — Built on a cleaned, structured dataset of destinations across the island.
- **Web-Based Interface** — Simple, accessible interface for browsing and discovering destinations.
- **Local Database Storage** — Destination and vibe data stored and queried efficiently via SQLite.
- **Data Preprocessing Pipeline** — Dedicated data loading and cleaning scripts to keep recommendations accurate.

---

## Technical Details 🛠️

| Component        | Technology                    |
|-------------------|-------------------------------|
| Backend           | Python (Flask)                |
| Frontend          | HTML5, CSS3                   |
| Database          | SQLite (`ceylon_vibe.db`, `destination.db`) |
| Data              | `sri_lanka_travel_data_cleaned.csv` |

---

## Project Structure 📁

```
AI-Travel-Recommendation-System/
├── instance/                          Instance-specific config/data
├── static/                            CSS, JS, and static assets
├── templates/                         HTML templates
├── app.py                             Main Flask application
├── data_loader.py                     Data loading & preprocessing
├── main.py                            Entry point script
├── ceylon_vibe.db                     SQLite database
├── destination.db                     SQLite database
├── sri_lanka_travel_data_cleaned.csv  Cleaned travel dataset
└── README.md
```

---

## Installation Guide ⚙️

### 1. Clone the repository
```bash
git clone https://github.com/shehanidileka/AI-Travel-Recommendation-System.git
cd AI-Travel-Recommendation-System
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the application
```bash
python app.py
```

### 4. Open in browser
Navigate to `http://localhost:5000` (or the port shown in your terminal).

---

## 📌 About This Project

This project explores how AI and data-driven approaches can simplify travel planning by matching user preferences with real destination data — with a focus on showcasing the beauty and diversity of Sri Lanka as a travel destination.

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome. Feel free to check the [issues page](https://github.com/shehanidileka/AI-Travel-Recommendation-System/issues).

## 📄 License

This project is open source and available for personal and educational use.
