from datetime import datetime, timedelta


# 因为谷露每次筛选限制为1W个，所以通过将时间段按每天分割
def split_date_range(start_date: str, end_date: str):
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")
    date_ranges = []

    while start_date < end_date:
        next_date = start_date + timedelta(days=1)
        date_ranges.append({
            "startTime": start_date.strftime("%Y-%m-%d"),
            "endTime": next_date.strftime("%Y-%m-%d")
        })
        start_date = next_date

    return date_ranges

