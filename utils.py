import requests
from bs4 import BeautifulSoup
import csv
import json
import matplotlib.pyplot as plt
import numpy as np
import math
import pandas as pd

def getHTML(url):
    try:
        r = requests.get(url, timeout = 30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        print("Succeed.")
        return r.text
    except:
        print("Failure.")
        return " "

# Get the data for 7 days
def get(html):
    final = []
    bs = BeautifulSoup(html, "html.parser")
    body = bs.body
    data = body.find('div',{'id':'7d'}) # Find label div and id = 7d

    data2 = body.find_all('div',{'class':'left-div'})
    text = data2[2].find('script').string
    text = text[text.index('=')+1 : -2]
    jd = json.loads(text)
    dayone = jd['od']['od2']
    final_day = [] # Store the data of the day
    count = 0
    for i in dayone:
        temp = []
        if count <= 23:
            temp.append(i['od21']) # Time
            temp.append(i['od22']) # Temperature
            temp.append(i['od24']) # Wind direction
            temp.append(i['od25']) # Wind strength
            temp.append(i['od26']) # Precipitation
            temp.append(i['od27']) # Relative humidity
            temp.append(i['od28']) # Air quality

            final_day.append(temp)
        
        count += 1

    ul = data.find('ul') # Find label 'ul'
    li = ul.find_all('li') # Find label "li"
    i = 0
    for day in li:
        if i < 7 and i > 0:
            temp = []
            date = day.find('h1').string
            date = date[0:date.index('日')]
            temp.append(date)

            inf = day.find_all('p')
            temp.append(inf[0].string)

            tem_low = inf[1].find('i').string

        
            tem_high = inf[1].find('span').string
            temp.append(tem_low[:-1])
            if tem_high[-1] == '℃':
                temp.append(tem_high[:-1])
            else:
                temp.append(tem_high)

            wind = inf[2].find_all('span') # Find the wind direction
            for j in wind:
                temp.append(j['title'])

            wind_scale = inf[2].find('i').string
            index1 = wind_scale.index('级')
            temp.append(int(wind_scale[index1-1:index1]))
            final.append(temp)
        i += 1
    return final_day, final

# Get the data for 14 days
def get2(html):
    final = []
    bs = BeautifulSoup(html, "html.parser")
    body = bs.body
    data = body.find('div',{'id':'15d'}) # Find label div and id = 7d
    ul = data.find('ul')
    li = ul.find_all('li')
    i = 0
    for day in li:
        if i < 8:
            temp = []
            date = day.find('span',{'class':'time'}).string
            date = date[date.index('（')+1:-2]
            temp.append(date)
            weather = day.find('span',{'class':'wea'}).string
            temp.append(weather)
            tem = day.find('span',{'class':'tem'}).text
            temp.append(tem[tem.index('/')+1:-1])
            temp.append(tem[:tem.index('/')-1])
            wind = day.find('span',{'class':'wind'}).string
            if '转' in wind:
                temp.append(wind[:wind.index('转')])
                temp.append(wind[wind.index('转')+1:])
            else:
                temp.append(wind)
                temp.append(wind)
            wind_scale = day.find('span',{'class':'wind1'}).string
            index1 = wind_scale.index('级')
            temp.append(int(wind_scale[index1-1:index1]))

            final.append(temp)
    return final

def write_to_csv(file_name,data,day=14):
    with open(file_name,'w',errors='ignore',newline='') as f:
        if day == 14:
            header = ['日期','天气','最低气温','最高气温','风向1','风向2','风级']
        else:
            header = ['小时','温度','风力方向','风级','降水量','相对湿度','空气质量']
        f_csv = csv.writer(f)
        f_csv.writerow(header)
        f_csv.writerows(data)

# Data analysis part
    
# Temperature curve in a day
def tem_curve(data):
    hour = list(data['小时'])
    tem = list(data['温度'])
    for i in range(0,24):
        if math.isnan(tem[i]) == True:
            tem[i] = tem[i-1]
    tem_ave = sum(tem)/24
    tem_max = max(tem)
    tem_max_hour = hour[tem.index(tem_max)]
    tem_min = min(tem)
    tem_min_hour = hour[tem.index(tem_min)]
    x = []
    y = []
    for i in range(0,24):
        x.append(i)
        y.append(tem[hour.index(i)])
    plt.figure(1)
    plt.plot(x,y,color = 'red', label = "Temperature")
    plt.scatter(x,y,color = 'red')
    plt.plot([0, 24], [tem_ave, tem_ave], c = "blue", linestyle = '--', label = 'Average Temperature')
    plt.text(tem_max_hour+0.15, tem_max+0.15, str(tem_max), ha='center', va='bottom', fontsize=10.5)
    plt.text(tem_min_hour+0.15, tem_min+0.15, str(tem_min), ha='center', va='bottom', fontsize=10.5)
    plt.xticks(x)
    plt.legend()
    plt.title('Temperature change in 24h')
    plt.xlabel('Time')
    plt.ylabel('Temperature')
    plt.show()

# Relative humidity curve in a day
def hum_curve(data):
    hour = list(data['小时'])
    hum = list(data['相对湿度'])
    for i in range(0,24):
        if math.isnan(hum[i]) == True:
            hum[i] = hum[i-1]
    hum_ave = sum(hum)/24
    hum_max = max(hum)
    hum_max_hour = hour[hum.index(hum_max)]
    hum_min = min(hum)
    hum_min_hour = hour[hum.index(hum_min)]
    x = []
    y = []
    for i in range(0,24):
        x.append(i)
        y.append(hum[hour.index(i)])
    plt.figure(1)
    plt.plot(x,y,color = 'blue', label = "Relative humidity")
    plt.scatter(x,y,color = 'blue')
    plt.plot([0, 24], [hum_ave, hum_ave], c = "blue", linestyle = '--', label = 'Average Relative humidity')
    plt.text(hum_max_hour+0.15, hum_max+0.15, str(hum_max), ha='center', va='bottom', fontsize=10.5)
    plt.text(hum_min_hour+0.15, hum_min+0.15, str(hum_min), ha='center', va='bottom', fontsize=10.5)
    plt.xticks(x)
    plt.legend()
    plt.title('Relative humidity change in 24h')
    plt.xlabel('Time')
    plt.ylabel('Percentage')
    plt.show()

# Temperature for 14 days
def temper14(data):
    date = list(data['日期'])
    tem_low = list(data['最低气温'])
    tem_high = list(data['最高气温'])
    for i in range(0,14):
        if math.isnan(tem_low[i]) == True:
            tem_low[i] = tem_low[i-1]
        if math.isnan(tem_high[i]) == True:
            tem_high[i] = tem_high[i-1]

    tem_high_ave = sum(tem_high)/14
    tem_low_ave = sum(tem_low)/14

    tem_max = max(tem_high)
    tem_max_date = tem_high.index(tem_max)
    tem_min = min(tem_low)
    tem_min_date = tem_low.index(tem_min)

    x = range(1,15)
    plt.figure(1)
    plt.plot(x, tem_high, color = 'red', label = 'High')
    plt.scatter(x, tem_high, color = 'red')
    plt.plot(x, tem_low, color = 'blue', label = 'Low')
    plt.scatter(x, tem_low, color = 'blue')

    plt.plot([1, 15], [tem_high_ave, tem_high_ave], c='black', linestyle='--')
    plt.plot([1, 15], [tem_low_ave, tem_low_ave], c='black', linestyle='--')
    plt.legend()
    plt.text(tem_max_date+0.15, tem_max+0.15, str(tem_max), ha='center',va='bottom',fontsize=10.5)
    plt.text(tem_min_date+0.15, tem_min+0.15, str(tem_min), ha='center',va='bottom',fontsize=10.5)
    plt.xticks(x)
    plt.title('Temperature change in 14 days')
    plt.xlabel('Days')
    plt.ylabel('Temperature')
    plt.show()


# Wind
def change_wind(wind):
    for i in range(0,14):
        if wind[i] == "北风":
            wind[i] = 90
        elif wind[i] == "南风":
            wind[i] = 270
        elif wind[i] == "西风":
            wind[i] = 180
        elif wind[i] == "东风":
            wind[i] = 360
        elif wind[i] == "东北风":
            wind[i] = 45
        elif wind[i] == '西北风':
            wind[i] = 135
        elif wind[i] == "东北风":
            wind[i] = 315
    return wind

def wind_radar(data):
    wind1 = list(data['风向1'])
    wind2 = list(data['风向2'])
    wind_speed = list(data['风级'])
    wind1 = change_wind(wind1)
    wind2 = change_wind(wind2)

    degs = np.arange(45,361,45)
    temp = []
    for deg in degs:
        speed = []
        # Get the average wind speed within the specified range
        for i in range(0,14):
            if wind1[i] == deg:
                speed.append(wind_speed[i])
            if wind2[i] == deg:
                speed.append(wind_speed[i])
        if len(speed) == 0:
            temp.append(0)
        else:
            temp.append(sum(speed)/len(speed))
    N = 8
    theta = np.arange(0.+np.pi/8,2*np.pi+np.pi/8,2*np.pi/8)
    radii = np.array(temp)
    plt.axes(polar=True)
    # The larger is x, the color is more close to blue
    colors = [(1-x/max(temp), 1-x/max(temp),0.6) for x in radii]
    plt.bar(theta,radii,width=(2*np.pi/N),bottom=0.0,color=colors)
    plt.title('Wind scale for the next 14 days')
    plt.show()

def wind_radar_24h(data):
    wind = list(data['风力方向'])
    wind_speed = list(data['风级'])

    for i in range(0,24):
        if wind[i] == "北风":
            wind[i] = 90
        elif wind[i] == "南风":
            wind[i] = 270
        elif wind[i] == "西风":
            wind[i] = 180
        elif wind[i] == "东风":
            wind[i] = 360
        elif wind[i] == "东北风":
            wind[i] = 45
        elif wind[i] == '西北风':
            wind[i] = 135
        elif wind[i] == "东北风":
            wind[i] = 315
    degs = np.arange(45,361,45)
    temp = []
    for deg in degs:
        speed = []
        # Get the average wind speed within the specified range
        for i in range(0,14):
            if wind[i] == deg:
                speed.append(wind_speed[i])
        if len(speed) == 0:
            temp.append(0)
        else:
            temp.append(sum(speed)/len(speed))
    N = 8
    theta = np.arange(0.+np.pi/8,2*np.pi+np.pi/8,2*np.pi/8)
    radii = np.array(temp)
    plt.axes(polar=True)
    # The larger is x, the color is more close to blue
    colors = [(1-x/max(temp), 1-x/max(temp),0.6) for x in radii]
    plt.bar(theta,radii,width=(2*np.pi/N),bottom=0.0,color=colors)
    plt.title('Wind scale in 24h')
    plt.show()

# Weather pie plot
def weather_pie(data):
    weather = list(data['天气'])
    dic_wea = {}
    for i in range(0,14):
        if weather[i] in dic_wea.keys():
            dic_wea[weather[i]] += 1
        else: 
            dic_wea[weather[i]] = 1
    # print(dic_wea)
    explode = [0.01] * len(dic_wea.keys())
    color = ['red','orange','yellow','green','lightskyblue','blue','purple']
    plt.pie(dic_wea.values(),explode=explode,labels=dic_wea.keys(),autopct='%1.1f%%',colors=color)
    plt.title('Weather ratio for the next 14 days')
    plt.show()

