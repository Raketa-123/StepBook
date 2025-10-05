from django.urls import path, include
from django.contrib import admin
from rest_framework.routers import DefaultRouter

from user.views import UserViewSet, RegisterView, LoginView, RegisterPage, LoginPage, HomePage, LogoutPage
from book.views import BookViewSet, AuthorViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'books', BookViewSet, basename='book')
router.register(r'authors', AuthorViewSet, basename='author')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    
    # API endpoints
    path('api/register/', RegisterView.as_view(), name='api-register'),
    path('api/login/', LoginView.as_view(), name='api-login'),

    # HTML pages
    path('register/', RegisterPage.as_view(), name='register_page'),
    path('logout/', LogoutPage.as_view(), name='logout_page'),
    path('', HomePage.as_view(), name='home_page'),
    path('login/', LoginPage.as_view(), name='login_page'),
]