"""requests кітапханасының мысалы: app.py API-іне сұраныс жібереді.
Алдымен басқа терминалда `python app.py` іске қосыңыз."""
import requests

BASE = "http://127.0.0.1:5000"
try:
    p = requests.get(f"{BASE}/api/puzzle", params={"seed": 3}, timeout=10).json()
    print("Шарттар:", p["clues"], "| шешім саны:", p["solutions"], "| код:", p["secret"])
    m = requests.get(f"{BASE}/api/maze", params={"n": 15, "seed": 1}, timeout=10).json()
    print("A*: жол ұзындығы", len(m["path"]) - 1, "ашылған түйін", m["expanded"])
    print("Қате (n=8):", requests.get(f"{BASE}/api/maze", params={"n": 8}, timeout=10).json())
except requests.exceptions.ConnectionError:
    print("Сервер қосылмаған. Алдымен орындаңыз: python app.py")
