# 보건복지부_코로나19해외발생_현황
import requests
import xmltodict
import json
import datetime

def getCovidKR(end_day, start_day): 
    url='http://openapi.data.go.kr/openapi/service/rest/Covid19/getCovid19NatInfStateJson' 
    api_key = '41cYgMWSvkL+jGmAZC/qLP0wimM1uABR3s2ehXnFqosoJBesTnXIFqj5UAlmPIRzClMLpQT8G+/UxwrF8v9HWw=='
    #ServiceKey는 url decode 한 값임. 
    params = { 
        'serviceKey' : api_key, 
        'pageNo' : '1',
        'numOfRows' : 10,
        'startCreateDt' : start_day, 
        'endCreateDt' : end_day, 
    } 
    res = requests.get(url, params=params) 
    # print(res.url)
    if (res.status_code == 200): 
        # Ordered dictionary type 
        result = xmltodict.parse(res.text) 
        #dictionlay type 
        data = json.loads(json.dumps(result))         
        # leng = int(len(data['response']['body']['items']['item']) / 2)
        leng = len(data['response']['body']['items']['item'])
        leng = int(data['response']['body']['totalCount'])
        print('나라\t확진자\t사망자\t사망률')
        for i in range(leng):
            nationNm = data['response']['body']['items']['item'][i]['nationNm']
            nationNmEn = data['response']['body']['items']['item'][i]['nationNmEn']
            natDefCnt = data['response']['body']['items']['item'][i]['natDefCnt']
            natDeathCnt = data['response']['body']['items']['item'][i]['natDeathCnt']
            natDeathRate = data['response']['body']['items']['item'][i]['natDeathRate']

            print('%d-%s(%s)\t%s\t%s\t%s'%(i, nationNm, nationNmEn, natDefCnt, natDeathCnt, natDeathRate))

        
    else: 
        print('res.status_code is NOT ok') 
        
if __name__ == "__main__": 
    today = datetime.datetime.now() 
    yesterday = today - datetime.timedelta(1) 
    day1 = today.strftime("%Y%m%d") 
    day2 = yesterday.strftime("%Y%m%d") 
    getCovidKR(day1, day1)
    