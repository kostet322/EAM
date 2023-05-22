from django import forms
from .models import Asset,Maintenance,Repair

class AssetForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = ['asset_name', 'asset_serial_number', 'asset_description', 'location', 'date_purchased', 'cost']


class MaintenanceForm(forms.ModelForm):
    class Meta:
        model = Maintenance
        exclude = ['asset']

class RepairForm(forms.ModelForm):
    class Meta:
        model = Repair
        exclude = ['asset']

class AssetDeleteForm(forms.ModelForm):
    class Meta:
                model = Asset
                fields = []

    def delete(self):
                self.instance.delete()