from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from datetime import date
from datetime import datetime
from django.http import JsonResponse
from django.contrib.auth.hashers import check_password
from .firebase.firestore_service import FirestoreService
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .credentials import MpesaAccessToken, LipanaMpesaPpassword
from .utilis import get_pesapal_access_token
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import datetime
from .forms import Meet, SignUpForm, RegisterChamaForm, ArticleForm
from .models import Meetings, RegisterChama, Article, SignUp
from .firebase.firestore_service import FirestoreService
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.conf import settings
from .firebase.firestore_service import FirestoreService
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from .firebase.firestore_service import FirestoreService
import requests
from requests.auth import HTTPBasicAuth
import json
import time
from .credentials import MpesaAccessToken, LipanaMpesaPpassword
from .utilis import get_pesapal_access_token
from django.conf import settings
import time
from .forms import Meet, SignUpForm, RegisterChamaForm,ArticleForm
from .models import Meetings, RegisterChama,Article,SignUp
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render, redirect 
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from django.shortcuts import render, redirect

firestore_service = FirestoreService()

# MPESA Payment Processing


@csrf_exempt  # Remove this if you are passing CSRF token correctly in AJAX
def pay(request):
    if request.method == "POST":
        # Try to get data from JSON (AJAX) or form (regular POST)
        try:
            if request.content_type == "application/json":
                data = json.loads(request.body)
                phone = data.get('phone')
                amount = data.get('amount')
            else:
                phone = request.POST.get('phone')
                amount = request.POST.get('amount')
        except Exception as e:
            return JsonResponse({"success": False, "message": "Invalid data format."}, status=400)

        # MPESA STK Push logic
        access_token = MpesaAccessToken.validated_mpesa_access_token
        api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
        headers = {"Authorization": "Bearer %s" % access_token}
        request_data = {
            "BusinessShortCode": LipanaMpesaPpassword.Business_short_code,
            "Password": LipanaMpesaPpassword.decode_password,
            "Timestamp": LipanaMpesaPpassword.lipa_time,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": phone,
            "PartyB": LipanaMpesaPpassword.Business_short_code,
            "PhoneNumber": phone,
            "CallBackURL": "https://sandbox.safaricom.co.ke/mpesa/",
            "AccountReference": "Chama Programme",
            "TransactionDesc": "Chama Contribution" if not request.GET.get('fine') else "Chama Fine"
        }

        response = requests.post(api_url, json=request_data, headers=headers)
        if response.status_code == 200:
            # If AJAX, return JSON for toast
            if request.content_type == "application/json":
                return JsonResponse({
                    "success": True,
                    "message": f"Member has been fined Ksh {amount} for late payment." if request.GET.get('fine') else "STK Push sent successfully! Please check your phone to complete the payment."
                })
            # If regular POST, show message and redirect
            messages.success(request, "STK Push sent successfully! Please check your phone to complete the payment.")
            return redirect('admin_dashboard')
        else:
            error_msg = "Failed to initiate STK Push. Please try again."
            if request.content_type == "application/json":
                return JsonResponse({"success": False, "message": error_msg}, status=400)
            messages.error(request, error_msg)
            return redirect('admin_dashboard')

    # For GET requests, render the MPESA page as usual
    return render(request, 'MPESA.html', {'navbar': 'MPESA'})

def token(request):
    consumer_key = '77bgGpmlOxlgJu6oEXhEgUgnu0j2WYxA'
    consumer_secret = 'viM8ejHgtEmtPTHd'
    api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'

    r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    mpesa_access_token = json.loads(r.text)
    validated_mpesa_access_token = mpesa_access_token["access_token"]

    return render(request, 'token.html', {"token": validated_mpesa_access_token})
# Payment Methods
def MPESA(request):
    return render(request, 'MPESA.html', {'navbar': 'MPESA'})


def method(request):
    return render(request, 'Payment Methods.html')


def kcb(request):
    return render(request, 'kcb.html')


def equity(request):
    return render(request, 'equity.html')


def pesapal(request):
    return render(request, 'pesapal.html')

def paypal(request):
    return render(request, 'paypal.html')

def calendar(request):
    return render(request, 'calendar.html')


# Pesapal Payment Integration
def initiate_payment(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        amount = request.POST.get('amount')

        if not all([name, email, phone, amount]):
            return JsonResponse({"error": "All fields are required"}, status=400)

        access_token = get_pesapal_access_token()
        if not access_token:
            return JsonResponse({"error": "Failed to get access token"}, status=400)

        url = f"{settings.PESAPAL_API_BASE_URL}/Transactions/SubmitOrderRequest"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}"
        }
        data = {
            "id": str(int(time.time())),
            "currency": "KES",
            "amount": amount,
            "description": "Payment for Services",
            "callback_url": settings.CALLBACK_URL,
            "notification_id": "your_notification_id",
            "billing_address": {
                "email_address": email,
                "phone_number": phone,
                "first_name": name.split(" ")[0],
                "last_name": " ".join(name.split(" ")[1:]) if len(name.split(" ")) > 1 else ""
            }
        }

        response = requests.post(url, json=data, headers=headers)

        if response.status_code == 200:
            return JsonResponse(response.json())
        else:
            return JsonResponse({"error": "Payment request failed", "details": response.text}, status=400)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=400)


def check_payment_status(request, order_tracking_id):
    access_token = get_pesapal_access_token()
    if not access_token:
        return JsonResponse({"error": "Failed to get access token"}, status=400)

    url = f"{settings.PESAPAL_API_BASE_URL}/Transactions/GetTransactionStatus?orderTrackingId={order_tracking_id}"
    headers = {"Authorization": f"Bearer {access_token}"}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return JsonResponse(response.json())
    else:
        return JsonResponse({"error": "Failed to check payment status", "details": response.text}, status=400)


# General Views

from datetime import date
from django.core.paginator import Paginator

def index(request):
    articles_stream = firestore_service.get_all_articles()
    articles = []
    today_str = date.today().strftime('%Y-%m-%d')
    for doc in articles_stream:
        data = doc.to_dict()
        data['id'] = doc.id
        scheduled_date = data.get('scheduled_date')
        if (
            not scheduled_date or
            scheduled_date.strip() == "" or
            scheduled_date.lower() == "none" or
            scheduled_date.lower() == "null" or
            scheduled_date <= today_str
        ):
            articles.append(data)
    articles.sort(key=lambda x: (x.get('scheduled_date') or today_str, x['id']), reverse=True)
    paginator = Paginator(articles, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'index.html', {'page_obj': page_obj})

def events(request):
    return render(request, 'events.html')


def meetings(request):
    meetings = firestore_service.get_all_meetings()
    # Convert Firestore docs to dicts if needed
    meeting_list = []
    for doc in meetings:
        data = doc.to_dict()
        data['id'] = doc.id
        meeting_list.append(data)
    return render(request, 'meetings.html', {'meetings': meeting_list})

def sign_up(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            firestore_service.create_sign_up(form.cleaned_data)
            messages.success(request, "Sign up successful!")
            return redirect('sign_up')
    else:
        form = SignUpForm()
    return render(request, 'sign up.html', {'signup_form': form})

def register(request):
    if request.method == "POST":
        form = RegisterChamaForm(request.POST)
        if form.is_valid():
            firestore_service.create_register_chama(form.cleaned_data)
            messages.success(request, "Registration successful!")
            return redirect('register')
    else:
        form = RegisterChamaForm()
    return render(request, 'sign up.html', {'register_form': form})


@csrf_exempt
def add_meeting(request):
    if request.method == 'POST':
        form = Meet(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            # Convert date and time to string
            if 'date' in data and hasattr(data['date'], 'isoformat'):
                data['date'] = data['date'].isoformat()
            if 'time' in data and hasattr(data['time'], 'isoformat'):
                data['time'] = data['time'].isoformat()
            firestore_service.create_meeting(data)
            # Return JSON for AJAX
            if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.content_type == 'application/json':
                return JsonResponse({"success": True, "message": "Meeting added successfully!"})
            # Fallback for non-AJAX
            messages.success(request, "Meeting added successfully!")
            return redirect('admin_dashboard')
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.content_type == 'application/json':
                return JsonResponse({"success": False, "message": "Invalid form data."})
    # GET or fallback
    form = Meet()
    return render(request, 'admin_dashboard.html', {'form': form})

def meeting_detail(request, meeting_id):
    meeting = firestore_service.get_meeting(meeting_id)
    return render(request, 'meetings.html', {'meeting': meeting})

def delete_meeting(request, meeting_id):
    if request.method == 'POST':
        firestore_service.delete_meeting(meeting_id)
        messages.success(request, "Meeting deleted successfully!")
        return redirect('meetings')
    return render(request, 'admin_dashboard.html')


def admin_sign(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        phone_number = request.POST.get("phone_number")
        name_of_chama = request.POST.get("name_of_chama")
        password = request.POST.get("password")

        admin = FirestoreService.find_register_chama(first_name, phone_number, name_of_chama)
        if admin:
            # Password may be hashed or plain, adjust as needed
            if check_password(password, admin.get("password", "")) or password == admin.get("password", ""):
                request.session["admin_id"] = admin["id"]
                return redirect("admin_dashboard")
            else:
                messages.error(request, "NOT CHAIRLADY")
        else:
            messages.error(request, "NOT CHAIRLADY")

    return render(request, "admin sign.html")



@csrf_exempt
def articles(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            # Explicitly extract fields
            title = form.cleaned_data.get('title', '').strip()
            headline = form.cleaned_data.get('headline', '').strip()
            link = form.cleaned_data.get('link', '').strip()
            image_file = request.FILES.get('image')
            image_url = ""
            if image_file:
                path = default_storage.save('articles/' + image_file.name, ContentFile(image_file.read()))
                image_url = default_storage.url(path)
            # Build the data dict for Firestore
            data = {
                'title': title,
                'headline': headline,
                'link': link,
                'image': image_url
            }
            firestore_service.create_article(data)
            return JsonResponse({"success": True, "message": "Article added successfully!"})
        else:
            return JsonResponse({"success": False, "message": "Invalid form data."})

    # For GET, render the page with articles
    articles_stream = firestore_service.get_all_articles()
    article_list = []
    for doc in articles_stream:
        data = doc.to_dict()
        data['id'] = doc.id
        article_list.append(data)
    return render(request, 'admin_dashboard.html', {
        'articles': article_list,
        'article_form': ArticleForm()
    })

@csrf_exempt
def delete_article(request):
    if request.method == 'POST':
        article_id = request.POST.get('article_id')
        if article_id:
            firestore_service.delete_article(article_id)
            return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)

    # views.py


def get_articles_by_date(request):
    date_str = request.GET.get('date')
    articles_stream = firestore_service.get_all_articles()
    articles = []
    for doc in articles_stream:
        data = doc.to_dict()
        data['id'] = doc.id
        if data.get('scheduled_date') == date_str:
            articles.append(data)
    return JsonResponse({'articles': articles})


@csrf_exempt
def schedule_article(request):
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        headline = request.POST.get('headline', '').strip()
        link = request.POST.get('link', '').strip()
        scheduled_date = request.POST.get('scheduled_date', '').strip()
        image_file = request.FILES.get('image')
        image_url = ""
        if image_file:
            path = default_storage.save('articles/' + image_file.name, ContentFile(image_file.read()))
            image_url = default_storage.url(path)
        data = {
            'title': title,
            'headline': headline,
            'link': link,
            'image': image_url,
            'scheduled_date': scheduled_date  # Store as string (YYYY-MM-DD)
        }
        firestore_service.create_article(data)
        return JsonResponse({"success": True, "message": "Article scheduled successfully!"})
    return JsonResponse({"success": False, "message": "Invalid request."})

def user_login(request):
    if request.method == "POST":
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password')

        # Try signups collection first
        user = FirestoreService.find_signup_by_phone(phone_number)
        # If not found, try register_chama collection
        if not user:
            user = FirestoreService.find_register_chama_by_phone(phone_number)

        if user:
            if password == user.get('password', ''):
                messages.success(request, "Login successful!")
                request.session['user_id'] = user['id']
                return redirect("home")
            else:
                messages.error(request, "Invalid phone number or password. Please try again.")
                return render(request, "sign up.html", {"show_login": True})
        else:
            messages.error(request, "User does not exist. Please sign up first.")
            return render(request, "sign up.html", {"show_login": True})
    return render(request, "sign up.html")


# Admin Dashboard: Only accessible if admin is logged in
def admin_dashboard(request):
    admin_id = request.session.get("admin_id")
    if not admin_id:
        messages.error(request, "You must be logged in as admin.")
        return redirect("admin_login")
    # Fetch meetings and articles for dashboard display
    meetings = firestore_service.get_all_meetings()
    articles_stream = firestore_service.get_articles()
    articles = []
    for doc in articles_stream:
        data = doc.to_dict()
        data['id'] = doc.id
        articles.append(data)
    article_form = ArticleForm()
    form = Meet()
    return render(request, "admin_dashboard.html", {
        "meetings": meetings,
        "articles": articles,
        "article_form": article_form,
        "form": form,
    })

# Admin Login (renders admin sign-in form and handles POST)
def admin_login(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        phone_number = request.POST.get("phone_number")
        name_of_chama = request.POST.get("name_of_chama")
        password = request.POST.get("password")

        admin = FirestoreService.find_register_chama(first_name, phone_number, name_of_chama)
        if admin:
            if check_password(password, admin.get("password", "")) or password == admin.get("password", ""):
                request.session["admin_id"] = admin["id"]
                return redirect("admin_dashboard")
            else:
                messages.error(request, "NOT CHAIRLADY")
        else:
            messages.error(request, "NOT CHAIRLADY")
    return render(request, "admin sign.html")

# Logout for admin and users
def logout(request):
    request.session.flush()
    messages.success(request, "You have been logged out.")
    return redirect("/?show=login")

def user_logout(request):
    request.session.flush()
    messages.success(request, "You have been logged out.")
    return redirect("/?show=login")

# Other views remain unchanged, but should be updated to use Firestore service functions