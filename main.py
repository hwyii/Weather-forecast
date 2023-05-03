from utils import *
import tkinter as tk
import tkinter.filedialog as tkfd
from PIL import Image, ImageTk

def main():
    url1 = 'http://www.weather.com.cn/weather/101220101.shtml'
    url2 = 'http://www.weather.com.cn/weather15d/101220101.shtml'

    html1 = getHTML(url1)
    data1, data1_7 = get(html1)

    html2 = getHTML(url2)
    data8_14 = get2(html2)
    data14 = data1_7 + data8_14

    write_to_csv('weather14.csv',data14,14)
    write_to_csv('weather1.csv',data1,1)

    # In order to recognize Chinese
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False

    data1 = pd.read_csv('weather1.csv',encoding='gb2312')
    data14 = pd.read_csv('weather14.csv',encoding='gb2312')

    import tkinter as tk

    class APP():
        def __init__(self, root):
    
            bt1 = tk.Button(root, text="Temerature(24h)",command=self.Day_temp)
            bt2 = tk.Button(root, text="Humidity(24h)",command=self.Day_hum)
            bt3 = tk.Button(root, text="Wind scale(24h)",command=self.wind24)
            bt4 = tk.Button(root, text="Wind scale(14 days)",command=self.Wind_radar)
            bt5 = tk.Button(root, text="Weather ratio(14 days)",command=self.Wea_pie)
            bt6 = tk.Button(root, text="Temperature(14 days)",command=self.Temper)
            # Location settings
            bt1.grid(row=1,column=0)
            bt2.grid(row=1,column=1)
            bt3.grid(row=1,column=2)
            bt4.grid(row=2,column=0)
            bt5.grid(row=2,column=1)
            bt6.grid(row=2,column=2)

        # Daily data
        def Day_temp(self):
            tem_curve(data1)

        def Day_hum(self):
            hum_curve(data1)
        
        def wind24(self):
            wind_radar_24h(data1)

        # 14 days forecast
        def Wind_radar(self):
            wind_radar(data14)

        def Wea_pie(self):
            weather_pie(data14)

        def Temper(self):
            temper14(data14)

    root = tk.Tk()
    root.title('Weather in Hefei')
    root.geometry('500x200')
    app = APP(root)
    root.mainloop()
    
if __name__ == '__main__':
    main()