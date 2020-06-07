#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  4 15:38:47 2020

@author: root
"""

import random,time
from itertools import count
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

#plt.style.use('fivethirtyeight')

x_values = []
y_values = []
z_values = []

index = count()


def animate(i):
    time.sleep(2)
    x_values.append(next(index))
    y_values.append(random.randint(0, 5))
    z_values.append(random.randint(0, 5))
    plt.cla()
    plt.plot(x_values, y_values,'r*-',x_values, z_values,'b*-')


ani = FuncAnimation(plt.gcf(), animate, 100)


plt.tight_layout()
plt.show()