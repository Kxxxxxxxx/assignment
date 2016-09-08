from django import forms


class HpForm(forms.Form):
    address = forms.CharField()
