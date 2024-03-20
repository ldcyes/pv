# 脚本名: daily_script.py

# 示例：发送一封测试邮件
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from get_stock_data import *
import pandas as pd
from global_var import *
from train_once import *

def send_email(subject, body):
    # 设置邮箱登录信息
    email_sender = 'ldcyes@163.com'
    email_receiver = email_sender
    password = 'jfx-win'

    # 构建邮件
    msg = MIMEMultipart()
    msg['From'] = email_sender
    msg['To'] = email_receiver
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'html', 'utf-8'))

    # 发送邮件
    try:
        server = smtplib.SMTP('smtp.163.com',25)
        server.starttls()
        server.login(email_sender, password)
        text = msg.as_string()
        server.sendmail(email_sender, email_receiver, text)
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print("Email failed to send.")
        print(e)

if __name__ == "__main__":
    current_date = datetime.now()
    formatted_date = current_date.strftime('%Y%m%d')

    if(train):
        start_date = train_start_date
        end_date   = str(formatted_date)
        file_name = "STOCK_TRAIN_DATA.csv"
    else:
        start_date = test_start_date
        end_date   = str(formatted_date)
        file_name = "STOCK_TEST_DATA.csv"
    table= build_frame(x_stocks,start_date,end_date)
    csv_df = pd.DataFrame(data=table,index=None)
    csv_df.to_csv("./stock_data/"+file_name)
    res = train_once()
    html_content=res.to_html(index=True,header=True)
    send_email("stock predictor", html_content)
