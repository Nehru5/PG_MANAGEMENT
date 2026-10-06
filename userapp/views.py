from django.shortcuts import render,redirect
from django.http import HttpResponse
from userapp.models import User,UserProfile,Booking
from adminapp.models import Room,Bed

def homepage(request):
  return render(request,"adminapp/home.html")

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
      return redirect("user_dashboard_link")
    else:
      return HttpResponse("Invalid Credentials")
  else:
    return render(request,"userapp/login.html")
  
def userDashboard(request):
  if "user_name" not in request.session:
    return redirect("user_login_link")
  username = request.session.get("user_name")
  rooms = Room.objects.all()
  return render(request,"userapp/dashboard.html",{"username":username,"rooms":rooms})


def user_profile_update(request):
  if "user_name" not in request.session:
    return redirect("user_login_link")
  
  if request.method=="POST":
    city = request.POST.get("city")
    pincode = request.POST.get("pincode")
    state = request.POST.get("state")
    country = request.POST.get("country")
    address = request.POST.get("address")
    bio = request.POST.get("bio")
    aadhar_no = request.POST.get("aadhar_no")
    aadhar_image = request.FILES.get("aadhar_image")
    profile_pic = request.FILES.get("profile_pic")
    
    user_id = request.session.get("user_id")
    user = User.objects.get(id = user_id)
    
    UserProfile.objects.create(
      user=user,
      city=city,
      pincode=pincode,
      state=state,
      country=country,
      address = address,
      bio=bio,
      aadhar_no=aadhar_no,
      aadhar_image=aadhar_image,
      profile_pic=profile_pic
    )
    return redirect("user_dashboard_link")
  else:
    return render(request,"userapp/user_profile_update.html")
  
def user_profile(request):
  if "user_name" not in request.session:
    return redirect("user_login_link")
  user_id = request.session.get("user_id")
  # user = User.objects.get(id = user_id)
  user_data = UserProfile.objects.filter(id = user_id).first()
  return render(request,"userapp/user_profile.html",{"user_data":user_data})

def user_room_view(request,id):
  if "user_name" not in request.session:
    return redirect("user_login_link")
  
  room = Room.objects.get(id=id)
  bed = Bed.objects.filter(room = room)
  return render(request,"userapp/user_room_view.html",{"room":room,"beds":bed})

  
def book_room(request,room_id,bed_id):
  if "user_name" not in request.session:
    return redirect("user_login_link")
  
  if request.method=="POST":
    user_id = request.session.get("user_id")
    user = User.objects.get(id = user_id)
    room = Room.objects.get(id = room_id)
    bed = Bed.objects.get(id = bed_id)
    
    existing_booking = Booking.objects.filter(
      user = user,
      status__in=["Pending","Approved"]
      ).first()
    
    if existing_booking:
      return HttpResponse("You already Booked this room")
    
    if bed.status != "Available":
      return HttpResponse("Bed is not available, already booked")
    
    Booking.objects.create(user = user,room = room,bed = bed,status="Pending")
    return redirect("user_dashboard_link")
  return redirect("user_dashboard_link")
    
    
  

  
    
  
  


