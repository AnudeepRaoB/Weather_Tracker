# Weather Tracker | Predictive Analytics
A sophisticated weather platform that tracks real-time data, maintains an extensive 5-year historical archive, and provides AI-driven temperature forecasts using machine learning.

## Demo 
https://drive.google.com/file/d/18_QYuK-Jl9nVZ1E1WN3QQQxyccpcyBbX/view?usp=sharing

## Features
- **Real-time Data**: Fetches precise weather and atmospheric stats via Open-Meteo API.
- **Archive Sync**: Automatically downloads **5 years of historical data** for new cities.
- **Predictive AI**: Uses a Multi-Variate Random Forest model to forecast next-hour temperatures.
- **24h Forecast**: Full daily timeline visualization with dynamic weather icons.
- **History Chart**: High-density 7-day trend analysis with horizontal scrolling.

## Technology Stack
- **Backend**: Python 3.x with Flask Framework.
- **Frontend**: HTML5, Vanilla CSS, and JavaScript.
- **AI/ML**: Scikit-Learn (Random Forest), Pandas, NumPy.
- **Database**: SQLite with SQLAlchemy ORM.
- **Visualization**: Matplotlib.

## Prerequisites
- Python 3.x or higher.
- Terminal/CLI access.
- Internet connectivity (for API data).

## Installation
1. Clone the repository to your local machine.
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the root directory and add:
   ```
   FLASK_SECRET_KEY=your_secret_key_here
   DATABASE_URL=sqlite:///weather.db
   ```

## Running the Application
To start the application, run the following command in the project root directory:
```bash
python3 app.py
```
Once started, the application will be available at: **http://127.0.0.1:5001**

## Project Structure
- **app.py**: Core Flask application and plot generation logic.
- **api_client.py**: Integration with Open-Meteo for real-time and archive data.
- **predictor.py**: Random Forest machine learning model and trend analysis.
- **database.py**: SQLite database schema and ORM models.
- **templates/**: Contains the frontend HTML views.
- **static/**: Contains the CSS styling and JavaScript logic.
- **requirements.txt**: Project dependencies list.
