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
    html_body = ''.join(body)
    msg.attach(MIMEText(html_body, 'html', 'utf-8'))

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
    formatted_date = current_date.strftime('%Y-%m-%d')

    if(train):
        start_date = train_start_date
        end_date   = str(formatted_date)
        print(end_date)
        file_name = "STOCK_TRAIN_DATA.csv"
    else:
        start_date = test_start_date
        end_date   = str(formatted_date)
        file_name = "STOCK_TEST_DATA.csv"
    
    mail_stocks = ['NVDA','TSLA','LI','QCOM','BIDU']
    html_content = []
    col_list = []
       
    for target in train_targets:
              for string in [' pred',' confid']:
                     col_list.append(str(target)+string)
       
    model_name=[#'decision tree',#'SVM',
                   'RandomForest',#'MLP','SGD',
                   'XGboost']
       
    res = pd.DataFrame(columns=col_list,index=model_name)
    for stock in mail_stocks:
        table= build_frame(['QQQ',stock],start_date,end_date)
        csv_df = pd.DataFrame(data=table,index=None)
        csv_df.to_csv("./stock_data/"+str(stock)+file_name)
        df_org = pd.read_csv("./stock_data/"+str(stock)+"STOCK_TRAIN_DATA.csv")
        res = train_once(df_org=df_org,x_stocks=['QQQ',stock],res_df=res,train_targets=train_targets,y_stock=stock,features=features)
        html_content.append(res.to_html(index=True,header=True))
    send_email("stock predictor", html_content)
