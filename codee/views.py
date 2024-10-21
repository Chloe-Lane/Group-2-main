import string, random, logging
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from PIL import Image, ImageDraw, ImageFont
from django.http import HttpResponse
from django.contrib import messages
from django.conf import settings
from profiles.models import Profile


def generate_captcha(request):
    captcha_text = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    request.session['captcha'] = captcha_text  # Save the CAPTCHA text in the session

    # Create CAPTCHA image
    img = Image.new('RGB', (250, 80), color='white')
    d = ImageDraw.Draw(img)

    # Set font size and load a font
    font_size = 30  # Increase font size here
    try:
        # Load a font (you may need to provide the correct path to a .ttf file)
        font = ImageFont.truetype("arial.ttf", font_size)  # Adjust font size and type as needed
    except IOError:
        font = ImageFont.load_default()  # Fallback to default font if specific font cannot be loaded

    # Draw the text with the specified font
    d.text((10, 20), captcha_text, fill=(0, 0, 0), font=font)

    response = HttpResponse(content_type="image/png")
    img.save(response, "PNG")
    return response


last_registered_email = ""
last_registered_password = ""
last_registered_first_name = ""
last_registered_last_name = ""


def home(request):
    global last_registered_email, last_registered_password, last_registered_first_name, last_registered_last_name, hide_last_name

    if request.method == 'POST':
        if request.POST['captcha'] != request.session['captcha']:
            messages.error(request, 'Invalid Captcha, Please try again!')
            return render(request, 'auth/home.html')  # Re-render the page with error message

        try:
            last_registered_email = request.POST['email']
            last_registered_password = request.POST['password']
            last_registered_first_name = request.POST['first_name']
            last_registered_last_name = request.POST['last_name']

            hide_last_name = request.POST.get('hide_last_name') is not None
            request.session['hide_last_name'] = hide_last_name

            username = last_registered_email.split('@')[0]

            while User.objects.filter(username=username).exists():
                username += str(random.randint(1, 1000))  # Append a random number if the username exists

            user = User.objects.create_user(username=username, email=last_registered_email,
                                            password=last_registered_password)

            # Ensure no automatic friendship is created
            if not hasattr(user, 'profile'):
                Profile.objects.create(user=user)  # Create the profile only if it doesn't exist

            return redirect('login')

        except Exception as e:
            logger.error(f"Error in user registration: {e}")
            messages.error(request, 'Registration failed, please try again.')

    return render(request, 'auth/home.html')


def login_view(request):
    global last_registered_email, last_registered_password, last_registered_first_name, last_registered_last_name  # Access the global variables

    error = None  # Initialize the error variable

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Check if the email and password match the last registered user's credentials
        if email == last_registered_email and password == last_registered_password:
            # Extract username from the email
            username = last_registered_email.split('@')[0]
            return redirect('page_view', username=username)  # Redirect to the profile using username
        else:
            error = 'Invalid email or password'  # Set error if credentials don't match

    # Render the login page with the error message if it exists
    return render(request, 'auth/login.html', {'error': error})


def custom_logout(request):
    logout(request)  # Log the user out
    return redirect('login')  # Redirect to the login page


def page_view(request, username):
    user = get_object_or_404(User, username=username)

    return render(request, 'homep/page.html', {
        'user': user,
    })


import time

timestamp = int(time.time())


def forgot_password(request):
    return render(request, 'password/forgot_password.html')


logger = logging.getLogger(__name__)


# Your existing imports...

def send_reset_code(request):
    if request.method == 'POST':
        email = request.POST['email']
        phone = request.POST['phone']  # Get the cellphone number
        user = User.objects.filter(email=email).first()

        if user and user.profile.phone == phone:  # Assuming you have a profile model linked to the User
            # Generate a reset code
            reset_code = random.randint(100000, 999999)

            # Save the reset code in the session or database for verification later
            request.session['reset_code'] = reset_code

            # Send SMS (you'll need an SMS gateway service)
            try:
                # Use an SMS API service to send the reset code
                send_sms(phone, f'Your password reset code is: {reset_code}')
                messages.success(request, 'A password reset code has been sent to your cellphone.')
            except Exception as e:
                logger.error(f"Failed to send SMS: {e}")
                messages.error(request, 'Failed to send SMS. Please try again later.')
            return redirect('login')
        else:
            messages.error(request, 'Email address or cellphone number not found.')
            return render(request, 'password/forgot_password.html')

    return render(request, 'password/forgot_password.html')


def reset_password(request):
    if request.method == 'POST':
        entered_code = request.POST.get('reset_code')
        new_password = request.POST.get('new_password')

        if entered_code == str(request.session.get('reset_code')):  # Check if code matches
            user = User.objects.get(phone=request.POST['phone'])  # Retrieve user by phone if needed
            user.set_password(new_password)
            user.save()
            messages.success(request, 'Your password has been reset successfully.')
            return redirect('login')
        else:
            messages.error(request, 'Invalid reset code.')

    return render(request, 'password/reset_password.html')


def send_sms(to, message):
    # Your Twilio account credentials
    account_sid = 'AC2b73693c4aaa9c7999405b793a7f49b9'
    auth_token = 'cd5eccb364449075bb4ead648b156801'
    client = Client(account_sid, auth_token)

    client.messages.create(
        body=message,
        from_='0985088850',  # Your Twilio phone number
        to=to
    )


def verify_code(request):
    if request.method == 'POST':
        phone_number = request.session.get('phone_number')  # Get the stored phone number
        verification_code = request.POST['code']  # Code entered by the user

        # Initialize the Twilio client
        account_sid = 'AC2b73693c4aaa9c7999405b793a7f49b9'
        auth_token = 'cd5eccb364449075bb4ead648b156801'  # Replace with your actual auth token
        client = Client(account_sid, auth_token)

        # Send a verification code to the user's phone number
        verification = client.verify.v2.services('VA26390ea7fd9651fc23d9409f86842bb6') \
            .verifications \
            .create(to=+639850885850, channel='sms')

        # Check if the verification code matches
        verification_check = client.verify.v2.services('VA26390ea7fd9651fc23d9409f86842bb6') \
            .verification_checks \
            .create(to=+639850885850, code=verification_code)

        if verification_check.status == 'approved':
            messages.success(request, 'Verification successful! You can now reset your password.')
            return redirect('reset_password')  # Redirect to your password reset page
        else:
            messages.error(request, 'Invalid verification code. Please try again.')

    return render(request, 'password/verify_code.html')


def send_verification_code(request):
    if request.method == 'POST':
        phone_number = request.POST['phone_number']  # User's phone number input

        # Create a Twilio client
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

        # Send verification code
        try:
            verification = client.verify.v2.services(settings.TWILIO_VERIFY_SERVICE_SID) \
                .verifications \
                .create(to=+639850885850, channel='sms')

            # Optional: Store the phone number in the session for later use
            request.session['phone_number'] = phone_number
            messages.success(request, 'A verification code has been sent to your phone.')
            return redirect('verify_code')  # Redirect to a page for code verification
        except Exception as e:
            messages.error(request, f'Failed to send verification code: {e}')
            return render(request, 'password/forgot_password.html')

    return render(request, 'password/forgot_password.html')

def fetch_photos_for_album(album_id):
    # Placeholder logic: Replace this with actual data retrieval from your database or media storage
    photos = []
    if album_id == 1:
        photos = [{'url': '/static/images/album1/photo1.jpg'}, {'url': '/static/images/album1/photo2.jpg'}]
    elif album_id == 2:
        photos = [{'url': '/static/images/album2/photo1.jpg'}, {'url': '/static/images/album2/photo2.jpg'}]
    elif album_id == 3:
        photos = [{'url': '/static/images/album3/photo1.jpg'}, {'url': '/static/images/album3/photo2.jpg'}]
    elif album_id == 4:
        photos = [{'url': '/static/images/album4/photo1.jpg'}, {'url': '/static/images/album4/photo2.jpg'}]
    return photos

# Updated album_view to handle different albums
def album_view(request, username, album_id):
    # Fetch different content based on album_id
    if album_id == 1:
        album_data = {"title": "Album 1", "photos": fetch_photos_for_album(1)}
    elif album_id == 2:
        album_data = {"title": "Album 2", "photos": fetch_photos_for_album(2)}
    elif album_id == 3:
        album_data = {"title": "Album 3", "photos": fetch_photos_for_album(3)}
    elif album_id == 4:
        album_data = {"title": "Album 4", "photos": fetch_photos_for_album(4)}
    else:
        album_data = {"title": "Unknown Album", "photos": []}

    return render(request, 'auth/album.html', {'album_data': album_data, 'username': username})
