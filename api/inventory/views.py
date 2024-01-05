from django.db.models import F, Sum, Value
from django.db.models.functions import Coalesce
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView

from api.inventory import serializers
from api.inventory.exception import BusinessException
from api.inventory.models import Product, Purchase, Sales
from api.inventory.serializers import (
    InventorySerializer,
    ProductSerializer,
    PurchaseSerializer,
    SalesSerializer,
)


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

    def delete(self, request, id, format=None):
        """
        商品を削除する
        """
        product = self.get_object(id)
        product.delete()
        return Response(status=status.HTTP_200_OK)


class PurchaseView(APIView):
    """
    仕入れ操作に関する関数
    """

    def post(self, request, format=None):
        """
        仕入れ情報を登録する
        """
        serializer = PurchaseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_201_CREATED)


class SalesView(APIView):
    """
    売上操作に関する関数
    """

    def post(self, request, format=None):
        """
        売上情報を登録する
        """
        serializer = SalesSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # 在庫が売る分の数量を超えないかチェック
        # 在庫テーブルのレコードを取得
        purchase = Purchase.objects.filter(
            product_id=request.data["product"]
        ).aaggregate(quantity_sum=Coalesce(Sum("quantity"), 0))
        # 卸しテーブルのレコードを取得
        sales = Sales.objects.filter(product_id=request.data["product"]).aaggregate(
            quantity_sum=Coalesce(Sum("quantity"), 0)
        )

        #
        if purchase["purchase_sum"] < sales["quantity_sum"] + int(
            request.data["quantity"]
        ):
            raise BusinessException("在庫数量を超過することはできません")

        serializer.save()
        return Response(serializer.data, status.HTTP_201_CREATED)


class InventoryView(APIView):
    """
    仕入れ・売上情報に関する関数
    """

    def get(self, request, id=None, format=None):
        """
        仕入れ・売上情報を取得する
        """
        if id is None:
            # 件数が多くなるので商品IDは必ず指定する
            return Response(serializers.data, status.HTTP_400_BAD_REQUEST)
        else:
            # UNIONするために、それぞれのフィールド名を再定義している
            purchase = (
                Purchase.objects.filter(product_id=id)
                .prefetch_related("product")
                .values(
                    "id",
                    "quantity",
                    type=Value("1"),
                    date=F("purchase_date"),
                    unit=F("product__price"),
                )
            )
            sales = (
                Purchase.objects.filter(product_id=id)
                .prefetch_related("product")
                .values(
                    "id",
                    "quantity",
                    type=Value("2"),
                    date=F("sales_date"),
                    unit=F("product__price"),
                )
            )
            queryset = purchase.union(sales).order_by(F("date"))
            serializer = InventorySerializer(queryset, many=True)
        return Response(serializer.date, status.HTTP_200_OK)
