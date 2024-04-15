from django.http import JsonResponse
from rest_framework.decorators import api_view
from .models import Weather
from .serializers import WeatherDataSerializer

@api_view(['GET'])
def weather_view(request, pk):
    try:
        weather = Weather.objects.get(pk=pk)
    except Weather.DoesNotExist:
        return JsonResponse({'error': 'Weather not found'}, status=404)

    serializer = WeatherDataSerializer(weather)
    return JsonResponse(serializer.data, safe=False)