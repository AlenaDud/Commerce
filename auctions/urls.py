from django.urls import path
from . import views

urlpatterns = [
    path("", views.IndexListView.as_view(), name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create-listing", views.CreateListingView.as_view(), name="create"),
    path("create-listing/successful", views.CreateListingDoneView.as_view()),
    path("listings/<int:pk>", views.ListingDetailView.as_view(), name='listing_detail')
]
