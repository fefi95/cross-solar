from rest_framework import viewsets, status
from rest_framework.views import APIView, Response
from django.db.models import Avg, Sum, Min, Max
from django.db.models.functions import TruncDay
from .models import Panel, OneHourElectricity
from .serializers import PanelSerializer, OneHourElectricitySerializer

class PanelViewSet(viewsets.ModelViewSet):
    queryset = Panel.objects.all()
    serializer_class = PanelSerializer

class HourAnalyticsView(APIView):
    serializer_class = OneHourElectricitySerializer
    def get(self, request, panelid):
        panelid = int(self.kwargs.get('panelid', 0))
        queryset = OneHourElectricity.objects.filter(panel_id=panelid)
        items = OneHourElectricitySerializer(queryset, many=True)
        return Response(items.data)
    def post(self, request, panelid):
        panelid = int(self.kwargs.get('panelid', 0))
        serializer = OneHourElectricitySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DayAnalyticsView(APIView):
    def get(self, request, panelid):
        # Please implement this method to return Panel's daily analytics data
        queryset = OneHourElectricity.objects.filter(panel_id=panelid)\
                .annotate(datetime=TruncDay('date_time')).values('datetime') \
                .annotate(
                    sum=Sum('kilo_watt'),
                    average=Avg('kilo_watt'),
                    maximum=Max('kilo_watt'),
                    minimum=Min('kilo_watt')
                )
        print(queryset)
        # return Response([{
        #     "date_time": "[date for the day]",
        #     "sum": 0,
        #     "average": 0,
        #     "maximum": 0,
        #     "minimum": 0
        # }])
        return Response(queryset)
