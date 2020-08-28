from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('<int:listing_id>',views.listing,name='listing'),
    path('create_listing',views.create_listing,name='create_listing'),
    path('watchlist', views.whatchlist, name='watchlist'),
    path('watchlist/<int:listing_id>',views.addLista, name='addLista'),
    path('remove_from_list/<int:listing_id>', views.remove_from_list, name='remove_from_list'),
    path('close/<int:listing_id>',views.close, name='close'),
    path('comment/<int:listing_id>',views.comment_view, name='comment'),
    path('categories',views.categories, name='categories'),
    path('categories/<str:categoria>',views.categoria, name='categoria'),
]
