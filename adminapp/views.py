from django.shortcuts import render,redirect
from django.http import HttpResponse
from adminapp.models import Admin

def login(request):
  if request.method == "POST":
    email = request.POST.get("email")
    password = request.POST.get("password")
    
    admin = Admin.objects.filter(email = email,password=password).first()
    
    if(admin):
      request.session["admin_id"] = admin.id
      request.session["admin_name"] = admin.username
      request.session["admin_email"] = admin.email
      return redirect("admin_dashboard_link")
    else:
      return HttpResponse("Invalid credentials")
  else:
    return render(request,"adminapp/login.html")
  
  
def dashboard(request):
  admin_name = request.session.get("admin_name")
  return render(request,"adminapp/dashboard.html",{"admin_name":admin_name})


def adminprofile(request):
  admin_id = request.session.get("admin_id")
  admin = Admin.objects.get(id = admin_id)
  return render(request,"adminapp/admin_profile.html",{"admin":admin})

def updateAdminProfile(request):
  if request.method=="POST":
    username = request.POST.get("username")
    email = request.POST.get("email")
    phone = request.POST.get("phone")
    admin_pic = request.FILES.get("admin_pic")
    
    admin_id = request.session.get("admin_id")
    admin = Admin.objects.filter(id=admin_id).first()
    admin.username = username
    admin.email = email
    admin.phone=phone
    admin.admin_pic=admin_pic
    admin.save()
    return redirect("admin_profile_link")
  else:
    return render(request,"adminapp/admin_profile_update.html")


