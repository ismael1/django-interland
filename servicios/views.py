import datetime
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from django.views.decorators.clickjacking import xframe_options_sameorigin
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.decorators import api_view

from rest_framework.response import Response
from django.db.models import Count

from .models import Services
from .serializers import ServicesSerializer, ServiciosSerializer, ServiciosCotizacionesSerializer, getIdSerializers
from django.db.models.query_utils import Q

class ServicesViewSet(viewsets.ModelViewSet):
    # authentication_classes = (BasicAuthentication,)
    # permission_classes = (IsAuthenticated,)
    queryset = Services.objects.filter(Q(status=1))
    serializer_class = ServicesSerializer


@csrf_exempt 
@api_view(['POST', 'GET'])
def serviciosLista(request):
    dato = request.data.get('aplica')

    if dato:
        servicio = Services.objects.filter(aplica__icontains=dato)
        # que=str(servicio.query)
        # print(que)
        serializer = ServiciosSerializer(servicio, many=True)
        return Response(serializer.data)
    else:
        return Response({"no result": []})
    

@csrf_exempt 
@api_view(['POST', 'GET'])
def searchService(request):
    dato = request.data.get('data')

    if dato:
        servicio = Services.objects.filter(nameproduct__icontains=dato)
        # que=str(servicio.query)
        # print(que)
        serializer = ServiciosSerializer(servicio, many=True)
        return Response(serializer.data)
    else:
        return Response({"no result": []})

@csrf_exempt
@api_view(['GET'])
def ListServicioCotizacionesFiltro(request):

    page = int(request.GET.get('page', 1))
    size = int(request.GET.get('size', 1))
    palabra=str(request.GET.get('palabra', 1))
    data_start = (page - 1) * size
    data_end = page * size

    if (palabra == ""):
        goodslist = Services.objects.filter(Q(status=1) | Q(status=0))[data_start:data_end]
        count = Services.objects.filter(Q(status=1) | Q(status=0)).count()
    else:
        goodslist = Services.objects.filter(Q(nombreProductoServicios__icontains=palabra) | Q(duracion__icontains=palabra) | Q(tiempo__icontains=palabra)).filter(Q(status=1) | Q(status=0))[data_start:data_end]
        count=Services.objects.filter(Q(nombreProductoServicios__icontains=palabra) | Q(duracion__icontains=palabra) | Q(tiempo__icontains=palabra)).filter(Q(status=1) | Q(status=0))[data_start:data_end].count()

    goods_ser = ServiciosCotizacionesSerializer(goodslist,many=True)

    return Response({
        'total':count,
        'data':goods_ser.data
    })

@csrf_exempt 
@api_view(['POST'])
def obtenerId(request):

    consecutivo = Services.objects.all().order_by("-id")[:1]
    serializer = getIdSerializers(consecutivo, many=True)

    return Response(serializer.data)

@csrf_exempt 
@api_view(['POST', 'GET'])
def insertServicio(request):  

    id = request.data.get('id')
    codeproduct = request.data.get('codeproduct')
    nameproduct = request.data.get('nameproduct')
    status = request.data.get('status')
    codeunit = request.data.get('codeunit')
    type = request.data.get('type')
    unit = request.data.get('unit')
    description = request.data.get('description')
 
    nuevoServ = Services.objects.create(id=id, codeproduct=codeproduct, nameproduct=nameproduct, status=status, codeunit=codeunit, unit=unit, type=type, description=description)
    serializer = ServiciosSerializer(nuevoServ)
    return Response(serializer.data)

@csrf_exempt 
@api_view(['POST', 'GET'])
def getServicio(request, pk):

    serv = Services.objects.get(id=pk)
    serializer = ServiciosSerializer(serv)
    return Response(serializer.data)

@csrf_exempt 
@api_view(['PUT'])
def updateServicios(request):
    
    idS = request.data.get('id')
    codeproduct = request.data.get('codeproduct')
    nameproduct = request.data.get('nameproduct')
    codeunit = request.data.get('codeunit')
    unit = request.data.get('unit')
    type = request.data.get('type')
    status = request.data.get('status')
    description = request.data.get('description')

    if id != 0:
        serv = Services.objects.get(id=idS)
        serv.codeproduct = codeproduct
        serv.nameproduct = nameproduct
        serv.codeunit = codeunit
        serv.unit = unit
        serv.type = type
        serv.status = status
        serv.description = description
        serv.save()
        return Response("exito")
    else:
        return Response({"no update"})
 
@csrf_exempt 
@api_view(['PUT'])
def deleteServicios(request, pk):
    
    idS = pk
    status = request.data.get('status')

    if id != 0:
        serv = Services.objects.get(id=idS)
        serv.status = status
        serv.save()
        return Response("exito")
    else:
        return Response({"no delete"})
