'''
Purpose: This program contains USD yield curve date class
Update:
Author: Mengheng
Date: 03/29/2019
'''

import datetime
import logging


class USDYieldCurveDate(object):
    def __init__(self, *args):  # args: holiday_calendar, trade_date
        self._holiday_list = []
        self._trade_date = None
        self.read_trade_date(args[0])
        self._spot_date = self.calculate_spot_date(self.trade_date)
        self.read_holiday_calendar(args[1])

    @property
    def trade_date(self):
        return self._trade_date

    @property
    def spot_date(self):
        return self._spot_date

    @property
    def holiday_list(self):
        return self._holiday_list

    # function to read trade date
    def read_trade_date(self, trade_date):
        with open(trade_date, 'r') as fp:
            for row in fp:
                ymd = row.strip().split('-')
                self._trade_date = datetime.date(int(ymd[0]), int(ymd[1]), int(ymd[2]))

    # function to read holidayCalendar file
    def read_holiday_calendar(self, holiday_calendar):
        with open(holiday_calendar, 'r') as fp:
            for row in fp:
                ymd = row.strip().split('-')
                date_item = datetime.date(int(ymd[0]), int(ymd[1]), int(ymd[2]))
                self._holiday_list.append(date_item)

    # function to determine date is weekend
    @staticmethod
    def is_weekend(date):
        dow = date.weekday()
        return dow >= 5  # 5,6 is Saturday, Sunday

    # function to determine date is holiday
    def is_holiday(self, date):
        return self.is_weekend(date) or date in self._holiday_list

    # function to obtain the next business day
    def following(self, date):
        date += datetime.timedelta(days=1)
        while self.is_holiday(date):
            date += datetime.timedelta(days=1)
        return date

    # function to determine the next payment date
    def modified_following(self, date):
        payment_date = date
        while self.is_holiday(payment_date):
            payment_date += datetime.timedelta(days=1)
        if payment_date.month > date.month:
            payment_date = date
            while self.is_holiday(payment_date):
                payment_date -= datetime.timedelta(days=1)

        return payment_date

    # calculate the spot date which is two business days after the trade date
    def calculate_spot_date(self, trade_date):
        spot_date = self.following(trade_date)
        spot_date = self.following(spot_date)
        return spot_date

    @staticmethod
    def third_wednesday(year, month):
        third = datetime.date(year, month, 15)  # The 15th is the lowest third day in the month
        w = third.weekday()  # What day of the week is the 15th?
        # Wednesday is weekday 2
        if w != 2:
            # Replace just the day (of month)
            third = third.replace(day=(15 + (2 - w) % 7))
        return third
