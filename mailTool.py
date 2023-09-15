import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr


def mail(mailText: str, mailSubject: str, mailSender: str, mailVPW: str) -> bool:
    ret = True
    try:
        my_sender = mailSender  # Sender's mail address
        my_pass = mailVPW  # Sender's mail password
        my_user = mailSender  # Reciever's mail address
        msg = MIMEText(mailText, 'plain', 'utf-8')
        msg['From'] = formataddr(["图书馆自动预约系统", my_sender])
        msg['To'] = formataddr(["Me", my_user]) 
        msg['Subject'] = mailSubject  # Mail title

        server = smtplib.SMTP_SSL("smtp.qq.com", 465)  
        server.login(my_sender, my_pass) 
        server.sendmail(my_sender, [my_user, ], msg.as_string())  
        server.quit()  
    except Exception:  
        ret = False
    return ret


def mailAndCheck(mailText: str, mailSubject: str, mailSender: str, mailVPW: str):
    ret = mail(mailText, mailSubject, mailSender, mailVPW)
    if ret:
        print("邮件发送成功")
    else:
        print("邮件发送失败")
