
# Import Libraries
import pandas as pd
from sklearn.linear_model import LogisticRegression
from datetime import date, timedelta
import pyttsx3
import speech_recognition as sr
import datetime
# from requests import get
# import datetime
import sys
import requests
import os
from dateutil.parser import parse
import warnings
warnings.filterwarnings("ignore")
# Redirect stderr to /dev/null to ignore warnings
sys.stderr = open(os.devnull, 'w')
# Disable ALSA warnings
os.environ['PYALSA_CARD'] = 'plug:default'
# ignore DeprecationWarning
warnings.filterwarnings("ignore", category=DeprecationWarning)

# import warnings
# warnings.filterwarnings("ignore", message="X does not have valid feature names*")


# Generating an engine for converting written text to voice
engine = pyttsx3.init()
voices = engine.getProperty('voices')
print(voices[0].id)
engine.setProperty('voices', voices[0].id)


# text to voice function
def speak(audio):
    engine.say(audio)
    print(audio)
    engine.runAndWait()


# voice to text function
def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening......")
        r.pause_threshold = 1
        audio = r.listen(source, timeout=1, phrase_time_limit=5)

    try:
        print("Recognizing.....")
        query = r.recognize_google(audio, language='en-in')
        print(f"you said :{query}")

    except Exception as e:
        speak('Please Say again')
        return "none"
    return query


# good wishes function
def wish():
    hour = int(datetime.datetime.now().hour)

    if hour >= 0 and hour <= 12:
        speak("Good Morning ............")
    elif hour > 12 and hour < 18:
        speak(("Good Afternoon.........."))
    else:
        speak("Good Evening..............")

    speak("How may i assist you sir! ")

# Function for (weather forecast for any date)


def is_valid_date(date_str):
    try:
        date_obj = parse(date_str)
        return True
    except ValueError:
        return False


# Predicts wheather
def predict_weather(inputdate):
    data = pd.read_csv('/home/ehtisham_nasir/Desktop/MLP/seattle-weather.csv')

    data['date'] = pd.to_datetime(data['date'])

    # Define the input and output variables
    X = data[['precipitation', 'temp_max', 'temp_min', 'wind']]
    y = data['weather']

    # Train the model
    model = LogisticRegression(max_iter=10000)
    model.fit(X, y)

    # Get today's date
    today = pd.to_datetime(inputdate).date()

    # Extract the precipitation, maximum temperature, minimum temperature, and wind speed from the current date
    today_data = data[data['date'].dt.date == today]
    if len(today_data) > 0:
        precipitation = today_data.iloc[0]['precipitation']
        temp_max = today_data.iloc[0]['temp_max']
        temp_min = today_data.iloc[0]['temp_min']
        wind = today_data.iloc[0]['wind']
    else:
        # If there is no data for today, use the mean values from the dataset
        precipitation = data['precipitation'].mean()
        temp_max = data['temp_max'].mean()
        temp_min = data['temp_min'].mean()
        wind = data['wind'].mean()

    # Make a prediction for the weather based on the input features
    prediction = model.predict([[precipitation, temp_max, temp_min, wind]])

   # Print the result
    result = f'Weather Status: {prediction[0]}'
    temp_max = float("{0:.2f}".format(temp_max))
    temp_min = float("{0:.2f}".format(temp_min))
    precipitation = float("{0:.2f}".format(precipitation))
    speak("temprature max:"+str(temp_max))
    speak("temprature min:"+str(temp_min))
    speak("precepitation:"+str(precipitation))
    # speak("")
    return result


# for today weather
def get_weather(city):
    response = requests.get(url.format(city, api_key))
    if response.status_code == 200:
        data = response.json()
        temperature = data['main']['temp']
        humidity = data['main']['humidity']
        weather_description = data['weather'][0]['description']
        # speak(f"The current temperature in {city} is {temperature}°C.")
        # speak(f"Humidity: {humidity}%.")
        # speak(f"Weather description: {weather_description}.")
        return f"The current temperature in {city} is {temperature}°C. \nHumidity: {humidity}%. \nWeather description: {weather_description}."
    else:
        return "Error fetching data from API."


# for tomorrow weather
def get_tomorrow_weather(city):
    api_key = "d28bf5e4806c0746b214d36188783fae"
    url = "https://api.openweathermap.org/data/2.5/forecast?q={}&appid={}&units=metric"

    response = requests.get(url.format(city, api_key))
    if response.status_code == 200:
        data = response.json()
        tomorrow = (datetime.datetime.now() +
                    datetime.timedelta(days=1)).strftime('%Y-%m-%d')
        for weather in data['list']:
            if weather['dt_txt'].startswith(tomorrow):
                temperature = weather['main']['temp']
                weather_description = weather['weather'][0]['description']
                return f"Tomorrow's temperature in {city} will be {temperature}°C. \nWeather description: {weather_description}."
        return "Weather data for tomorrow not found."
    else:
        return "Error fetching data from API."


# main function
if __name__ == "__main__":
    wish()
    while True:
        query = take_command().lower()

# Today Weather Query
        if "today weather" in query:
            speak("Sir! today weather is")
            result = predict_weather('today')
            speak(result)


# Yesterday weather Query
        elif "yesterday weather" in query:
            speak("Sir! yesterday weather was")
            today1 = date.today()
        # Get tomorrow's date
            yesterday = today1 - timedelta(days=1)
        # Format tomorrow's date as a string in the format 'yy-mm-dd'
            yesterday_str = yesterday.strftime('%y-%m-%d')
            result = predict_weather(yesterday_str)
            speak(result)


# Tomorrow weather Query
        elif "tomorrow weather" in query:
            speak("Sir! tomorrow weather will be ")
            today1 = date.today()
        # Get tomorrow's date
            tomorrow = today1 + timedelta(days=1)
        # Format tomorrow's date as a string in the format 'yy-mm-dd'
            tomorrow_str = tomorrow.strftime('%y-%m-%d')
            result = predict_weather(tomorrow_str)
            speak(result)


# Weather forecast for different dates
        elif "weather forecast" in query:
            speak("Sir! tell me the date")
            SOC = take_command().lower()
            if is_valid_date(f"{SOC}"):
                result = predict_weather(f"{SOC}")
                speak(result)
            else:
                speak("{SOC} is not a valid date")

# weather / weather tomorrow
        elif "weather today" in query:
            speak("Sir! tell me the city")
            city = take_command().lower()
            api_key = "d28bf5e4806c0746b214d36188783fae"
            url = "https://api.openweathermap.org/data/2.5/weather?q={}&appid={}&units=metric"
            report = get_weather(city)
            speak(report)

        elif "weather tomorrow" in query:
            speak("Sir! tell me the city")
            city = take_command().lower()
            report = get_tomorrow_weather(city)
            speak(report)



# For Exit or Quiting
        elif "no thanks" in query:
            speak("Iam glad to help you!")
            sys.exit()
        speak("May i further help you, sir ....... ")


# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
