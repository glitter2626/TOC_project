from transitions.extensions import GraphMachine
import re
import requests
import datetime
import time

DARK_SKY_URL = 'https://api.darksky.net/forecast/'
DARK_SKY_KEY = ''

GOOGLE_MAP_KEY = ''
GOOGLE_MAP_URL = 'https://maps.googleapis.com/maps/api/geocode/json'

location = 'tainan'
param_map = {'address' : location , 'key' : GOOGLE_MAP_KEY}
param_weather = {'lang' : 'zh-tw'}
header_weather = {'Accept-Encoding' : 'gzip,deflate'}
point = []
address = None

class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(
            model = self,
            **machine_configs
        )

    def is_going_to_usr(self, update):
        return True

    def on_enter_usr(self, update):
        update.message.reply_text("\nWeatherbot !\n\n    Type \"/help\" to learn more about it.\n\nThis bot use information from Dark Sky & Google Map")
    
    def is_going_to_help(self, update):
        text = update.message.text
        return text.lower() == '/help'
        
    def on_enter_help(self, update):
        update.message.reply_text("You can type where you are or <latitude , longitude> to get wheather information from Dark Sky.\n\n    ex: Tainan or <22.34,122.582>\n\nChoose one type:\n    1)location\n    2)<latitude,longitude>");
        self.init(update)
        
    def is_going_to_state1(self, update):
        text = update.message.text
        if text.lower() == '/help':
            return False
        m = re.search(r'.*<.*>.*', text)
        if m is None:
            return True
        else:
            return False

    def on_enter_state1(self, update):
        global point
        try:
            #update.message.reply_text("I'm entering state1")
            text = update.message.text
            param_map['address'] = text.strip()
            r = requests.get(GOOGLE_MAP_URL, params = param_map)

            if r.status_code == requests.codes.ok:
	            reply = r.json()
	            point.append(reply['results'][0]['geometry']['location']['lat'])
	            point.append(reply['results'][0]['geometry']['location']['lng'])
	            address = reply['results'][0]['formatted_address']
	            print(point)
	            print(address)
	            self.go(update)
            else:
                update.message.reply_text("Warning ! incorrect input")
                point = []
                self.init(update)   
        except:
            point = []
            update.message.reply_text("Warning ! incorrect input")
            self.init(update)
                        
    def state1_is_going_to_state2(self, update):
        return True	        
        
    def is_going_to_state2(self, update):
        global point
        text = update.message.text
        m = re.search(r'<(.+),(.+)>', text)
        print(m)
        if m is not None:
            try:
                float(m.group(1).strip())
                float(m.group(2))
                point.append(m.group(1).strip())
                point.append(m.group(2).strip())
                return True
            except ValueError:
                point = []                
                return False
        else:
            point = []
            return False
            
    def on_enter_state2(self, update):
        global point
        try:
            #update.message.reply_text("I'm entering state2")
            text = update.message.text
            r = requests.get(DARK_SKY_URL+DARK_SKY_KEY+'/'+str(point[0])+','+str(point[1]), params = param_weather, headers = header_weather)
            point = []
            if r.status_code == requests.codes.ok:
                reply = r.json()
                time = datetime.datetime.fromtimestamp(int(reply['currently']['time'])).strftime("%Y-%m-%d %H:%M:%S")
                update.message.reply_text('\n **********天氣結果*********\n\n'+'     時間 : '+time+'\n'+'     緯度: '+str(reply['latitude'])+'\n     經度: '+str(reply['longitude'])+'\n---------------------------------------------\n'+'\n-->天氣總結 : '+str(reply['currently']['summary'])+'\n\n   降雨機率 : '+str(100*reply['currently']['precipProbability'])+' %'+'\n   溫度 : '+str(round((reply['currently']['temperature']-32)*5/9,2))+' °C'+'\n   露點 : '+str(round((reply['currently']['dewPoint']-32)*5/9, 2))+' °C'+'\n   濕度 : '+str(100*reply['currently']['humidity'])+' %'+'\n   氣壓 : '+str(reply['currently']['pressure'])+' 帕'+'\n   風速 : '+str(1.61*reply['currently']['windSpeed'])+' km/h'+'\n   風向 : '+str(reply['currently']['windBearing'])+' 度 （從 N ,順時針）'+'\n   雲量 : '+str(100*reply['currently']['cloudCover'])+' %'+'\n   紫外線指數 : '+str(reply['currently']['uvIndex'])+'\n   臭氧濃度 : '+ str(reply['currently']['ozone'])+' psi')
                update.message.reply_text('\n **********周天氣預報結果***********\n\n'+'-->'+reply['daily']['summary']+'\n\n------------------------------------------------------------\n\n'+datetime.datetime.fromtimestamp(int(reply['daily']['data'][0]['time'])).strftime("%Y-%m-%d")+'    '+reply['daily']['data'][0]['summary']+'\n'+datetime.datetime.fromtimestamp(int(reply['daily']['data'][1]['time'])).strftime("%Y-%m-%d")+'    '+reply['daily']['data'][1]['summary']+'\n'+datetime.datetime.fromtimestamp(int(reply['daily']['data'][2]['time'])).strftime("%Y-%m-%d")+'    '+reply['daily']['data'][2]['summary']+'\n'+datetime.datetime.fromtimestamp(int(reply['daily']['data'][3]['time'])).strftime("%Y-%m-%d")+'    '+reply['daily']['data'][3]['summary']+'\n'+datetime.datetime.fromtimestamp(int(reply['daily']['data'][4]['time'])).strftime("%Y-%m-%d")+'    '+reply['daily']['data'][4]['summary']+'\n'+datetime.datetime.fromtimestamp(int(reply['daily']['data'][5]['time'])).strftime("%Y-%m-%d")+'    '+reply['daily']['data'][5]['summary']+'\n'+datetime.datetime.fromtimestamp(int(reply['daily']['data'][6]['time'])).strftime("%Y-%m-%d")+'    '+reply['daily']['data'][6]['summary']+'\n'+datetime.datetime.fromtimestamp(int(reply['daily']['data'][7]['time'])).strftime("%Y-%m-%d")+'    '+reply['daily']['data'][7]['summary'])
                self.init(update)
            else:
                update.message.reply_text("Warning1 ! incorrect input")
                point = []
                self.init(update)
               
        except:
            update.message.reply_text("Warning2 ! incorrect input")
            point = []
            self.init(update)
           
