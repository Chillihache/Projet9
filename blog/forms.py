from django.forms import Form, ModelForm, CharField, TextInput, ChoiceField, RadioSelect

from blog.models import Ticket, Review


class FollowForm(Form):
    username = CharField(
        widget=TextInput(attrs={"placeholder": "Nom d'utilisateur"})
    )


class TicketForm(ModelForm):
    class Meta:
        model = Ticket
        fields = ('title', 'description', 'image')
        labels = {
            "title": "Titre",
        }


class ReviewForm(ModelForm):
    RATING_CHOICES = [
        (0, '0'),
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    ]
    rating = ChoiceField(choices=RATING_CHOICES, widget=RadioSelect(attrs={"class": "d-flex  justify-content-evenly text-center"}), label="Note")

    class Meta:
        model = Review
        fields = ('headline', 'rating', 'body')
        labels = {
            'headline': 'Titre',
            'body': 'Commentaire',
        }
