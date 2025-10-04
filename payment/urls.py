from django.urls import path
from . import views

urlpatterns = [
    # accounts
    path("checkout/<str:order_id>/", views.checkout, name="checkout"),
    path("status/<str:order_id>/", views.payment_status_page, name="payment_status_page"),
    path('handle-gateway-response/', views.handle_razorpay_response, name='handle_razorpay_response'),
]
