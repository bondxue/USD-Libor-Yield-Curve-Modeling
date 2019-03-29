'''
Purpose: This program is test libor yield curve functionality
Update:
Author: Mengheng
Date: 03/29/2019
'''

from USDYieldCurve import USDYieldCurve
from USDYieldCurveDate import USDYieldCurveDate


def main():
    # usd_curve_date = USDYieldCurveDate('tradeDate.txt', 'holidayCalendar.txt')
    # print(usd_curve_date.holiday_list)
    # print(usd_curve_date.trade_date)

    usd_curve = USDYieldCurve('depoRates.txt', 'futuresPrices.txt', 'tradeDate.txt', 'holidayCalendar.txt')
    # print(usd_curve.df_future_expiry())
    # print(usd_curve.get_dfs_dates())
    # usd_curve.print_dfs_dates()
    # print('\n')
    # print(usd_curve.deposit_rates)
    # print(usd_curve.getDfToDate("2015-12-1"))
    print(usd_curve.getDfToDate("2018-2-1"))
    # print(usd_curve.getFwdRate("2016-12-1", "2016-2-1"))
    #
    # # test error case that given input is incomplete for bulid curve
    # usd_curve2 = USDYieldCurve('depoRates.txt', 'futuresPrices.txt', 'holidayCalendar.txt')


if __name__ == '__main__':
    main()
