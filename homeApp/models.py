from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Hardware(models.Model):
    hardwareID = models.BigIntegerField(primary_key=True)
    name       = models.CharField(max_length=100,null=False,default="not specified")
    owner      = models.ForeignKey(User,on_delete=models.CASCADE,related_name="unit")
    

class Device(models.Model):
      deviceName    = models.CharField(max_length=200)
      pinNumber     = models.PositiveSmallIntegerField()
      input = "INPUT"
      output= "OUTPUT"
      oprChoices =[
     (input,"INPUT"),
     (output,"OUTPUT"),
     ] 
      modeOperation = models.CharField(max_length=6,choices=oprChoices,default=output)
      boolType = "bool"
      floatType= "float"
      usageChoices = [
        (boolType,"bool"),
        (floatType,"float")
      ]
      amp = "amps"
      volt= "volt"
      temp= "°C"
      rpm = "rpm"
      degs= "°"
      unitChoices = [
        (degs,"amps"),
        (amp,"amps"),
        (volt,"volt"),
        (temp,"°C"),
        (rpm,"rpm"),
      ]
      unit          = models.CharField(max_length=20,choices=unitChoices,default=amp)
      usage         = models.CharField(max_length=7,choices=usageChoices,default=boolType)
      state         = models.BooleanField(default=False) #on or off
      floatValue    = models.FloatField(default=0.0,validators=[MinValueValidator(-50.0), MaxValueValidator(50.0)])
      node          = models.ForeignKey(Hardware,on_delete=models.CASCADE,related_name="Entries",blank=True)

      def serialize(self):
        return {
            "pinNumber"    :self.pinNumber,
            "usage"        :self.usage,
            "state"        :self.state,
            "floatValue"   :self.floatValue,
            "deviceName"   :self.deviceName,
            "modeOperation":self.modeOperation,
            "unit"         : self.unit,
        }
      
