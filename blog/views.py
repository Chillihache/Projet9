from django.shortcuts import render, redirect
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, DeleteView, UpdateView, View
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from authentication.models import User
from blog.models import Ticket, Review, UserFollows
from blog.forms import FollowForm, TicketForm, ReviewForm


@login_required
def home(request):
    user = request.user
    follows = UserFollows.objects.filter(user=user)
    tickets_and_reviews = list(Ticket.objects.filter(user=user)) + list(Review.objects.filter(user=user))
    for follow in follows:
        tickets_and_reviews += list(Ticket.objects.filter(user=follow.followed_user))
        tickets_and_reviews += list(Review.objects.filter(user=follow.followed_user))
    tickets_and_reviews += list(Review.objects.filter(ticket__user=user).exclude(user=user))
    tickets_and_reviews = sorted(tickets_and_reviews, key=lambda obj: obj.time_created, reverse=True)
    rating_range = range(1, 6)
    user_reviews_ticket_ids = list(Review.objects.filter(user=user).values_list('ticket_id', flat=True))
    return render(request, "blog/home.html", {"tickets_and_reviews": tickets_and_reviews,
                                              "rating_range": rating_range, "user_reviews_ticket_ids": user_reviews_ticket_ids})


@login_required
def posts(request):
    user = request.user
    tickets_and_reviews = list(Ticket.objects.filter(user=user)) + list(Review.objects.filter(user=user))
    tickets_and_reviews = sorted(tickets_and_reviews, key=lambda obj: obj.time_created, reverse=True)
    rating_range = range(1, 6)
    return render(request, "blog/posts.html", {"tickets_and_reviews": tickets_and_reviews,
                                               "rating_range": rating_range})


@login_required
def follows(request):
    return render(request, "blog/follow.html")


class CreateTicket(LoginRequiredMixin, CreateView):
    template_name = "blog/create_ticket.html"
    model = Ticket
    fields = ('title', 'description', 'image')
    success_url = reverse_lazy('blog:posts')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["title"].label = "Titre"
        form.fields["title"].widget.attrs.update({"placeholder": "Titre"})
        return form

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)


class DeleteTicket(LoginRequiredMixin, DeleteView):
    model = Ticket
    success_url = reverse_lazy('blog:posts')

    def dispatch(self, request, *args, **kwargs):
        ticket = self.get_object()
        if ticket.user != request.user:
            return redirect('blog:home')
        return super().dispatch(request, *args, **kwargs)


class UpdateTicket(LoginRequiredMixin, UpdateView):
    template_name = "blog/update_ticket.html"
    model = Ticket
    fields = ('title', 'description', 'image')
    success_url = reverse_lazy('blog:posts')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["title"].label = "Titre"
        form.fields["title"].widget.attrs.update({"placeholder": "Titre"})
        return form

    def dispatch(self, request, *args, **kwargs):
        ticket = self.get_object()
        if ticket.user != request.user:
            return redirect('blog:home')
        return super().dispatch(request, *args, **kwargs)


class CreateReview(LoginRequiredMixin, CreateView):
    template_name = "blog/create_review.html"
    model = Review
    form_class = ReviewForm
    success_url = reverse_lazy('blog:posts')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ticket_id = self.kwargs["pk"]
        ticket = Ticket.objects.get(id=ticket_id)
        context['ticket'] = ticket
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        ticket_id = self.kwargs["pk"]
        self.object.ticket = Ticket.objects.get(id=ticket_id)
        self.object.save()
        return super().form_valid(form)


class DeleteReview(LoginRequiredMixin, DeleteView):
    model = Review
    success_url = reverse_lazy('blog:posts')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        rating_range = range(1, 6)
        context["rating_range"] = rating_range
        return context

    def dispatch(self, request, *args, **kwargs):
        review = self.get_object()
        if review.user != request.user:
            return redirect('blog:home')
        return super().dispatch(request, *args, **kwargs)


class UpdateReview(LoginRequiredMixin, UpdateView):
    template_name = "blog/update_review.html"
    model = Review
    form_class = ReviewForm
    success_url = reverse_lazy('blog:posts')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        review = self.get_object()
        context['ticket'] = review.ticket
        return context

    def dispatch(self, request, *args, **kwargs):
        review = self.get_object()
        if review.user != request.user:
            return redirect('blog:home')
        return super().dispatch(request, *args, **kwargs)


class CreateReviewAndTicket(FormView):
    template_name = "blog/create_review_and_ticket.html"
    form_class = TicketForm
    success_url = reverse_lazy('blog:posts')
    review_form_class = ReviewForm

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        self.review_form = self.review_form_class(self.request.POST or None)
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['review_form'] = self.review_form
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        review_form = self.review_form
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.user = self.request.user
            review.ticket = self.object
            review.save()
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        review_form = self.review_form_class(request.POST)

        if form.is_valid() and review_form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class Follow(View):
    template_name = "blog/follow.html"
    form_class = FollowForm

    def get(self, request):
        form = self.form_class
        message = ''
        follows = self.get_followed_users(request)
        followers = self.get_followers((request))
        return render(request, self.template_name, {'form': form, 'message': message,
                                                    'follows': follows, 'followers': followers})

    def post(self, request):
        form = self.form_class(request.POST)
        follows = self.get_followed_users(request)
        followers = self.get_followers(request)
        if form.is_valid:
            try:
                user = User.objects.get(username=form['username'].value())
                try:
                    if user != request.user:
                        userfollows = UserFollows()
                        userfollows.user = request.user
                        userfollows.followed_user = user
                        userfollows.save()
                        message = f"Vous suivez désormais {user.username}"
                    else:
                        message = f"Vous êtes déja connecté en tant que {user.username}"
                except IntegrityError:
                    message = f"Vous êtes déjà abonné à {user.username}"
            except User.DoesNotExist:
                message = f"{form['username'].value()} est introuvable"

            return render(request, self.template_name, {
                'form': form,
                'message': message,
                'follows': follows,
                'followers': followers
            })

    def get_followed_users(self, request):
        followed_users = UserFollows.objects.filter(user=request.user)
        return followed_users

    def get_followers(self, request):
        followers = UserFollows.objects.filter(followed_user=request.user)
        return followers


class DeleteUserFollows(LoginRequiredMixin, DeleteView):
    model = UserFollows
    success_url = reverse_lazy('blog:follow')
