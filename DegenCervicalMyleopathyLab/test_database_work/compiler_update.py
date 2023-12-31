#imports and setup
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from functions import *
from process_tests import *
from datetime import datetime, timedelta
import math
import itertools
import threading
import time
import sys
test_database_token = 'FF0D4AB80BDB63716462F02BB9291897'
# pilot_database_token = 'BA2BB285FFCF240F0144FB02710BF64F'
token=test_database_token
print()

start=datetime.now()

done = False
def animate():
    for c in itertools.cycle(["⢿", "⣻", "⣽", "⣾", "⣷", "⣯", "⣟", "⡿"]):
        if done:
            break
        cur=datetime.now()
        total_seconds=round((cur-start).seconds)
        total_hours=math.floor(total_seconds/60/60)
        total_minutes=math.floor((total_seconds/60)-(60*total_hours))
        total_seconds=total_seconds%60
        out_message="Time Elapsed "
        if total_hours>0:
            out_message=out_message+str(total_hours)+" hours, "
        out_message=out_message+str(total_minutes)+" minutes, "+str(total_seconds)+" seconds "
        sys.stdout.write('\r' + out_message + c + "   ")
        sys.stdout.flush()
        time.sleep(.125)
    sys.stdout.write('\rDone!     \n')

t = threading.Thread(target=animate)
t.daemon = True
t.start()


new_df=process_tap(cleanTests(allOfOneTypeOfTest('tap',token, sinceLastWeek())))
old_df=pd.read_csv('compiled/tapping.csv',index_col=0)
for i in list(new_df.index):
    participant_previous_entries=old_df[old_df['participant_id']==int(new_df.loc[i,'participant_id'])]
    if (new_df.loc[i,'redcap_repeat_instance'] in list(pd.to_numeric(participant_previous_entries['redcap_repeat_instance'])))==False:
        old_df.loc[len(old_df),:]=new_df.loc[i,:].values
old_df.to_csv('compiled/tapping.csv')



new_df=process_peg(cleanTests(allOfOneTypeOfTest('peg',token, sinceLastWeek())))
old_df=pd.read_csv('compiled/nine_hole_peg.csv',index_col=0)
for i in list(new_df.index):
    participant_previous_entries=old_df[old_df['participant_id']==int(new_df.loc[i,'participant_id'])]
    if (new_df.loc[i,'redcap_repeat_instance'] in list(pd.to_numeric(participant_previous_entries['redcap_repeat_instance'])))==False:
        old_df.loc[len(old_df),:]=new_df.loc[i,:].values
old_df.to_csv('compiled/nine_hole_peg.csv')



new_df=process_gai(cleanTests(allOfOneTypeOfTest('gai',token, sinceLastWeek())), token, thresh='default')
old_df=pd.read_csv('compiled/gait_walking.csv',index_col=0)
for i in list(new_df.index):
    participant_previous_entries=old_df[old_df['participant_id']==int(new_df.loc[i,'participant_id'])]
    if (new_df.loc[i,'redcap_repeat_instance'] in list(pd.to_numeric(participant_previous_entries['redcap_repeat_instance'])))==False:
        old_df.loc[len(old_df),:]=new_df.loc[i,:].values
old_df.to_csv('compiled/gait_walking.csv')
##kill matlab windows from runs where error was thrown
command="taskkill /F /IM MATLAB.exe"
subprocess.run(command, stdout=subprocess.PIPE).stdout.decode('utf-8')




done = True

end=datetime.now()
total_seconds=round((end-start).seconds)
total_hours=math.floor(total_seconds/60/60)
total_minutes=math.floor((total_seconds/60)-(60*total_hours))
total_seconds=total_seconds%60
out_message="\rTotal Time "
if total_hours>0:
    out_message=out_message+str(total_hours)+" hours, "
out_message=out_message+str(total_minutes)+" minutes, "+str(total_seconds)+" seconds, \t\t"
print(out_message)