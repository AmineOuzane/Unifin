from django.urls import path

from myapp.views import index, contact

from . import views
urlpatterns = [
    path('', index, name='acceuil'),
    
    path('register/', views.registerpage, name='register'),
    path('login/', views.loginpage, name='login'),
    path('logout/', views.logoutuser, name='logout'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),


    
    
    path('produits/', views.product_list_general, name='product_list_general'),   

    path('search/', views.search_results, name='search_results'),
    
    path('daawat/', views.daawat, name='daawat'),
    path('catania/', views.catania, name='catania'),  
    path('magicclean/', views.magicclean, name='magicclean'), 
    
    path('detail/<int:produit_id>/', views.detail, name='detail'),
  
    path('cart/', views.cart, name='cart' ),
    path('add_to_cart/<int:produit_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/delete', views.delete_cart, name='delete_cart' ),
     path('delete_order/<int:order_id>/', views.delete_order, name='delete_order'),
    
    
    path('recette/', views.recette, name='recette'),  
    path('blog/', views.blog, name='blog'),    
    path('checkout/', views.checkout, name='checkout'),
    path('about/', views.about, name='about'),
    path('contact/', contact, name='contact'),
    
]
