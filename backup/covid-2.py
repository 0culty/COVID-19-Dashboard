# 보건복지부_코로나19 시·도발생_현황
import requests
import xmltodict
import json
import datetime

def getCovidKR(end_day, start_day): 
    url='http://openapi.data.go.kr/openapi/service/rest/Covid19/getCovid19SidoInfStateJson' 
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
        # leng = int(len(data['response']['body']['items']['item']) / 2 -1)
        leng = int(data['response']['body']['totalCount'])
        print('지역\t확진자\t사망자\t격리해제\t발생률*')
        for i in range(leng):
            City = data['response']['body']['items']['item'][i]['gubun']
            Confirmed = data['response']['body']['items']['item'][i]['defCnt']
            # Confirmed_Plus = data['response']['body']['items']['item'][i]['incDec']
            Death = data['response']['body']['items']['item'][i]['deathCnt']
            # Death_Plus = str(int(data['response']['body']['items']['item'][i]['deathCnt']) - int(data['response']['body']['items']['item'][i+leng]['deathCnt']))
            Recovered = data['response']['body']['items']['item'][i]['isolClearCnt']
            Incidence = data['response']['body']['items']['item'][i]['qurRate']

            # print('%s\t%s(%s)\t%s(%s)\t%s\t%s'%(City, Confirmed, Confirmed_Plus, Death, Death_Plus, Recovered, Incidence))
            print('%s\t%s\t%s\t%s\t\t%s'%(City, Confirmed, Death, Recovered, Incidence))

        
    else: 
        print('res.status_code is NOT ok') 
        
if __name__ == "__main__": 
    today = datetime.datetime.now() 
    yesterday = today - datetime.timedelta(1) 
    day1 = today.strftime("%Y%m%d") 
    day2 = yesterday.strftime("%Y%m%d") 
    getCovidKR(day1, day1)
    