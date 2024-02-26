import runpy

import schedule
from db_requests import db
import threading
import time
# from telegram_bot import pending_orders
import datetime as dt
import runpy
# def vk():
#     import vk_bot


def tg():
    runpy.run_module('telegram_bot', {}, "__main__")


tg_thread = threading.Thread(target=tg)
# vk_thread = threading.Thread(target=vk)
tg_thread.start()
# vk_thread.start()


# # # down here is the test area

# db.del_item('Orders', 3)
# with db.db as con:
#     # pass
#     print(con.execute('SELECT * FROM Orders').fetchall())
#     print(con.execute('SELECT * FROM Order_lists').fetchall())


#print(f"{time.localtime().tm_mday}.{time.localtime().tm_mon}.{time.localtime().tm_year}")


# def daily_stat():
#     today_date = f"{time.localtime().tm_mday}.{time.localtime().tm_mon}.{time.localtime().tm_year}"
#     print(db.day_stat(today_date))
#
#
# def weekly_stat():
#     today_date = f"{time.localtime().tm_mday}.{time.localtime().tm_mon}.{time.localtime().tm_year}"
#     print(db.week_stat(today_date))



# schedule.every().day.at('08:00').do(weekly_stat)
# schedule.every().day.at('20:00').do(daily_stat)


while True:
    schedule.run_pending()
    print(str(time.localtime().tm_hour)+':'+str(time.localtime().tm_min))
    time.sleep(5)
# print(get_client(123456789))
# print(get_client(123456788))


