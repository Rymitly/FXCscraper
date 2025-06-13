from scraper_utils import *

def run(driver, wait, sending_countries, time_period):
    # Fixed country list
    receiving_countries = ['Honduras']

    # Date range
    end_date_str = pd.Timestamp.today().strftime("%d/%m/%Y")
    start_date_str = (pd.Timestamp.today() - pd.Timedelta(days=time_period)).strftime("%d/%m/%Y")
    d_list = get_dates(start_date_str, end_date_str)

    # Loop through sending countries
    for send_country in sending_countries:
        print(f"Sending from: {send_country}")
        for attempt in range(3):
            try:
                set_sending_country(driver, wait, send_country)
                ensure_sending_country(driver, wait, send_country)
                break
            except Exception as e:
                print(f" Retry setting sending country: {e}")
        else:
            print(f"Skipping send country: {send_country}")
            continue  # skip to next sender

        # Now run report logic for this sender
        for d in d_list:
            set_report_date(driver, wait, d)
            for c in receiving_countries:
                for attempt in range(4):
                    try:
                        select_receiving_country(driver,wait, c)
                        ensure_receiving_country(driver, wait, c)
                        break
                    except Exception as e:
                        print(f"Retry receiving country: {e}")
                else:
                    print(f"Failed to set receiving country: {c}")
                    continue

                select_all_options_in_dropdown(driver, wait, "Pay In")
                select_all_options_in_dropdown(driver, wait, "Pay Out")
                select_all_provider_checkboxes(driver)
                click_download_report(driver, wait)
                time.sleep(2)
