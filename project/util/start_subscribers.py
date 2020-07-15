from project.model.subscriber.baby_monitor_subscriber import BabyMonitorSubscriber
from project.model.subscriber.smartphone_subscriber import SmartphoneSubscriber
from project.model.subscriber.smart_tv_subscriber import SmartTvSubscriber
from multiprocessing import Process
from time import sleep
import pika
# baby_monitor = BabyMonitorSubscriber()
# baby_monitor.start()
# baby_monitor.join()

# import subprocess
# import sys
# p = subprocess.Popen(
#     [sys.executable, '-c', 'import time; time.sleep(100)'],
#     stdout=subprocess.PIPE,
#     stderr=subprocess.STDOUT
# )

# smartphone_bm = SmartphoneSubscriber('babymonitor')
# smartphone_bm.start()
# smartphone_bm.join()
# import ipdb; ipdb.set_trace()
# smartphone_st = SmartphoneSubscriber('smart_tv')
# smartphone_st.start()
# smartphone_st.join()

# smart_tv = SmartTvSubscriber()
# smart_tv.start()
# smart_tv.join()

subscriber_list = []
subscriber_list.append(BabyMonitorSubscriber())
subscriber_list.append(SmartphoneSubscriber('babymonitor'))
subscriber_list.append(SmartphoneSubscriber('smart_tv'))
subscriber_list.append(SmartTvSubscriber())

# execute
process_list = []
for sub in subscriber_list:
    process = Process(target=sub.run)
    process.start()
    process_list.append(process)

sleep(1)

# wait for all process to finish
# for process in process_list:
#    process.join()
