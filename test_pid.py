#!/usr/bin/python
#
# This file is part of IvPID.
# Copyright (C) 2015 Ivmech Mechatronics Ltd. <bilgi@ivmech.com>
#
# IvPID is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# IvPID is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

#title           :test_pid.py
#description     :python pid controller test
#author          :Caner Durmusoglu
#date            :20151218
#version         :0.1
#notes           :
#python_version  :2.7
#dependencies    : matplotlib, numpy, scipy
#==============================================================================

import PID
import time
import matplotlib.pyplot as plt
import numpy as np
#from scipy.interpolate import spline
from scipy.interpolate import BSpline, make_interp_spline #  Switched to BSpline

def test_pid(P = 0.2,  I = 0.0, D= 0.0, L=100):
    """Self-test PID class

    .. note::
        ...
        for i in range(1, END):
            pid.update(feedback)
            output = pid.output
            if pid.SetPoint > 0:
                feedback += (output - (1/i))
            if i>9:
                pid.SetPoint = 1
            time.sleep(0.02)
        ---
    """
    pid = PID.PID(P, I, D) # 각각의 PID.py의 PID 클래스에 각각의 PID값을 선언한 pid 인스턴스

    pid.SetPoint=0.0  # 컨트롤 하고자하는 온도 설정
    pid.setSampleTime(0.01) # 0.01 초를 샘플링 타임으로 설정. update

    END = L  # 총 몇초간 볼 것인가? 실제 제어 상황이라면 필요 없다.
    feedback = 0  #  feedback 변수 이것을 온도 센서의 값으로 치환해준다.

    feedback_list = [] # 나중에 plot을 하기위한 리스트: 피드백 받은 값을 저장한다.
    time_list = []  # 가상의 시간축을 형성하는 리스트
    setpoint_list = [] # 셋팅포인트가 달라지는 시점을 파악하기 위한 리스트

    for i in range(1, END): # 끝나는 시점까지 루프를 돌린다. 향 후에는 조건버튼을 넣는다.
        pid.update(feedback) # feedback 인자를 pid 인스턴스에 업데이트한다.
        output = pid.output # 업데이트 된 pid의 output 변수를 가져온다. 이 변수로 히터를 제어
        if pid.SetPoint > 0: 
            feedback += (output - (1/i))
        if i>9:
            pid.SetPoint = 3
        time.sleep(0.02)

        feedback_list.append(feedback)
        setpoint_list.append(pid.SetPoint)
        time_list.append(i)

    time_sm = np.array(time_list)
    time_smooth = np.linspace(time_sm.min(), time_sm.max(), 300)

    # feedback_smooth = spline(time_list, feedback_list, time_smooth)
    # Using make_interp_spline to create BSpline
    helper_x3 = make_interp_spline(time_list, feedback_list)
    feedback_smooth = helper_x3(time_smooth)
    
    plt.plot(time_smooth, feedback_smooth)
    plt.plot(time_list, setpoint_list)
#    plt.xlim((0, L))
#    plt.ylim((min(feedback_list)-0.5, max(feedback_list)+0.5))
    plt.xlabel('time (s)')
    plt.ylabel('PID (PV)')
    plt.title('TEST PID')

#    plt.ylim((1-0.5, 1+0.5))

    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    test_pid(0.8, 0.01, 0.001, L=50)
#    test_pid(0.8, L=50)
