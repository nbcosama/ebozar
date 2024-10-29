import smtplib
from email.mime.text import MIMEText
from django.http import JsonResponse
import re



def sendemail(request, email, random_number):
    to_email = email
    random_num = random_number
    
    def is_valid_email(to_email):
        return re.match(r"[^@]+@[^@]+\.[^@]+", to_email) is not None

    if not is_valid_email(to_email):
        return JsonResponse({"message": "Invalid email format", "mail": "Failed"})

    from_email = "smtp.otp@gmail.com"
    app_password = "emir yxvo wpsr ctuv"

    msg = MIMEText(f"Hi there! This is your verification code {random_num}")
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = "Verification Code"

    try:
        connection = smtplib.SMTP("smtp.gmail.com", 587)
        connection.starttls() 
        connection.login(user=from_email, password=app_password)
        connection.sendmail(from_addr=from_email, to_addrs=[to_email], msg=msg.as_string())
        connection.close() 
        return True
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return JsonResponse({"message": "Error", "mail": str(e)})




def send_username(request, email, username):
    to_email = email
    user_name = username
    
    def is_valid_email(to_email):
        return re.match(r"[^@]+@[^@]+\.[^@]+", to_email) is not None

    if not is_valid_email(to_email):
        return JsonResponse({"message": "Invalid email format", "mail": "Failed"})

    from_email = "smtp.otp@gmail.com"
    app_password = "emir yxvo wpsr ctuv"

    msg = MIMEText(f"Hi there! <strong>{user_name}</strong> is your user name" , "html")
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = "User Name"

    try:
        connection = smtplib.SMTP("smtp.gmail.com", 587)
        connection.starttls() 
        connection.login(user=from_email, password=app_password)
        connection.sendmail(from_addr=from_email, to_addrs=[to_email], msg=msg.as_string())
        connection.close() 
        return True
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return JsonResponse({"message": "Error", "mail": str(e)})
    
    
    


