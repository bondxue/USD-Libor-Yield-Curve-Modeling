'''
Purpose: this program contains USD yield curve class
Update:
Author: Mengheng
Date: 03/26/2019
'''

from dateutil.relativedelta import relativedelta
from USDYieldCurveDate import USDYieldCurveDate
import math
import logging


class USDYieldCurve(USDYieldCurveDate):
    # arguments: depo_rates, futures_prices, holiday_calendar, trade_date
    def __init__(self, *args):
        if len(args) != 4:
            logging.error('Cannot build curve from given inputs.')
            exit()
        else:
            self._deposit_rates = []
            self._future_price_rates = []
            self._holiday_list = []
            super(USDYieldCurve, self).__init__(args[2], args[3]) # args: holiday_calendar, trade_date
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
            for row in fp:
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
            for row in fp:
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
        df_mature_dates = []
        for i in range(len(self.deposit_rates)):
            df = 1 / (1 + self.deposit_rates[i][1] * ((self.deposit_rates[i][0] - self.spot_date).days) / 36000)
            df_mature_dates.append((self.deposit_rates[i][0], df))
        return df_mature_dates

    # get discount factor for future expiry dates
    def df_future_expiry(self):
        df_future_expiry = []
        date_depo_max = self.deposit_rates[-1][0]
        for i in range(len(self.future_prices_rates)):
            date = self.future_prices_rates[i][0]
            # TODO: NEED TO CHANGE THE IF CONDITION
            if date < date_depo_max:  #
                for j in range(len(self.deposit_rates) - 1):
                    date1 = self.deposit_rates[j][0]
                    date2 = self.deposit_rates[j + 1][0]
                    deposit_rate_date1 = self.deposit_rates[j][1]
                    deposit_rate_date2 = self.deposit_rates[j + 1][1]
                    if date1 < date < date2:
                        df_date1 = 1 / (1 + deposit_rate_date1 * (date1 - self.spot_date).days / 36000)
                        df_date2 = 1 / (1 + deposit_rate_date2 * (date2 - self.spot_date).days / 36000)
                        df = math.exp(math.log(df_date1) + (date - date1) / (date2 - date1) * (
                                math.log(df_date2) - math.log(df_date1)))
                        df_future_expiry.append((date, df))
                    break
            else:
                df = df_future_expiry[i - 1][1] / (1 + self.future_prices_rates[i - 1][2] * (
                        date - self.future_prices_rates[i - 1][0]).days / 360)
                df_future_expiry.append((date, df))
        return df_future_expiry

    # function to obtain df-to-date list
    def get_dfs_dates(self):
        df_mature_dates = self.df_mature_dates()
        df_future_expiry = self.df_future_expiry()
        df_dates = sorted(df_mature_dates + df_future_expiry, key=lambda tup: tup[0])
        return df_dates

    # function to get the discount factor
    def get_df_date(self, date):
        dfs_dates = self.get_dfs_dates()
        date_max = dfs_dates[-1][0]  # last date discount factor curve defined
        if date < self.spot_date or date > date_max:
            logging.error(
                'Input date should be larger than {spot} and less than {last}'.format(spot=str(self.spot_date),
                                                                                      last=str(date_max)))
        else:

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

    # function to obtain forward rate
    def get_fwd_rate(self, date1, date2):
        if date1 > date2:
            logging.error('date2 should larger than date1.')
        else:
            df_date1 = self.get_df_date(date1)
            df_date2 = self.get_df_date(date1)
            fwd_rate = 360 * (df_date1 / df_date2 - 1) / (date2 - date1).days
            return fwd_rate
