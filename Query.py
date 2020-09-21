import csv
import pandas as pd
import sys
from datetime import datetime
import requests
soc  = []
volt = []
curr = []
for a in range(1,27):
    
    url_soc = "http://172.16.1.99:9090/api/v1/query_range?start=2020-06-"+str(a).zfill(2)+"T00:00:00.000Z&end=2020-06-"+str(a).zfill(2)+"T23:59:59.000Z&step=1m&query=ess_soc"
    payload = {}
    headers= {}
    response_soc = requests.request("GET", url_soc, headers=headers, data = payload)
    # print(response.text.encode('utf8'))
    results_soc = response_soc.json()['data']['result']
    for soc_l in range(len(results_soc[0]['values'])):
        soc.append(results_soc[0]['values'][soc_l])
        
    ####################        
        
    
    url_current = "http://172.16.1.99:9090/api/v1/query_range?start=2020-06-"+str(a).zfill(2)+"T00:00:00.000Z&end=2020-06-"+str(a).zfill(2)+"T23:59:59.000Z&step=1m&query=ess_current"
    payload = {}
    headers= {}
    response_current = requests.request("GET", url_current, headers=headers, data = payload)
    # print(response.text.encode('utf8'))
    results_current = response_current.json()['data']['result']
    for c_l in range(len(results_current[0]['values'])):
        curr.append(results_current[0]['values'][soc_l])
    ##############
        
        
    url_voltage = "http://172.16.1.99:9090/api/v1/query_range?start=2020-06-"+str(a).zfill(2)+"T00:00:00.000Z&end=2020-06-"+str(a).zfill(2)+"T23:59:59.000Z&step=1m&query=ess_voltage"
    payload = {}
    headers= {}
    response_voltage = requests.request("GET", url_voltage, headers=headers, data = payload)
    # print(response.text.encode('utf8'))
    results_voltage = response_voltage.json()['data']['result']
    for v_l in range(len(results_voltage[0]['values'])):
        volt.append(results_voltage[0]['values'][soc_l])
        
        
        
for i in range(len(soc)):
    soc[i].append(curr[i][1])
    soc[i].append(volt[i][1])
    timest = datetime.utcfromtimestamp(soc[i][0]).strftime('%Y-%m-%d %H:%M:%S')
    soc[i][0] = timest
df = pd.DataFrame(soc, columns = ['Time', 'SOC', 'Current', 'Voltage'])
df.to_csv('UMASS.csv',index=False)
