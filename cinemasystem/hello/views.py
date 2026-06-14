from django.shortcuts import render, redirect
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from .models import Booking, Production, Customer
from .serializers import ProductionSerializer, CustomerSerializer, BookingSerializer
from rest_framework import status
from django.contrib.auth.hashers import make_password, check_password
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, AllowAny
import requests
from django.contrib import messages
from rest_framework_simplejwt.authentication import JWTAuthentication

#for jwt auth to use email for login, also api for login
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import EmailTokenObtainPairSerializer

class EmailTokenObtainPairView(TokenObtainPairView):
    serializer_class = EmailTokenObtainPairSerializer

# =========================
# 🔐 API: FETCH PRODUCTIONS (PROTECTED)
# =========================
@api_view(['GET'])
@permission_classes([AllowAny])
def fetch_productions(request):

    productions = Production.objects.all()
    product = Production.objects.all().values("id", "production_name")

    movies = productions.filter(production_type="movie")
    plays = productions.filter(production_type="play")
    concerts = productions.filter(production_type="concert")

    return Response({
        "movies": ProductionSerializer(movies, many=True).data,
        "plays": ProductionSerializer(plays, many=True).data,
        "concerts": ProductionSerializer(concerts, many=True).data,
        "productions": list(product)
    })

@api_view(['POST'])  # ✅ changed from GET/POST
@permission_classes([IsAuthenticated])
def fetch_seats(request):
    production_id = request.data.get("production_id")
    bookings = Booking.objects.filter(production_id=production_id)
    serializer = BookingSerializer(bookings, many=True)
    return Response({"booked_seats": serializer.data}, status=200)


# =========================
# 🎟️ API: BOOKING (PROTECTED)
# =========================
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def booking(request):

    # 🔐 logged-in user from JWT
    customer = request.user

    production_name = request.data.get("production_name")
    seat = request.data.get("seat_preference")

    # ❌ validation
    if not production_name or not seat:
        return Response(
            {"error": "production_name and seat_preference required"},
            status=400
        )

    # 🔍 find production (case-insensitive)
    production = Production.objects.filter(
        production_name__iexact=production_name
    ).first()

    if not production:
        return Response({"error": "Production not found"}, status=404)

    # 🚫 prevent duplicate booking
    if Booking.objects.filter(production=production, seat_preference=seat).exists():
        return Response({"error": "Seat already booked"}, status=400)

    # ✅ create booking
    booking_obj = Booking.objects.create(
        customer=customer,
        production=production,
        seat_preference=seat
    )

    return Response({
        "message": "Booking successful",
        "booking_id": booking_obj.id,
        "amount": booking_obj.amount
    }, status=201)


# =========================================
# 👤 API: REGISTER CUSTOMER and GET CUSTOMER ACCESSIBILITY ANYONE
# ========================================
@api_view(['GET', 'POST'])
@permission_classes([AllowAny]) 
def register_customer(request):

    # 📌 GET all customers
    if request.method == 'GET':
        customers = Customer.objects.all()
        serializer = CustomerSerializer(customers, many=True)

        return Response({
            "count": customers.count(),
            "customers": serializer.data
        })

    # 📌 POST register new customer
    elif request.method == 'POST':

        data = request.data


        serializer = CustomerSerializer(data=data)

        if serializer.is_valid():
            customer = serializer.save()

            # 🔑 generate JWT tokens
            refresh = RefreshToken.for_user(customer)

            return Response({
                "message": "Customer created successfully",
            }, status=201)

        return Response(serializer.errors, status=400)



# =========================
# 🌐 FRONT PAGE
# =========================
def front(request):
    return render(request, 'index.html')


# =========================
# 🔐 ACCOUNT PAGE (CONSUMES API)
# =========================
def account(request):

    token = request.session.get('access')
    print("TOKEN:", token)  # 🔥 DEBUG LINE


    if not token:
        messages.error(request, "Please login first")
        return redirect("front")

    url = "http://127.0.0.1:8000/api/fetch_productions/"

    

    response = requests.get(url)
    data = response.json()

    return render(request, "account.html", data)


# =========================
# 👤 REGISTER CONSUMER VIEW
# =========================
def register_customerapi_consumption(request):

    if request.method == "POST":

        url = "http://127.0.0.1:8000/api/register_customer/"

        data = {
            "first_name": request.POST.get("first_name"),
            "last_name": request.POST.get("last_name"),
            "email": request.POST.get("email"),
            "phone": request.POST.get("phone"),
            "address": request.POST.get("address"),
            "password": request.POST.get("password")
        }
        
        if not all(data.values()):
            messages.error(request, "All fields are required")
            return redirect("front")

        # send request only if valid
        response = requests.post(url, json=data)

        if response.status_code == 201:
            messages.success(request, "Registration successful please login")
        else:
            error_detail = response.json()
            messages.error(request, f"Registration failed: {error_detail}")

        return redirect("front")

        
            

# =========================
# 🎟️ BOOKING CONSUMER VIEW
# =========================
def booking_api_consumption(request):

    if request.method == 'POST':

        token = request.session.get('access')

        if not token:
            messages.error(request, "Please login first")
            return redirect("front")

        url = "http://127.0.0.1:8000/api/booking/"

        data = {
            "production_name": request.POST.get("production_name"),
            "seat_preference": request.POST.get("seat_preference")
        }

        headers = {
            "Authorization": f"Bearer {token}"
        }

        response = requests.post(url, json=data, headers=headers)
        result = response.json()

        if response.status_code == 201:
            messages.success(request, "Booking successful!")
        else:
            messages.error(request, result.get("error", "Booking failed"))

        return redirect("account")

    return redirect("account")


# =========================
# 🔑 LOGIN CONSUMER VIEW
# =========================
def loginapiconsumer(request):

    if request.method == "POST":

        url = "http://127.0.0.1:8000/api/token/"

        data = {
            "email": request.POST.get("email"),
            "password": request.POST.get("password")
        }

        response = requests.post(url, json=data)
        result = response.json()

        if response.status_code == 200:
            request.session['access'] = result['access']
            request.session['refresh'] = result['refresh']
            messages.success(request, "Login successful")
            return redirect("account")

        messages.error(request, "Invalid credentials")
        return redirect("front")

    return render(request, "index.html")




#=====================
# board fetch_seats
#====================
def checkseats(request):
    token = request.session.get("access")
    if not token:
        messages.error(request, "Please login first")
        return redirect("front")

    url = "http://127.0.0.1:8000/api/fetch_productions/"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    data = response.json()

    production = data.get("productions", [])  # list of {id, production_name}

    return render(request, "test.html", {"production": production})

def board(request):
    token = request.session.get("access")
    if not token:
        messages.error(request, "Please login first")
        return redirect("front")

    if request.method == "POST":
        production_id = request.POST.get("production_name")

        url = "http://127.0.0.1:8000/api/fetch_seats/"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        # ✅ use POST not GET
        response = requests.post(url, headers=headers, json={"production_id": production_id})
        
        # ✅ guard against empty/bad response
        if response.status_code != 200:
            messages.error(request, f"Failed to fetch seats: {response.status_code}")
            return redirect("test")

        data = response.json()
        booked_list = [b["seat_preference"] for b in data.get("booked_seats", [])]
        all_seats = list(range(1, 301))

        prod_response = requests.get(
            "http://127.0.0.1:8000/api/fetch_productions/",
            headers=headers
        )
        production = prod_response.json().get("productions", [])

        return render(request, "test.html", {
            "booked_seats": booked_list,
            "seats": all_seats,
            "production": production,
        })

    return redirect("test")



# ====================
# 🚪 LOGOUT
# =========================
def logout_view(request):
    request.session.flush()
    messages.success(request, "Logged out successfully")
    return redirect("front")