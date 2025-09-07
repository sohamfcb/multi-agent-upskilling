from typing import Any
from fastapi.responses import JSONResponse
import resend

import os
from dotenv import load_dotenv
from resend.exceptions import ResendError
from core.logger_config import get_logger

from services.workflows.agent_model import Chatbot

import requests, json

logger=get_logger(name="otp-verifier")

load_dotenv()

RESEND_API_KEY=os.getenv("RESEND_API_KEY")
SENDER_MAIL=os.getenv("SENDER_MAIL")

resend.api_key=RESEND_API_KEY


def stream_json(message: str, thread_id: str, _sqlite: bool = True):
    # bot = Chatbot(model_name="gpt-4o", thread_id=thread_id).build_graph()
    bot = Chatbot(model_name="gpt-4o").build_graph(_sqlite=_sqlite)
    for chunk in bot.stream(user_message=message, thread_id=thread_id):
        yield json.dumps({
            "thread_id": thread_id,
            "type": "message_chunk",
            "content": chunk
        }) + "\n"


def return_response(message: str, status: bool = False, data: Any = None, status_code: int = 200):
    return JSONResponse(
        status_code=status_code,
        content={
            "status": status,
            "message": message,
            "data": data
        }
    )

def send_email_otp(email: str, code: str) -> None:
    url = "https://api.resend.com/emails"
    headers = {
        "Authorization": f"Bearer {RESEND_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "from": f"{SENDER_MAIL}",
        "to": email,
        "subject": "skillSync Code",
        "text": f"Your skillSync AI login code is {code}. It expires in 10 minutes. "
                    "If you didn’t request this, you can ignore this email.",
        "html": f"""
    <!doctype html>
    <html>
    <body style="margin:0;padding:0;background:#f6f7f9;">
        <!-- preheader (shows in inbox preview) -->
        <div style="display:none;max-height:0;overflow:hidden;opacity:0;">
        Your one-time login code for skillSync is {code}. Expires in 10 minutes.
        </div>

        <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="background:#f6f7f9;">
        <tr><td align="center" style="padding:32px 16px;">
            <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="max-width:560px;background:#ffffff;border-radius:12px;overflow:hidden;border:1px solid #e9edf3;">
            <!-- Header -->
            <tr>
                <td style="padding:20px 24px;background:#0f172a;color:#ffffff;font-family:system-ui,-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif;">
                <h1 style="margin:0;font-size:18px;font-weight:700;">skillSync AI</h1>
                <div style="font-size:12px;opacity:.9;margin-top:4px;">Sign in securely</div>
                </td>
            </tr>

            <!-- Body -->
            <tr>
                <td style="padding:24px;font-family:system-ui,-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif;color:#0f172a;">
                <h2 style="margin:0 0 8px 0;font-size:18px;font-weight:700;">Your one-time code</h2>
                <p style="margin:0 0 16px 0;font-size:14px;line-height:1.5;color:#334155;">
                    Enter this code to continue. It expires in <b>10 minutes</b>.
                </p>

                <!-- Big code boxes -->
                <table role="presentation" cellspacing="0" cellpadding="0" border="0" align="center" style="margin:16px auto 8px auto;">
                    <tr>
                    {''.join(f'''
                    <td style="background:#0f172a;color:#ffffff;font-weight:700;font-size:22px;
                                font-family:ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
                                text-align:center;border-radius:8px;padding:12px 14px;letter-spacing:0.5px;
                                min-width:40px;border:1px solid #0b1227;">
                        {d}
                    </td>
                    <td style="width:8px;"></td>
                    ''' for d in code)}
                    </tr>
                </table>

                <!-- Fallback plain code line -->
                <p style="margin:12px 0 0 0;font-size:13px;color:#64748b;text-align:center;">
                    Can’t see the boxes? Your code is: <b style="font-family:ui-monospace,Menlo,Consolas,monospace;
                    letter-spacing:2px;">{code}</b>
                </p>

                <!-- Tip -->
                <p style="margin:20px 0 0 0;font-size:12px;color:#475569;">
                    If you didn’t request this, you can safely ignore this email.
                </p>

                <!-- Button (optional) -->
                <!--
                <div style="text-align:center;margin-top:20px;">
                    <a href="#" style="display:inline-block;background:#0f172a;color:#ffffff;text-decoration:none;
                    padding:10px 16px;border-radius:8px;font-size:14px;font-weight:600;">
                    Open the app
                    </a>
                </div>
                -->
                </td>
            </tr>

            <!-- Footer -->
            <tr>
                <td style="padding:14px 24px;background:#fafafa;border-top:1px solid #eef2f7;
                        font-family:system-ui,-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif;">
                <p style="margin:0;color:#94a3b8;font-size:12px;">
                    Sent by SkillSync AI • This is an automated message
                </p>
                </td>
            </tr>
            </table>
        </td></tr>
        </table>
    </body>
    </html>
            """,
    }
    resp = requests.post(url, headers=headers, data=json.dumps(payload), timeout=10)
    if resp.status_code >= 300:
        logger.error("Resend error:", resp.json())
        # raise RuntimeError(f"Resend failed: {resp.status_code}")
