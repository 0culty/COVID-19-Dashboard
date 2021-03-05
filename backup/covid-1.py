# 보건복지부_코로나19 감염_현황
import requests
import xmltodict
import json
import datetime
import pandas as pd

def getCovidKR(end_day, start_day): 
    url='http://openapi.data.go.kr/openapi/service/rest/Covid19/getCovid19InfStateJson' 
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
    if (res.status_code == 200): 
        # Ordered dictionary type 
        result = xmltodict.parse(res.text) 
        
        #dictionlay type 
        data = json.loads(json.dumps(result)) 
        df = pd.DataFrame.from_dict([data])
        print(df)
        

        # print('%s일 %s시 기준' %(data['response']['body']['items']['item']["stateDt"], data['response']['body']['items']['item']["stateTime"]))
        # print('확진자:', data['response']['body']['items']['item']['decideCnt']) 
        # print('사망자:', data['response']['body']['items']['item']['deathCnt']) 
        # print('격리해제:', data['response']['body']['items']['item']['clearCnt']) 
        # print('총검사자:', data['response']['body']['items']['item']['accExamCnt']) 
        # print('검사중:', data['response']['body']['items']['item']['examCnt']) 
        # print('결과음성:', data['response']['body']['items']['item']['resutlNegCnt']) 

    else: 
        print('res.status_code is NOT ok') 
    
    return df
        
if __name__ == "__main__": 
    today = datetime.datetime.now() 
    yesterday = today - datetime.timedelta(1) 
    day1 = today.strftime("%Y%m%d") 
    day2 = yesterday.strftime("%Y%m%d") 
    getCovidKR(day1, day1)
    