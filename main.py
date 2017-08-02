import urllib, urllib.request
import itchat
import time



currency=['DINIW','aud','eur','gbp','cad','jpy','chf','nzd','sgd','dkk','hkd','nok','sek','try','zar','cnh','czk','huf','pln','rub','thb','mxn']
weight={'uer':0.576, 'jpy':0.136, 'gbp':0.119,'cad':0.091,'chf':0.036, 'sek':0.042}

def request_data(): 
    urlstr=''
    for it in currency[1:]:
        urlstr+='fx_susd'+it+','
    urlstr=urlstr[:-1]    
    url='http://hq.sinajs.cn/rn=dd2i1&list=DINIW,'+urlstr
    # print(url)
    # round=lambda x,y:float(('%.'+str(y)+'f') % x)
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
            result[it]=100*float(resp[it][-5])/float(resp[it][4])
        tem=currency[0]
        xx=lambda x,y:100*(x-y)/y
        dxy=xx(float(resp[tem][1]), float(resp[tem][2]))
        result[tem]=round(dxy,5)

        for it in currency[1:]:
            ressss=-result[it]+result[tem]*(1.0 if not weight.get(it) else (1.0-weight[it]))
            result[it]=round(ressss,4)

        sortresult=sorted(result.items(),key=lambda t:t[1],reverse=True)

        sortresult=sortresult[0:8]+[(currency[0], result[currency[0]])]+sortresult[-8:]

        print('data processing complete!')
        return sortresult

        # print(resp)  #-5  / 4 

    else:
        print('\nerror！！\n')

    pass

if __name__ == '__main__':
    data=[]
    itchat.auto_login(hotReload=True, statusStorageDir='itchat.pkl',enableCmdQR=2,picDir='./QRcode')
    account = ['请思君','开心果','猴哥','EAMiracle01','EAMiracle02']    
    # print(wchatUser)
    while True:
        data.append(request_data())
        msg=str(data[-1])[1:-1] 
        msg=msg.replace('), ', ')\n')
        print(msg)
        for ic in account:
            itchat.send(msg,itchat.search_friends(ic)[0]['UserName'])
        time.sleep(900)
        pass
    