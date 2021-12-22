import os
import pymysql
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

#设置登录及服务器信息
mail_host='smtp.qq.com'
mail_user='1069503555@qq.com'
mail_pass='qmpkyuzivhxfbfea'
sender='ghz'
receivers=['10012187@zte.com.cn']


#conn = pymysql.connect(host=DATABASES['default']['HOST'],port=int(DATABASES['default']['PORT']), user=DATABASES['default']['USER'],password=DATABASES['default']['PASSWORD'],database=os.environ.get("MYSQL_DATABASE", 'django_demo'),charset="utf8")
conn = pymysql.connect(host='10.0.224.3', port=3306,user='root',password=')bk7K.9w',database='django_demo',charset="utf8")

# 得到一个可以执行SQL语句的光标对象
cursor = conn.cursor()
sql='select * from Markers'

cursor.execute(sql)
ret=cursor.fetchall()

filename='daka.txt'

with open(filename,'w') as f:
    for r in ret:
        f.write(str(r)+'\n')
    print('Data write is over')



#设置eamil信息
#添加一个MIMEmultipart类，处理正文及附件
message = MIMEMultipart()
message['From'] = sender
message['To'] = receivers[0]
message['Subject'] = 'title'

#设置txt参数
part2 = MIMEText('viwes.py','plain','utf-8')
#附件设置内容类型，方便起见，设置为二进制流
part2['Content-Type'] = 'application/octet-stream'
#设置附件头，添加文件名
part2['Content-Disposition'] = 'attachment;filename="daka.txt"'
message.attach(part2)

#登录并发送
try:
    smtpObj = smtplib.SMTP()
    smtpObj.connect(mail_host,25)
    smtpObj.login(mail_user,mail_pass)
    smtpObj.sendmail(
        sender,receivers,message.as_string())
    print('success')
    smtpObj.quit()
except smtplib.SMTPException as e:
    print('error',e)