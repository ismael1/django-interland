from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from django.http import Http404

from django.views.decorators.clickjacking import xframe_options_sameorigin
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.decorators import api_view

from rest_framework.response import Response
from django.http import JsonResponse, HttpResponse
from django.db.models import Count

from django.db.models.query_utils import Q

from .models import Proveedor, ContactoP, FilesP, DataComplementaryP, RutasP
from .serializers import ProveedorSerializer, ProveedoresSerializer, ContactoPSerializer, ContactoProSerializer, FilesPSerializer, FilesProSerializer, DataComplementaryPSerializer, RutasPSerializer, RutasSerializer

class ProveedorViewSet(viewsets.ModelViewSet):
    queryset = Proveedor.objects.all()
    serializer_class = ProveedorSerializer

class ContactoPViewSet(viewsets.ModelViewSet):
    queryset = ContactoP.objects.all()
    serializer_class = ContactoPSerializer

class FilesPViewSet(viewsets.ModelViewSet):
    queryset = FilesP.objects.all()
    serializer_class = FilesPSerializer

class DataComplementaryPViewSet(viewsets.ModelViewSet):
    queryset = DataComplementaryP.objects.all()
    serializer_class = DataComplementaryPSerializer

class RutasPViewSet(viewsets.ModelViewSet):
    queryset = RutasP.objects.all()
    serializer_class = RutasPSerializer

#Rutas
class ListRutas(APIView):
    def get_object(self, idProvider):
        try:
            resul = RutasP.objects.filter(idProvider=idProvider)
            return resul
        except RutasP.DoesNotExist:
            return Http404
    
    def get(self, request, idProvider, format=None):        
        ruta = self.get_object(idProvider)
        serializer = RutasSerializer(ruta,many=True)
        return Response(serializer.data)

#Lista Archivos
class ListFiles(APIView):
    def get_object(self, idProvider):
        try:
            return FilesP.objects.filter(idProvider_id=idProvider)
        except FilesP.DoesNotExist:
            return Http404
    
    def get(self, request, idProvider, format=None):        
        files = self.get_object(idProvider)
        serializer = FilesProSerializer(files,many=True)
        return Response(serializer.data)

class ListContacts(APIView):
    def get_object(self, idProvider):
        try:
            return ContactoP.objects.filter(idProvider=idProvider)
        except ContactoP.DoesNotExist:
            return Http404
    
    def get(self, request, idProvider, format=None):        
        contacto = self.get_object(idProvider)
        serializer = ContactoProSerializer(contacto,many=True)
        return Response(serializer.data)

class ContactDetail(APIView):
    def get_object(self, idProvider):
        # print(idCliente)
        try:
            return ContactoP.objects.get(id=idProvider)
        except ContactoP.DoesNotExist:
            return Http404
    
    def get(self, request, idProvider, format=None):
        
        contacto = self.get_object(idProvider)
        serializer = ContactoProSerializer(contacto)
        return Response(serializer.data)

class ProviderDetail(APIView):    
    def get_object(self, idProvider):
        try:
            return Proveedor.objects.get(id=idProvider)
        except Proveedor.DoesNotExist:
            return Http404
    
    def get(self, request, idProvider, format=None):
        
        provee = self.get_object(idProvider)
        serializer = ProveedoresSerializer(provee)
        return Response(serializer.data)

class ListDataComplementary(APIView): #Agregado David 310521
    def get_object(self, idProvider):
        try:
            return DataComplementaryP.objects.get(idProvider=idProvider)
        except DataComplementaryP.DoesNotExist:
            return Http404

    def get(self, request, idProvider, format=None):
        
        datacomplementary = self.get_object(idProvider)
        serializer = DataComplementaryPSerializer(datacomplementary)
        return Response(serializer.data)

#AutoComplete
@csrf_exempt 
@api_view(['POST', 'GET'])
def searchProveedor(request):
    dato = request.data.get('data')

    if dato:
        servicio = Proveedor.objects.filter(name__icontains=dato)
        serializer = ProveedoresSerializer(servicio, many=True)
        return Response(serializer.data)
    else:
        return Response({"no result": []})

#Agregar Archivos
@csrf_exempt 
@api_view(['POST', 'GET'])
def addFiles(request):  

    files_ = request.FILES.get('files_')
    idProveedor = request.POST.get('idCustomer')
    tipo = request.POST.get('tipo')

    goods_obj = FilesP.objects.create(name=files_, ruta=files_, tipo=tipo, statuspdf=0, idProvider_id=idProveedor)
    serializer = FilesProSerializer(goods_obj)
    return Response(serializer.data)

#Mostrar PDF
@csrf_exempt 
@api_view(['POST', 'GET'])
def showpDF(request):

    idF = request.POST.get('idFile')
    resume = FilesP.objects.get(id=idF)
    ru2='media/' + str(resume.ruta)
    namef= str(resume.name)
    ru='http://127.0.0.1:8000/' + ru2

    try:
        return HttpResponse(ru, content_type='application/pdf')
    except FileNotFoundError:
        raise Http404()

@csrf_exempt 
@api_view(['POST'])
def consultarFiles(request):
    
    proveedor = request.data.get('idProvider_id')
    tipofile = request.data.get('tipo')

    if proveedor:
        buscar = FilesP.objects.filter(idProvider_id=proveedor).filter(tipo=tipofile)
        # red = str(buscar.query)
        # print (red)
        serializer = FilesProSerializer(buscar, many=True)
        return Response(serializer.data)
    else:
        return Response({"no result": []})

@csrf_exempt 
@api_view(['GET'])
def ListProviderFiltro(request):

        page = int(request.GET.get('page', 1))
        size = int(request.GET.get('size', 1))
        palabra = str(request.GET.get('palabra', 1))
        data_start = (page - 1) * size
        data_end = page * size

        if (palabra == ""):            
            goodslist=Proveedor.objects.all()[data_start:data_end]
            count=Proveedor.objects.count()

        else:   
            goodslist = Proveedor.objects.filter(Q(name__icontains=palabra) | Q(name__icontains=palabra))[data_start:data_end]
            count=Proveedor.objects.filter(Q(name__icontains=palabra) | Q(name__icontains=palabra))[data_start:data_end].count()

        goods_ser=ProveedoresSerializer(goodslist,many=True)
        return Response({
            'total':count,
            'data':goods_ser.data
        })