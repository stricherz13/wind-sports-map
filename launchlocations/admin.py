from django.contrib import admin
from django.forms import ModelForm
from django import forms

from .models import LaunchLocation, Weather, Direction

admin.site.register(LaunchLocation)
admin.site.register(Weather)


class DirectionAdminForm(forms.ModelForm):
    class Meta:
        model = Direction
        fields = '__all__'
        widgets = {
            'directions': forms.CheckboxSelectMultiple
        }


class DirectionAdmin(admin.ModelAdmin):
    form = DirectionAdminForm


admin.site.register(Direction, DirectionAdmin)
