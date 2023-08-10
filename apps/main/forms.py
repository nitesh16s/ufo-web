from django import forms
from apps.main.models import Query, WorkWithUs


class QueryForm(forms.ModelForm):
    class Meta:
        model = Query
        fields = ['query']