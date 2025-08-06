

# **Google OAuth Login Integration (Django DRF + Vite Vanilla JS)**

This project demonstrates how to implement **"Continue with Google" OAuth 2.0 login flow** using:

* **Django DRF (Backend API)**
* **Vite + Vanilla JavaScript (Frontend)**

Users can authenticate using their Google account. The frontend obtains a **Google ID Token** and sends it to the Django DRF backend, where it is verified and a **JWT Token** is returned for further authentication.

---

## **Project Structure**

```
my-project/
├── backend/              # Django DRF Backend
│   ├── manage.py
│   ├── myproject/
│   └── app/
├── frontend/             # Vite Vanilla JS Frontend
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   └── src/
│       └── main.js
└── README.md
```

---

## **Setup Instructions**

### 1. **Google Cloud Console Setup**

* Go to [Google Cloud Console](https://console.cloud.google.com/).
* Create a **new project**.
* Navigate to **APIs & Services > Credentials**.
* **Create OAuth Client ID**:

  * Application Type: **Web**
  * **Authorized JavaScript origins**: `http://localhost:5173`
  * **Authorized redirect URIs**: (leave empty)
* Copy the **Client ID** for frontend integration.

---

### 2. **Backend (Django DRF) Setup**

#### Prerequisites:

* Python 3.x
* pip

#### Install Dependencies:

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

#### `requirements.txt`:

```
Django
djangorestframework
djangorestframework-simplejwt
google-auth
django-cors-headers
```

#### Django Config:

* Add `'corsheaders'`, `'rest_framework'`, and your app in **INSTALLED\_APPS**.
* Enable **CORS** for frontend origin in `settings.py`:

```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
]
```

* Add URL route in `urls.py`:

```python
from django.urls import path
from app.views import GoogleLoginAPIView

urlpatterns = [
    path('api/google-login/', GoogleLoginAPIView.as_view(), name='google-login'),
]
```

#### Run Backend Server:

```bash
python manage.py runserver
```

---

### 3. **Frontend (Vite Vanilla JS) Setup**

#### Prerequisites:

* Node.js & npm

#### Install Dependencies:

```bash
cd frontend
npm install
```

#### Start Development Server:

```bash
npm run dev
```

#### index.html:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Google Login</title>
    <script src="https://accounts.google.com/gsi/client" async defer></script>
</head>
<body>
    <div id="g_id_onload"
         data-client_id="YOUR_GOOGLE_CLIENT_ID"
         data-callback="handleCredentialResponse">
    </div>

    <div class="g_id_signin"
         data-type="standard"></div>

    <script type="module" src="/src/main.js"></script>
</body>
</html>
```

#### main.js:

```javascript
export function handleCredentialResponse(response) {
    console.log("ID Token: ", response.credential);
    fetch('http://localhost:8000/api/google-login/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ token: response.credential })
    })
    .then(res => res.json())
    .then(data => {
        console.log('Backend Response:', data);
    })
    .catch(err => {
        console.error('Error sending token to backend:', err);
    });
}

window.handleCredentialResponse = handleCredentialResponse;
```

---

## **Flow Overview**

1. User clicks **Continue with Google**.
2. Google returns an **ID Token (JWT)** to frontend.
3. Frontend sends this token to backend `/api/google-login/`.
4. Backend verifies the token with Google API.
5. Backend checks/creates the user in DB.
6. Backend returns **JWT access/refresh tokens**.
7. Frontend receives and can store/access user info securely.

---

## **Important Notes**

* This setup uses **Google One Tap Sign-In (GSI Library)**.
* Backend uses **SimpleJWT** for generating app-specific JWTs.
* Ensure CORS is properly configured between frontend & backend.
* This example uses **Vanilla JS**, but similar logic applies to React, Vue, etc.

---

## **Commands Summary**

| Task                           | Command                           |
| ------------------------------ | --------------------------------- |
| Backend: Install Dependencies  | `pip install -r requirements.txt` |
| Backend: Run Server            | `python manage.py runserver`      |
| Frontend: Install Dependencies | `npm install`                     |
| Frontend: Run Dev Server       | `npm run dev`                     |

---

