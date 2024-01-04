from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView

from api.inventory.models import Product
from api.inventory.serializers import (ProductSerializer, PurchaseSerializer,
                                       SalesSerializer)


class ProductView(APIView):
  """
  商品操作に関する関数
  """
  
  def get_object(self, pk):
    """
    商品操作に関する関数で共通で使用する商品取得関数
    """
    try:
      return Product.objects.get(pk=pk)
    except Product.DoesNotExist:
      raise NotFound

  def get(self, request, id=None, format=None):
    """
    商品の一覧もしくは一意の商品を取得する
    """
    if id is None:
      queryset = Product.objects.all()
      serializer = ProductSerializer(queryset, many=True)
    else:
      product = self.get_object(id)
      serializer = ProductSerializer(product)
    return Response(serializer.data, status.HTTP_200_OK)

  def post(self, request, format=None):
    """
    商品を登録する
    """
    serializer = ProductSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status.HTTP_201_CREATED)
  
  def put(self, request, id, format=None):
    """
    商品の情報を更新する
    """
    product = self.get_object(id)
    serializer = ProductSerializer(instance=product, data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status.HTTP_200_OK)


class PurchaseView(APIView):
  def post(self, request, format=None):
    """
    仕入れ情報を登録する
    """
    serializer = PurchaseSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status.HTTP_201_CREATED)


class SalesView(APIView):
  def post(self, request, format=None):
    """
    売上情報を登録する
    """
    serializer = SalesSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status.HTTP_201_CREATED)
