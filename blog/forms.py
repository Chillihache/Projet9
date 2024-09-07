from django import forms
from blog.models import Ticket


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ["title", "description", "image"]

    title = forms.CharField(max_length=128, label="Titre")
    description = forms.CharField(max_length=2048, required=False,
                                  widget=forms.Textarea(attrs={"rows": 4, "cols": 40}),
                                  label="Description")
    image = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={'multiple': False}))
