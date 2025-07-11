# Installation Guide

## Local Development

1. Install Python 3.11
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   streamlit run app.py --server.port 5000
   ```

## Render Deployment

1. Fork/upload this repository to GitHub
2. Create new Web Service on Render
3. Connect your GitHub repository  
4. Render will automatically:
   - Install dependencies from requirements.txt
   - Start the application using the start command
   - Assign a public URL

## Environment Variables

No additional environment variables required. The application uses local JSON files for data storage.

## File Structure

```
EduScan_Somalia_RENDER_ULTIMATE_FIX/
├── .streamlit/
│   └── config.toml
├── data/
│   ├── learning_difficulty_detector.pkl
│   ├── scaler.pkl
│   ├── app_settings.json
│   ├── parent_observations.json
│   └── student_data.json
├── pages/
│   └── __init__.py
├── pictures/
│   └── [educational images]
├── utils/
│   └── __init__.py
├── app.py
├── requirements.txt
├── render.yaml
├── README.md
└── INSTALLATION.md
```