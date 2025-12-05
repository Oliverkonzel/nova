"""
Quick test to trigger Notion integration via the webhook
Run this while your server is running to see live logs
"""
import httpx
import asyncio

async def test_webhook():
    """Simulate a webhook call that triggers Notion"""

    # Make sure your server is running on localhost:8000
    base_url = "http://localhost:8000"

    print("Testing Notion integration via webhook...")
    print("Make sure your server is running with: cd backend && python main.py")
    print("-" * 60)

    # Simulate the booking webhook which triggers Notion
    try:
        async with httpx.AsyncClient() as client:
            # This endpoint calls create_lead() which saves to Notion
            response = await client.post(
                f"{base_url}/webhooks/voice/book",
                data={
                    "CallSid": "TEST_CALL_SID_" + str(asyncio.get_event_loop().time()),
                    "SpeechResult": "Yes, book me for the first slot"
                },
                timeout=30.0
            )

            print(f"Response status: {response.status_code}")
            print(f"Response: {response.text[:500]}")
            print("\nCheck your server terminal for Notion logs!")

    except httpx.ConnectError:
        print("❌ Could not connect to server at http://localhost:8000")
        print("Make sure the server is running with: cd backend && python main.py")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_webhook())
