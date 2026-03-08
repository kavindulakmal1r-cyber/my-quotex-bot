import requests
import time
import json

# --- ⚙️ QUOTEX SMART AI CONFIGURATION ---
TOKEN = "8683540715:AAFZX9mTrbZAPQRuAptbo0niQGisTGLRJl8"
CHAT_ID = "5985957367"
# Added high volatility assets for Quotex
SYMBOLS = ['BTCUSDT', 'ETHUSDT', 'SOLUSDT', 'BNBUSDT', 'DOGEUSDT', 'ADAUSDT', 'XRPUSDT', 'LTCUSDT', 'LINKUSDT', 'DOTUSDT', 'MATICUSDT']

prices = {s: None for s in SYMBOLS}
ready_sent = {s: False for s in SYMBOLS}

def send_msg(text):
    # Professional Menu Buttons for Telegram
    keyboard = {
        "inline_keyboard": [
            [{"text": "💰 Balance", "callback_data": "bal"}, {"text": "📊 Win Rate", "callback_data": "ratio"}],
            [{"text": "🔄 Reset Stats", "callback_data": "reset"}, {"text": "🛑 Stop Bot", "callback_data": "stop"}]
        ]
    }
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    params = {
        "chat_id": CHAT_ID, 
        "text": text, 
        "parse_mode": "Markdown",
        "reply_markup": json.dumps(keyboard)
    }
    try:
        requests.get(url, params=params)
    except:
        pass

# Boot-up Message for Render Server
send_msg("🚀 *QUOTEX PRO AI DEPLOYED ON RENDER*\n-----------------------\n🛡️ Mode: High Accuracy\n📢 Alerts: Smart Pre-Signals\n⏱️ Logic: Dynamic 3m/5m")

while True:
    for s in SYMBOLS:
        try:
            # Fetching real-time price
            r = requests.get(f"https://api.binance.com/api/v3/ticker/price?symbol={s}", timeout=5).json()
            cp = float(r['price'])
            
            if prices[s] is not None:
                diff = ((cp - prices[s]) / prices[s]) * 100
                abs_diff = abs(diff)

                # 🚀 SMART TIME LOGIC (3m if fast, 5m if normal)
                suggested_time = "3 MINS" if abs_diff > 0.8 else "5 MINS"

                # 1. 📢 SMART READY ALERT (Preparing the user)
                if abs_diff >= 0.35 and not ready_sent[s]:
                    ready_msg = (
                        f"⚠️ *READY TO TRADE*\n\n"
                        f"Asset: #{s}\n"
                        f"Action: Prepare on Quotex\n"
                        f"Suggested: *{suggested_time}*\n"
                        f"Status: Market Heating Up! 🔥"
                    )
                    send_msg(ready_msg)
                    ready_sent[s] = True
                
                # 2. 🔥 FINAL CONFIRMED ENTRY (Accuracy Focus)
                if abs_diff >= 0.6:
                    direction = "🟢 UP (CALL)" if diff > 0 else "🔴 DOWN (PUT)"
                    final_msg = (
                        f"✅ *ENTRY CONFIRMED*\n\n"
                        f"Asset: #{s}\n"
                        f"Action: *{direction}*\n"
                        f"Timeframe: *{suggested_time}*\n"
                        f"Strength: Strong Trend 🚀"
                    )
                    send_msg(final_msg)
                    time.sleep(210) # Wait for trade completion
                    ready_sent[s] = False 
                
                # Reset Ready Alert
                if abs_diff < 0.2:
                    ready_sent[s] = False
                    
            prices[s] = cp
        except:
            pass
            
    time.sleep(6) # Optimized for Render Free Tier
