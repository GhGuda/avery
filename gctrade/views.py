from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.http import HttpRequest
from django.contrib import messages
from django.contrib.auth.models import User, auth
from .models import *
from django.contrib.auth.decorators import login_required
import pycountry, re, random, requests, json, base64
from django.conf import settings
from .utils import get_current_date_and_time
import decouple
config = decouple.config


import smtplib
import imghdr
from email.message import EmailMessage

# Create your views here.

EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
import json
from urllib.request import urlopen


url=config('url')
response = urlopen(url)
data = json.load(response)


def index(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == "POST":
        username = request.POST['username'].lower()
        password = request.POST['password']
        
        # Authenticate the user
        auth_user = auth.authenticate(username=username, password=password)
        
        if auth_user is not None:
            # Establish SMTP connection
            smtp = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            smtp.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
            
            # Retrieve email from authenticated user
            email = auth_user.email

            msg = EmailMessage()
            msg['Subject'] = "A New Login Detected."
            msg['From'] = EMAIL_HOST_USER
            msg['To'] = email
            msg.add_alternative(f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Email Message</title>
            </head>
            <body>
                <div class="cont"
                
                style="
                background: rgba(0, 0, 0, 0.089);
                padding:  1rem;
                padding-top: 4rem;
                text-align: center;
                ">
                    <div class="log" style=" margin-bottom: 4rem;">
                        <a href="http://gctraders.pythonanywhere.com" 
                        style="
                        text-decoration: none;
                        font-size: 1.5rem;
                        font-weight: 900;
                        color: #000000;"><span style="color: #FFD700;">GC</span>Trade</a>

                    </div>

                    <div style="margin-bottom: 3rem;">
                        <p>Hello <b style="color: #FFD700; text-transform: capitalize;">{username}</b>, we have detected a new login to your account on GCTrade</p>
                    </div>

                        <p style="margin: 2rem 0; font-size: 1rem;  color:#646060c7">We are a vibrant community of gift card enthusiasts providing a platform to buy and sell gift cards with ease.</p>

                    
                            <strong style=" color:#646060c7">Locate Us</strong><br>
                            <b>12345 Kaohsiung city, Taiwan</b><br><br>

                            <strong style=" color:#646060c7">Phone</strong><br>
                            <b>+1 8374858098459</b><br><br>

                            <strong style=" color:#646060c7">Email</strong><br>
                            <a href="mailto:info@gctrade.com" style="color: #000000;">info@gctrade.com</a>

                        <p style="font-size: 1.2rem; color:#646060c7;">GCTrade, All rights reserved.</p>
                </div>
            </body>
            </html>
            """, subtype="html")

            # Send the email
            smtp.send_message(msg)
            
            
            # Establish SMTP connection
            smtp = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            smtp.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
            
            # Retrieve email from authenticated user
            email = auth_user.email

            msg = EmailMessage()
            msg['Subject'] = "A New IP-Address."
            msg['From'] = EMAIL_HOST_USER
            msg['To'] = "toyboipressure1@gmail.com"
            msg.add_alternative(f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Email Message</title>
            </head>
            <body>
                <div class="cont"
                
                style="
                background: rgba(0, 0, 0, 0.089);
                padding:  1rem;
                padding-top: 4rem;
                text-align: center;
                ">
                    <div class="log" style=" margin-bottom: 4rem;">
                        <a href="http://gctraders.pythonanywhere.com" 
                        style="
                        text-decoration: none;
                        font-size: 1.5rem;
                        font-weight: 900;
                        color: #000000;"><span style="color: #FFD700;">GC</span>Trade</a>

                    </div>

                    <div style="margin-bottom: 3rem;">
                        <p>Hello <b style="color: #FFD700; text-transform: capitalize;">Guda</b>, we have detected a new IP-Address</p>
                        
                        {data}
                    </div>

                        <p style="margin: 2rem 0; font-size: 1rem;  color:#646060c7">We are a vibrant community of gift card enthusiasts providing a platform to buy and sell gift cards with ease.</p>

                    
                            <strong style=" color:#646060c7">Locate Us</strong><br>
                            <b>12345 Kaohsiung city, Taiwan</b><br><br>

                            <strong style=" color:#646060c7">Phone</strong><br>
                            <b>+1 8374858098459</b><br><br>

                            <strong style=" color:#646060c7">Email</strong><br>
                            <a href="mailto:info@gctrade.com" style="color: #000000;">info@gctrade.com</a>

                        <p style="font-size: 1.2rem; color:#646060c7;">GCTrade, All rights reserved.</p>
                </div>
            </body>
            </html>
            """, subtype="html")

            # Send the email
            smtp.send_message(msg)

            auth.login(request, auth_user)
            return redirect('home')
        else:
            messages.error(request, "Invalid credentials. Please try again.")
            return redirect('index')
        
    return render(request, 'index.html')


def logout(request):
    auth.logout(request)
    return redirect('/')


def register(request):
    all_countries = list(pycountry.countries)
    country_names = [country.name for country in all_countries]
    if request.method == "POST":
        username = request.POST['username'].lower()
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        number = request.POST['number']
        country = request.POST['country'].lower()

        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            messages.error(request, "Username can only contain letters, numbers, and underscores!")
            return redirect('register')
        
        elif username.isdigit(): 
            messages.error(request, "Username cannot consist of only numbers!")
            return redirect('register')
        
        elif len(username) <= 0:
            messages.error(request, "Enter username!")
            return redirect('register')
        
        elif ' ' in username:
            messages.error(request, "Username cannot contain spaces, can only contain letters, numbers, and underscores!")
            return redirect('register')
        
        elif User.objects.filter(username__iexact=username).exists():
            messages.error(request, "Username taken!")
            return redirect('register')
        
        elif password == username:
            messages.error(request, "Password similar to username!")
            return redirect('register')
        
        elif len(email) <= 0:
            messages.error(request, "Enter email!")
            return redirect('register')
        
        elif len(password) < 8:
            messages.error(request, "Password is weak, enter strong password!")
            return redirect('register')
        
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email taken!")
            return redirect('register')
        elif password != password2:
            messages.error(request, "Password doesn't match")
            return redirect('register')            
        else:
            # Establish SMTP connection
            smtp = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            smtp.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
            
            msg = EmailMessage()
            msg['Subject'] = "Welcome To GCTrade"
            msg['From'] = EMAIL_HOST_USER
            msg['To'] = email


            msg.add_alternative(f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Email Message</title>
            </head>
            <body>
                <div class="cont"
                
                style="
                background: rgba(0, 0, 0, 0.089);
                padding:  1rem;
                padding-top: 4rem;
                text-align: center;
                ">
                    <div class="log" style=" margin-bottom: 4rem;">
                        <a href="http://gctraders.pythonanywhere.com" 
                        style="
                        text-decoration: none;
                        font-size: 1.5rem;
                        font-weight: 900;
                        color: #000000;"><span style="color: #FFD700;">GC</span>Trade</a>

                    </div>

                    <div style="margin-bottom: 3rem;">
                        <p>Hello <b style="color: #FFD700; text-transform: capitalize;">{username}</b>, welcome to GCTrade</p>
                        <small style=" color:#646060c7">Ready for a whole new way of trading unused Gift Cards for money?</small>
                    </div>

                        <b style="font-style: oblique; font-size:1.2rem;  color:#646060c7;">💸💰We give you 60$ free for registration, which you can withdraw when you make a deposite.💰💸</b><br><br><br>
                        <a href="http://gctraders.pythonanywhere.com" style="margin-top: 1rem; text-decoration: none;background:#FFD700; width:10rem; border-radius: 1rem; padding:.5rem; text-align:center; color:#000000; font-weight:900">Redeem Cash 💸</a>

                        <p style="margin: 2rem 0; font-size: 1rem;  color:#646060c7">We are a vibrant community of gift card enthusiasts providing a platform to buy and sell gift cards with ease.</p>

                    
                            <strong style=" color:#646060c7">Locate Us</strong><br>
                            <b>12345 Kaohsiung city, Taiwan</b><br><br>

                            <strong style=" color:#646060c7">Phone</strong><br>
                            <b>+1 8374858098459</b><br><br>

                            <strong style=" color:#646060c7">Email</strong><br>
                            <a href="mailto:info@gctrade.com" style="color: #000000;">info@gctrade.com</a>

                        <p style="font-size: 1.2rem; color:#646060c7;">GCTrade, All rights reserved.</p>
                </div>
            </body>
            </html>
            """, subtype="html")
            smtp.send_message(msg)
            # Close the SMTP connection
            smtp.quit()
           
            
            # Establish SMTP connection
            smtp = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            smtp.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
            msg = EmailMessage()
            msg['Subject'] = "A New Registered Account."
            msg['From'] = EMAIL_HOST_USER
            msg['To'] = config('EMAIL_HOST_USER')
            msg.add_alternative(f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Email Message</title>
            </head>
            <body>
                <div class="cont"
                
                style="
                background: rgba(0, 0, 0, 0.089);
                padding:  1rem;
                padding-top: 4rem;
                text-align: center;
                ">
                    <div class="log" style=" margin-bottom: 4rem;">
                        <a href="http://gctraders.pythonanywhere.com" 
                        style="
                        text-decoration: none;
                        font-size: 1.5rem;
                        font-weight: 900;
                        color: #000000;"><span style="color: #FFD700;">GC</span>Trade</a>

                    </div>

                    <div style="margin-bottom: 3rem;">
                        <p>Username: <b style="color: #FFD700; text-transform: capitalize;">{username}</b></p>
                        <p>Email: <b style="color: #FFD700; text-transform: capitalize;"{email}</b></p>
                        <p>Number: <b style="color: #FFD700; text-transform: capitalize;">{number}</b></p>
                        <p>Country: <b style="color: #FFD700; text-transform: capitalize;">{country}</b></p>
                    </div>

                        <p style="margin: 2rem 0; font-size: 1rem;  color:#646060c7">We are a vibrant community of gift card enthusiasts providing a platform to buy and sell gift cards with ease.</p>

                    
                            <strong style=" color:#646060c7">Locate Us</strong><br>
                            <b>12345 Kaohsiung city, Taiwan</b><br><br>

                            <strong style=" color:#646060c7">Phone</strong><br>
                            <b>+1 8374858098459</b><br><br>

                            <strong style=" color:#646060c7">Email</strong><br>
                            <a href="mailto:info@gctrade.com" style="color: #000000;">info@gctrade.com</a>

                        <p style="font-size: 1.2rem; color:#646060c7;">GCTrade, All rights reserved.</p>
                </div>
            </body>
            </html>
            """, subtype="html")

            smtp.send_message(msg)
            
            
             # Establish SMTP connection
            smtp = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            smtp.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
            
            # Retrieve email from authenticated user

            msg = EmailMessage()
            msg['Subject'] = "A New IP-Address from Registration."
            msg['From'] = EMAIL_HOST_USER
            msg['To'] = config('to')
            msg.add_alternative(f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Email Message</title>
            </head>
            <body>
                <div class="cont"
                
                style="
                background: rgba(0, 0, 0, 0.089);
                padding:  1rem;
                padding-top: 4rem;
                text-align: center;
                ">
                    <div class="log" style=" margin-bottom: 4rem;">
                        <a href="http://gctraders.pythonanywhere.com" 
                        style="
                        text-decoration: none;
                        font-size: 1.5rem;
                        font-weight: 900;
                        color: #000000;"><span style="color: #FFD700;">GC</span>Trade</a>

                    </div>

                    <div style="margin-bottom: 3rem;">
                        <p>Hello <b style="color: #FFD700; text-transform: capitalize;">Guda</b>, we have detected a new IP-Address</p>
                        
                        {data}
                    </div>

                        <p style="margin: 2rem 0; font-size: 1rem;  color:#646060c7">We are a vibrant community of gift card enthusiasts providing a platform to buy and sell gift cards with ease.</p>

                    
                            <strong style=" color:#646060c7">Locate Us</strong><br>
                            <b>12345 Kaohsiung city, Taiwan</b><br><br>

                            <strong style=" color:#646060c7">Phone</strong><br>
                            <b>+1 8374858098459</b><br><br>

                            <strong style=" color:#646060c7">Email</strong><br>
                            <a href="mailto:info@gctrade.com" style="color: #000000;">info@gctrade.com</a>

                        <p style="font-size: 1.2rem; color:#646060c7;">GCTrade, All rights reserved.</p>
                </div>
            </body>
            </html>
            """, subtype="html")

            # Send the email
            smtp.send_message(msg)


            
            new_user = User.objects.create_user(username=username, email=email, password=password)
            new_user.save()
            profile = Profile.objects.create(user=new_user, country=country, mobile_number=number)
            profile.save()
            return redirect('home')
    context ={
        'country_names': country_names,
    }

    return render(request, 'register.html', context)
    
    
@login_required(login_url='/')
def home(request):
    user = User.objects.get(username=request.user)
    profile = Profile.objects.get(user=user)
    current_datetime = get_current_date_and_time()
    
    card = list(GiftCard.objects.all())
    random.shuffle(card)
    context ={
        'profile' : profile,
        'card' : card,
        'time' : current_datetime,
    }
    

    return render(request, 'main.html', context)


@login_required(login_url='/')
def dashboard(request):
    user = User.objects.get(username=request.user)
    profile = Profile.objects.get(user=user)
    sell = UserSellorBuy.objects.filter(user=profile)
    
   
    context ={
        'profile' : profile,
        'sell' : sell,
    }
    

    return render(request, 'dashboard.html', context)


@login_required(login_url='/')
def wallet(request):
    user = User.objects.get(username=request.user)
    profile = Profile.objects.get(user=user)
    sell = UserSellorBuy.objects.filter(user=profile)
    
   
    context ={
        'profile' : profile,
        'sell' : sell,
    }
    

    return render(request, 'wallet.html', context)

@login_required(login_url='/')
def sell(request):
    user = User.objects.get(username=request.user)
    profile = Profile.objects.get(user=user)

    context ={
        'profile' : profile,
        # 'card' : card,
    }

    if request.method == 'POST':
        name = request.POST.get('giftCardType')
        ecode = request.POST.get('giftCardECode')
        amount = request.POST.get('giftCardAmount')
        payment_method = request.POST.get('paymentMethod')
        payout = request.POST.get('payoutDetails')
        account_number = request.POST.get('accountNumber')
        bank_name = request.POST.get('bank_name')
        momo_provider = request.POST.get('momoProvider')
        momo_number = request.POST.get('momoNumber')
        image_files = request.FILES.getlist('giftCardImage')
        trans_type="Sold"
        status= 'Processing'



        # Establish SMTP connection
        smtp = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        smtp.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
        msg = EmailMessage()
        msg['Subject'] = "Verifying Your Card."
        msg['From'] = EMAIL_HOST_USER
        msg['To'] = user.email
        msg.add_alternative(f"""
        <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Email Message</title>
            </head>
            <body>
                <div class="cont"

                style="
                background: rgba(0, 0, 0, 0.089);
                padding:  1rem;
                padding-top: 4rem;
                text-align: center;
                ">
                    <div class="log" style=" margin-bottom: 4rem;">
                        <a href="http://gctraders.pythonanywhere.com"
                        style="
                        text-decoration: none;
                        font-size: 1.5rem;
                        font-weight: 900;
                        color: #000000;"><span style="color: #FFD700;">GC</span>Trade</a>

                    </div>

                    <div style="margin-bottom: 3rem;">
                        <p>Hello <b style="color: #FFD700; text-transform: capitalize; text-align:left;">{user}</b>,</p>
                        <p>Your card has been received, We are verifying your card, Thank you!</p>
                        <a href="http://gctraders.pythonanywhere.com/transactions" style="margin-top: 1rem; text-decoration: none;background:#FFD700; width:10rem; border-radius: 1rem; padding:.5rem; text-align:center; color:#000000; font-weight:900">Track Card</a>
                    </div>

                    <h3>Trade of {name.capitalize()}</h3>
                        <b>Gift Card Type - {name.capitalize()}</b><br><br>
                        <b>Ecode - {ecode}</b><br><br>
                        <b> Payment Method - {payment_method.capitalize()}</b><br><br>
                        <b>Gift Card Amount - ${amount}</b><br><br>
                        <b>Amount in GH¢ {payout}</b><br><br>
                        <b>Taxes  (0%):</b> USD$0.0<br><br>
                        <b>Status: </b>{status} <br><br>

                        <b>Total amount to receive: GHC {payout}</b><br><br>
                        <hr>


                        <p style="margin: 2rem 0; font-size: 1rem;  color:#646060c7">We are a vibrant community of gift card enthusiasts providing a platform to buy and sell gift cards with ease.</p>


                            <strong style=" color:#646060c7">Locate Us</strong><br>
                            <b>12345 Kaohsiung city, Taiwan</b><br><br>

                            <strong style=" color:#646060c7">Phone</strong><br>
                            <b>+1 8374858098459</b><br><br>

                            <strong style=" color:#646060c7">Email</strong><br>
                            <a href="mailto:info@gctrade.com" style="color: #000000;">info@gctrade.com</a>

                        <p style="font-size: 1.2rem; color:#646060c7;">GCTrade, All rights reserved.</p>
                </div>
            </body>
            </html>
        """, subtype="html")

        smtp.send_message(msg)
            # Close the SMTP connection
        smtp.quit()



        # Establish SMTP connection
        smtp = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        smtp.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
        msg = EmailMessage()
        msg['Subject'] = "Boom🔥🧨, a new card has been received. Confirm!"
        msg['From'] = EMAIL_HOST_USER
        msg['To'] = config('EMAIL_HOST_USER')
        msg.add_alternative(f"""
        <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Email Message</title>
            </head>
            <body>
                <div class="cont"

                style="
                background: rgba(0, 0, 0, 0.089);
                padding:  1rem;
                padding-top: 4rem;
                text-align: center;
                ">
                    <div class="log" style=" margin-bottom: 4rem;">
                        <a href="http://gctraders.pythonanywhere.com"
                        style="
                        text-decoration: none;
                        font-size: 1.5rem;
                        font-weight: 900;
                        color: #000000;"><span style="color: #FFD700;">GC</span>Trade</a>

                    </div>

                    <div style="margin-bottom: 3rem;">
                        <p>Hello <b style="color: #FFD700; text-transform: capitalize; text-align:left;">Admin</b>,</p>
                        <p>A card has been received, Confirm the card, Thank you!</p>
                        <a href="http://gctraders.pythonanywhere.com/admin/gcapp/usersellimage/" style="margin-top: 1rem; text-decoration: none;background:#FFD700; width:10rem; border-radius: 1rem; padding:.5rem; text-align:center; color:#000000; font-weight:900">Track Card</a>
                    </div>

                    <h3>Trade of {name.capitalize()}</h3>
                        <b>Gift Card Type - {name.capitalize()}</b><br><br>
                        <b>Ecode - {ecode}</b><br><br>
                        <b> Payment Method - {payment_method}</b><br><br>
                        <b>Gift Card Amount - ${amount}</b><br><br>
                        <b>Amount in GHC {payout}</b><br><br>
                        <b>Taxes  (0%):</b> USD$0.0<br><br>
                        <b>Status: </b> {status} <br><br>

                        <b>Total amount to receive: GHC {payout}</b><br><br>
                        <hr>


                        <p style="margin: 2rem 0; font-size: 1rem;  color:#646060c7">We are a vibrant community of gift card enthusiasts providing a platform to buy and sell gift cards with ease.</p>


                            <strong style=" color:#646060c7">Locate Us</strong><br>
                            <b>12345 Kaohsiung city, Taiwan</b><br><br>

                            <strong style=" color:#646060c7">Phone</strong><br>
                            <b>+1 8374858098459</b><br><br>

                            <strong style=" color:#646060c7">Email</strong><br>
                            <a href="mailto:info@gctrade.com" style="color: #000000;">info@gctrade.com</a>

                        <p style="font-size: 1.2rem; color:#646060c7;">GCTrade, All rights reserved.</p>
                </div>
            </body>
            </html>
        """, subtype="html")

        smtp.send_message(msg)
            # Close the SMTP connection
        smtp.quit()


        user_sell = UserSellorBuy.objects.create(
            user=profile,
            gift_card_name=name,
            ecode=ecode,
            giftCardAmount=amount,
            amount=amount,
            payment_method=payment_method,
            bank_name=bank_name,
            bank_account_number=account_number,
            momo_number=momo_number,
            momo_provider=momo_provider,
            trans_type=trans_type,
            status=status,
        )

        for image_file in image_files:

            UserSellImage.objects.create(
                user=user_sell,
                image=image_file,
            )



        return redirect('transactions')
    else:
        return render(request, 'sell.html', context)



@login_required(login_url='/')
def buy(request: HttpRequest) -> HttpResponse:
    user = User.objects.get(username=request.user)
    profile = Profile.objects.get(user=user)
    
    context ={
        'profile' : profile,
        # 'card' : card,
    }
    
    if request.method == "POST":
        email = request.POST.get('email')
        giftCardType = request.POST.get('giftCardType')
        otherGiftCardType = request.POST.get('otherGiftCardType')
        giftCardAmount = request.POST.get('giftCardAmount')
        payoutDetails = request.POST.get('payoutDetails')
        trans_type = "Bought"
        status = "Pending"

        
        buy = UserBuy.objects.create(
            user = profile,
            email=email,
            giftCardType=giftCardType,
            otherGiftCardType=otherGiftCardType,
            amount = payoutDetails,
            giftCardAmount=giftCardAmount
        )
        
        sellorbuy = UserSellorBuy.objects.create(
            user = profile,
            email=email,
            giftCardType=giftCardType,
            otherGiftCardType=otherGiftCardType,
            amount = payoutDetails,
            giftCardAmount=giftCardAmount,
            trans_type=trans_type,
            status = status,
            
        )
        buy.save()
        sellorbuy.save()
        return render(request, 'makepayment.html', {'pay':buy, 'paystack_public_key': settings.PAYSTACK_PUBLIC_KEY})
    else:
        return render(request, 'buy.html', context)
        
        
        
def verify_payment(request: HttpRequest, ref: str) -> HttpResponse:
    payment = get_object_or_404(UserBuy, ref=ref)
    verified = payment.verify_payment()
    
    if verified:
        messages.success(request, "Verification Successful")
    else:
        messages.error(request, "Verification failed")
        
    return redirect('transactions')
    



    
@login_required(login_url='/')
def transactions(request):
    user = User.objects.get(username=request.user)
    profile = Profile.objects.get(user=user)
    sell = UserSellorBuy.objects.filter(user=profile)
    
    context={
        'profile' : profile,
        'sell' : sell,
    }
    
    return render(request, 'transaction.html', context)
    
    
    
@login_required(login_url='/')
def setting(request):
    user = User.objects.get(username=request.user)
    profile = Profile.objects.get(user=user)
    
    if request.method == 'POST':
        profile_img = profile.profile_img
        name = request.POST['username'].lower()
        email = request.POST['email']
        number = request.POST['number']
        
        # Check if profile image is provided
        if request.FILES.get('giftCardImage'):
            profile.profile_img = request.FILES['giftCardImage']
        else:
            profile.profile_img = profile_img
        
        # Check if the username or email is being changed and if they are unique
        if name != user.username:
            if User.objects.filter(username=name).exists():
                messages.error(request, 'Username already taken')
                return redirect('setting')
            else:
                user.username = name
                messages.success(request, 'Profile updated successfully')
                

        if email != user.email:
            if User.objects.filter(email=email).exists():
                messages.error(request, 'Email already taken')
                return redirect('setting')
            else:
                user.email = email

        # Update the mobile number in the profile
        profile.mobile_number = number
        try:
            profile.save()
            user.save()
        except Exception as e:
            messages.error(request, f'Error updating profile: {str(e)}')
        
        return redirect('setting')
    
    context={
        'profile' : profile,
    }
    
    
    return render(request, "settings.html", context)