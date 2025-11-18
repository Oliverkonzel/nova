"""
Test the complete booking flow with Cal.com
"""
import asyncio
import sys
import os

# Fix encoding for Windows console
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.services.calendar import get_available_slots, book_appointment

async def test_complete_booking_flow():
    """Test the complete booking flow"""
    print("\n" + "="*60)
    print("TESTING COMPLETE BOOKING FLOW")
    print("="*60)

    try:
        # Step 1: Get available slots
        print("\n1. Fetching available slots...")
        slots = await get_available_slots(days_ahead=7)

        if not slots:
            print("❌ No slots available!")
            return False

        print(f"✅ Found {len(slots)} slots")
        print(f"\nUsing slot: {slots[0]['date']} at {slots[0]['time']}")

        # Step 2: Book an appointment
        print("\n2. Booking test appointment...")
        result = await book_appointment(
            name="Test Booking Flow",
            email="testflow@example.com",
            phone="+15559876543",
            datetime_slot=slots[0]['datetime']
        )

        if result.get("success"):
            print("✅ SUCCESS: Appointment booked!")
            print(f"   Booking ID: {result.get('booking_id')}")
            print(f"   Start Time: {result.get('start_time')}")
            if result.get('booking_url'):
                print(f"   URL: {result.get('booking_url')}")
            return True
        else:
            print(f"❌ FAILED: {result.get('error')}")
            return False

    except Exception as e:
        print(f"❌ FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    success = await test_complete_booking_flow()

    print("\n" + "="*60)
    if success:
        print("🎉 COMPLETE BOOKING FLOW WORKING!")
    else:
        print("⚠️  BOOKING FLOW FAILED")
    print("="*60 + "\n")

    return 0 if success else 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
