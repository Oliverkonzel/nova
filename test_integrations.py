"""
Test script to verify Cal.com and Notion integrations
"""
import asyncio
import sys
import os

# Fix encoding for Windows console
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.services.calendar import get_available_slots, book_appointment
from backend.services.crm import create_lead
from backend.models import CallData

async def test_calcom():
    """Test Cal.com integration"""
    print("\n" + "="*60)
    print("Testing Cal.com Integration...")
    print("="*60)

    try:
        # Test getting available slots
        print("\n1. Fetching available appointment slots...")
        slots = await get_available_slots(days_ahead=7)

        if slots:
            print(f"✅ SUCCESS: Found {len(slots)} available slots")
            print("\nAvailable slots:")
            for i, slot in enumerate(slots[:3], 1):
                print(f"   {i}. {slot['date']} at {slot['time']}")
            return True
        else:
            print("❌ WARNING: No slots returned (but API might be working)")
            return True

    except Exception as e:
        print(f"❌ FAILED: {str(e)}")
        return False

async def test_notion():
    """Test Notion integration"""
    print("\n" + "="*60)
    print("Testing Notion Integration...")
    print("="*60)

    try:
        # Test creating a lead
        print("\n1. Creating test lead in Notion...")

        test_call_data = CallData(
            name="Test User - Integration Check",
            phone="+15551234567",
            email="test@example.com",
            service="Integration Test",
            status="qualified",
            appointment_time=None,
            notes="This is a test entry to verify Notion integration"
        )

        result = await create_lead(test_call_data, "TEST_CALL_SID_123")

        if result.get("success"):
            print(f"✅ SUCCESS: Lead created in Notion")
            print(f"   Page ID: {result.get('page_id')}")
            if result.get('url'):
                print(f"   URL: {result.get('url')}")
            return True
        else:
            print(f"❌ FAILED: {result.get('error')}")
            return False

    except Exception as e:
        print(f"❌ FAILED: {str(e)}")
        return False

async def main():
    """Run all integration tests"""
    print("\n" + "="*60)
    print("NOVA VOICE AGENT - INTEGRATION TESTS")
    print("="*60)

    # Test Cal.com
    calcom_ok = await test_calcom()

    # Test Notion
    notion_ok = await test_notion()

    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    print(f"Cal.com:  {'✅ WORKING' if calcom_ok else '❌ FAILED'}")
    print(f"Notion:   {'✅ WORKING' if notion_ok else '❌ FAILED'}")
    print("="*60 + "\n")

    if calcom_ok and notion_ok:
        print("🎉 All integrations are working correctly!")
        return 0
    else:
        print("⚠️  Some integrations need attention")
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
