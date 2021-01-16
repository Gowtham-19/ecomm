from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt

import braintree


gateway = braintree.BraintreeGateway(
    braintree.Configuration(
        braintree.Environment.Sandbox,
        merchant_id="qfj747842mwgv4ny",
        public_key="gmvf3rnvsrxwtkyp",
        private_key="fbe5bf52afdb2db338c3ba43694fdfb7"
    )
)

@csrf_exempt
def generate_token(request,id,token):
    if not validate_user_session(id,token):
        return JsonResponse({"error":"Invalid session please login again!"})
    return JsonResponse({'clientToken':gateway.client_token.generate()})

@csrf_exempt
def process_payment(request,id,token):
    if not validate_user_session(id,token):
        return JsonResponse({"error":"Invalid session please login again!"})
    return JsonResponse({'clientToken':gateway.client_token.generate()})
    nonce_from_the_client = request.POST["paymentMethodNonce"]
    amount_from_the_client = request.POST["amount"]

    result = gateway.transaction.sale({
        "amount":amount_from_the_client,
        "payment_method_nonce":nonce_from_the_client,
        "options":{
            "submit_for_settlement":True
        }
    })

    if result.is_success:
        return JsonResponse({
            "Successs":result.is_success,"transaction":{'id':result.transaction.id,'amount':result.transaction}
            })
    else:
        return JsonResponse({'error':True,'sucess':False})

def validate_user_session(id,token):
    UserModel = get_user_model()
    try:
        user =UserModel.objects.get(pk=id)
        if user.session_token == token:
            return True
        return False        
    except Exception:
        return False 

