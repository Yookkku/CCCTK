from argparse import Action
from datetime import date
from re import T
import requests
import base64
import jwt
import time
from timeOperation import Date


SECRET_KEY = '.mkidhf.jsi,]]sje. f'

def jiami(token):
    a = base64.b64encode(token.encode('utf-8'))
    return a.decode('utf-8')


def jiemi(token):
    b=base64.b64decode(token)
    return b.decode('utf-8')


def mem_file(filename,words):
    with open(filename+'.txt', 'w') as f:
        f.write(jiami(words))
        f.close()
    

def read_file(filename):
    with open(filename+'.txt','rt') as fo:
       t=fo.readline()
       fo.close()
    return jiemi(t)    


def decode_token(t):
    return jwt.decode(t, SECRET_KEY, algorithms=['HS256'])            


def register(email, username, password):
    response = requests.post("http://81.70.180.118:12346/api/v1/user/",
                             data={'email': email, 'username': username, 'password': password, 'action': 'register'})
    data = response.json()
    # print(data)
    if data['code'] == 200:
        mem_file('token',data['token'])
        return True
    else:
        return data['message']


def login(username, password,ifautologin):
    if ifautologin=='1':
        mem_file('username',username)
        mem_file('password',password)
        mem_file('ifautologin','1')
    else:
        mem_file('ifautologin','0')    
    
    response = requests.post("http://81.70.180.118:12346/api/v1/user/",
                             data={'username': username, 'password': password, 'action': 'login'})
    data = response.json()
    # print(data)
    # print(response.text)
    if data['code'] == 200:
        mem_file('token',data['token'])
        return True
    else:
        return False

def addThing(username, thingname, class_, predate, ddl):
    d = Date()
    predate = d.getTimestamp(*predate)
    ddl = d.getTimestamp(*ddl)
    response = requests.post("http://81.70.180.118:12346/api/v1/thing/",
                             data={'username': username, 'thingname': thingname, 'class_': class_,
                                   'predate': predate, 'ddl': ddl, 'token': read_file('token')})
    data = response.json()
    if data['code'] == 200:
        mem_file('token',data['token'])
        return True
    else:
        return data['message']


def getThing(username):
    response = requests.get("http://81.70.180.118:12346/api/v1/thing/",
                            params={'username': username, 'token': read_file('token')})
    data = response.json()
    if data['code'] == 200:
        mem_file('token',data['token'])
        info = data['info']
        for i in info:
            d = Date()
            i['predate']=d.getDate(i['predate'])
            i['ddl']=d.getDate(i['ddl'])
        return info
        
    else:
        return data['message']                        






def deleteThing(username,  thingid):
    response = requests.delete("http://81.70.180.118:12346/api/v1/thing/",
                               data={'username': username, 'token': read_file('token'), 'thingid': thingid})
    data = response.json()
    if data['code'] == 200:
        mem_file('token',data['token'])
        return True
    else:
        return data['message']


def changeThing(username, thingid , changeName, changeVal):
    if changeName == 'predate':
        d = Date()
        changeVal= d.getTimestamp(*changeVal)
    if changeName == 'ddl':
        d = Date()
        changeVal = d.getTimestamp(*changeVal)
    # changeName: username, thingid, thingname, class_, predate, ddl
    response = requests.put("http://81.70.180.118:12346/api/v1/thing/",
                             data={'username':username,'thingid':thingid,changeName: changeVal, 'token': read_file('token')})
    # print(response.text)
    data = response.json()
    if data['code'] == 200:
        mem_file('token',data['token'])
        return True
    else:
        return data['message']
def autologin() -> bool:
    if read_file('ifautologin')=='1':
        username=read_file('username')
        password=read_file('password')
        token=read_file('token')
        t=decode_token(token)
        timestramp=int(time.time())
        if t['exp']>=timestramp:
            return login(username,password,'1')
        else:
            return False 
def check_email(email):          
    response=requests.post('http://81.70.180.118:12346/captcha/',data={'email':email})
    data=response.json()
    if data['status']==200:
        return data['captcha']
    else:
        return data['message']   
        
                                   
if __name__ == '__main__':
    login('zr', '123456', '0')
    # print(login('hhc','111111','1'))
    print(autologin())
    # print(addThing('hhc','辣','666',(2022,3,27),(2022,3,27)))
    # print(getThing('hhc'))
    # changeThing('cgy_test','44','ddl',(2022,3,27))
    # for i in range(13,20):
    #     print(login('cgy_test','111111'))
    #     print(deleteThing('cgy_test',i))

    # print(getThing('cgy_test'))
    # register('hhc@qq.com','hhc','111111')  
    # print(jiemi('ZXlKMGVYQWlPaUpLVjFRaUxDSmhiR2NpT2lKSVV6STFOaUo5LmV5SmxlSEFpT2pFMk5UQXdNRFF5TURBc0luVnpaWEp1WVcxbElqb2lhR2hqSWl3aWRHbHRaWE4wWVcxd0lqb3hOalE1TXprNU5EQXdmUS5Bb1RNUnBlbjd0QTBPei1lekVXTzFyQU5lbURrLWlWUXBCdktYR0F5T3FB'))