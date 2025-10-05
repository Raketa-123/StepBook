from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from django.contrib.auth import authenticate, login
from rest_framework_simplejwt.tokens import RefreshToken
from user.serializers import UserRegisterSerializer, LoginSerializer
from user.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer


class RegisterView(APIView):
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Пользователь зарегистрирован!"}, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(email=serializer.validated_data['email'], password=serializer.validated_data['password'])
        if not user:
            return Response({"error": "Неверный email или пароль"}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)
        return Response({
            "message": "Успешный вход",
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        })

        
class RegisterPage(View):
    template_name = 'register.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        email = request.POST.get("email")
        name = request.POST.get("name")
        password = request.POST.get("password")

        if User.objects.filter(email=email).exists():
            return render(request, self.template_name, {
                "errors": {"email": ["Этот email уже зарегистрирован."]}
            })

        data = {"email": email, "name": name, "password": password}
        serializer = UserRegisterSerializer(data=data)

        if serializer.is_valid():
            user = serializer.save()
            user.is_active = True
            user.save()
            return redirect(reverse('login_page'))

        return render(request, self.template_name, {"errors": serializer.errors})
    

class LoginPage(View):
    template_name = 'login.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            errors = {"__all__": ["Неверное имя пользователя или пароль."]}
            return render(request, self.template_name, {"errors": errors})
        

@method_decorator(login_required(login_url='login_page'), name='dispatch')
class HomePage(View):
    template_name = 'home.html'

    def get(self, request):
        return render(request, self.template_name)


from django.contrib.auth import logout

class LogoutPage(View):
    def get(self, request):
        logout(request)
        return redirect('login_page')
