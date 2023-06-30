"""Speed_Sport_Souvenirs URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from base import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tmp/', views.tmp, name="tmp"),
    path('', views.home_page, name="Home"),
    path('product/<int:product_id>', views.product_page, name="Product"),
    path('add_product/', views.add_product_page, name="Add_Product"),
    path('edit_product/<int:product_id>', views.edit_product_page, name="Edit_Product"),
    path('confirm_delete/<int:product_id>', views.confirm_delete_page, name="Confirm_Delete"),
    path('delete_product/<int:product_id>', views.delete_product_page, name="Delete_Product"),
    path('products/', views.search_products, name="Products"),
    path('login/', views.login_page, name="Login"),
    path('logout/', views.logout_method, name="Logout"),
    path('register/', views.register_page, name="Register"),
    path('cart/', views.cart_page, name="Cart"),
    path('profile/<int:user_id>', views.profile_page, name="Profile"),
    path('edit_profile/', views.edit_profile_page, name="Edit_Profile"),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='Add_To_Cart'),
    path('cart/remove/<int:item_id>', views.remove_from_cart, name="Remove_From_Cart"),
    path('cart/increment/<int:item_id>/', views.increment_quantity, name='Increment'),
    path('cart/decrement/<int:item_id>/', views.decrement_quantity, name='Decrement'),
    path('cart/payment/', views.payment, name="Payment"),
    path('cart/payment/successful', views.payment_success_page, name="Payment_Success"),
    path('cart/', views.cart_page, name="Cart"),
    path('legal/', views.legal_info_page, name="Legal"),
    path('about/', views.about_page, name="About")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
