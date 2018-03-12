from django import forms
from main.models import Evaluation

class EvaluationForm(forms.ModelForm):
    class Meta:
        model = Evaluation
        exclude = ["house", "user"]
