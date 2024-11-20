from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from rest_framework.decorators import api_view
from django.db.models.query_utils import Q
from rest_framework.views import APIView
from rest_framework.response import Response

from servicioVenta.serializers import FiltroServiceSerializer

from .models import Rutas
from .serializers import SerializerRutas

class ajustesRutasViewSet(viewsets.ModelViewSet):
    queryset = Rutas.objects.all()
    serializer_class = SerializerRutas

@csrf_exempt
@api_view(['GET'])
def ListRutaFiltro(request):

        page = int(request.GET.get('page', 1))
        size = int(request.GET.get('size', 1))
        palabra=str(request.GET.get('palabra', 1))
        data_start = (page - 1) * size
        data_end = page * size

        if (palabra == ""):
            goodslist = Rutas.objects.filter(Q(estatus=0))[data_start:data_end]
            count = Rutas.objects.filter(Q(estatus=0)).count()
        else:
            goodslist = Rutas.objects.filter(Q(origen__icontains=palabra) | Q(destino__icontains=palabra) | Q(tipoEnvio__icontains=palabra) | Q(precioKilometros__icontains=palabra)).filter(Q(estatus=0))[data_start:data_end]
            count = Rutas.objects.filter(Q(origen__icontains=palabra) | Q(destino__icontains=palabra) | Q(tipoEnvio__icontains=palabra) | Q(precioKilometros__icontains=palabra)).filter(Q(estatus=0))[data_start:data_end].count()

        goods_ser=SerializerRutas(goodslist,many=True)

        return Response({
            'total':count,
            'data':goods_ser.data
        })
