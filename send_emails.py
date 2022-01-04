# sending an email to a list of addresses
def send_email(mailing_list, message, sender_email, EMAIL_PASSWORD):
    import smtplib, ssl
    # For gmail, must go to the following link to allow less secure access:
    # https://www.google.com/settings/security/lesssecureapps

    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, EMAIL_PASSWORD)
        for receiver_email in mailing_list:
            try:
                server.sendmail(sender_email, receiver_email, message)
                print(f"Sent to {receiver_email}")
            except:
                print(f"Could not mail to {receiver_email}")

def determine_greeting():
    try:
        from datetime import datetime
        now = str(datetime.now().time()) # time xx:xx:xx.xxxxx in string format

        if 3 < int(now[:2]) < 12:
            return "Good morning"
        elif 12 <= int(now[:2]) < 17:
            return "Good afternoon"
        elif 17<=int(now[:2])< 20:
            return "Good evening"
        elif 20 <= int(now[:2]) or int(now[:2])<= 3:
            return "Good night"
        else:
            return "Good morning"
    except:
        print("could not determine greeting. Using generic greeting instead.")
        return "Hello"


# PUT EMAILS AS STRINGS HERE
mailing_list = []

message = f"Subject: {determine_greeting()}!!\n\nI hope you are well.\n\n This message is sent from Python. This is a test.\n\nKind Regards,\nQingyuan."

SENDER_EMAIL = input("Enter sender's email to send grade update notifications: ") # to get notification after grade update
EMAIL_PASSWORD = input("Enter sender's email password: ")

send_email(mailing_list, message, SENDER_EMAIL, EMAIL_PASSWORD)