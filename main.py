from time import sleep
import smtplib
from email.message import EmailMessage
import re
import os
import json
import requests
from datetime import datetime
from classes.Scraper import FlightScraper

# =================== EMAIL CONFIGURATION ===================
# Configure your email settings here
EMAIL_ENABLED = False  # Set to True to enable email notifications
EMAIL_FROM = os.getenv("EMAIL_FROM", "your_email@gmail.com")  # Your email address
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "your_app_password")  # Your email password or app-specific password
EMAIL_TO = os.getenv("EMAIL_TO", "your_email@gmail.com")  # Where to send alerts (can be same as FROM)
EMAIL_SMTP = "smtp.gmail.com"  # SMTP server (for Gmail)
EMAIL_PORT = 587  # SMTP port

# =================== PUSHOVER CONFIGURATION ===================
# Pushover notifications (emergency mode - will wake you up!)
PUSHOVER_ENABLED = False  # Set to True to enable pushover notifications
PUSHOVER_USER_KEY = os.getenv("PUSHOVER_USER_KEY", "your_user_key")  # Your user key
PUSHOVER_API_TOKEN = os.getenv("PUSHOVER_API_TOKEN", "your_api_token")  # Your API token
PUSHOVER_PRIORITY = 2  # Emergency - Critical Alert toca em modo Sono (iOS: 1x, Android: repete)
PUSHOVER_RETRY = 30
PUSHOVER_EXPIRE = 600

# Points threshold for alert
POINTS_THRESHOLD = 300000  # Alert when points are below this value

# Database file
DB_FILE = "best_points.json"

def load_database():
    """
    Load the database from JSON file.
    Returns empty dict if file doesn't exist.
    """
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Warning: Could not load database: {e}")
            return {}
    return {}

def save_database(db):
    """
    Save the database to JSON file.
    """
    try:
        with open(DB_FILE, 'w') as f:
            json.dump(db, f, indent=2)
    except Exception as e:
        print(f"Warning: Could not save database: {e}")

def update_and_check_best_points(db, origin: str, date: str, points: str):
    """
    Update database with new points value if it's lower than current best.
    Always saves the lowest value found (even above threshold).
    Only sends alert if below threshold.
    Returns True if should send alert (below threshold and new lower value).
    """
    points_value = parse_points(points)

    # Skip if no points
    if points_value == 0:
        return False

    # Check if should send alert (below threshold)
    should_alert = points_value < POINTS_THRESHOLD

    # Create unique key for origin + date
    key = f"{origin}-{date}"

    # Check if we have a previous best for this origin+date
    if key in db:
        previous_best = db[key]['points_value']
        previous_points = db[key]['points']

        # Only update database if new value is lower
        if points_value < previous_best:
            print(f"📉 New lower value for {origin}-{date}: {previous_points} → {points}")
            db[key] = {
                'points': points,
                'points_value': points_value,
                'last_updated': datetime.now().isoformat()
            }
            # Only alert if below threshold
            return should_alert
        else:
            print(f"ℹ️  {origin}-{date}: Current best is {previous_points} (found {points})")
            return False
    else:
        # First time seeing this origin+date
        print(f"✨ New entry for {origin}-{date}: {points}")
        db[key] = {
            'points': points,
            'points_value': points_value,
            'last_updated': datetime.now().isoformat()
        }
        # Only alert if below threshold
        return should_alert


def send_email_alert(origin: str, date: str, points: str):
    """
    Send email alert when points are below threshold.
    """
    if not EMAIL_ENABLED:
        return False

    try:
        msg = EmailMessage()
        msg['Subject'] = f"🚨 Low Points Alert: {origin}-{date}"
        msg['From'] = EMAIL_FROM
        msg['To'] = EMAIL_TO

        body = f"""
ALERT: Low points value found!

Origin: {origin}
Date: {date}
Points: {points}
Threshold: {POINTS_THRESHOLD:,}

Check the Azul website for booking.
"""
        msg.set_content(body)

        with smtplib.SMTP(EMAIL_SMTP, EMAIL_PORT) as server:
            server.starttls()
            server.login(EMAIL_FROM, EMAIL_PASSWORD)
            server.send_message(msg)

        print(f"📧 Email alert sent for {origin}-{date} (points: {points})")
        return True

    except Exception as e:
        print(f"------------- Failed to send email: {str(e)}")
        return False

def send_pushover_alert(origin: str, date: str, points: str):
    """
    Send Pushover alert with EMERGENCY priority (keeps sounding for 30 seconds).
    """
    if not PUSHOVER_ENABLED:
        return False

    try:
        message = f"New lower value found!\n\nOrigin: {origin}\nDate: {date}\nPoints: {points}\nThreshold: {POINTS_THRESHOLD:,}"

        data = {
            'user': PUSHOVER_USER_KEY,
            'token': PUSHOVER_API_TOKEN,
            'message': message,
            'title': f"🚨 FLIGHT ALERT: {origin}-{date}",
            'priority': PUSHOVER_PRIORITY,
            'retry': PUSHOVER_RETRY,
            'expire': PUSHOVER_EXPIRE,
            'sound': 'persistent'
        }

        response = requests.post(
            'https://api.pushover.net/1/messages.json',
            data=data,
            timeout=10
        )

        if response.status_code == 200:
            print(f"📱 Pushover alert sent for {origin}-{date} (points: {points})")
            return True
        else:
            print(f"------------- Pushover error: {response.text}")
            return False

    except Exception as e:
        print(f"------------- Failed to send Pushover: {str(e)}")
        return False

def send_alerts(origin: str, date: str, points: str):
    """
    Send both email and Pushover alerts.
    Script continues even if one fails.
    """
    print(f"\n🚨 SENDING ALERTS for {origin}-{date} (points: {points})")

    # Try to send email
    email_sent = send_email_alert(origin, date, points)

    # Try to send Pushover
    pushover_sent = send_pushover_alert(origin, date, points)

    # Report results
    if email_sent and pushover_sent:
        print("✅ Both email and Pushover sent successfully!")
    elif email_sent:
        print("⚠️  Only email sent (Pushover failed)")
    elif pushover_sent:
        print("⚠️  Only Pushover sent (Email failed)")
    else:
        print("❌ Both email and Pushover failed!")

    return email_sent or pushover_sent  # Return True if at least one succeeded

def parse_points(points_text: str) -> int:
    """
    Parse points value from text like "348.000" to integer 348000.
    """
    if not points_text:
        return 0
    # Remove dots and convert to integer
    return int(points_text.replace('.', '').replace(',', '').strip())


if __name__ == "__main__":
    # Dates to check: April 26, 27, 28, 29, 30 and May 1, 2 of 2026
    dates = [
        '2026-04-26',
        '2026-04-27',
        '2026-04-28',
        '2026-04-29',
        '2026-04-30',
        '2026-05-01',
        '2026-05-02'
    ]

    # Origins to check
    origins = ['GRU', 'VCP']

    # Base URL template (origin and date will be inserted)
    url_template = 'https://azulpelomundo.voeazul.com.br/flights/OW/{origin}/PUJ/-/-/{date}/-/2/0/0/0/0/ALL/F/BUSINESS/-/-/-/-/A/-'

    # Load database
    print("Loading database...")
    db = load_database()
    if db:
        print(f"Loaded {len(db)} dates from database")
        print("Current best values:")
        for date, data in db.items():
            print(f"  {date}: {data['points']}")
    else:
        print("No existing database found. Starting fresh.")

    iteration = 0
    scraper = None

    try:
        while True:
            iteration += 1
            print(f"\n{'='*50}")
            print(f"ITERATION {iteration}")
            print(f"{'='*50}\n")

            try:
                # Initialize scraper for each iteration
                if scraper is None:
                    scraper = FlightScraper()

                results = {}

                for origin in origins:
                    for date in dates:
                        url = url_template.format(origin=origin, date=date)
                        points_value = scraper.scrape_azul(url, date)
                        key = f"{origin}-{date}"
                        results[key] = {'origin': origin, 'date': date, 'points': points_value}
                        sleep(1)  # Pause between requests to avoid overloading Chrome

                # Print all results and check for new lower values
                print("\n===== RESULTS =====")
                alerts_sent = []

                for key, data in results.items():
                    origin = data['origin']
                    date = data['date']
                    points = data['points']
                    print(f"{key}: {points}")

                    # Check if this is a new lower value
                    if points and update_and_check_best_points(db, origin, date, points):
                        alerts_sent.append((origin, date, points))

                # Save database after each iteration
                save_database(db)

                # Send alerts for new lower values (both email and Pushover)
                if alerts_sent:
                    print(f"\n📧 Sending {len(alerts_sent)} alert(s) (email + Pushover)...")
                    for origin, date, points in alerts_sent:
                        send_alerts(origin, date, points)
                else:
                    print("\n✅ No new lower values found. No alerts sent.")

                print("\nFlight search completed.")

            except Exception as e:
                print('------------- An error occurred:', str(e))
                # Close scraper on error to force re-initialization
                if scraper:
                    scraper.close()
                    scraper = None

            # Wait 10 minutes before next iteration
            print("\nWaiting 10 minutes before next search...")
            sleep(600)

    except KeyboardInterrupt:
        print("\n\nScript stopped by user.")
    finally:
        # Clean up
        if scraper:
            scraper.close()
            print("Scraper closed.")