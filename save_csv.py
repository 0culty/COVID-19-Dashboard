import requests
import xmltodict
import json
import datetime
import pandas as pd

# 보건복지부_코로나19 감염_현황
def get_Covid19_KR(end_day, start_day): 
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
        leng = int(data['response']['body']['totalCount'])
        values = []
        for i in range(leng):
            day = data['response']['body']['items']['item'][i]["stateDt"]
            times = data['response']['body']['items']['item'][i]["stateTime"]
            t = datetime.datetime(int(day[0:4]), int(day[4:6]), int(day[6:]), int(times[0:2]),0,0,0)
            time = t.strftime("%Y%m%dT%H:%M:%SZ")
            Confirmed = int(data['response']['body']['items']['item'][i]['decideCnt'])
            Deaths = int(data['response']['body']['items']['item'][i]['deathCnt']) 
            Recovered = int(data['response']['body']['items']['item'][i]['clearCnt'])
            Testing = int(data['response']['body']['items']['item'][i]['examCnt'])             
            try:
                Tested = int(data['response']['body']['items']['item'][i]['accExamCnt'])
            except KeyError as e:
                Tested = 0
            try:
                Negative = int(data['response']['body']['items']['item'][i]['resutlNegCnt'])
            except KeyError as e:
                Negative = 0
            
            if len(values) > 1:
                if day != values[-1][0][0:8]:
                    values.append((time, Confirmed, Deaths, Recovered, Tested, Testing, Negative))
            else:
                values.append((time, Confirmed, Deaths, Recovered, Tested, Testing, Negative))



        values = list(reversed(values))
        columns = ['time', 'Confirmed', 'Deaths', 'Recovered', 'Tested', 'Testing', 'Negative']        
        df = pd.DataFrame(values, columns=columns)

    else: 
        print('res.status_code is NOT ok') 
    
    return df

# 보건복지부_코로나19 시·도발생_현황
def get_Covid19_KR_Sido(end_day, start_day): 
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
    if (res.status_code == 200): 
        # Ordered dictionary type 
        result = xmltodict.parse(res.text) 
        #dictionlay type 
        data = json.loads(json.dumps(result))         
        leng = int(data['response']['body']['totalCount'])
        values = []
        # print('지역\t확진자\t사망자\t격리해제\t발생률*')
        for i in range(leng):
            day = data['response']['body']['items']['item'][i]["stdDay"]
            times = day.split()
            t = datetime.datetime(int(times[0][0:-1]), int(times[1][0:-1]), int(times[2][0:-1]), int(times[3][0:-1]),0,0,0)
            time = t.strftime("%Y%m%dT%H:%M:%SZ")
            City = data['response']['body']['items']['item'][i]['gubun']
            Confirmed = data['response']['body']['items']['item'][i]['defCnt']
            Death = data['response']['body']['items']['item'][i]['deathCnt']
            Incidence = data['response']['body']['items']['item'][i]['qurRate']
            try:
                Recovered = data['response']['body']['items']['item'][i]['isolClearCnt']
            except KeyError as e:
                Recovered = 0
                
            values.append((time, City, Confirmed, Death, Recovered, Incidence))

        values = list(reversed(values))
        columns = ['time', 'City', 'Confirmed', 'Death', 'Recovered', 'Incidence']
        df = pd.DataFrame(values, columns=columns)
        
    else: 
        print('res.status_code is NOT ok') 

    return df

# 보건복지부_코로나19해외발생_현황
def get_Covid19_GB(end_day, start_day): 
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
    if (res.status_code == 200): 
        # Ordered dictionary type 
        result = xmltodict.parse(res.text) 
        #dictionlay type 
        data = json.loads(json.dumps(result))         
        leng = int(data['response']['body']['totalCount'])
        values = []
        print('나라\t확진자\t사망자\t사망률')
        for i in range(leng):
            day = data['response']['body']['items']['item'][i]["stdDay"]
            times = day.split()
            t = datetime.datetime(int(times[0][0:-1]), int(times[1][0:-1]), int(times[2][0:-1]), int(times[3][0:-1]),0,0,0)
            time = t.strftime("%Y%m%dT%H:%M:%SZ")
            nationNm = data['response']['body']['items']['item'][i]['nationNm']
            natDefCnt = data['response']['body']['items']['item'][i]['natDefCnt']
            natDeathCnt = data['response']['body']['items']['item'][i]['natDeathCnt']

            if data['response']['body']['items']['item'][i]['natDeathRate'] == 'NaN':
                natDeathRate = 0.0
            else:
                natDeathRate = data['response']['body']['items']['item'][i]['natDeathRate']
            
            if data['response']['body']['items']['item'][i]['nationNmEn'] == None:
                nationNmEn = 'missing'
            else:
                nationNmEn = data['response']['body']['items']['item'][i]['nationNmEn']
            
            
            values.append((time, nationNm, nationNmEn, natDefCnt, natDeathCnt, natDeathRate))

        values = list(reversed(values))
        values = values[1:]
        columns = ['time', 'nationNm', 'nationNmEn', 'natDefCnt', 'natDeathCnt', 'natDeathRate']
        df = pd.DataFrame(values, columns=columns)
        
    else: 
        print('res.status_code is NOT ok') 

    return df

# 보건복지부_코로나19 연령별·성별감염_현황
def get_Covid19_KR_GenAge(end_day, start_day): 
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
    if (res.status_code == 200): 
        # Ordered dictionary type 
        result = xmltodict.parse(res.text) 
        #dictionlay type 
        data = json.loads(json.dumps(result))         
        leng = int(data['response']['body']['totalCount'])
        values = []
        for i in range(leng):
            t = data['response']['body']['items']['item'][i]['createDt'].split()
            day = t[0].split('-')
            times =  t[1].split(':')
            t = datetime.datetime(int(day[0]), int(day[1]), int(day[2]), int(times[0]),0,0,0)
            time = t.strftime("%Y%m%dT%H:%M:%SZ")
            gubun = data['response']['body']['items']['item'][i]['gubun']               # 구분
            confCase = data['response']['body']['items']['item'][i]['confCase']         # 확진자
            confCaseRate = data['response']['body']['items']['item'][i]['confCaseRate'] # 확진률
            death = data['response']['body']['items']['item'][i]['death']               # 사망자
            deathRate = data['response']['body']['items']['item'][i]['deathRate']       # 사망률
            criticalRate = data['response']['body']['items']['item'][i]['criticalRate'] # 치명률

            values.append((time, gubun, confCase, confCaseRate, death, deathRate, criticalRate))

        values = list(reversed(values))
        columns = ['time', 'gubun', 'confCase', 'confCaseRate', 'death', 'deathRate', 'criticalRate']
        df = pd.DataFrame(values, columns=columns)
        
    else: 
        print('res.status_code is NOT ok') 

    return df


if __name__ == '__main__':
    today = datetime.datetime.now() 
    day1 = today.strftime("%Y%m%d") 

    # 보건복지부_코로나19 감염_현황
    day2 = '20200203'
    ret = get_Covid19_KR(day1, day2) # '20200203' 부터
    ret.to_csv('data/Covid19_KR.csv', sep=',', na_rep='NaN')

    # 보건복지부_코로나19 시·도발생_현황
    day2 = '20200304'
    ret = get_Covid19_KR_Sido(day1, day2) # '20200304' 부터
    ret.to_csv('data/Covid19_KR_Sido.csv', sep=',', na_rep='NaN')

    # 보건복지부_코로나19해외발생_현황
    day2 = '20200316'
    ret = get_Covid19_GB(day1, day2) # '20200316' 부터
    ret.to_csv('data/Covid19_GB.csv', sep=',', na_rep='NaN')

    # 보건복지부_코로나19 연령별·성별감염_현황
    day2 = '20200408'
    ret = get_Covid19_KR_GenAge(day1, day2) # '20200408' 부터
    ret.to_csv('data/Covid19_KR_GenAge.csv', sep=',', na_rep='NaN')






