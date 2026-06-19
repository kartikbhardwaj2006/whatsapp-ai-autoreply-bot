import pyautogui
import pyperclip
import time
import win32gui
import win32con
from openai import OpenAI

pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0.05


client = OpenAI(
    api_key="xyz",
    base_url="https://api.groq.com/openai/v1"
)



MOHIT_CHAT_X       = 290    
MOHIT_CHAT_Y       = 262

CHAT_AREA_X        = 950    
CHAT_AREA_Y        = 400

CHAT_DRAG_START_X  = 515    
CHAT_DRAG_START_Y  = 115
CHAT_DRAG_END_X    = 1385   
CHAT_DRAG_END_Y    = 755

MESSAGE_BOX_X      = 950 
MESSAGE_BOX_Y      = 781



def get_whatsapp_hwnd():
    """
    Return the hwnd of the main WhatsApp Desktop window.
    We look for the window titled exactly 'WhatsApp' that is NOT minimized
    to -32000 (which means it's hidden/tray).
    """
    candidates = []
    def cb(hwnd, _):
        if not win32gui.IsWindowVisible(hwnd):
            return
        title = win32gui.GetWindowText(hwnd)
        if title == "WhatsApp":
            rect = win32gui.GetWindowRect(hwnd)
            
            if rect[0] > -10000:
                candidates.append((hwnd, rect))
    win32gui.EnumWindows(cb, None)

    if candidates:
        candidates.sort(key=lambda c: (c[1][2]-c[1][0]) * (c[1][3]-c[1][1]), reverse=True)
        return candidates[0][0]
    return None



def focus_whatsapp():
    hwnd = get_whatsapp_hwnd()
    if not hwnd:
        print("  [!] WhatsApp window not found. Is WhatsApp Desktop running?")
        return False

    win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
    time.sleep(0.3)
    win32gui.SetForegroundWindow(hwnd)
    time.sleep(0.8)
    return True

def open_mohit_chat():
    print(">> Bringing WhatsApp to front and maximizing...")
    if not focus_whatsapp():
        return

    print(f">> Clicking Mohit's chat at ({MOHIT_CHAT_X}, {MOHIT_CHAT_Y})...")
    pyautogui.click(MOHIT_CHAT_X, MOHIT_CHAT_Y)
    time.sleep(1.5)


    pyautogui.click(CHAT_AREA_X, CHAT_AREA_Y)
    time.sleep(0.3)
    pyautogui.hotkey('ctrl', 'End')   
    time.sleep(1.0)
    print(">> Mohit's chat is open and scrolled to bottom!\n")



def read_chat():
    
    focus_whatsapp()
    time.sleep(0.4)

    pyautogui.click(CHAT_AREA_X, CHAT_AREA_Y)
    time.sleep(0.3)
    pyautogui.hotkey('ctrl', 'End')
    time.sleep(0.8)

    pyautogui.moveTo(CHAT_DRAG_START_X, CHAT_DRAG_START_Y)
    time.sleep(0.2)
    pyautogui.dragTo(CHAT_DRAG_END_X, CHAT_DRAG_END_Y, duration=1.0, button='left')
    time.sleep(0.3)

    pyautogui.hotkey('ctrl', 'c')
    time.sleep(1.0)

    pyautogui.click(MESSAGE_BOX_X, MESSAGE_BOX_Y)
    time.sleep(0.3)

    return pyperclip.paste()

def is_last_message_from_mohit(chat_text, sender_name="Mohit"):
    """
    WhatsApp Desktop copies selected messages like:
        Mohit
        Hey bhai kya haal
        10:30 AM

        You
        Sab badhiya!
        10:31 AM

    Walk lines in reverse. First name-line found = last sender.
    """
    lines = [l.strip() for l in chat_text.strip().split('\n') if l.strip()]
    for line in reversed(lines):
        if line == sender_name:
            return True
        if line == "You":
            return False
    for line in reversed(lines[-40:]):
        if sender_name.lower() in line.lower():
            return True
        if line.lower() == "you":
            return False
    return False


def generate_reply(chat_history):
    lines = [l.strip() for l in chat_history.strip().split('\n') if l.strip()]
    trimmed = '\n'.join(lines[-60:])

    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are Kartik, an Indian coder who speaks Hindi and English. "
                    "You are funny, friendly and casual. "
                    "Read the chat history and write ONLY the next reply as Kartik. "
                    "Plain text only — no timestamps, no name prefix, no quotes."
                )
            },
            {"role": "user", "content": trimmed}
        ]
    )
    return completion.choices[0].message.content.strip()


def send_reply(reply_text):
    focus_whatsapp()
    time.sleep(0.3)

    pyperclip.copy(reply_text)
    pyautogui.click(MESSAGE_BOX_X, MESSAGE_BOX_Y)
    time.sleep(0.5)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(0.5)
    pyautogui.press('enter')
    print(f">> Sent: {reply_text}\n")


print("=" * 55)
print("  WhatsApp Bot  |  Auto-replying to Mohit as Kartik")
print("=" * 55)
print(f"Screen: {pyautogui.size()}")
print()

open_mohit_chat()

print("Monitoring chat every 5 seconds... Press Ctrl+C to stop.\n")

last_tail = ""

while True:
    try:
        time.sleep(5)

        chat_text = read_chat()

        if not chat_text.strip() or len(chat_text.strip()) < 5:
            print("[!] Nothing copied — WhatsApp may not be focused. Retrying...")
            open_mohit_chat()
            continue

        if "import pyautogui" in chat_text or "def read_chat" in chat_text:
            print("[!] Copied code instead of chat. Re-opening WhatsApp...")
            open_mohit_chat()
            continue

    
        lines = [l.strip() for l in chat_text.strip().split('\n') if l.strip()]
        tail  = '\n'.join(lines[-8:])
        print("--- Last lines of chat ---")
        print(tail)
        print("-" * 26)

        from_mohit = is_last_message_from_mohit(chat_text)
        is_new     = (tail != last_tail)
        print(f"Last msg from Mohit: {from_mohit} | New message: {is_new}\n")

        if from_mohit and is_new:
            print(">> Mohit sent something! Generating reply...")
            reply = generate_reply(chat_text)
            send_reply(reply)
            last_tail = tail
            time.sleep(10)   #? Cooldown to avoid double-reply

    except KeyboardInterrupt:
        print("\nBot stopped. Goodbye!")
        break
    except Exception as e:
        print(f"[ERROR] {e}")
        time.sleep(5)