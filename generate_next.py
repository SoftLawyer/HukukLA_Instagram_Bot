#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HukukLA Instagram Carousel Generator
"Sıradaki" komutuyla bekleyen sıradaki konuyu hazırlar, İndirilenler klasörüne kaydeder
ve paylaşım metnini (açıklama) hazırlar.
"""

import sys
import os
import json
import argparse
from carousel_engine import render_topic_carousel, DOWNLOADS_BASE

TOPICS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "carousel_topics.json")

def load_topics():
    if not os.path.exists(TOPICS_FILE):
        print(f"[!] Hata: {TOPICS_FILE} bulunamadı!")
        sys.exit(1)
    with open(TOPICS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def list_topics(topics):
    print("\n" + "="*75)
    print("📚 HUKUKLA INSTAGRAM CAROUSEL KONU LİSTESİ (20 KONU)")
    print("="*75)
    for t in topics:
        status_symbol = "✅ [TAMAMLANDI]" if t.get("status") == "completed" else "⏳ [BEKLİYOR]  "
        print(f"{t['id']:02d}. {status_symbol} {t['topic_cyan_title']}")
    print("="*75 + "\n")

def reset_topics():
    topics = load_topics()
    for t in topics:
        t["status"] = "pending"
        t["generated_at"] = None
        t["output_dir"] = None
    with open(TOPICS_FILE, "w", encoding="utf-8") as f:
        json.dump(topics, f, ensure_ascii=False, indent=2)
    print("🔄 Tüm konular 'bekliyor' (pending) durumuna sıfırlandı.")

def get_next_pending_topic(topics):
    for t in topics:
        if t.get("status") != "completed":
            return t
    return None

def main():
    parser = argparse.ArgumentParser(description="HukukLA Instagram Carousel Generator")
    parser.add_argument("--list", action="store_true", help="Tüm konuları ve durumlarını listele")
    parser.add_argument("--id", type=int, help="Belirli bir konu numarasını (1-20) üret")
    parser.add_argument("--reset", action="store_true", help="Tüm konuları bekliyor durumuna getir")
    args = parser.parse_args()

    topics = load_topics()

    if args.list:
        list_topics(topics)
        return

    if args.reset:
        reset_topics()
        return

    if args.id:
        target_id = args.id
        target = next((t for t in topics if t["id"] == target_id), None)
        if not target:
            print(f"[!] Hata: ID={target_id} olan konu bulunamadı (1-20 arası seçiniz).")
            return
    else:
        target = get_next_pending_topic(topics)
        if not target:
            print("\n🎉 Tebrikler! Tüm 20 konunun carouseli zaten üretilmiş.")
            print("Yeniden başlatmak için: python generate_next.py --reset\n")
            return
        target_id = target["id"]

    print("\n" + "="*75)
    print(f"🚀 SIRADAKİ CAROUSEL HAZIRLANIYOR: #{target_id:02d}")
    print(f"📌 Başlık : {target['title']}")
    print(f"🏷️ Cyan Başlık: {target['topic_cyan_title']}")
    print(f"📁 Klasör : {target['folder_name']}")
    print("="*75)

    try:
        topic_info, output_folder, files, caption = render_topic_carousel(target_id, TOPICS_FILE)
        print("\n" + "-"*75)
        print("✅ CAROUSEL VE AÇIKLAMA METNİ BAŞARIYLA OLUŞTURULDU!")
        print(f"📂 Kayıt Yeri: {output_folder}")
        print("🖼️ Üretilen Dosyalar:")
        for f in files:
            size_kb = os.path.getsize(f) // 1024 if os.path.getsize(f) > 1024 else 1
            print(f"   • {os.path.basename(f)} ({size_kb} KB)")
        print("\n📝 INSTAGRAM GÖNDERİ AÇIKLAMASI (aciklama.txt olarak da kaydedildi):")
        print("~"*75)
        print(caption)
        print("~"*75 + "\n")
    except Exception as e:
        print(f"[!] Carousel üretilirken bir hata oluştu: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
