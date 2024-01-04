from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.inventory.models import Product
from api.inventory.serializers import (ProductSerializer, PurchaseSerializer,
                                       SalesSerializer)


class ProductView(APIView):
  """
  商品操作に関する関数
  """
  
  def get_product_data(self, request, format=None):
    """
    商品の一覧を取得する
    """
    queryset = Product.objects.all()
    serializer = ProductSerializer(queryset, many=True)
    return Response(serializer.data, status.HTTP_200_OK)

  def post_product_data(self, request, format=None):
    """
    商品を登録する
    """
    serializer = ProductSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status.HTTP_201_CREATED)


class PurchaseView(APIView):
  def post_purchase_data(self, request, format=None):
    """
    仕入れ情報を登録する
    """
    serializer = PurchaseSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status.HTTP_201_CREATED)


class SalesView(APIView):
  def post_sales_data(self, request, format=None):
    """
    売上情報を登録する
    """
    serializer = SalesSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status.HTTP_201_CREATED)
