from django.urls import path

from api.inventory import views

urlpatterns = [
    path("products/", views.ProductView.as_view())
]
