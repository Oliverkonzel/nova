"""
CRM Service - Integrates with Notion database and CRM backend
"""
import httpx
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import NOTION_TOKEN, NOTION_DATABASE_ID, NOTION_API_URL, CRM_BACKEND_URL, CRM_BACKEND_TOKEN
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

async def push_to_crm_backend(call_data: CallData, call_sid: str = None) -> dict:
    """
    Push contact/call data to CRM backend API.
    
    Posts to the CRM backend's /contacts/ endpoint with call data in JSON format.
    Maps CallData fields to CRM ContactCreate schema fields.
    
    Args:
        call_data: CallData object containing collected information
        call_sid: Optional Twilio call SID for reference
        
    Returns:
        dict: {"success": True/False, "error": error message if failed}
        
    Note:
        - Requires CRM_BACKEND_URL and CRM_BACKEND_TOKEN environment variables
        - Will not crash on failure, only logs errors
        - Uses Bearer token authentication
    """
    # Skip if CRM backend is not configured
    if not CRM_BACKEND_URL or not CRM_BACKEND_TOKEN:
        print("CRM backend not configured (CRM_BACKEND_URL or CRM_BACKEND_TOKEN missing), skipping push")
        return {"success": False, "error": "CRM backend not configured"}
    
    try:
        # Construct the full endpoint URL
        url = f"{CRM_BACKEND_URL.rstrip('/')}/contacts/"
        
        headers = {
            "Authorization": f"Bearer {CRM_BACKEND_TOKEN}",
            "Content-Type": "application/json"
        }
        
        # Map CallData fields to CRM ContactCreate schema
        # Assuming CRM expects: name, phone, email, service, status, notes, appointment_time
        payload = {
            "name": call_data.name or "Unknown",
            "phone": call_data.phone or "",
            "email": call_data.email or "",
            "service": call_data.service or "",
            "status": call_data.status or "new",
            "notes": call_data.notes or "",
        }
        
        # Add optional fields
        if call_data.appointment_time:
            payload["appointment_time"] = call_data.appointment_time
            
        if call_sid:
            # Include call SID in notes for reference
            payload["notes"] = f"Call SID: {call_sid}\n{payload['notes']}"
        
        print(f"Pushing to CRM backend: {url}")
        
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(url, json=payload, headers=headers)
            response.raise_for_status()  # Raise exception for 4xx/5xx status codes
            
            print(f"✅ CRM backend: Contact created successfully")
            result = response.json() if response.text else {}
            return {
                "success": True,
                "contact_id": result.get("id"),
                "response": result
            }
                
    except httpx.TimeoutException as e:
        error_msg = f"CRM backend request timeout: {str(e)}"
        print(f"❌ {error_msg}")
        return {"success": False, "error": error_msg}
    except httpx.HTTPStatusError as e:
        error_detail = e.response.text if hasattr(e, 'response') else str(e)
        print(f"❌ CRM backend HTTP error: {e}")
        print(f"Response body: {error_detail}")
        return {"success": False, "error": error_detail}
    except Exception as e:
        error_msg = f"CRM backend error: {str(e)}"
        print(f"❌ {error_msg}")
        import traceback
        traceback.print_exc()
        return {"success": False, "error": error_msg}
