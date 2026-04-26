from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.decorators import api_view, permission_classes #for function based api views
from rest_framework.response import Response
from .models import Booking, Production, Customer
from .serializers import ProductionSerializer, BookingSerializer, CustomerSerializer
from rest_framework import status
from django.contrib.auth.hashers import make_password, check_password
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
import requests
from django.contrib import messages

#this are api endpoints
@api_view(['GET']) 
@permission_classes([IsAuthenticated])  #authentication is required to access this apiendpoint ie jwt token is required
def fetch_productions(request):         #here jwt is used to protect my api 
    productions = Production.objects.all()

    movies = productions.filter(production_type="Movie")
    plays = productions.filter(production_type="Play")
    concerts = productions.filter(production_type="Concert")

    return Response({
        "movies": ProductionSerializer(movies, many=True).data,
        "plays": ProductionSerializer(plays, many=True).data,
        "concerts": ProductionSerializer(concerts, many=True).data,
    }) 
 #.data means the fetched data from database is converted into json directly ie {
 # "movies": [...],
 # "plays": [...],
#  "concerts": [...]
#}



@api_view(['POST'])
def register_customer(request):
    data = request.data.copy()  # ✅ fix immutability

    # hash password
    data['password'] = make_password(data['password'])

    serializer = CustomerSerializer(data=data)

    # ✅ validate FIRST
    if serializer.is_valid():
        customer = serializer.save()  # save ONCE

        # generate JWT
        refresh = RefreshToken.for_user(customer)

        return Response({
            "message": "Customer created successfully",
            "customer": serializer.data,
            "refresh": str(refresh),
            "access": str(refresh.access_token)
        }, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#loginendpoint  api for gold cinema
@api_view(['POST'])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')

    try:
        customer = Customer.objects.get(email=email)
    except Customer.DoesNotExist:
        return Response(
            {"error": "Invalid credentials"},
            status=status.HTTP_401_UNAUTHORIZED
        )

    # check password
    if not check_password(password, customer.password):
        return Response(
            {"error": "Invalid credentials"},
            status=status.HTTP_401_UNAUTHORIZED
        )

    # generate JWT
    refresh = RefreshToken.for_user(customer)

    return Response({
        "message": "Login successful",
        "customer": {
            "id": customer.id,
            "first_name": customer.first_name,
            "last_name": customer.last_name,
            "email": customer.email
        },
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }, status=status.HTTP_200_OK)


@api_view(["GET", "POST"])
#def booking(request): #proceed with fetching booked seats and booking api




#this code here is not an api endpoint but a views that  consumes apis



def front(request):
    return render(request, 'index.html')

# ✅ PROTECTED PAGE (USES TOKEN)
def account(request):
    token = request.session.get('access')

    # 🚫 not logged in
    if not token:
        messages.error(request, "Please login first")
        return redirect("front")

    url = "http://127.0.0.1:8000/api/fetch_production/"

    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(url, headers=headers)

    # 🚫 token expired or invalid
    if response.status_code == 401:
        messages.error(request, "Session expired. Please login again")
        return redirect("front")

    data = response.json()

    return render(request, "account.html", data)



def loginapiconsumer(request):
    import requests
    if request.method == "POST":
        url = "http://127.0.0.1:8000/api/login/"

        data = {
            "email": request.POST.get("email"),
            "password": request.POST.get("password")
        }

        response = requests.post(url, json=data)

        if response.status_code == 200:
            tokens = response.json()

            # ✅ store token in session
            request.session['access'] = tokens['access']
            messages.success(request, "Login successful")

            return redirect("account")
        else:
            messages.error(request, "invalid credentials")
            return render(request, "index.html")
        
        

    return render(request, "index.html")

# ✅ LOGOUT (VERY IMPORTANT)
def logout_view(request):
    request.session.flush()
    messages.success(request, "Logged out successfully")
    return redirect("front")

