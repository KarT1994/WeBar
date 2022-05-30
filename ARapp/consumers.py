from channels.generic.websocket import WebsocketConsumer
import json
import threading
import time
import requests
import pandas as pd
from geopy.distance import geodesic
from django.conf import settings

class TestConsumer(WebsocketConsumer):
    view_lat = '0.1'
    view_lng = '0.1'
    cnt = 0

    def connect(self):
        self.message = "OOKK"
        self.accept()
        self.start_publish()

    def disconnect(self, close_code):
        self.stop_publish()

    def start_publish(self):
        self.publishing = True
        self.t = threading.Thread(target=self.interval_publish)
        self.t.start()

    def stop_publish(self):
        self.publishing = False
        self.t.join()

    def interval_publish(self):
        while True:
            if self.publishing == False:
                break
            time.sleep(1)

    def receive(self, text_data=None):
        dis = "Loading..."
        if text_data != None:
            text_data_json = json.loads(text_data)
            #self.message = text_data_json['message']

            _location = text_data_json['message']
            if "," in _location:
                shop_num = 5
                _array_location = _location.split(",")
                lat = _array_location[0]
                lng = _array_location[1]
                HP_data = HotpepperAPI(lat_st=lat,lng_st=lng )
                shop_array = [""] * shop_num
                lat_array = ["0.0"] * shop_num
                lng_array = ["0.0"] * shop_num
                dis_array = [0] * shop_num
                appeal = [""] * shop_num
                shop_urls = [""] * shop_num

                shop_array[2] = "お店を検索中…"
                for i in range(0,shop_num):
                    try:
                        #self.name = HP_data['name'][0]
                        shop_array[i] = HP_data['name'][i]
                        lat_array[i] = HP_data["lat"][i]
                        lng_array[i] = HP_data["lng"][i]
                        currentPosition = (float(lat), float(lng))
                        shopPosition = (float(lat_array[i]), float(lng_array[i]))
                        dis = int(geodesic(currentPosition, shopPosition).m)
                        dis_array[i] = str(dis)
                        appeal[i] = HP_data["catch"][i]
                        shop_urls[i] = HP_data["urls"][i]
                    except:
                        pass

            else:
                self.name = 'Failed:location'

            self.send(text_data=json.dumps({
                'message0':shop_array[0],
                "shop_lat0":lat_array[0],
                "shop_lng0":lng_array[0],
                "shop_dis0":dis_array[0],
                "catch0":appeal[0],
                "urls0":shop_urls[0],
                'message1':shop_array[1],
                "shop_lat1":lat_array[1],
                "shop_lng1":lng_array[1],
                "shop_dis1":dis_array[1],
                "catch1":appeal[1],
                "urls1":shop_urls[1],
                'message2':shop_array[2],
                "shop_lat2":lat_array[2],
                "shop_lng2":lng_array[2],                
                "shop_dis2":dis_array[2],
                "catch2":appeal[2],
                "urls2":shop_urls[2],
                'message3':shop_array[3],
                "shop_lat3":lat_array[3],
                "shop_lng3":lng_array[3],
                "shop_dis3":dis_array[3],
                "catch3":appeal[3],
                "urls3":shop_urls[3],
                'message4':shop_array[4],
                "shop_lat4":lat_array[4],
                "shop_lng4":lng_array[4],
                "shop_dis4":dis_array[4],
                "catch4":appeal[4],
                "urls4":shop_urls[4],
            }))
        else:
            pass

def HotpepperAPI(lat_st, lng_st):
    api_key = settings.HOTPEPPER_API_KEY
    print(api_key)
    api = "http://webservice.recruit.co.jp/hotpepper/gourmet/v1/?" \
            "key={key}&lat={lat}&lng={lng}&range=1&count=10&order=4&format=json"

    url=api.format(key=api_key,lat=lat_st, lng=lng_st)
    response = requests.get(url)
    result_list = json.loads(response.text)['results']['shop']
    shop_datas=[]
    for shop_data in result_list:
        shop_datas.append([shop_data["name"],
                            shop_data["address"],
                            shop_data["urls"]['pc'], 
                            shop_data["budget"]['average'],
                            shop_data["photo"]['pc']["l"],
                            shop_data["logo_image"],
                            shop_data["lat"],
                            shop_data["lng"],
                            shop_data["catch"]
                            ])           
    columns = ['name','address', 'urls', 'budget', 'photo', "logo_image","lat","lng","catch"]
    HP_data =pd.DataFrame(shop_datas, columns=columns)
    return HP_data
