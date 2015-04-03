import requests,getpass
from bs4 import BeautifulSoup

login_data = {
    'user':input('請輸入帳號:'),
    'pass':getpass.getpass('請輸入密碼:'),
    'Submit':'登入'
}

sess = requests.session()
sess.get('https://ceiba.ntu.edu.tw/')
sess.post('https://ceiba.ntu.edu.tw/ChkSessLib.php')
sess.get('https://web2.cc.ntu.edu.tw/p/s/login2/p1.php')
r = sess.post('https://web2.cc.ntu.edu.tw/p/s/login2/p1.php',
        data = login_data)
sess.get(r.url)
r = sess.get('https://ceiba.ntu.edu.tw/student/index.php?seme_op=all')

soup = BeautifulSoup(r.content.decode('big5'))
courses = soup.table.find_all(target='_blank')
for idx,item in enumerate(courses):
    print(idx+1,'.',item.string)
go = int(input('選擇資料夾編號(輸入0返回上一頁):'))

r = requests.get(courses[go-1]['href'])
serial = r.url.split('=')[1]
sess.get('https://ceiba.ntu.edu.tw/modules/index.php?csn='+
        serial+'&default_fun=hw&current_lang=chinese')
sess.get('https://ceiba.ntu.edu.tw/modules/main.php?csn='+
        serial+'&default_fun=hw&current_lang=chinese')
r = sess.get(r.url)

soup = BeautifulSoup(r.content.decode('big5'))
hw = soup.find_all('tr')
for idx,item in enumerate(hw):
    try:
        print(idx+1,'.',item.td.string)
    except:
        pass
go = int(input('選擇作業:'))

r = sess.get('https://ceiba.ntu.edu.tw/modules/hw/'+hw[go-1].a['href'])
print(r.content.decode('big5'))

path = input('輸入上傳檔案路徑:')

upload_data = {
    'op':'hw_upload',
    'hw_sn':'114530',
    'old_file':'/hw114530/hw114530_b03705024_e43d16c2c6814a2_336.png',
    'MAX_FILE_SIZE':200000000000,
    'Submit2':'確定並送出'
}

r = sess.post('https://ceiba.ntu.edu.tw/modules/hw/hw_show.php?current_lang=chinese',
        data = upload_data,
        files = {'file': open(path,'rb')})
