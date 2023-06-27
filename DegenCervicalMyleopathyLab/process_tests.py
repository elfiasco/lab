import json
from datetime import datetime, timedelta
import functions as f
import pandas as pd
import subprocess
import time
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import numpy as np

with open('paths_n_fun.txt') as paths_file:
    paths = eval(paths_file.read())
    paths_file.close()


def second_gai_process(d, show_plots, thresh):
    df_outdevice = f.dictListToDF(d['outdevice'])
    df_restdevice = f.dictListToDF(d['restdevice'])
    df_returndevice = f.dictListToDF(d['returndevice'])

    start_time = datetime.strptime(d['startdate'], '%Y-%m-%d %H:%M:%S')

    # df_restdevice['timestamp']=(df_restdevice['timestamp']).apply(lambda x: start_time+timedelta(seconds=x))
    # df_restdevice = df_restdevice.drop(['gravity.x', 'gravity.y','gravity.z','magneticField.x','magneticField.y','magneticField.z','magneticField.accuracy'], axis=1)
    # df_restdevice = df_restdevice.rename(columns={'userAcceleration.x' : 'AccelX','userAcceleration.y': 'AccelY','userAcceleration.z': 'AccelZ','attitude.y':'QuatY','attitude.w': 'QuatW','attitude.x': 'QuatX','attitude.z': 'QuatZ','rotationRate.x':'GyroX', 'rotationRate.x':'GyroX', 'rotationRate.y':'GyroY', 'rotationRate.z':'GyroZ','timestamp':'Timestamp'})
    # df_restdevice = df_restdevice.reindex(columns=['Timestamp', 'AccelX', 'AccelY','AccelZ','GyroX','GyroY','GyroZ','QuatW','QuatX','QuatY','QuatZ' ])
    # df_restdevice=df_restdevice.set_index('Timestamp')
    # df_restdevice[['AccelX', 'AccelY','AccelZ','GyroX','GyroY','GyroZ','QuatW','QuatX','QuatY','QuatZ']]=0

    df_outdevice['timestamp']=(df_outdevice['timestamp']).apply(lambda x: start_time+timedelta(seconds=x))
    df_outdevice = df_outdevice.drop(['gravity.x', 'gravity.y','gravity.z','magneticField.x','magneticField.y','magneticField.z','magneticField.accuracy'], axis=1)
    df_outdevice = df_outdevice.rename(columns={'userAcceleration.x' : 'AccelX','userAcceleration.y': 'AccelY','userAcceleration.z': 'AccelZ','attitude.y':'QuatY','attitude.w': 'QuatW','attitude.x': 'QuatX','attitude.z': 'QuatZ','rotationRate.x':'GyroX', 'rotationRate.x':'GyroX', 'rotationRate.y':'GyroY', 'rotationRate.z':'GyroZ','timestamp':'Timestamp'})
    df_outdevice = df_outdevice.reindex(columns=['Timestamp', 'AccelX', 'AccelY','AccelZ','GyroX','GyroY','GyroZ','QuatW','QuatX','QuatY','QuatZ' ])
    df_outdevice=df_outdevice.set_index('Timestamp')
    d2=df_outdevice
    s=abs(d2['AccelX'])+abs(d2['AccelY'])+abs(d2['AccelZ'])
    rm=s.rolling(50).mean()
    if thresh=='default':
        thresh=(np.nanmean(rm)/2)
    rm[rm<thresh]=0
    rm[rm.isna()]=0
    
    start_filter=list(rm[rm>0].index)
    if(len(start_filter)>0):
        start_filter=start_filter[0]
    else:
        start_filter=list(rm.index)[50*2]
    rm=rm.loc[start_filter:]
    rm[-1]=0
    rm=rm.loc[:list(rm[rm==0].index)[0]]
    end_filter=list(rm.index)
    if(len(end_filter)>0):
        end_filter=end_filter[-1]
    else:
        end_filter=list(d2.index)[-1]
    rm=rm.drop(list(rm.index)[-1])
    d3=d2.drop(d2[(d2.index)<start_filter].index)
    # d3.loc[d3[(d3.index)>end_filter].index,['AccelX', 'AccelY','AccelZ','GyroX','GyroY','GyroZ','QuatW','QuatX','QuatY','QuatZ']]=0
    d3=d3.drop(d3[(d3.index)>end_filter].index)
    df_outdevice=d3
    if show_plots:
        plt.plot(s)
        plt.plot(rm)
        plt.show()

    df_returndevice['timestamp']=(df_returndevice['timestamp']).apply(lambda x: start_time+timedelta(seconds=x+20))
    df_returndevice = df_returndevice.drop(['gravity.x', 'gravity.y','gravity.z','magneticField.x','magneticField.y','magneticField.z','magneticField.accuracy'], axis=1)
    df_returndevice = df_returndevice.rename(columns={'userAcceleration.x' : 'AccelX','userAcceleration.y': 'AccelY','userAcceleration.z': 'AccelZ','attitude.y':'QuatY','attitude.w': 'QuatW','attitude.x': 'QuatX','attitude.z': 'QuatZ','rotationRate.x':'GyroX', 'rotationRate.x':'GyroX', 'rotationRate.y':'GyroY', 'rotationRate.z':'GyroZ','timestamp':'Timestamp'})
    df_returndevice = df_returndevice.reindex(columns=['Timestamp', 'AccelX', 'AccelY','AccelZ','GyroX','GyroY','GyroZ','QuatW','QuatX','QuatY','QuatZ' ])
    df_returndevice=df_returndevice.set_index('Timestamp')
    d2=df_returndevice
    s=abs(d2['AccelX'])+abs(d2['AccelY'])+abs(d2['AccelZ'])
    rm=s.rolling(50).mean()
    if thresh=='default':
        thresh=(np.nanmean(rm)/3)
    rm[rm<thresh]=0
    rm[rm.isna()]=0
    start_filter=list(rm[rm>0].index)
    if(len(start_filter)>0):
        start_filter=start_filter[0]
    else:
        start_filter=list(rm.index)[50*2]
    rm=rm.loc[start_filter:]
    rm[-1]=0
    rm=rm.loc[:list(rm[rm==0].index)[0]]
    end_filter=list(rm.index)
    if(len(end_filter)>0):
        end_filter=end_filter[-1]
    else:
        end_filter=list(d2.index)[-1]
    rm=rm.drop(list(rm.index)[-1])
    d3=d2.drop(d2[(d2.index)<start_filter].index)
    # d3.loc[d3[(d3.index)>end_filter].index,['AccelX', 'AccelY','AccelZ','GyroX','GyroY','GyroZ','QuatW','QuatX','QuatY','QuatZ']]=0
    d3=d3.drop(d3[(d3.index)>end_filter].index)
    df_returndevice=d3
    if show_plots:
        plt.plot(s)
        plt.plot(rm)
        plt.show()
    # print(df_restdevice)
    # df_restdevice['timestamp']=(df_restdevice['timestamp']).apply(lambda x: start_time+timedelta(seconds=x))
    # df_restdevice = df_restdevice.drop(['gravity.x', 'gravity.y','gravity.z','magneticField.x','magneticField.y','magneticField.z','magneticField.accuracy'], axis=1)
    # df_restdevice = df_restdevice.rename(columns={'userAcceleration.x' : 'AccelX','userAcceleration.y': 'AccelY','userAcceleration.z': 'AccelZ','attitude.y':'QuatY','attitude.w': 'QuatW','attitude.x': 'QuatX','attitude.z': 'QuatZ','rotationRate.x':'GyroX', 'rotationRate.x':'GyroX', 'rotationRate.y':'GyroY', 'rotationRate.z':'GyroZ','timestamp':'Timestamp'})
    # df_restdevice = df_restdevice.reindex(columns=['Timestamp', 'AccelX', 'AccelY','AccelZ','GyroX','GyroY','GyroZ','QuatW','QuatX','QuatY','QuatZ' ])
    # df_restdevice=df_restdevice.set_index('Timestamp')
    # for col in df_restdevice.columns:
    #     df_restdevice[col]=0

    data = pd.concat([df_outdevice, df_returndevice])
    d['matlab_ready_df']=data
    return d, df_outdevice

def third_gai_process(trial, prints=False):
    trial['matlab_ready_df'].to_csv('out_data_here.csv')
    if prints==True:
        print("Data downloaded")
    #malab runner
    command=paths.get('matlab_path')+' -nosplash -nodesktop -r "run('+paths.get('two_lap_adj_code')+'); exit;"' #two-lap-adj   sincmotion-gait-matlab
    subprocess.run(command, stdout=subprocess.PIPE).stdout.decode('utf-8')
    start_time=time.time()
    if prints==True:
        print("Matlab code started")
    #reading of matlab output
    new=False
    wait_time=0
    while new==False and wait_time<15:
        with open(paths.get('two_lap_adj_output'), 'r') as file: #two-lap-adj
            data = file.read()
        file.close()
        data=data.split('\n')
        data_dict={}
        if(len(data)>0):
            for d in data[:-1]:
                label = d.split(': ')[0]
                if(len(d.split(': ')[1].split(' '))>1):
                    label=label+' ('+' '.join(d.split(': ')[1].split(' ')[1:])+')'
                data_dict[label]=float(d.split(': ')[1].split(' ')[0])
            if(data_dict['Time of computation (unix)']>start_time):
                new=True
        time.sleep(.5)
        wait_time=wait_time+.5
    if wait_time>=15:
        print("ERROR, MATLAB CALCULATIONS THREW ERROR")
        return trial
    if prints==True:
        print("Matlab code complete")
    for d in data_dict.keys():
        trial['m_'+d]=data_dict.get(d)
    return trial

def process_gai(summary_data, token, prints=False, show_plots=False, thresh=.05, decimals=10):
    if(type(summary_data))==list:
        data=[]
        for t in summary_data:
            data.append(process_gai(t,token,))
        data=pd.json_normalize(data)[['record_id', 'startdate', 'redcap_repeat_instance', 'm_Time of computation (unix)', 'm_Gait symmetry (percent)', 'm_Step length (m)', 'm_Step time (sec)', 'm_Step length variability (percent)', 'm_Step time variability (percent)', 'm_Step length asymmetry (percent)', 'm_Step time asymmetry (percent)', 'm_Step velocity (m/sec)', 'm_Step count lap 1', 'm_Step count lap 2']]
        data=data.rename(columns={'startdate':'test_time'})
        data['test_time']=pd.to_datetime(data['test_time'])
    else:

        repeat_instance=summary_data['redcap_repeat_instance']
        for field in ['outacc', 'outdevice', 'returnacc', 'returndevice', 'restacc', 'restdevice']:
            summary_data[field] = (f.exportFile(summary_data['record_id'], field, token,repeat_instance=repeat_instance))
            if type(summary_data[field])==dict and 'items' in list(summary_data[field].keys()):
                summary_data[field] = summary_data[field].get('items')
        data = summary_data
        data, d2=second_gai_process(data, show_plots=show_plots, thresh=thresh)
        data=third_gai_process(data, prints=prints)
        for key in data.keys():
            if type(data.get(key))==float:
                data[key]=round(data.get(key),decimals)
    return data



def process_tap(cleanedTapData, prints=True, plots=False, decimals=10):
    if type(cleanedTapData)==list:
        data=[]
        for i in range(len(cleanedTapData)):
            data.append(process_tap(cleanedTapData[i], prints=False, plots=plots))
        data=pd.json_normalize(data)
        data['test_time']=pd.to_datetime(data['test_time'])
        return data

    else:
        ##PART ONE, NORMALIZE ANDROID AND iOS
        tap=cleanedTapData
        record_id=(tap['record_id'])
        test_time=tap['startdate_2']
        redcap_repeat_instance=tap['redcap_repeat_instance']
        if type(eval(tap['leftjson']))==list: #android
            left_hand_samples=pd.json_normalize(eval(tap['leftjson'])[0]['TappingSamples']).rename(columns={"TappedButtonId":"ButtonId"})
            left_hand_samples['TapCoordinate']=left_hand_samples['TapCoordinate'].str[1:-1].str.split(', ')
            left_hand_samples['X']=pd.to_numeric(left_hand_samples['TapCoordinate'].str[0])
            left_hand_samples['Y']=pd.to_numeric(left_hand_samples['TapCoordinate'].str[1])
            left_hand_samples['timestamp']=(left_hand_samples['duration']-min(left_hand_samples['duration']))/1000
            left_hand_samples['ButtonId']=left_hand_samples['ButtonId'].str.replace('TappedButton','')
            left_hand_samples=left_hand_samples.drop(columns=['duration', 'TapCoordinate', 'TapTimeStamp'])

            right_hand_samples=pd.json_normalize(eval(tap['rightjson'])[0]['TappingSamples']).rename(columns={"TappedButtonId":"ButtonId"})
            right_hand_samples['TapCoordinate']=right_hand_samples['TapCoordinate'].str[1:-1].str.split(', ')
            right_hand_samples['X']=pd.to_numeric(right_hand_samples['TapCoordinate'].str[0])
            right_hand_samples['Y']=pd.to_numeric(right_hand_samples['TapCoordinate'].str[1])
            right_hand_samples['timestamp']=(right_hand_samples['duration']-min(right_hand_samples['duration']))/1000
            right_hand_samples['ButtonId']=right_hand_samples['ButtonId'].str.replace('TappedButton','')
            right_hand_samples=right_hand_samples.drop(columns=['duration', 'TapCoordinate', 'TapTimeStamp'])

            

            e=eval(tap['leftjson'])[0]
            screen_size_x=float(e['TappingViewSize'][1:-1].split(', ')[0])
            screen_size_y=float(e['TappingViewSize'][1:-1].split(', ')[1])
            
            left_button_height=float(e['ButtonRectLeft'].split('} {')[-1][:-2].split(', ')[-1])
            left_button_width=float(e['ButtonRectLeft'].split('} {')[-1][:-2].split(', ')[0])
            left_button_midpointX=float(e['ButtonRectLeft'][2:].split(', ')[0])+(left_button_width/2)
            left_button_midpointY=float(e['ButtonRectLeft'][2:].split(', ')[1].split('}')[0])+(left_button_height/2)

            right_button_height=float(e['ButtonRectRight'].split('} {')[-1][:-2].split(', ')[-1])
            right_button_width=float(e['ButtonRectRight'].split('} {')[-1][:-2].split(', ')[0])
            right_button_midpointX=float(e['ButtonRectRight'][2:].split(', ')[0])+(right_button_width/2)
            right_button_midpointY=float(e['ButtonRectRight'][2:].split(', ')[1].split('}')[0])+(right_button_height/2)


        else: #apple
            
            left_hand_samples=pd.json_normalize(eval(tap['leftjson'])['samples']).rename(columns={"buttonIdentifier":"ButtonId",'locationY':'Y','locationX':'X'})
            left_hand_samples['ButtonId']=left_hand_samples['ButtonId'].str[1:]
            left_hand_samples['X']=pd.to_numeric(left_hand_samples['X'])
            left_hand_samples['Y']=pd.to_numeric(left_hand_samples['Y'])
            left_hand_samples['timestamp']=pd.to_numeric(left_hand_samples['timestamp'])
            right_hand_samples=pd.json_normalize(eval(tap['rightjson'])['samples']).rename(columns={"buttonIdentifier":"ButtonId",'locationY':'Y','locationX':'X'})
            right_hand_samples['ButtonId']=right_hand_samples['ButtonId'].str[1:]
            right_hand_samples['X']=pd.to_numeric(right_hand_samples['X'])
            right_hand_samples['Y']=pd.to_numeric(right_hand_samples['Y'])
            right_hand_samples['timestamp']=pd.to_numeric(right_hand_samples['timestamp'])

            e=eval(tap['leftjson'])
            screen_size_x=float(e['stepViewSize'].get('width'))
            screen_size_y=float(e['stepViewSize'].get('height'))

            left_button_height=float(e['buttonRect1'].get('height'))
            left_button_width=float(e['buttonRect1'].get('width'))
            left_button_midpointX=float(e['buttonRect1'].get('locationX'))+(left_button_width/2)
            left_button_midpointY=float(e['buttonRect1'].get('locationY'))+(left_button_height/2)

            right_button_height=float(e['buttonRect2'].get('height'))
            right_button_width=float(e['buttonRect2'].get('width'))
            right_button_midpointX=float(e['buttonRect2'].get('locationX'))+(right_button_width/2)
            right_button_midpointY=float(e['buttonRect2'].get('locationY'))+(right_button_height/2)

        #PART TWO, COMPUTE OUT STATISTICS

        data={'record_id':record_id,'test_time':test_time,'redcap_repeat_instance':redcap_repeat_instance}

        print_out=""

        #notes:
        #right will always be positive for asymetry. for example if on the left hand the finger precisions are right:50, left:60, 
        #the precision score for the left hand is 55 and the asymetry score for the left hand is 10 (positive because right is better)

        #helpers
        left_finger_left_hand=left_hand_samples[left_hand_samples['ButtonId']=='Left']
        right_finger_left_hand=left_hand_samples[left_hand_samples['ButtonId']=='Right']
        left_finger_right_hand=right_hand_samples[right_hand_samples['ButtonId']=='Left']
        right_finger_right_hand=right_hand_samples[right_hand_samples['ButtonId']=='Right']
        location_precision_modifier=100/np.mean([left_button_width,right_button_width])



        #precision #average euclidean distance between each tap and mean tap
        precision_left_finger_left_hand=np.mean(((left_finger_left_hand['X']-np.mean(left_finger_left_hand['X']))**2+(left_finger_left_hand['Y']-np.mean(left_finger_left_hand['Y']))**2)**.5)*location_precision_modifier
        precision_right_finger_left_hand=np.mean(((right_finger_left_hand['X']-np.mean(right_finger_left_hand['X']))**2+(right_finger_left_hand['Y']-np.mean(right_finger_left_hand['Y']))**2)**.5)*location_precision_modifier
        precision_left_finger_right_hand=np.mean(((left_finger_right_hand['X']-np.mean(left_finger_right_hand['X']))**2+(left_finger_right_hand['Y']-np.mean(left_finger_right_hand['Y']))**2)**.5)*location_precision_modifier
        precision_right_finger_right_hand=np.mean(((right_finger_right_hand['X']-np.mean(right_finger_right_hand['X']))**2+(right_finger_right_hand['Y']-np.mean(right_finger_right_hand['Y']))**2)**.5)*location_precision_modifier
        left_hand_precision=np.mean([precision_left_finger_left_hand,precision_right_finger_left_hand])
        right_hand_precision=np.mean([precision_left_finger_right_hand,precision_right_finger_right_hand])
        left_hand_precision_asym=precision_right_finger_left_hand-precision_left_finger_left_hand
        right_hand_precision_asym=precision_right_finger_right_hand-precision_left_finger_right_hand

        print_out=print_out+'\n'+("LEFT HAND PRECISION: "+str(left_hand_precision)); data['left_hand_precision']=left_hand_precision
        print_out=print_out+'\n'+("RIGHT HAND PRECISION: "+str(right_hand_precision)); data['right_hand_precision']=right_hand_precision
        print_out=print_out+'\n'+("LEFT HAND PRECISION FINGER ASYMETRY: "+str(left_hand_precision_asym)); data['left_hand_precision_asym']=left_hand_precision_asym
        print_out=print_out+'\n'+("RIGHT HAND PRECISION FINGER ASYMETRY: "+str(right_hand_precision_asym)); data['right_hand_precision_asym']=right_hand_precision_asym
        print_out=print_out+'\n'

        #accuracy: #percentage of taps within the inner 95% of circle
        accuracy_modifier=1
        accuracy_left_finger_left_hand=1-(((((left_finger_left_hand['X']-left_button_midpointX)**2+(left_finger_left_hand['Y']-left_button_midpointY)**2)**.5)>(left_button_width/2)*accuracy_modifier).sum()/len(left_finger_left_hand))
        accuracy_right_finger_left_hand=1-(((((right_finger_left_hand['X']-right_button_midpointX)**2+(right_finger_left_hand['Y']-right_button_midpointY)**2)**.5)>(right_button_width/2)*accuracy_modifier).sum()/len(right_finger_right_hand))
        accuracy_left_finger_right_hand=1-(((((left_finger_right_hand['X']-left_button_midpointX)**2+(left_finger_right_hand['Y']-left_button_midpointY)**2)**.5)>(left_button_width/2)*accuracy_modifier).sum()/len(left_finger_left_hand))
        accuracy_right_finger_right_hand=1-(((((right_finger_right_hand['X']-right_button_midpointX)**2+(right_finger_right_hand['Y']-right_button_midpointY)**2)**.5)>(right_button_width/2)*accuracy_modifier).sum()/len(right_finger_right_hand))
        left_hand_accuracy=np.mean([accuracy_left_finger_left_hand,accuracy_right_finger_left_hand])
        right_hand_accuracy=np.mean([accuracy_left_finger_right_hand,accuracy_right_finger_right_hand])
        left_hand_accuracy_asym=accuracy_right_finger_left_hand-accuracy_left_finger_left_hand
        right_hand_accuracy_asym=accuracy_right_finger_right_hand-accuracy_left_finger_right_hand

        print_out=print_out+'\n'+("LEFT HAND ACCURACY: "+str(left_hand_accuracy)); data['left_hand_accuracy']=left_hand_accuracy
        print_out=print_out+'\n'+("RIGHT HAND ACCURACY: "+str(right_hand_accuracy)); data['right_hand_accuracy']=right_hand_accuracy
        print_out=print_out+'\n'+("LEFT HAND ACCURACY FINGER ASYMETRY: "+str(left_hand_accuracy_asym)); data['left_hand_accuracy_asym']=left_hand_accuracy_asym
        print_out=print_out+'\n'+("RIGHT HAND ACCURACY FINGER ASYMETRY: "+str(right_hand_accuracy_asym)); data['right_hand_accuracy_asym']=right_hand_accuracy_asym
        print_out=print_out+'\n'

        #speed #average number of taps per second
        left_hand_speed=1/np.mean(left_hand_samples['timestamp']-left_hand_samples['timestamp'].shift(1))
        right_hand_speed=1/np.mean(right_hand_samples['timestamp']-right_hand_samples['timestamp'].shift(1))

        print_out=print_out+'\n'+("LEFT HAND SPEED: "+str(left_hand_speed)); data['left_hand_speed']=left_hand_speed
        print_out=print_out+'\n'+("RIGHT HAND SPEED: "+str(right_hand_speed)); data['right_hand_speed']=right_hand_speed
        print_out=print_out+'\n'
        
        #stamina #coefficient of linear regression using times in between taps
        left_hand_stamina=(LinearRegression().fit(np.array(list(left_hand_samples.index)[2:-5]).reshape(-1, 1),1000*(left_hand_samples.loc[list(left_hand_samples.index)[1:-5],'timestamp']-left_hand_samples.loc[list(left_hand_samples.index)[1:-5],'timestamp'].shift(1)).dropna())).coef_[0]
        right_hand_stamina=(LinearRegression().fit(np.array(list(right_hand_samples.index)[2:-5]).reshape(-1, 1),1000*(right_hand_samples.loc[list(right_hand_samples.index)[1:-5],'timestamp']-right_hand_samples.loc[list(right_hand_samples.index)[1:-5],'timestamp'].shift(1)).dropna())).coef_[0]

        print_out=print_out+'\n'+("LEFT HAND STAMINA: "+str(left_hand_stamina)); data['left_hand_stamina']=left_hand_stamina
        print_out=print_out+'\n'+("RIGHT HAND STAMINA: "+str(right_hand_stamina)); data['right_hand_stamina']=right_hand_stamina
        print_out=print_out+'\n'

        #double_taps #number of times user taps the same button twice instead of alternating
        left_hand_double_taps=((left_hand_samples['ButtonId'])==(left_hand_samples['ButtonId'].shift(1))).value_counts().get(True,default=0)
        right_hand_double_taps=((right_hand_samples['ButtonId'])==(right_hand_samples['ButtonId'].shift(1))).value_counts().get(True,default=0)
        print_out=print_out+'\n'+("LEFT HAND DOUBLE TAPS: "+str(left_hand_double_taps)); data['left_hand_double_taps']=left_hand_double_taps
        print_out=print_out+'\n'+("RIGHT HAND DOUBLE TAPS: "+str(right_hand_double_taps)); data['right_hand_double_taps']=right_hand_double_taps
        print_out=print_out+'\n'

        #distance_between_taps_over_time
        
        left_finger_left_hand_distance_between_taps_over_time=(LinearRegression().fit(np.array(list(left_finger_left_hand.index)[1:-1]).reshape(-1, 1),((((left_finger_left_hand['X']-left_finger_left_hand['X'].shift(1))**2 + (left_finger_left_hand['Y']-left_finger_left_hand['Y'].shift(1))**2)**.5).iloc[1:-1]))).coef_[0]
        right_finger_left_hand_distance_between_taps_over_time=(LinearRegression().fit(np.array(list(left_finger_right_hand.index)[1:-1]).reshape(-1, 1),((((left_finger_right_hand['X']-left_finger_right_hand['X'].shift(1))**2 + (left_finger_right_hand['Y']-left_finger_right_hand['Y'].shift(1))**2)**.5).iloc[1:-1]))).coef_[0]
        left_finger_right_hand_distance_between_taps_over_time=(LinearRegression().fit(np.array(list(left_finger_right_hand.index)[1:-1]).reshape(-1, 1),((((left_finger_right_hand['X']-left_finger_right_hand['X'].shift(1))**2 + (left_finger_right_hand['Y']-left_finger_right_hand['Y'].shift(1))**2)**.5).iloc[1:-1]))).coef_[0]
        right_finger_right_hand_distance_between_taps_over_time=(LinearRegression().fit(np.array(list(right_finger_right_hand.index)[1:-1]).reshape(-1, 1),((((right_finger_right_hand['X']-right_finger_right_hand['X'].shift(1))**2 + (right_finger_right_hand['Y']-right_finger_right_hand['Y'].shift(1))**2)**.5).iloc[1:-1]))).coef_[0]
        left_hand_distance_between_taps_over_time=np.mean([left_finger_left_hand_distance_between_taps_over_time,right_finger_left_hand_distance_between_taps_over_time])
        right_hand_distance_between_taps_over_time=np.mean([left_finger_right_hand_distance_between_taps_over_time,right_finger_right_hand_distance_between_taps_over_time])
        
        print_out=print_out+'\n'+("LEFT HAND DISTANCE BTWN TAPS OVER TIME: "+str(left_hand_distance_between_taps_over_time)); data['left_hand_distance_between_taps_over_time']=left_hand_distance_between_taps_over_time
        print_out=print_out+'\n'+("RIGHT HAND DISTANCE BTWN TAPS OVER TIME: "+str(right_hand_distance_between_taps_over_time)); data['right_hand_distance_between_taps_over_time']=right_hand_distance_between_taps_over_time
        print_out=print_out+'\n'

        #heteroskedasticity regession
        left_hand_time_abs_residuals=np.abs(1000*(left_hand_samples.loc[list(left_hand_samples.index)[1:-5],'timestamp']-left_hand_samples.loc[list(left_hand_samples.index)[1:-5],'timestamp'].shift(1)).dropna()-(LinearRegression().fit(np.array(list(left_hand_samples.index)[2:-5]).reshape(-1, 1),1000*(left_hand_samples.loc[list(left_hand_samples.index)[1:-5],'timestamp']-left_hand_samples.loc[list(left_hand_samples.index)[1:-5],'timestamp'].shift(1)).dropna())).predict(np.array(list(left_hand_samples.index)[2:-5]).reshape(-1, 1)))
        left_hand_heteroskedasticity=(LinearRegression().fit(np.array(list(left_hand_samples.index)[2:-5]).reshape(-1, 1),left_hand_time_abs_residuals)).coef_[0]
        right_hand_time_abs_residuals=np.abs(1000*(right_hand_samples.loc[list(right_hand_samples.index)[1:-5],'timestamp']-right_hand_samples.loc[list(right_hand_samples.index)[1:-5],'timestamp'].shift(1)).dropna()-(LinearRegression().fit(np.array(list(right_hand_samples.index)[2:-5]).reshape(-1, 1),1000*(right_hand_samples.loc[list(right_hand_samples.index)[1:-5],'timestamp']-right_hand_samples.loc[list(right_hand_samples.index)[1:-5],'timestamp'].shift(1)).dropna())).predict(np.array(list(right_hand_samples.index)[2:-5]).reshape(-1, 1)))
        right_hand_heteroskedasticity=(LinearRegression().fit(np.array(list(right_hand_samples.index)[2:-5]).reshape(-1, 1),right_hand_time_abs_residuals)).coef_[0]
        print_out=print_out+'\n'+("LEFT HAND TIME HETEROSKEDASTICITY: "+str(left_hand_heteroskedasticity)); data['left_hand_heteroskedasticity']=left_hand_heteroskedasticity
        print_out=print_out+'\n'+("RIGHT HAND TIME HETEROSKEDASTICIT: "+str(right_hand_heteroskedasticity)); data['right_hand_heteroskedasticity']=right_hand_heteroskedasticity
        print_out=print_out+'\n'


        #steadiness #score from 0-100 with 100 being the best which looks to combine jumpiness/variability of placement of taps with tap in between taps
        left_hand_steadiness=100-(left_hand_precision-5)*2-((np.std(1000*(left_hand_samples.loc[list(left_hand_samples.index)[1:-5],'timestamp']-left_hand_samples.loc[list(left_hand_samples.index)[1:-5],'timestamp'].shift(1)).dropna()))**.5)-left_hand_double_taps**.5
        right_hand_steadiness=100-(right_hand_precision-5)*2-((np.std(1000*(right_hand_samples.loc[list(right_hand_samples.index)[1:-5],'timestamp']-right_hand_samples.loc[list(right_hand_samples.index)[1:-5],'timestamp'].shift(1)).dropna()))**.5)-right_hand_double_taps**.5
        print_out=print_out+'\n'+("LEFT HAND STEADINESS: "+str(left_hand_steadiness)); data['left_hand_steadiness']=left_hand_steadiness
        print_out=print_out+'\n'+("RIGHT HAND STEADINESS: "+str(right_hand_steadiness)); data['right_hand_steadiness']=right_hand_steadiness
        print_out=print_out+'\n'



        # plt.plot(1000*(left_hand_samples.loc[list(left_hand_samples.index)[1:-5],'timestamp']-left_hand_samples.loc[list(left_hand_samples.index)[1:-5],'timestamp'].shift(1)).dropna())
        # plt.plot(1000*(right_hand_samples.loc[list(right_hand_samples.index)[1:-5],'timestamp']-right_hand_samples.loc[list(right_hand_samples.index)[1:-5],'timestamp'].shift(1)).dropna())
        # plt.show()
        if plots==True:
            fig, axes = plt.subplots(nrows=1, ncols=4, figsize=(15, 3))  
            axes[0].plot(left_finger_left_hand['X'],left_finger_left_hand['Y'])
            axes[0].plot(right_finger_left_hand['X'],right_finger_left_hand['Y'])
            theta = np.linspace( 0 , 2 * np.pi , 150 )
            radius = left_button_width/2
            a = radius * np.cos( theta )
            b = radius * np.sin( theta )
            axes[0].plot(left_button_midpointX + a,left_button_midpointY + b)
            axes[0].plot(right_button_midpointX + a,right_button_midpointY + b)
            axes[0].set_title('Left Hand')

            axes[2].plot(left_finger_right_hand['X'],left_finger_right_hand['Y'])
            axes[2].plot(right_finger_right_hand['X'],right_finger_right_hand['Y'])
            theta = np.linspace( 0 , 2 * np.pi , 150 )
            radius = left_button_width/2
            a = radius * np.cos( theta )
            b = radius * np.sin( theta )
            axes[2].plot(left_button_midpointX + a,left_button_midpointY + b)
            axes[2].plot(right_button_midpointX + a,right_button_midpointY + b)
            axes[2].set_title('Right Hand')

            axes[1].plot(1000*(left_hand_samples.loc[list(left_hand_samples.index)[1:-5],'timestamp']-left_hand_samples.loc[list(left_hand_samples.index)[1:-5],'timestamp'].shift(1)).dropna())
            axes[1].set_title('Left Hand Time Between Taps')
            
            axes[3].plot(1000*(right_hand_samples.loc[list(right_hand_samples.index)[1:-5],'timestamp']-right_hand_samples.loc[list(right_hand_samples.index)[1:-5],'timestamp'].shift(1)).dropna())
            axes[3].set_title('Right Hand Time Between Taps')

            fig.tight_layout()
            plt.show()

        for key in data.keys():
            if type(data.get(key))==float:
                data[key]=round(data.get(key),decimals)

        return data


def process_peg(cleanedPegData, decimals=10):
    if type(cleanedPegData)==list:
        data=[]
        for i in range(len(cleanedPegData)):
            data.append(process_peg(cleanedPegData[i]))
        data=pd.json_normalize(data)
        data['test_time']=pd.to_datetime(data['test_time'])
        return data
    else:
        peg=cleanedPegData
        record_id=peg['record_id']
        redcap_repeat_instance=peg['redcap_repeat_instance']
        test_time=peg['startdate_3']

        data={
            'record_id':record_id,
            'redcap_repeat_instance':redcap_repeat_instance,
            'test_time':test_time
        }

        partitions=['dom_place', 'dom_remove', 'nondom_place', 'nondom_remove']
        failuress=[]
        time_deviations=[]
        for i in partitions:
            failures=int(eval(peg.get(i)).get('totalFailures'));failuress.append(failures)
            samples=pd.json_normalize(eval(peg.get(i)).get('samples'))
            time_deviation=round(np.std(pd.to_numeric(samples['time'])),decimals);time_deviations.append(time_deviation)

            data[i+'_failures']=failures
            data[i+'_time_deviation']=time_deviation
            
        data['average_failures']=round(np.mean(failuress),decimals)
        data['average_time_deviations']=round(np.mean(time_deviations),decimals)

        data['dom_preference_failures']=round((data['dom_place_failures']+data['dom_remove_failures']-data['nondom_place_failures']-data['nondom_remove_failures'])/2,decimals)
        data['dom_preference_time_deviation']=round((data['dom_place_time_deviation']+data['dom_remove_time_deviation']-data['nondom_place_time_deviation']-data['nondom_remove_time_deviation'])/2,decimals)


        return data