import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr


def mail(mailText: str, mailSubject: str) -> bool:
    ret = True
    try:
        my_sender = 'dezhengli@foxmail.com'  # 发件人邮箱账号
        my_pass = 'mzwlghduktwibadb'  # 发件人邮箱密码
        my_user = 'dezhengli@foxmail.com'  # 收件人邮箱账号，我这边发送给自己
        msg = MIMEText(mailText, 'plain', 'utf-8')
        msg['From'] = formataddr(["图书馆自动预约系统", my_sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
        msg['To'] = formataddr(["Me", my_user])  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
        msg['Subject'] = mailSubject  # 邮件的主题，也可以说是标题

        server = smtplib.SMTP_SSL("smtp.qq.com", 465)  # 发件人邮箱中的SMTP服务器，端口是25
        server.login(my_sender, my_pass)  # 括号中对应的是发件人邮箱账号、邮箱密码
        server.sendmail(my_sender, [my_user, ], msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
        server.quit()  # 关闭连接
    except Exception as e:  # 如果 try 中的语句没有执行，则会执行下面的 ret=False
        ret = False
    return ret


ret = mail(mailText='gg', mailSubject='Smart Falcon desu~')
if ret:
    print("邮件发送成功")
else:
    print("邮件发送失败")