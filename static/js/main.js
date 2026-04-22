document.addEventListener('DOMContentLoaded', () => {
    const btn = document.getElementById('searchBtn');
    const input = document.getElementById('cityInput');
    const dash = document.getElementById('dashboard');
    const load = document.getElementById('loader');

    btn.addEventListener('click', () => {
        getData(input.value);
    });

    input.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') getData(input.value);
    });

    async function getData(city) {
        if (!city) {
            alert("Enter City");
            return;
        }
        load.classList.remove('hidden');
        dash.classList.add('hidden');
        try {
            const res = await fetch('/api/weather', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ city: city })
            });
            const data = await res.json();
            if (data.error) {
                alert("Error: " + data.error);
                load.classList.add('hidden');
                return;
            }
            load.classList.add('hidden');
            dash.classList.remove('hidden');
            show(data);
        } catch (err) {
            alert('Server Error');
            load.classList.add('hidden');
        }
    }

    function show(data) {
        document.getElementById('cityName').textContent = data.current.city;
        document.getElementById('currentTemp').textContent = data.current.temp + "°C";
        document.getElementById('weatherDesc').textContent = data.current.description;
        document.getElementById('humidity').textContent = data.current.humidity + "%";
        document.getElementById('windSpeed').textContent = data.current.wind_speed + " m/s";

        const pred = document.getElementById('predictedTempVal');
        if (data.prediction && data.prediction.temp) {
            pred.textContent = `${data.prediction.temp} for ${data.prediction.time}`;
        } else {
            pred.textContent = "Low Data";
        }

        document.getElementById('avgTemp').textContent = data.trends.avg + "°C";

        const img = document.getElementById('chartImg');
        if (data.chart_url) {
            img.src = data.chart_url;
            img.classList.remove('hidden');
        } else {
            img.classList.add('hidden');
        }
        list(data.forecast);
    }

    function list(forecast) {
        const box = document.getElementById('forecastContainer');
        box.innerHTML = '';
        if (!forecast || forecast.length === 0) {
            box.innerHTML = '<p>No Data</p>';
            return;
        }
        forecast.forEach(item => {
            const div = document.createElement('div');
            div.className = 'forecast-item';
            div.innerHTML = `
                <div>${item.time}</div>
                <img src="https://openweathermap.org/img/wn/${item.icon}.png" width="40">
                <div><strong>${item.temp}°C</strong></div>
            `;
            box.appendChild(div);
        });
    }
});
