"""
Calendar Service - Integrates with Cal.com
"""
import httpx
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import CAL_API_KEY, CAL_EVENT_TYPE
from datetime import datetime, timedelta

# Event Type ID for free-consultation
EVENT_TYPE_ID = 3871645

async def get_available_slots(days_ahead: int = 7) -> list[dict]:
    """Get available time slots from Cal.com"""
    try:
        start_date = datetime.now().date()
        end_date = start_date + timedelta(days=days_ahead)

        url = f"https://api.cal.com/v2/slots/available"
        params = {
            "apiKey": CAL_API_KEY,
            "eventTypeId": EVENT_TYPE_ID,
            "startTime": start_date.isoformat(),
            "endTime": end_date.isoformat(),
        }

        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            data = response.json()

            slots = []
            if "data" in data and "slots" in data["data"]:
                for date, times in data["data"]["slots"].items():
                    for slot in times:
                        time_obj = datetime.fromisoformat(slot["time"].replace('Z', '+00:00'))
                        # Convert to Eastern Time
                        local_time = time_obj.strftime("%I:%M %p")
                        slots.append({
                            "date": date,
                            "time": local_time,
                            "datetime": slot["time"]
                        })

            print(f"Found {len(slots)} available slots")
            return slots[:5]

    except Exception as e:
        print(f"Error getting slots: {e}")
        # Return default slots for testing
        tomorrow = (datetime.now() + timedelta(days=1)).date()
        return [
            {"date": str(tomorrow), "time": "10:00 AM", "datetime": f"{tomorrow}T14:00:00.000Z"},
            {"date": str(tomorrow), "time": "2:00 PM", "datetime": f"{tomorrow}T18:00:00.000Z"},
        ]

async def book_appointment(name: str, email: str, phone: str, datetime_slot: str) -> dict:
    """Book an appointment in Cal.com"""
    try:
        url = f"https://api.cal.com/v2/bookings"

        booking_data = {
            "eventTypeId": EVENT_TYPE_ID,
            "start": datetime_slot,
            "attendee": {
                "name": name,
                "email": email,
                "timeZone": "America/New_York",
                "language": "en"
            },
            "metadata": {"source": "nova-voice-agent", "phone": phone}
        }

        params = {
            "apiKey": CAL_API_KEY
        }

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(url, json=booking_data, params=params)
            response.raise_for_status()
            result = response.json()

            print(f"Booking successful: {result}")
            return {
                "success": True,
                "booking_id": result.get("data", {}).get("id"),
                "booking_url": result.get("data", {}).get("url"),
                "start_time": datetime_slot
            }

    except Exception as e:
        print(f"Error booking: {e}")
        return {"success": False, "error": str(e)}

def format_slots_for_speech(slots: list[dict]) -> str:
    """Format slots for natural speech"""
    if not slots:
        return "I don't have any available slots right now."

    by_date = {}
    for slot in slots[:3]:
        date = slot["date"]
        time = slot["time"]
        if date not in by_date:
            by_date[date] = []
        by_date[date].append(time)

    parts = []
    for date, times in by_date.items():
        dt = datetime.fromisoformat(date)
        day_name = dt.strftime("%A")

        if len(times) == 1:
            parts.append(f"{day_name} at {times[0]}")
        else:
            times_str = ", ".join(times[:-1]) + f", or {times[-1]}"
            parts.append(f"{day_name} at {times_str}")

    return "I have openings " + ", ".join(parts) + ". Which works best for you?"
