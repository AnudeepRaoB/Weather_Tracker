# Predictive Weather Analytics

WeatherSphere is a premium Python application that not only tracks real-time weather but also analyzes historical trends and provides AI-driven temperature forecasts using machine learning.

![Dashboard Preview](https://img.icons8.com/clouds/100/000000/cloud.png)

## Features
- **Real-time Data**: Fetches precise weather data using the OpenWeatherMap API.
- **Historical Tracking**: Stores history in a local SQLite database for trend analysis.
- **Predictive Analytics**: Uses Scikit-learn Linear Regression to forecast temperatures.
- **Interactive Visuals**: Dynamic charts powered by Plotly.js.

##  Tech Stack
- **Backend**: Flask, SQLAlchemy
- **Data**: Pandas, Scikit-learn
- **Frontend**: HTML5, Vanilla CSS, Plotly.js

##  Installation & Setup

1. **Clone the repository** (if applicable) and navigate to the directory.
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Configure API Key**:
   - Get a free API key from [OpenWeatherMap](https://openweathermap.org/api).
   - Create a `.env` file in the root directory.
   - Add your key: `OPENWEATHER_API_KEY=your_key_here`.
4. **Run the Application**:
   ```bash
   python app.py
   ```
5. Open your browser and go to `http://127.0.0.1:5001`.

##  How the Prediction Works
The system uses a **Linear Regression model** specifically trained on the specific city's recent weather history (the last 20 records). It calculates the slope of temperature change over time to predict the likely value for the next hour. 
