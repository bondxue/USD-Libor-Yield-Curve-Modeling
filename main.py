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
    # usd_curve = USDYieldCurve('depoRates.txt', 'futuresPrices.txt', 'holidayCalendar.txt', trade_date)
    # # print(usd_curve.holiday_list)
    # # print(usd_curve.trade_date)
    # # print(usd_curve.spot_date)
    # # print(usd_curve.deposit_rates)
    # # print(usd_curve.future_prices_rates)
    # # # print(usd_curve.holiday_list)
    # # print(usd_curve.df_mature_dates())
    # # print(usd_curve.df_future_expiry())
    # for i in range(len(usd_curve.get_dfs_dates())):
    #     print(usd_curve.get_dfs_dates()[i])
    #
    # print('\n')
    # date1 = datetime.date(2015, 5, 26)
    # date2 = datetime.date(2015, 6, 17)
    # date3 = datetime.date(2015, 9, 15)
    # print(usd_curve.get_df_date(date1))
    # print(usd_curve.get_df_date(date2))
    # print(usd_curve.get_df_date(date3))

    usd_curve2 = USDYieldCurve('depoRates.txt', 1, 2 , trade_date)
    # print(usd_curve2.future_prices_rates)


if __name__ == '__main__':
    main()
