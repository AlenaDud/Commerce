from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from .forms import ListingForm, BidForms, CommentsForm
from django.views import View
from django.db.models import Max
from django.views.generic import FormView, TemplateView, ListView, DetailView
from .models import User, Listing, Category, Bid, Comments, Watchlist
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.forms import ValidationError
from decimal import Decimal


class IndexListView(ListView):
    template_name = 'auctions/index.html'
    model = Listing
    context_object_name = 'listings'

    def get_queryset(self):
        queryset = super().get_queryset().annotate(maximum=Max('bid__cost'))

        return queryset.filter(is_active=True).order_by('date_of_create')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'categories': Category.objects.all()})
        return context


class IndexFilteredListView(ListView):
    template_name = 'auctions/filter_index.html'
    model = Listing
    context_object_name = 'listings'

    def get_queryset(self):
        queryset = super().get_queryset().annotate(maximum=Max('bid__cost'))
        cat = self.kwargs['category_id']
        return queryset.filter(is_active=True).filter(category=cat).order_by('date_of_create')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'categories': Category.objects.all()})
        return context


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


class CreateListingView(FormView):
    form_class = ListingForm
    template_name = 'auctions/create_listing.html'
    success_url = '/create-listing/successful'

    @method_decorator(login_required)
    def form_valid(self, form):
        post = form.save(commit=False)
        post.user = self.request.user
        post.save()
        return super().form_valid(post)


class CreateListingDoneView(TemplateView):
    template_name = 'auctions/create_done.html'


class ListingDetailView(View):
    def get(self, request, listing_id):
        current_listing = Listing.objects.get(id=listing_id)  # mb use select_related
        if not current_listing.is_active:
            return HttpResponseRedirect(reverse('not_active', args=(listing_id, )))
        current_max_bid = current_listing.bid_set.aggregate(Max('cost'))['cost__max']
        if current_max_bid is None:
            current_max_bid = current_listing.start_price

        bid_form = BidForms()
        if request.user.is_authenticated:
            watchlist_flag = Watchlist.objects.filter(user=self.request.user, listing_id=listing_id).exists()
        else:
            watchlist_flag = None
        comment_form = CommentsForm()
        comment_for_listing = Comments.objects.filter(listing_id=listing_id)

        return render(request, 'auctions/listing.html',
                      context={'listing': current_listing, 'max_bid': current_max_bid,
                               'bid_form': bid_form, 'comment_form': comment_form,
                               'comments': comment_for_listing, 'watchlist_flag': watchlist_flag})

    @method_decorator(login_required)
    def post(self, request, listing_id):
        current_listing = Listing.objects.get(listing_id)  # mb use select_related
        current_max_bid = current_listing.bid_set.aggregate(Max('cost'))['cost__max']
        if current_max_bid is None:
            current_max_bid = current_listing.start_price

        bid_form = BidForms(request.POST)
        comment_form = CommentsForm(request.POST)
        watchlist_flag = Watchlist.objects.filter(user=self.request.user, listing_id=listing_id).exists()
        comment_for_listing = Comments.objects.filter(listing_id=listing_id)

        if bid_form.is_valid():
            bid = bid_form.save(commit=False)
            if bid.cost < current_max_bid:
                message = 'The rate must be equal to or higher than the current one'
                return render(request, 'auctions/listing.html',
                              context={'listing': current_listing, 'max_bid': current_max_bid,
                                       'bid_form': bid_form, 'message': message, 'comment_form': comment_form,
                                       'comments': comment_for_listing, 'watchlist_flag': watchlist_flag})
            else:
                bid.user = self.request.user
                bid.listing = current_listing
                bid.save()
                return HttpResponseRedirect(reverse('listing_detail', args=(listing_id,)))
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = self.request.user
            comment.listing = current_listing
            comment.save()
            return HttpResponseRedirect(reverse('listing_detail', args=(listing_id,)))

        return render(request, 'auctions/listing.html',
                      context={'listing': current_listing, 'max_bid': current_max_bid,
                               'bid_form': bid_form, 'comment_form': comment_form,
                               'comments': comment_for_listing, 'watchlist_flag': watchlist_flag})


@login_required
def watchlist(request, listing_id):
    if request.POST['del_or_add'] == 'Add to watchlist':
        Watchlist.objects.create(user_id=request.user.id,
                                 listing_id=listing_id)
        return HttpResponseRedirect(reverse('listing_detail', args=(listing_id,)))
    else:
        Watchlist.objects.get(user_id=request.user.id, listing_id=listing_id).delete()
        return HttpResponseRedirect(reverse('listing_detail', args=(listing_id,)))


class WatchlistView(View):
    @method_decorator(login_required)
    def get(self, request):
        listings = Listing.objects.filter(watchlist__user=request.user)
        return render(request, 'auctions/watchlist.html', context={'listings': listings})


def not_active(request, listing_id):
    current_listing = Listing.objects.get(id=listing_id)
    if request.user == current_listing.user:
        message = f'Thanks you for posting. Listing - "{current_listing.name}" was sold to {current_listing.winner.username}'
    elif request.user == current_listing.winner:
        message = f'The owner has closed the auction for "{current_listing.name}". Congratulation you win!'
    else:
        message = f'The owner has closed the auction for "{current_listing.name}".'
    return render(request, 'auctions/not_active.html', context={'message': message})


def closing(request, listing_id):
    current_listing = Listing.objects.get(id=listing_id)
    if current_listing.user == request.user:
        current_listing.is_active = False
        max_bid = Bid.objects.filter(listing=listing_id).values('user_id').annotate(Max('cost'))
        current_listing.winner = User.objects.get(id=max_bid[0]['user_id'])
        current_listing.save()
        price = max_bid[0]['cost__max']
        return render(request, 'auctions/not_active.html', context={'listings': current_listing,
                                                                    'price': price})



