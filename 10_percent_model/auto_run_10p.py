# 脚本名: daily_script.py

# 示例：发送一封测试邮件
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import pandas as pd
from tenrise_global_var import *
import efinance as ef
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO

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
    with open('dataframe_plot.jpg', 'rb') as f:
        img = MIMEImage(f.read())
        img.add_header('Content-Disposition', 'attachment', filename='dataframe_plot.jpg')
        msg.attach(img)

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
    from tenrise_get_stock_data import *
    from tenrise_predict_today import *
    eft_id_list = [
    '399006',
    '399001',
    '399005',
    '000905']
    stock_keys=None
    file_name = "10rise_TEST_DATA.csv"
    for id in eft_id_list:
        stocks=ef.stock.get_members(id)# CYB300
        stock_keys=pd.concat([stock_keys,stocks['股票名称']])
    current_date = datetime.now()
    formatted_date = current_date.strftime('%Y%m%d')
    start_date = test_start_date
    end_date   = str(formatted_date)
    stock_keys=stock_keys.drop_duplicates(inplace=False)
    print("the stock total numbers ",stock_keys.shape)

    table=build_frame(list(stock_keys.values),start_date,end_date)
    csv_df = pd.DataFrame(data=table,index=None)
    csv_df.to_csv("./stock_data/"+file_name)
    res = pd.DataFrame()
    res = predict_now()
    plt.figure()
    res.plot(kind='bar')
    
    plt.savefig('dataframe_plot.jpg')
    plt.close()
    html_content=res.to_html(index=True,header=True)
    send_email("10 rise stock predictor", html_content)