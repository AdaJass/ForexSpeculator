import urllib, urllib.request
import itchat
import time



currency=['DINIW','aud','eur','gbp','cad','jpy','chf','nzd','sgd','dkk','hkd','nok','sek','try','zar','cnh','czk','huf','pln','rub','thb','mxn']

def request_data(): 
    urlstr=''
    for it in currency[1:]:
        urlstr+='fx_susd'+it+','
    urlstr=urlstr[:-1]    
    url='http://hq.sinajs.cn/rn=dd2i1&list=DINIW,'+urlstr
    # print(url)
    request=urllib.request.Request(url)  
    result=urllib.request.urlopen(request, timeout=25)
    if result.code == 200 or 204:
        jstr=str(result.read(),encoding='gbk')
        slist=jstr.split(';\n') 
        resp={}
        for it in currency[1:]:
            for hq in slist:
                if hq.find('susd'+it) != -1:
                    resp[it]=hq.split(',')[1:-2]                
        for hq in slist:
            if hq.find(currency[0]) !=-1:
                resp[currency[0]]=hq.split(',')[1:-1]   

        result={}
        for it in currency[1:]:
            result[it]=round(100*float(resp[it][-5])/float(resp[it][4]),4)
        tem=currency[0]
        xx=lambda x,y:round(100*(x-y)/y,4)
        dxy=xx(float(resp[tem][1]), float(resp[tem][2]))
        result[tem]=dxy

        for it in currency[1:]:
            result[it]=-result[it]+result[currency[0]]

        sortresult=sorted(result.items(),key=lambda t:t[1],reverse=True)

        sortresult=sortresult[0:3]+sortresult[-3:]
        sortresult=[(currency[0], result[currency[0]])] + sortresult
        print('data processing complete!')
        print(sortresult)
        return sortresult

        # print(resp)  #-5  / 4 

    else:
        print('\nerror！！\n')

    pass

if __name__ == '__main__':
    data=[]
    itchat.auto_login()
    flist=itchat.get_friends()
    for f in flist:
        if f['NickName'] == '请思君':
            wchatUser=f['UserName']
    print(wchatUser)
    while True:
        data.append(request_data())
        msg=str(data[-1])[1:-1] 
        msg=msg.replace('), ', ')\n')
        itchat.send(msg,wchatUser)

        time.sleep(900)
        pass
    