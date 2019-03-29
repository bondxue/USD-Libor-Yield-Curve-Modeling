'''
Purpose: This program is test libor yield curve functionality
Update:
Author: Mengheng
Date: 03/26/2019
'''
from __future__ import division
from USDYieldCurve import USDYieldCurve
from USDYieldCurveDate import USDYieldCurveDate
import datetime


def main():
    trade_date = datetime.date(2015, 4, 22)
    # usd_curve_date = USDYieldCurveDate('holidayCalendar.txt', trade_date)
    # # print(usd_curve_date.holiday_list)
    # # print(usd_curve_date.trade_date)
    # #
    # #
    # #
    # # print(usd_curve_date.is_weekend(trade_date))
    # # print(usd_curve_date.is_holiday(trade_date))
    # # print(usd_curve_date.following(trade_date))
    # # print(usd_curve_date.calculate_spot_date(trade_date))
    # # print(usd_curve_date.spot_date)
    #
    usd_curve = USDYieldCurve('depoRates.txt', 'futuresPrices.txt', 'holidayCalendar.txt', trade_date)
    # # print(usd_curve.holiday_list)
    # # print(usd_curve.trade_date)
    # # print(usd_curve.spot_date)
    # # print(usd_curve.deposit_rates)
    # # print(usd_curve.future_prices_rates)
    # # # print(usd_curve.holiday_list)
    # # print(usd_curve.df_mature_dates())
    # # print(usd_curve.df_future_expiry())
    # usd_curve.print_dfs_dates()
    #
    # print('\n')
    date1 = datetime.date(2016, 3, 20)
    date2 = datetime.date(2016, 3, 20)
    date3 = datetime.date(2017, 2, 2)
    print(usd_curve.get_df_date(date1))
    print(usd_curve.get_fwd_rate(date2, date3))
    # print(usd_curve.get_df_date(date2))
    # print(usd_curve.get_df_date(date3))
    # print(usd_curve.get_df_date(date2)/usd_curve.get_df_date(date3)-1.0)

    # usd_curve2 = USDYieldCurve('depoRates.txt', 'holidayCalendar.txt', trade_date)
    # print(usd_curve2.future_prices_rates)


if __name__ == '__main__':
    main()
