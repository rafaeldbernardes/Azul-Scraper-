from utils.build_url import build_url
from datetime import datetime, timedelta

def get_flight_search_inputs(url_base: str):
    urls = []
    departure_dates = ["16/09/2025", "17/09/2025"]
    return_dates = []

    for departure_date in departure_dates:
        # Generate future return dates (13–15 days after the current departure date)
        base_return_date = datetime.strptime(departure_date, "%d/%m/%Y")
        future_return_dates = [
            (base_return_date + timedelta(days=i)).strftime("%d/%m/%Y")
            for i in range(13, 16)
        ]
        return_dates.extend(future_return_dates)

        # Build URLs for each combination of the current departure date and return dates
        for future_return_date in future_return_dates:
            url = build_url(url_base, departure_date, future_return_date, "GRU", "MAD")
            urls.append(url)  # Append the generated URL to the list

    # Print the URLs and dates for debugging or confirmation
    print("Generated URLs:", urls)
    print("Departure Dates:", departure_dates)
    print("Return Dates:", return_dates)

    return urls, departure_dates, return_dates, "GRU", "MAD"