#!/usr/bin/env python3
"""
Test script for Pushover notifications.
Sends a test notification to verify the integration is working.
"""

import requests

# =================== PUSHOVER CONFIGURATION ===================
PUSHOVER_USER_KEY = "u7vw3t8hofn7381eej4ppb2waq8jao"
PUSHOVER_API_TOKEN = "apdqrsvcckxwa9woaqycbu5vjh21sj"

def send_test_notification():
    """Send a test notification to verify Pushover is working."""

    print("Sending test notification to Pushover...")
    print("-" * 50)

    message = "This is a TEST notification from your flight scraper!\n\nIf you see this, Pushover is working correctly."

    # Test with pushover sound
    tests = [
        {
            'name': 'CRITICAL ALERT - som persistent',
            'data': {
                'user': PUSHOVER_USER_KEY,
                'token': PUSHOVER_API_TOKEN,
                'message': message + "\n\n📱 Som: PERSISTENT\n\nPriority 2 + persistent sound + retry 30s + expire 600s",
                'title': "🚨 FLIGHT ALERT: TESTE",
                'priority': 2,
                'retry': 30,
                'expire': 600,
                'sound': 'persistent'
            }
        }
    ]

    for i, test in enumerate(tests, 1):
        print(f"\nTest {i}: {test['name']}")
        print(f"Priority: {test['data']['priority']}")

        try:
            response = requests.post(
                'https://api.pushover.net/1/messages.json',
                data=test['data'],
                timeout=10
            )

            if response.status_code == 200:
                result = response.json()
                print(f"✅ SUCCESS!")
                print(f"   Status: {result.get('status', 'N/A')}")
                print(f"   Request: {result.get('request', 'N/A')}")
            else:
                print(f"❌ FAILED!")
                print(f"   Status Code: {response.status_code}")
                print(f"   Error: {response.text}")
        except Exception as e:
            print(f"❌ EXCEPTION: {str(e)}")

    print("\n" + "=" * 50)
    print("Test complete!")
    print("\nNOTE: If your phone is in Sleep/Do Not Disturb mode,")
    print("notifications may still not sound even with Emergency priority.")
    print("Check Pushover app settings to ensure sounds are enabled.")

if __name__ == "__main__":
    send_test_notification()
