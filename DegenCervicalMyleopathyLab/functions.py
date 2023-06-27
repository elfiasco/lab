import requests
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import pandas as pd
from datetime import datetime, timedelta

with open('paths_n_fun.txt') as paths_file:
    paths = eval(paths_file.read())
    paths_file.close()
test_database_token = paths.get('test_database_token')
pilot_database_token = paths.get('pilot_database_token')
token=pilot_database_token


all_keys = ['record_id', 'redcap_repeat_instrument', 'redcap_repeat_instance', 'dem_firstname', 'dem_lastname', 'dem_zerodate', 'dem_code', 'dem_joindate', 'dem_pushids', 'demographic_complete', 'ran_uuid', 'ran_startdate', 'ran_enddate', 'ran_scheduledate', 'ran_status', 'ran_supplementaldata', 'ran_serializedresult', 'ran_flexion', 'ran_extension', 'ran_devicemotion', 'range_of_motion_complete', 'gai_uuid', 'gai_startdate', 'gai_enddate', 'gai_scheduledate', 'gai_status', 'gai_supplementaldata', 'gai_serializedresult', 'gai_outacc', 'gai_outdevice', 'gai_returnacc', 'gai_returndevice', 'gai_restacc', 'gai_restdevice', 'gait_walking_complete', 'tap_uuid', 'tap_startdate', 'tap_enddate', 'tap_scheduledate', 'tap_status', 'tap_supplementaldata', 'tap_serializedresult', 'tap_leftjson', 'tap_leftaccelerometer', 'tap_rightjson', 'tap_rightaccelerometer', 'tapping_complete', 'peg_uuid', 'peg_startdate', 'peg_enddate', 'peg_scheduledate', 'peg_status', 'peg_supplementaldata', 'peg_serializedresult', 'peg_dom_place', 'peg_dom_remove', 'peg_nondom_place', 'peg_nondom_remove', 'peg_test_complete', 'tim_uuid', 'tim_startdate', 'tim_enddate', 'tim_scheduledate', 'tim_status', 'tim_supplementaldata', 'tim_serializedresult', 'tim_trial1', 'tim_turnaround', 'tim_trial2', 'timed_walk_complete', 'tes948_uuid', 'tes948_startdate', 'tes948_enddate', 'tes948_scheduledate', 'tes948_status', 'tes948_supplementaldata', 'tes948_serializedresult', 'tes948_json', 'test_taks_complete']
test_mapping = {
        'dem':'',
        'ran':'range_of_motion',
        'gai':'gait_task',
        'tap':'tapping_task',
        'peg': 'hole_peg_task',
        'tim': 'timed_walk',
        'tes': 'test_taks'
    }

def executeRequest(data, token, data_type='json'):
    default_data = {
    'content': 'record',
    'action': 'export',
    'format': 'json',
    'csvDelimiter': '',
    'returnFormat': 'json'
    }
    default_data['format']=data_type
    default_data['returnFormat']=data_type
    default_data['token']=token
    for field in data.keys():
        default_data[field]=data.get(field)
    data=default_data
    r = requests.post('https://redcap.wustl.edu/redcap/api/',data=data)
    if(data_type=='json'):
        return r.json()
    if(data_type=='csv'):
        return r.text

    else:
        return "Invalid Response Type"


def listOfParticipantIds(token):
    data = {
        'fields[0]': 'record_id',
        }
    d = executeRequest(data, token)
    record_ids = []
    for entry in d:
        if "record_id" in entry:
            record_ids.append(entry["record_id"])
    return record_ids

def cleanTest(raw_test_data, default=True):
    if type(raw_test_data) == list and default==True:
        raw_test_data = raw_test_data[0] #if the data is given as a list, return the first test by default
    #now, raw_test_data is one singluar test, not in a list
    output = {}
    test = raw_test_data.get('redcap_repeat_instrument')
    test_shorthand = (list(test_mapping.keys())[list(test_mapping.values()).index(test)])
    chosen_variables = ([item for keep, item in zip([w[0:3]==test_shorthand for w in all_keys], all_keys) if keep])
    for var in chosen_variables:
        output[var] = raw_test_data.get(var)
    output['record_id'] = raw_test_data.get('record_id')
    output['redcap_repeat_instance'] = raw_test_data.get('redcap_repeat_instance')
    return output

def cleanTests(raw_test_data):
    output = []
    if type(raw_test_data)==list:
        for t in raw_test_data:
            output.append(cleanTest(t))
    else:
        output.append(cleanTest(raw_test_data))
    return output


def allDataForParticipant(id, token):
    data = {
        'records[0]': id,
    }
    d = executeRequest(data, token)
    return d

def allTestsOverview(token):
    data = {}
    d = executeRequest(data, token)
    output = []
    for test in d:
        overview = {}
        overview['record_id'] = test['record_id']
        overview['test_type'] = list(test_mapping.keys())[list(test_mapping.values()).index(test['redcap_repeat_instrument'])]
        output.append(overview)
    return output
    
def oneTypeOfTestForParticipant(id, test, token): #returns list of test objects of the same kind of test for the same participant.
    d = allDataForParticipant(id, token)
    
    test = test_mapping.get(test.lower())
    tests = []
    for t in d:
        if t.get('redcap_repeat_instrument')==test:
            tests.append(t)
    return tests

def allOfOneTypeOfTest(test, token, since=None): #returns list of test objects of the same kind of test
    data = {
        'fields[0]': 'record_id',
        "forms": test_mapping.get(test.lower()),
        }
    if since:
        data['dateRangeBegin']=since
    d = executeRequest(data, token)
    tests = []
    if len(d)>0:
        for t in d:
            if t.get('redcap_repeat_instrument')==test_mapping.get(test.lower()):
                tests.append(t)
    return tests

def sinceYesterday():
    (datetime.now()-timedelta(days=1)).strftime('%Y-%m-%d')+' 00:00:00'

def sinceLastWeek():
    (datetime.now()-timedelta(days=7)).strftime('%Y-%m-%d')+' 00:00:00'


def exportFile(Id, field, token, data_type = 'json',event='', repeat_instance=0):
    data = {
        'content': 'file',
        'action': 'export',
        'record': Id,
        'field': field,
        'repeat_instance':repeat_instance,
        'event': event,
        'returnFormat': data_type
        
    }
    return(executeRequest(data, token, data_type))

def dict_reverse_get(value, dict):
    return(list(dict.keys())[list(dict.values()).index(value)])

def ThreeDPlot(data, x, y, z, c='none', view_angle_x=15, view_angle_y=75):
    ax = plt.axes(projection='3d')
    if c!='none':
        c=data[c]
        print(c)
    ax.xaxis.set_pane_color((.2, 1, 1, .5)); 
    ax.yaxis.set_pane_color((1, 1, .2, .5)); 
    ax.xaxis.set_label_text(x);ax.yaxis.set_label_text(y);ax.zaxis.set_label_text(z)
    ax.plot3D(data[x], data[y], data[z], 'gray')
    ax.scatter3D(data[x], data[y], data[z], c=c, cmap='Greens')
    ax.view_init(view_angle_x, view_angle_y)
    plt.show()

def dictListToDF(dict_list):
    if type(dict_list)!=dict and type(dict_list)!=list:
        print("ERROR: TYPE MUST BE DICT OR LIST FOR dictListToDF()")
        print('TYPE: '+str(type(dict_list)))
        return "ERROR" 
    if type(dict_list)==dict and 'items' in list(dict_list.keys()):
                dict_list = dict_list.get('items')
    return(pd.json_normalize(dict_list))

