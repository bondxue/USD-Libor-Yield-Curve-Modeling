'''
Purpose: this program contains USD yield curve class
Update:  03/29/2019 Add print dfs_dates function
Author: Mengheng
Date: 03/29/2019
'''

from dateutil.relativedelta import relativedelta
from USDYieldCurveDate import USDYieldCurveDate
import datetime
import math
import logging


class USDYieldCurve(USDYieldCurveDate):
    # arguments: depo_rates, futures_prices, trade_date, holiday_calendar
    def __init__(self, *args):
        if len(args) != 4:
            logging.error('Cannot build curve from given inputs.')
            return
        else:
            self._deposit_rates = []
            self._future_price_rates = []
            self._trade_date = None
            self._holiday_list = []
            super(USDYieldCurve, self).__init__(args[2], args[3])  # args: trade_date, holiday_calendar
            self.read_depo_rates(args[0])
            self.read_futures_prices(args[1])

    @property
    def deposit_rates(self):
        return self._deposit_rates

    @property
    def future_prices_rates(self):
        return self._future_price_rates

    # function to read depoRate file
    def read_depo_rates(self, depo_rates):
        with open(depo_rates, 'r') as fp:
            rows = (line.rstrip() for line in fp)  # All lines including the blank ones
            rows = (line for line in rows if line)  # Non-blank lines
            for row in rows:
                item = row.strip().split('\t')
                if item[0][-1] == 'D':
                    date_to_mature = relativedelta(days=int(item[0][-2]))
                elif item[0][-1] == 'W':
                    date_to_mature = relativedelta(weeks=int(item[0][-2]))
                else:
                    date_to_mature = relativedelta(months=int(item[0][-2]))
                mature_date = self.modified_following(self._spot_date + date_to_mature)
                self._deposit_rates.append((mature_date, float(item[1])))

    # function to read futurePrice file
    def read_futures_prices(self, futures_prices):
        with open(futures_prices, 'r') as fp:
            rows = (line.rstrip() for line in fp)  # All lines including the blank ones
            rows = (line for line in rows if line)  # Non-blank lines
            for row in rows:
                item = row.strip().split('\t')
                year = 2010 + int(item[0][-1])
                if item[0][-2] == 'H':
                    month = 3
                elif item[0][-2] == 'M':
                    month = 6
                elif item[0][-2] == 'U':
                    month = 9
                else:
                    month = 12
                date = self.third_wednesday(year, month)
                price = float(item[1])
                rate = (100 - price) / 100.0
                self._future_price_rates.append((date, price, rate))

    # get discount factors for deposit mature dates
    def df_mature_dates(self):
        df_mature_dates = [(self.spot_date, 1.0)]
        for i in range(len(self.deposit_rates)):
            df = 1 / (1 + self.deposit_rates[i][1] * (self.deposit_rates[i][0] - self.spot_date).days / 36000.0)
            df_mature_dates.append((self.deposit_rates[i][0], df))
        return df_mature_dates

    # get discount factor for future expiry dates
    def df_future_expiry(self):
        df_future_expiry = []
        date_depo_max = self.deposit_rates[-1][0]
        date_depo_min = self.deposit_rates[0][0]
        date_first_future = self.future_prices_rates[0][0]
        if date_first_future <= date_depo_min or date_first_future >= date_depo_max:
            logging.error("Insufficient LIBOR cash rate data.")
            return None
        for i in range(len(self.future_prices_rates)):
            date = self.future_prices_rates[i][0]
            if not df_future_expiry:  # df_future_expiry is empty
                for j in range(len(self.deposit_rates) - 1):
                    date1 = self.deposit_rates[j][0]
                    date2 = self.deposit_rates[j + 1][0]
                    deposit_rate_date1 = self.deposit_rates[j][1]
                    deposit_rate_date2 = self.deposit_rates[j + 1][1]
                    if date1 < date < date2:
                        df_date1 = 1 / (1 + deposit_rate_date1 * (date1 - self.spot_date).days / 36000.0)
                        df_date2 = 1 / (1 + deposit_rate_date2 * (date2 - self.spot_date).days / 36000.0)
                        df = math.exp(math.log(df_date1) + (date - date1) / (date2 - date1) * (
                                math.log(df_date2) - math.log(df_date1)))
                        df_future_expiry.append((date, df))
                        break
            else:
                df = df_future_expiry[i - 1][1] / (1 + self.future_prices_rates[i - 1][2] * (
                        date - self.future_prices_rates[i - 1][0]).days / 360.0)
                df_future_expiry.append((date, df))
        return df_future_expiry

    # function to obtain df-to-date list
    def get_dfs_dates(self):
        df_mature_dates = self.df_mature_dates()
        df_future_expiry = self.df_future_expiry()
        if df_future_expiry is None:
            return None
        else:
            df_dates = sorted(df_mature_dates + df_future_expiry, key=lambda tup: tup[0])
            return df_dates

    # print dfs_dates
    def print_dfs_dates(self):
        dfs_dates = self.get_dfs_dates()
        if dfs_dates is None:
            return None
        else:
            for i in range(len(dfs_dates)):
                print(dfs_dates[i][0], self.round_up(dfs_dates[i][1]))

    # function to get the discount factor to one date
    def get_df_date(self, date):
        dfs_dates = self.get_dfs_dates()
        if dfs_dates is None:
            return None
        else:
            date_max = dfs_dates[-1][0]  # last date discount factor curve defined
            date_min = dfs_dates[0][0] # first date discount factor curve defined
            if date < date_min or date > date_max:
                logging.error(
                    'Input date should be between {first} and {last}.'.format(first=str(date_min),
                                                                                          last=str(date_max)))
            else:
                if self.is_holiday(date):
                    logging.warning('{date} is a holiday'.format(date=date))
                for i in range(len(dfs_dates) - 1):
                    date1 = dfs_dates[i][0]
                    date2 = dfs_dates[i + 1][0]
                    df_date1 = dfs_dates[i][1]
                    df_date2 = dfs_dates[i + 1][1]
                    if date == date1:  # date equals to the current df date
                        df_date = df_date1
                        return df_date
                    elif date1 < date < date2:  # less than the next df to date
                        df_date = math.exp(math.log(df_date1) + (date - date1) / (date2 - date1) * (
                                math.log(df_date2) - math.log(df_date1)))
                        return df_date
                    elif date == date2:
                        df_date = df_date2  # date equals to the next df date
                        return df_date

    # funciton for get the discount factor with str input
    def getDfToDate(self, date_str):
        ymd = date_str.strip().split('-')
        date = datetime.date(int(ymd[0]), int(ymd[1]), int(ymd[2]))
        df_date = self.get_df_date(date)
        if df_date is None:
            return None
        else:
            return self.round_up(df_date)

    # function to obtain forward rate
    def get_fwd_rate(self, date1, date2):
        if date1 > date2:
            logging.error('First parameter date should be larger than the second one.')
        else:
            if self.is_holiday(date1) or self.is_holiday(date2):
                logging.warning('Input dates include holidays.')
            df_date1 = self.get_df_date(date1)
            df_date2 = self.get_df_date(date2)
            if df_date1 is None or df_date2 is None:
                return None
            else:
                fwd_rate = 360.0 / (date2 - date1).days * (df_date1 / df_date2 - 1.0)
                return fwd_rate

    # function to obtain forward rate with str inputs
    def getFwdRate(self, date1_str, date2_str):
        ymd1 = date1_str.strip().split('-')
        ymd2 = date2_str.strip().split('-')
        date1 = datetime.date(int(ymd1[0]), int(ymd1[1]), int(ymd1[2]))
        date2 = datetime.date(int(ymd2[0]), int(ymd2[1]), int(ymd2[2]))
        fwd_rate = self.get_fwd_rate(date1, date2)
        if fwd_rate is None:
            return None
        else:
            return self.round_up(fwd_rate)

    # function to modify round()
    @staticmethod
    def round_up(value):
        return round(value * 1000000000) / 1000000000.0
