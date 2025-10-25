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
        server = smtplib.SMTP_SSL('smtp.163.com',465)
        #server.starttls()
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

    mail_stocks = ['SOXX','AMD','COIN','TSLA','BABA']# 'INTC', 'QCOM', 'AVGO', 'MSFT', 'GOOG', 'Meta', 'BABA', 'BILI', 'COIN', 'TSLA']
    html_content = []
    col_list = []
       
    model_name=[#'decision tree',#'SVM',
                   'RandomForest',#'MLP','SGD',
                   'XGboost']
       
    res = pd.DataFrame(columns=col_list,index=model_name)
    res_list = []
    table = build_frame(['QQQ']+mail_stocks, start_date, end_date)

    for stock in mail_stocks:
        #table = build_frame(['QQQ', stock], start_date, end_date)
        csv_df = pd.DataFrame(data=table, index=None)
        csv_df.to_csv("./stock_data/STOCK_TRAIN_DATA.csv", index=False)
        df_org = pd.read_csv("./stock_data/STOCK_TRAIN_DATA.csv")
        res_temp = train_once(
            df_org=df_org,
            x_stocks=['QQQ', stock],
            res_df=pd.DataFrame(columns=col_list, index=model_name),
            train_targets=train_targets,
            y_stock=stock,
            features=get_features_name(7)
        )
        res_list.append(res_temp)

    # 合并所有结果
    res_combined = pd.concat(res_list)

    # 按照 'pred' 列从大到小排序（假设列名为 'pred'，如有不同请替换为实际列名）
    if 'pred' in res_combined.columns:
        res_combined = res_combined.sort_values(by='pred', ascending=False)
    elif any(col.endswith(' pred') for col in res_combined.columns):
        # 如果有多个以 ' pred' 结尾的列，按第一个排序
        pred_col = [col for col in res_combined.columns if col.endswith(' pred')][0]
        res_combined = res_combined.sort_values(by=pred_col, ascending=False)

    html_content.append(res_combined.to_html(index=True, header=True))
    send_email("stock predictor", html_content)
