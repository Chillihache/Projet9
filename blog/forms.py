from django.forms import Form, ModelForm, CharField

from blog.models import Ticket, Review

class FollowForm(Form):
    username = CharField()

class TicketForm(ModelForm):
    class Meta:
        model = Ticket
        fields = ('title', 'description', 'image')


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ('headline', 'rating', 'body')