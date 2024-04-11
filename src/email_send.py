# need pip install: smtplib
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
import ssl


# function: 发送邮件
# param1  sender_email: 发送人邮箱
# param2  sender_password: 邮箱密码
# param3  receiver_email_list: 收件人列表
# param4  subject: 主题
# param5  message: 正文
# return  None
def send_email(sender_email, sender_password, receiver_email_list, subject, message):
    # 设置邮件内容
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['Subject'] = Header(subject, 'utf-8')

    # 邮件正文
    msg.attach(MIMEText(message, 'plain', 'utf-8'))

    # 连接 SMTP 服务器并发送邮件
    try:
        context = ssl.create_default_context()
        server = smtplib.SMTP_SSL('smtp.qq.com', 465, context=context)  # 使用客户端 SSL 上下文
        server.login(sender_email, sender_password)
        
        for receiver_email in receiver_email_list:
            msg['To'] = receiver_email
            server.sendmail(sender_email, receiver_email, msg.as_string())
            print(f"邮件发送成功至 {receiver_email}")
        
        server.quit()
        print("邮件发送完毕")
    except Exception as e:
        print("邮件发送失败:", str(e))