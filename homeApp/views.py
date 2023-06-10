from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect,HttpResponse
from homeApp.models import *
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .forms import DeviceRegistryForm
def home(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))    
    return render(request,"homeApp/index.html",{
         "Hardware"   :  User.objects.all().filter(username=request.user.username)[0].unit.all()
    })
           
def login_view(request):
    if request.method == "POST":
        username=request.POST["username"]
        password=request.POST["password"]
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return HttpResponseRedirect(reverse("index"))
        else:
             return render(request,"homeApp/login.html",{
                "message" : "Invalid credentials"
             })
    return render(request,"homeApp/login.html")

def logout_view(request):
    logout(request)
    return render(request,"homeApp/login.html" ,{
        "message" : "Logged out",
    })
    pass

@csrf_exempt
@login_required
def device_list(request,ID):
    hardware =  Hardware.objects.all().filter(hardwareID=ID).first()
    if(hardware is None ) or (hardware.owner != request.user):
        return HttpResponseRedirect(reverse("index"),{
               "message" : "Invalid HardwareID Requested",
               "Hardware"   :  User.objects.all().filter(username=request.user.username)[0].unit.all()
        })#render index
    ## render the device list
    if request.method == "PUT":
        data = json.loads(request.body)
        pin  = data["PIN"]
        usage=data["USAGE"]
        val  =data["VAL"]
    
        if data is None or usage is None or val is None:
            return JsonResponse({"message": "Key attributes are missing"}, status=400)


        device = hardware.Entries.all().filter(pinNumber=pin).all().first()

        if device is None:
            return JsonResponse({"message": "Device missing"}, status=400)
          
        if(usage == "bool"):
          device.state = val

        else:
            try:
                fval = float(val)
                if (fval >= -50.0 and fval <= 50.0):
                    device.floatValue = val
                else:
                    return HttpResponse(status=400)
            except:
                   return HttpResponse(status=400)
        device.save()
        return HttpResponse(status=204)
    if request.method == "GET":
        
        return render(request,"homeApp/deviceList.html",{
            "node"         :  hardware, # easy access
            "DeviceList"   :  hardware.Entries.all(),
            "form"         :  DeviceRegistryForm()
        })
     
@login_required   
def device_list_updated(request,ID):
     hardware =  Hardware.objects.all().filter(hardwareID=ID).first()
     if(hardware is None ) or (hardware.owner != request.user):
        return JsonResponse({"message": "Unoutherized request"}, status=400)
     
     if(request.method == "GET"):
       return JsonResponse([ i.serialize() for i in hardware.Entries.all() ],safe=False)
     else:
        return JsonResponse({"message": "Unoutherized request"}, status=400)

       

@login_required
def create_device(request,ID):
        hardware =  Hardware.objects.all().filter(hardwareID=ID).first()
        if(hardware is None ) or (hardware.owner != request.user):
           return  render(request,"homeApp/index.html",{
               "message" : "Invalid HardwareID Requested",
               "Hardware"   :  User.objects.all().filter(username=request.user.username)[0].unit.all()
        })
         
        if request.method == "POST":
           
           form = DeviceRegistryForm(request.POST)

           context = {
                "node"         :  hardware,
                "DeviceList"   :  hardware.Entries.all(),
                "form"         :  DeviceRegistryForm(),
                
           }
           
           if(form.is_valid()):
                node = form.cleaned_data.get("node") 
                pin  = form.cleaned_data.get("pinNumber")
                devicename = form.cleaned_data.get("deviceName")
                if(hardware.Entries.filter(deviceName=devicename).first() is not None ):
                  context["message"]="Device name is already in use in current Hardware unit"
                  return render(request,"homeApp/deviceList.html", context)
                if(hardware.Entries.filter(pinNumber=pin).first() is not None ):
                  context["message"]="Pin number already in use in current Hardware unit"
                  return render(request,"homeApp/deviceList.html", context)

                obj = form.save(False)
                obj.node = hardware 
                obj.save()
                return HttpResponseRedirect(reverse("deviceList",kwargs={'ID':ID}))
           else:
               context["message"]="Failed to attach a new device"
               context["form"]=form
               return render(request,"homeApp/deviceList.html", context)

        else:
            return JsonResponse({"message": "Unoutherized request"}, status=400)

@csrf_exempt
@login_required
def delete_device(request,ID):
    hardware =  Hardware.objects.all().filter(hardwareID=ID).first()
    if(hardware is None ) or (hardware.owner != request.user):
           return  render(request,"homeApp/index.html",{
               "message" : "Invalid HardwareID Requested",
               "Hardware"   :  User.objects.all().filter(username=request.user.username)[0].unit.all()
    })
  
    if request.method  == "DELETE":
       data = json.loads(request.body)
       pin  = data["PIN"]
       deviceToDetach  = hardware.Entries.filter(pinNumber=pin).first()
       if( deviceToDetach is not None ):
           deviceToDetach.delete()
           return JsonResponse({"message": "Done"}, status=200)
       else:
         JsonResponse({"message": "No device found with the given pin number"}, status=400)
        
    else:
     return JsonResponse({"message": "Invalid request"}, status=400)

@csrf_exempt
def hardware_query(request,ID):
    hardware =  Hardware.objects.all().filter(hardwareID=ID).first()
    if(hardware is None ):
        return JsonResponse({"message": "Restricted"}, status=400)
    if request.method == "GET":
       return JsonResponse([ i.serialize() for i in hardware.Entries.all() ],safe=False)
    if request.method == "PUT":
       data = json.loads(request.body)
       pin  = data["PIN"]
       usage=data["USAGE"]
       val  =data["VAL"]
       
       if data is None or usage is None or val is None:
            return JsonResponse({"message": "Key attributes are missing"}, status=400)
       device = hardware.Entries.all().filter(pinNumber=pin).all().first()
       if device is None:
          return JsonResponse({"message": "Device missing"}, status=400)
       if(usage == "bool"):
          device.state = val
       else:
            try:
                fval = float(val)
                if (fval >= -50.0 and fval <= 50.0):
                    device.floatValue = val
                else:
                    return HttpResponse(status=400)
            except:
                   return HttpResponse(status=400)
       device.save()
       return HttpResponse(status=204)

    