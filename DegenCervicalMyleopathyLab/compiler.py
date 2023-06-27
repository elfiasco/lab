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
import subprocess
test_database_token = 'FF0D4AB80BDB63716462F02BB9291897'
pilot_database_token = 'BA2BB285FFCF240F0144FB02710BF64F'
token=pilot_database_token

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
    sys.stdout.write('\rDone!     ')

t = threading.Thread(target=animate)
t.daemon = True
t.start()

process_tap(allOfOneTypeOfTest('tap',token), decimals=2).to_csv('compiled/tapping.csv')
process_peg(allOfOneTypeOfTest('peg',token), decimals=2).to_csv('compiled/nine_hole_peg.csv')
process_gai(allOfOneTypeOfTest('gai',token), token, thresh=0, show_plots=False, decimals=2).to_csv('compiled/gait_walking.csv')
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