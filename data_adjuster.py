import pandas as pd
import sys
import datetime


def main():
    if len(sys.argv) != 4:
        sys.exit("Usage: python3 data_adjuster.py keyword start_date end_date")

    keyword = sys.argv[1]

    if sys.argv[2] == "start":
        start_date = "2004-01-01"
    else:
        start_date = sys.argv[2]

    if sys.argv[3] == "today":
        end_date = str(datetime.date.today())
    else:
        end_date = sys.argv[3]

    try:
        monthly = pd.read_csv(
            f"data/{keyword}/{start_date}_{end_date}/unadjusted/monthly_{keyword}.csv")
    except:
        sys.exit(
            f"First run data_collector.py. (python3 data_collector.py {sys.argv[1]} {sys.argv[2]} {sys.argv[3]}")

    print(monthly.name())


def adjust_weekly():
    return


def adjust_daily():
    return


if __name__ == "__main__":
    main()
