from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, DeleteView
from django.views.generic import ListView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from blog.models import Ticket


@login_required
def home(request):
    tickets = Ticket.objects.all()
    return render(request, "blog/home.html", {"tickets": tickets})

@login_required
def posts(request):
    user = request.user
    tickets = Ticket.objects.filter(user=user)
    return render(request, "blog/posts.html", {"tickets": tickets})

class CreateTicket(LoginRequiredMixin, CreateView):
    template_name = "blog/create_ticket.html"
    model = Ticket
    fields = ('title', 'description', 'image')
    success_url = reverse_lazy('blog:posts')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)

class DeleteTicket(LoginRequiredMixin, DeleteView):
    model = Ticket
    success_url = reverse_lazy('blog:posts')


