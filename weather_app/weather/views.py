from django.shortcuts import render
import requests
from django.http import JsonResponse, HttpResponseBadRequest
from .models import SearchHistory
from django.conf import settings

def BASE(request):
    return render(request, 'home.html')  # Adjust this to your actual template

# Fetch current weather data for a specific city and country
# weather/views.py
# weather/views.py

def get_current_weather(request):
    city = request.GET.get('city')
    country_code = request.GET.get('country_code')
    
    # Validate city and country code inputs
    if not city or not country_code:
        return HttpResponseBadRequest("Please provide both city and country code.")

    # Weatherbit current weather API URL
    url = f"{settings.WEATHERBIT_BASE_URL}/current"
    params = {
        "city": city,
        "country": country_code,
        "key": settings.WEATHERBIT_API_KEY
    }

    # Make the request to Weatherbit API
    response = requests.get(url, params=params)
    
    # Check if the response was successful
    if response.status_code == 200:
        data = response.json()
        
        # Extract relevant information (assuming first item in data['data'] array)
        if 'data' in data and len(data['data']) > 0:
            weather_info = data['data'][0]
            result = {
                "temperature": f"{weather_info['temp']}°C",
                "condition": weather_info['weather']['description']
            }

            # Save to search history
            SearchHistory.objects.create(city=city, country_code=country_code)
            return JsonResponse(result)
        
        else:
            return JsonResponse({"error": "Unexpected data format received from API"}, status=500)
    else:
        return JsonResponse({"error": "Could not fetch weather data"}, status=response.status_code)


# def get_current_weather(request):
#     city = request.GET.get('city')
#     country_code = request.GET.get('country_code')
#     if not city or not country_code:
#         return HttpResponseBadRequest("Please provide both city and country code.")
    
#     url = f"{settings.WEATHERBIT_BASE_URL}/current"
#     params = {"city": city, "country": country_code, "key": settings.WEATHERBIT_API_KEY}
#     response = requests.get(url, params=params)
#     if response.status_code == 200:
#         data = response.json()["data"][0]
#         result = {
#             "temperature": data["temp"],
#             "app_temp": data["app_temp"],
#             "description": data["weather"]["description"],
#             "wind_spd": data["wind_spd"],
#             "humidity": data["rh"],
#             "aqi": data["aqi"],
#             "city_name": data["city_name"],
#             "country_code": data["country_code"],
#             "ob_time": data["ob_time"]
#         }
#         return JsonResponse(result)
#     else:
#         return JsonResponse({"error": "Could not fetch weather data"}, status=response.status_code)
    
    
# def get_forecast(request):
#     city = request.GET.get('city')
#     country_code = request.GET.get('country_code')
    
#     # Validate city and country code inputs
#     if not city or not country_code:
#         return HttpResponseBadRequest("Please provide both city and country code.")

#     # Weatherbit forecast API URL
#     url = f"{settings.WEATHERBIT_BASE_URL}/forecast/daily"
#     params = {
#         "city": city,
#         "country": country_code,
#         "key": settings.WEATHERBIT_API_KEY,
#         "days": 16
#     }

#     # Make the request to Weatherbit API
#     response = requests.get(url, params=params)
    
#     if response.status_code == 200:
#         data = response.json()
        
#         # Extract daily forecasts
#         if 'data' in data:
#             forecast_data = [
#                 {
#                     "date": day["datetime"],
#                     "max_temp": f"{day['max_temp']}°C",
#                     "min_temp": f"{day['min_temp']}°C",
#                     "condition": day['weather']['description']
#                 }
#                 for day in data['data']
#             ]
#             return JsonResponse(forecast_data, safe=False)
        
#         else:
#             return JsonResponse({"error": "Unexpected data format received from API"}, status=500)
#     else:
#         return JsonResponse({"error": "Could not fetch forecast data"}, status=response.status_code)


def get_forecast(request):
    city = request.GET.get('city')
    country_code = request.GET.get('country_code')
    if not city or not country_code:
        return HttpResponseBadRequest("Please provide both city and country code.")
    
    url = f"{settings.WEATHERBIT_BASE_URL}/forecast/daily"
    params = {"city": city, "country": country_code, "key": settings.WEATHERBIT_API_KEY, "days": 16}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        forecast_data = [
            {
                "date": day["datetime"],
                "max_temp": day["max_temp"],
                "min_temp": day["min_temp"],
                "description": day["weather"]["description"],
                "precip": day.get("precip", 0),
                "uv": day.get("uv", 0),
                "wind_cdir_full": day["wind_cdir_full"],
                "wind_spd": day["wind_spd"]
            }
            for day in response.json()["data"]
        ]
        return JsonResponse(forecast_data, safe=False)
    else:
        return JsonResponse({"error": "Could not fetch forecast data"}, status=response.status_code)



# Retrieve the last 5 searched cities from search history
def search_history(request):
    history = SearchHistory.objects.all()[:5]
    history_data = [{"city": record.city, "country_code": record.country_code, "search_time": record.search_time} for record in history]
    return JsonResponse(history_data, safe=False)

