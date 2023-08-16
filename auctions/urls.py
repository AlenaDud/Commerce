from django.urls import path
from . import views

urlpatterns = [
    path("", views.IndexListView.as_view(), name="index"),
    path("category/<int:category_id>", views.IndexFilteredListView.as_view(), name="filtered_index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    path("watchlist/<int:listing_id>", views.watchlist, name="watchlist"),
    path("watchlist", views.WatchlistView.as_view(), name="detail-watchlist"),

    path("closing/<int:listing_id>", views.closing, name="closing"),
    path("not-active/<int:listing_id>", views.not_active, name="not_active"),

    path("create-listing", views.CreateListingView.as_view(), name="create"),
    path("create-listing/successful", views.CreateListingDoneView.as_view()),
    path("listings/<int:listing_id>", views.ListingDetailView.as_view(), name='listing_detail'),
]
