from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .serializers import UserSerializer 
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login,logout
from .models import CustomUser
from django.http import JsonResponse
import random
import re 

#generating random token
def generate_session_token(length=10):
    return ''.join(random.SystemRandom().choice([ chr(i) for i in range(97,123)] + [str(i) for i in range(10)]) for _ in range(length))

#sign method
@csrf_exempt
def signin(request):
    if not request.method == 'POST':
        return JsonResponse({'error':'send a post request with valid parameters'})
    
    # is_private = request.POST.get('is_private', False)
    username = request.POST.get('email',False)
    print("username from postman",username)
    password = request.POST.get('password',False) 
    
    #validation part
    # if not  re.match("([\w\.\-_]+)?\w+@[\w-_]+(\.\w+){1,}/igm",username):
    #     return JsonResponse({'error':'Enter a valid email'})
    if len(password)<3:
        return JsonResponse({'error':'Passsowrd needs to be at least of 3'})
    
    
    UserModel = get_user_model()
    
    try:
        user = UserModel.objects.get(email=username)#fetching user basing on email
        
        if user.check_password(password):#password checking
            user_dict = UserModel.objects.filter(
                email= username).values().first()
            user_dict.pop('password')
            
            if user.session_token != "0":#session expiring
                user.session_token = "0"
                user.save()
                return JsonResponse({'error':"previous session exists!"})
           
            token = generate_session_token()#generating token
            user.session_token = token
            user.save()
            login(request,user)
            return JsonResponse({'token':token,'user':user_dict})
        else:
            return JsonResponse({'error':"Invalid password"})
    except UserModel.DoesNotExist:
        return JsonResponse({'error':'Invalid Email'})

#sign out method

def signout(request,id):
    logout(request)
   
    UserModel = get_user_model()
    try:
        user = UserModel.objects.get(pk=id) 
        user.session_token = "0"
        user.save()
        return JsonResponse({'success':'Logout Success'})
    except UserModel.DoesNotExist:
        return JsonResponse({'error':'Invalid user ID'})
   
class UserViewSet(viewsets.ModelViewSet):#serializer view
    permission_classes_by_action = {'create':[AllowAny]}
    
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
            
        except KeyError:
            return [permission() for permission in self.permission_classes]
   
 