from django.conf import settings
from django.shortcuts import get_object_or_404, render
import json
from .models import Checkout
import razorpay
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

# JS Submit razorepay resoponse to backend
@csrf_exempt
def handle_razorpay_response(request):
    """Callback after payment success"""
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))

        # Razorpay sends these fields
        payment_id = data.get("razorpay_payment_id")
        order_id = data.get("razorpay_order_id")
        signature = data.get("razorpay_signature")

        # ✅ Verify payment signature
        try:
            razorpay_client.utility.verify_payment_signature({
                "razorpay_order_id": order_id,
                "razorpay_payment_id": payment_id,
                "razorpay_signature": signature
            })

            # update to checkout record
            checkout = get_object_or_404(Checkout, order_id=order_id)
            checkout.payment_id = payment_id
            checkout.signature = signature
            checkout.status = "paid"
            checkout.save()

            
            # Save payment details to DB here if needed
            return JsonResponse({
                "status": "Payment verified successfully!",
                "razorpay_payment_id": payment_id,
                "razorpay_order_id": order_id
            })
        
        except razorpay.errors.SignatureVerificationError:
            return JsonResponse({"status": "Payment verification failed!"}, status=400)

    return JsonResponse({"error": "Invalid request"}, status=400)

def checkout(request, order_id):
    checkout = get_object_or_404(Checkout, order_id=order_id)
    project = checkout.visit.project
    return render(request, "payment/checkout.html", {"checkout": checkout, "project": project, "razorpay_key": settings.RAZORPAY_KEY_ID})

def payment_status_page(request, order_id):
    checkout = get_object_or_404(Checkout, order_id=order_id)
    project = checkout.visit.project
    return render(request, "payment/payment_status_page.html", {"amount": 2001.00, "checkout": checkout, "project": project})

