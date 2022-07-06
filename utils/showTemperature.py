import sys
sys.path.insert(0,'C:/Users/jorn-/Documents/school/y2/thesis/cuffling/code/Cuff_sensor/modules')
import time as t

from naoController import NaoController


nc = NaoController()
print('Left arm temperature in degrees')
print('')
print("Shoulder pitch\t Shoulder roll\t Elboy yaw\t elbow roll\t wrist yaw")
print('______________\t _____________\t _________\t __________\t _________')
while True:
    t.sleep(1.5)
    shoulder_p = nc.getSensorValue('Device/SubDeviceList/LShoulderPitch/Temperature/Sensor/Value')
    shoulder_r = nc.getSensorValue('Device/SubDeviceList/LShoulderRoll/Temperature/Sensor/Value')
    elbow_y = nc.getSensorValue('Device/SubDeviceList/LElbowYaw/Temperature/Sensor/Value')
    elbow_r = nc.getSensorValue('Device/SubDeviceList/LElbowRoll/Temperature/Sensor/Value')
    wrist_y = nc.getSensorValue('Device/SubDeviceList/LWristYaw/Temperature/Sensor/Value')

    message = ('\b'*200+ str(shoulder_p) + '\t\t ' + str(shoulder_r) + '\t\t ' + str(elbow_y) + '\t\t ' + str(elbow_r) + '\t\t ' + str(wrist_y))

    print message,