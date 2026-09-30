from django.shortcuts import render,redirect
from django.http import HttpResponse
from userapp.models import User

def user_signup(request):
  if request.method == "POST":
    username = request.POST.get("username")
    email = request.POST.get("email")
    phone = request.POST.get("phone")
    password = request.POST.get("password")
    
    User.objects.create(username=username,email=email,phone=phone,password=password)
    return redirect("user_signup_link")
  else:
    return render(request,"userapp/signup.html")
  
  
def user_login(request):
  if request.method=="POST":
    email = request.POST.get("email")
    password = request.POST.get("password")
    
    user = User.objects.filter(email=email,password=password).first()
    if(user):
      request.session["user_id"] = user.id
      request.session["user_name"] = user.username
      request.session["user_email"] = user.email
      return HttpResponse("Login Success")
    else:
      return HttpResponse("Invalid Credentials")
  else:
    return render(request,"userapp/login.html")
