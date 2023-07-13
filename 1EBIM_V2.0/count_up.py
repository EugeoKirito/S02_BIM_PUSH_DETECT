import random
import datetime
import cv2
import matplotlib.pyplot as plt

today = datetime.datetime.now().weekday() + 1

def save_pic(count, today, li):
    x = ['Mon', 'Tues', 'Wed', 'Thurs', 'Fri', 'Sat', 'Sun']
    # 绘图
    li[today - 1] = count
    plt.plot(x, li)
    # 展示
    plt.savefig("./sta.png")
    plt.close()
    return "./sta.png"


def update_count(push_count, today, li):
        save_pic(count=push_count, today=today, li=li)


