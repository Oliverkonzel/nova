"""
CRM Service - Integrates with Notion database
"""
import httpx
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import NOTION_TOKEN, NOTION_DATABASE_ID, NOTION_API_URL
from models import CallData
from datetime import datetime

async def create_lead(call_data: CallData, call_sid: str) -> dict:
    """Create a new lead entry in Notion"""
    try:
        url = f"{NOTION_API_URL}/pages"

        headers = {
            "Authorization": f"Bearer {NOTION_TOKEN}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28"
        }

        properties = {
            "Name": {
                "title": [{"text": {"content": call_data.name or "Unknown"}}]
            },
            "Phone_Number": {
                "phone_number": call_data.phone or ""
            },
            "Email": {
                "email": call_data.email or ""
            },
            "service": {
                "rich_text": [{"text": {"content": call_data.service or ""}}]
            },
            "status": {
                "select": {"name": call_data.status}
            },
            "Date": {
                "date": {"start": datetime.now().isoformat()}
            },
            "notes": {
                "rich_text": [{
                    "text": {
                        "content": f"Call SID: {call_sid}\n{call_data.notes}"
                    }
                }]
            }
        }

        if call_data.appointment_time:
            properties["notes"]["rich_text"][0]["text"]["content"] += f"\nAppointment: {call_data.appointment_time}"

        data = {
            "parent": {"database_id": NOTION_DATABASE_ID},
            "properties": properties
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=data, headers=headers)

            if response.status_code != 200:
                error_detail = response.text
                print(f"Notion API Error {response.status_code}:")
                print(f"Response: {error_detail}")
                return {"success": False, "error": error_detail}

            result = response.json()

            print(f"Notion lead created!")
            return {
                "success": True,
                "page_id": result.get("id"),
                "url": result.get("url")
            }

    except httpx.HTTPStatusError as e:
        error_detail = e.response.text if hasattr(e, 'response') else str(e)
        print(f"Notion HTTP error: {e}")
        print(f"Response body: {error_detail}")
        return {"success": False, "error": error_detail}
    except Exception as e:
        print(f"Notion error: {e}")
        import traceback
        traceback.print_exc()
        return {"success": False, "error": str(e)}
