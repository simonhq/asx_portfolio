############################################################
#
# This class aims to get the ASX pricing information for the stock
#
# written to be run from AppDaemon for a HASS or HASSIO install
#
# created: 19/08/2020
# 
############################################################

############################################################
# 
# In the apps.yaml file you will need the following
# updated for your database path, stop ids and name of your flag
#
# asx_portfolio:
#   module: asx_portfolio
#   class: Get_ASX_portfolio_info
#   PORT_NAME: "low_risk_inv"
#   TICKER: "CBA:10,TLS:30,BHP:15"
#   TICK_FLAG" "input_boolean.asx_portfolio_check"
#
############################################################

# import the function libraries
import requests
import datetime
import json
import appdaemon.plugins.hass.hassapi as hass

class Get_ASX_portfolio_info(hass.Hass):

    # the name of the flag in HA (input_boolean.xxx) that will be watched/turned off
    
    PORT_NAME = ""
    TICKER = ""
    TICK_FLAG = ""

    URLs = "https://www.asx.com.au/asx/1/share/"
    s_price = "/prices?interval=daily&count=1"    

    tick_up_mdi = "mdi:arrow-top-right"
    tick_down_mdi = "mdi:arrow-bottom-left"
    tick_mdi = "mdi:progress-check"

    up_sensor = "sensor.asx_portfolio_data_last_updated"
    asx_portfolio = "sensor.asx_portfolio_"

    up_mdi = "mdi:timeline-clock-outline"
    payload = {}
    headers = {
        'User-Agent': 'Mozilla/5.0'
    }

    # run each step against the database
    def initialize(self):

        # get the values from the app.yaml that has the relevant personal settings
        self.PORT_NAME = self.args["PORT_NAME"]
        self.TICKER = self.args["TICKER"]
        self.TICK_FLAG = self.args["TICK_FLAG"]

        # create the original sensor
        self.load()

        # listen to HA for the flag to update the sensor
        self.listen_state(self.main, self.TICK_FLAG, new="on")

        # set to run each morning at 5.23pm
        runtime = datetime.time(17,23,0)
        self.run_daily(self.daily_load, runtime)

    # run the app
    def main(self, entity, attribute, old, new, kwargs):
        """ create the sensor and turn off the flag
            
        """
        # create the sensor with the information 
        self.load()
        
        # turn off the flag in HA to show completion
        self.turn_off(self.TICK_FLAG)

    # run the app
    def daily_load(self, kwargs):
        """ scheduled run
        """
        # create the sensor with the dam information 
        self.load()

    def load(self):
        """ parse the ASX JSON datasets
        """

        #create a sensor to keep track last time this was run
        tim = datetime.datetime.now()
        #tomorrow = tim - datetime.timedelta(days=-1)
        date_time = tim.strftime("%d/%m/%Y, %H:%M:%S")
        #date_date = tim.strftime("%d/%m/%Y")
        #tomorrow_date = tomorrow.strftime("%d/%m/%Y")
        self.set_state(self.up_sensor, state=date_time, replace=True, attributes= {"icon": self.up_mdi, "friendly_name": "ASX Portfolio Data last sourced", "Companies": self.TICKER })

        #split the tickers into an array
        ticks = self.TICKER.split(",")

        # information about the stocks
        sym = ""                #symbol
        c_date = ""             #close date
        
        #p_price = []            #personal value of owned shares
        #chp_price = []          #change of personal value since yesterday

        t_price = 0.0            #total portfolio value
        cht_price = 0.0          #change of portfolio value since yesterday

        for tick in ticks:

            symcod = tick.split(":")

            #connect to the website and get the JSON dataset for that symbol
            url = self.URLs + symcod[0].strip() + self.s_price
            response = requests.request("GET", url, headers=self.headers, data = self.payload)
        
            #convert output to JSON
            jtags = json.loads(response.text)

            #get the date of close - ok to overwrite
            c_date = jtags['data'][0]['close_date']

            #get the share name and their values
            sym += jtags['data'][0]['code'] + ":" + str(symcod[1]) + ":" + str(jtags['data'][0]['close_price']) + ":" + str(jtags['data'][0]['change_price']) + "\n"
            
            #if we need to store the individual value of each stock - not used
            #p_price.append(float(symcod[1]) * float(jtags['data'][0]['close_price']))
            #chp_price.append(float(symcod[1]) * float(jtags['data'][0]['change_price']))

            #add each stock to the total value and change
            t_price += float(symcod[1]) * float(jtags['data'][0]['close_price'])
            cht_price += float(symcod[1]) * float(jtags['data'][0]['change_price'])

        # organise the arrow for the sensor
        diff = float(cht_price)

        if diff > 0:
            icon_mdi = self.tick_up_mdi
        elif diff < 0:
            icon_mdi = self.tick_down_mdi
        else:
            icon_mdi = self.tick_mdi

        t_price_str = "{:.2f}".format(t_price) 

        #create the sensor
        self.set_state(self.asx_portfolio + self.PORT_NAME, state=str(t_price_str), replace=True, attributes= {"icon": icon_mdi, "friendly_name": self.PORT_NAME + " Portfolio", "close_date": str(c_date), "stock_values": str(sym), "total_change": str(cht_price) })

            
        

#
