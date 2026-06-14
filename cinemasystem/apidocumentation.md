# Gold Cinema API Documentation

**Base URL:** `http://127.0.0.1:8000`  
**Authentication:** JWT (JSON Web Token) via Bearer token  
**Content-Type:** `application/json`

---

## Authentication

Gold Cinema uses JWT authentication. After login, include the access token in the `Authorization` header for all protected endpoints:

```
Authorization: Bearer <access_token>
```

Tokens expire after a set period. Use the refresh endpoint to get a new access token without logging in again.

---

## Endpoints

### 1. Register Customer

**`POST /api/register_customer/`**  
Access: Public (no token required)

Creates a new customer account.

**Request Body:**
```json
{
  "first_name": "John",
  "last_name": "Doe",
  "email": "john@example.com",
  "phone": "0712345678",
  "address": "Nairobi, Kenya",
  "password": "SecurePass123!"
}
```

**Success Response — `201 Created`:**
```json
{
  "message": "Customer created successfully"
}
```

**Error Response — `400 Bad Request`:**
```json
{
  "email": ["customer with this email already exists."]
}
```

---

### 2. Get All Customers

**`GET /api/register_customer/`**  
Access: Public (no token required)

Returns a list of all registered customers.

**Success Response — `200 OK`:**
```json
{
  "count": 2,
  "customers": [
    {
      "id": 1,
      "first_name": "John",
      "last_name": "Doe",
      "email": "john@example.com",
      "phone": "0712345678",
      "address": "Nairobi, Kenya"
    }
  ]
}
```

---

### 3. Login (Obtain JWT Token)

**`POST /api/token/`**  
Access: Public (no token required)

Authenticates a customer and returns JWT access and refresh tokens.

**Request Body:**
```json
{
  "email": "john@example.com",
  "password": "SecurePass123!"
}
```

**Success Response — `200 OK`:**
```json
{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Error Response — `401 Unauthorized`:**
```json
{
  "detail": "No active account found with the given credentials"
}
```

---

### 4. Refresh Token

**`POST /api/token/refresh/`**  
Access: Public (no token required)

Returns a new access token using a valid refresh token.

**Request Body:**
```json
{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Success Response — `200 OK`:**
```json
{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

---

### 5. Fetch Productions

**`GET /api/fetch_productions/`**  
Access: Public (no token required)

Returns all productions grouped by type (movies, plays, concerts), plus a flat list for dropdowns.

**Success Response — `200 OK`:**
```json
{
  "movies": [
    {
      "id": 1,
      "production_name": "Midnight Echo",
      "production_type": "movie",
      "description": "A thrilling night mystery.",
      "start_date": "2026-07-01",
      "production_show_time": "19:00:00"
    }
  ],
  "plays": [],
  "concerts": [],
  "productions": [
    { "id": 1, "production_name": "Midnight Echo" }
  ]
}
```

---

### 6. Book a Seat

**`POST /api/booking/`**  
Access: 🔒 Protected (JWT token required)

Books a seat for a production for the currently logged-in customer. Seat numbers are between 1 and 300. Amount is set automatically based on production type:

| Production Type | Amount (KES) |
|---|---|
| Movie | 300 |
| Play | 400 |
| Concert | 600 |

**Request Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "production_name": "Midnight Echo",
  "seat_preference": 45
}
```

**Success Response — `201 Created`:**
```json
{
  "message": "Booking successful",
  "booking_id": 7,
  "amount": 300
}
```

**Error Responses:**

`400` — Missing fields:
```json
{ "error": "production_name and seat_preference required" }
```

`400` — Seat already taken:
```json
{ "error": "Seat already booked" }
```

`404` — Production not found:
```json
{ "error": "Production not found" }
```

---

### 7. Fetch Booked Seats

**`POST /api/fetch_seats/`**  
Access: 🔒 Protected (JWT token required)

Returns all booked seats for a given production by its ID. Used to display the seat map.

**Request Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "production_id": 1
}
```

**Success Response — `200 OK`:**
```json
{
  "booked_seats": [
    {
      "id": 1,
      "customer_email": "john@example.com",
      "production_name": "Midnight Echo",
      "seat_preference": 45,
      "booked_at": "2026-06-14T15:30:00Z"
    }
  ]
}
```

---

## Pricing Summary

| Production Type | Price (KES) |
|---|---|
| Movie | 300 |
| Play | 400 |
| Concert | 600 |

Prices are automatically applied during booking based on production type. Customers cannot override the amount.

---

## Error Reference

| Status Code | Meaning |
|---|---|
| 200 | Success |
| 201 | Created successfully |
| 400 | Bad request / validation error |
| 401 | Unauthorized — token missing or expired |
| 404 | Resource not found |
| 500 | Server error |

---

## Notes

- All seat numbers must be between **1 and 300**.
- Each seat per production can only be booked **once**.
- Production names in booking requests are **case-insensitive** (`midnight echo` = `Midnight Echo`).
- JWT access tokens expire — use `/api/token/refresh/` to renew.
- Emails are sent automatically to all customers when a new production is added via the admin panel.

---

*Gold Cinema — Nairobi, Kenya | Built with Django REST Framework*