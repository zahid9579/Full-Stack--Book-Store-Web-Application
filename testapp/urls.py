from django.urls import path
from . import views


urlpatterns = [
  #  path('',views.index_views),
    path('book/', views.book_list_view, name='book_list'),
    path('book/<int:book_id>/', views.book_detail, name='book_detail'),  # Add this line
    path('add_to_cart/<int:book_id>/', views.add_to_cart, name='add_to_cart'),
    path('order_now/<int:book_id>/', views.order_now, name='order_now'),
    path('register/', views.register, name='register'),
    path('cancel_item/<int:book_id>/', views.cancel_item, name='cancel_item'),
]
