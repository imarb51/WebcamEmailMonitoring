import smtplib
import imghdr
from email.message import EmailMessage

EMAIL = "mrimranshaikh894@gmail.com"
PASSWORD = "hizelkrqlqrzyddc"
RECEIVER = "imranance99@gmail.com"
def send_email(image_path):
    email_msg =EmailMessage()
    email_msg["Subject"] = "New Customer Showed Up"
    email_msg.set_content("Hey, New Customer came up")

    with open(image_path,"rb") as file:
        content = file.read()
    email_msg.add_attachment(content,maintype = "image",subtype = imghdr.what(None,content))


    gmail = smtplib.SMTP("smtp.gmail.com",587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(EMAIL,PASSWORD)
    gmail.sendmail(EMAIL,RECEIVER,email_msg.as_string())
    gmail.quit()

if __name__ == "__main__":
    send_email(image_path="images/19.png")