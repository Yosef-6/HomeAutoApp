from django.forms import ModelForm , TextInput

from .models import Device

class DeviceRegistryForm(ModelForm):
    class Meta:
        model = Device
        fields= [
            'deviceName',
            'pinNumber',
            'modeOperation',
            'unit',
            'usage',
            'node'
        ]
        widgets = { "node": TextInput(attrs={'readonly': 'readonly', 'placeHolder' : 'Current Hardware Unit','style':'display:none;'} ) }

        