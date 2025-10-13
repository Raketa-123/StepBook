from django.urls import path, include
from django.contrib import admin
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static

from user.views import (
    UserViewSet, RegisterView, LoginView,
    RegisterPage, LoginPage, HomePage,
    LogoutPage, ProfilePage
)
from book.views import BookViewSet, BookDetailView, buy_book

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'books', BookViewSet, basename='book')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),

    # HTML pages
    path('', HomePage.as_view(), name='home_page'),
    path('books/<int:pk>/', BookDetailView.as_view(), name='book_detail'),
    path('books/<int:pk>/buy/', buy_book, name='buy_book'),

    path('register/', RegisterPage.as_view(), name='register_page'),
    path('login/', LoginPage.as_view(), name='login_page'),
    path('logout/', LogoutPage.as_view(), name='logout_page'),
    path('profile/', ProfilePage.as_view(), name='profile_page'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
