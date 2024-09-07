from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from blog import forms, models


@login_required
def home(request):
    tickets = models.Ticket.objects.all()
    return render(request, "blog/home.html", {"tickets": tickets})


@login_required
def posts(request):
    user = request.user
    tickets = models.Ticket.objects.filter(user=user)
    return render(request, "blog/posts.html", {"tickets": tickets})


class CreateTicket(LoginRequiredMixin, View):
    template_name = "blog/create_ticket.html"
    form_class = forms.TicketForm

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect('home')
        return render(request, self.template_name, {"form": form})


@login_required()
def delete_ticket(request, ticket_id):
    ticket = models.Ticket.objects.get(id=ticket_id)
    ticket.delete()
    return redirect('posts')

