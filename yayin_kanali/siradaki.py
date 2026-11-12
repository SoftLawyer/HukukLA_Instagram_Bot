#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HukukLA Instagram Yayın Kanalı - HAP BİLGİ & SINAV TRİCKİ MOTORU
Kullanıcı 'sıradaki' dedikçe bekleyen HMGS / Hakimlik / İcra Müdürlüğü
hap bilgi ve sınav tricklerini kopyalamaya hazır formatta teslim eder.
"""

import os
import sys
import json
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ICERIKLER_FILE = os.path.join(BASE_DIR, "icerikler.json")
STATE_FILE = os.path.join(BASE_DIR, "state.json")

def load_data():
    if not os.path.exists(ICERIKLER_FILE):
        print(f"Hata: {ICERIKLER_FILE} bulunamadı!")
        sys.exit(1)
    with open(ICERIKLER_FILE, "r", encoding="utf-8") as f:
        icerikler = json.load(f)

    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            state = json.load(f)
    else:
        state = {"current_index": 0, "total_contents": len(icerikler), "last_posted_id": None}
    
    return icerikler, state

def save_state(state):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)

def get_next(advance=True):
    icerikler, state = load_data()
    idx = state.get("current_index", 0)

    if idx >= len(icerikler):
        print("\n🎉 Tüm hap bilgiler tamamlandı! Başa sarmak için '--reset' kullanabilirsiniz.")
        return None

    item = icerikler[idx]

    output = f"""
================================================================================
📱 HUKUKLA YAYIN KANALI - HAP BİLGİ #{item['id']}
🎓 Sınav: {item['sinav']} | Ders: {item['ders']}
📌 Konu: {item['baslik']}
================================================================================

👇 AŞAĞIDAKİ METNİ KOPYALAYIP DİREKT YAYIN KANALINA YAPIŞTIRABİLİRSİNİZ:
--------------------------------------------------------------------------------
{item['icerik_metni']}
--------------------------------------------------------------------------------
"""
    print(output)

    if advance:
        state["current_index"] = idx + 1
        state["last_posted_id"] = item["id"]
        state["last_posted_at"] = datetime.now().isoformat()
        save_state(state)
        print(f"✅ Hap Bilgi #{item['id']} teslim edildi. Sıradaki: {state['current_index']}/{len(icerikler)}")
    
    return item

def reset_state():
    icerikler, _ = load_data()
    state = {
        "current_index": 0,
        "total_contents": len(icerikler),
        "last_posted_id": None,
        "last_posted_at": None
    }
    save_state(state)
    print("🔄 Durum sıfırlandı. 1. Hap Bilgiden başlanacak.")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="HukukLA Yayın Kanalı Hap Bilgi Motoru")
    parser.add_argument("--peek", action="store_true", help="İndeksi ilerletmeden sıradakini göster")
    parser.add_argument("--reset", action="store_true", help="İndeksi sıfırla")
    args = parser.parse_args()

    if args.reset:
        reset_state()
    elif args.peek:
        get_next(advance=False)
    else:
        get_next(advance=True)
