# 보건복지부_코로나19 연령별·성별감염_현황
import requests
import xmltodict
import json
import datetime

def getCovidKR(end_day, start_day): 
    url='http://openapi.data.go.kr/openapi/service/rest/Covid19/getCovid19GenAgeCaseInfJson' 
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
        print('구분\t확진자(확진률)\t사망자(사망률)\t치명률')
        for i in range(leng):
            gubun = data['response']['body']['items']['item'][i]['gubun']
            confCase = data['response']['body']['items']['item'][i]['confCase']
            confCaseRate = data['response']['body']['items']['item'][i]['confCaseRate']
            death = data['response']['body']['items']['item'][i]['death']
            deathRate = data['response']['body']['items']['item'][i]['deathRate']
            criticalRate = data['response']['body']['items']['item'][i]['criticalRate']

            print('%s\t%s(%s)\t%s(%s)\t%s'%(gubun, confCase, confCaseRate, death, deathRate, criticalRate))

        
    else: 
        print('res.status_code is NOT ok') 
        
if __name__ == "__main__": 
    today = datetime.datetime.now() 
    yesterday = today - datetime.timedelta(1) 
    day1 = today.strftime("%Y%m%d") 
    day2 = yesterday.strftime("%Y%m%d") 
    getCovidKR(day1, day1)
    