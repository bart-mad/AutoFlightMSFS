import matplotlib.pyplot as plt

from SimConnect import SimConnect
from SimConnect import AircraftRequests
from time import sleep
from controls.PID import PID

import streamlit as st

# Flag if should run in live-sim mode
IS_LIVE_SIM = True

# Create SimConnect link
if IS_LIVE_SIM:
    sim = SimConnect()
    # Create a Aircraft request object
    aq = AircraftRequests(sim, _time = 2000)

# Initialize the IAS PID controller
IAS_PID = PID(1,2.,0,0.01,0,100)
ALT_PID = PID(0.0001,0.001,0,0.01,-0.1,0.1)

SPEED_SP = 120
ALTITUDE_SP = 1000

S_E = []
S_C = []
T_S = []
ALT = []
ALT_ERR = []
Y_SP = []


fig, axs = plt.subplots(6,sharex = True)
fig.suptitle('Flight Control Panel')
axs[0].set_ylabel('Throttle Set-point [%]')
axs[1].set_ylabel('IAS [kts]')
axs[2].set_ylabel('IAS_Error [kts]')
axs[3].set_ylabel('Altitude [feet]')
#

#st.write("Hello")
empty = st.empty()
#for i in range(500):
if st.checkbox("Start_Button") == True:

    while True:       
        if IS_LIVE_SIM:
            SPEED_CP = aq.get("AIRSPEED_INDICATED")
            ALTITUDE = aq.get("INDICATED_ALTITUDE")

        SPEED_ERROR = (SPEED_SP - SPEED_CP)
        ALT_ERROR = (ALTITUDE_SP - ALTITUDE)

        THROTTLE_SP = IAS_PID.update(SPEED_ERROR)
        YOKE_SP = ALT_PID.update(ALT_ERROR)

        if IS_LIVE_SIM:
            aq.set("GENERAL_ENG_THROTTLE_LEVER_POSITION:1",THROTTLE_SP)
            aq.set("YOKE_Y_POSITION",YOKE_SP)

        S_E.append(SPEED_ERROR)
        S_C.append(SPEED_CP)
        T_S.append(THROTTLE_SP)
        ALT.append(ALTITUDE)
        ALT_ERR.append(ALT_ERROR)
        Y_SP.append(YOKE_SP)

        axs[0].plot(T_S,'tab:orange')

        axs[1].plot(S_C,'tab:green')

        axs[2].plot(S_E,'tab:blue')

        axs[3].plot(ALT,'tab:red')

        axs[4].plot(Y_SP,'tab:blue')

        axs[5].plot(ALT_ERR,'tab:orange')

        with empty.container():
            st.pyplot(fig)

        #plt.pause(0.01)

        #plt.show()


        


