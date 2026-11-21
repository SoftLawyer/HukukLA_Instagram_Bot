import json
import os
import glob
import html
from playwright.sync_api import sync_playwright

BASE_DIR = '/Users/elifgurler/Desktop/HukukLA_Instagram'
JSON_DIR = os.path.join(BASE_DIR, 'HukukLA/HUKUKÇIKTILARI/SORULARINJSONLARI')
STATE_FILE = os.path.join(BASE_DIR, 'cursor_state.json')

TEMPLATE_SORU = os.path.join(BASE_DIR, 'templates/template_soru.html')
TEMPLATE_CEVAP = os.path.join(BASE_DIR, 'templates/template_cevap.html')
OUT_DIR = BASE_DIR

# Okunabilirlik ve Ferahlık Kriterleri
MAX_QUESTION_LEN = 180      # Soru metni maksimum karakter
MAX_OPTION_LEN = 65         # Her bir şık için maksimum karakter
MAX_TOTAL_LEN = 450         # Soru + 5 Şık toplam maksimum karakter

# Doğru Türkçe Karakterli Ders / Mevzuat İsimleri
TOPIC_NAMES = {
    '1136_sayili_avukatlik_kanunu.json': '1136 Sayılı Avukatlık Kanunu',
    '2004_sayili_icra_iflas_kanunu.json': '2004 Sayılı İcra ve İflas Kanunu',
    '2577_sayili_idari_yargilama_usulu_kanunu.json': '2577 Sayılı İdari Yargılama Usulü Kanunu',
    '4857_sayili_is_kanunu.json': '4857 Sayılı İş Kanunu',
    '5237_sayili_turk_ceza_kanunu_genel_hukumler.json': '5237 Sayılı TCK (Genel Hükümler)',
    '5237_sayili_turk_ceza_kanunu_ozel_hukumler.json': '5237 Sayılı TCK (Özel Hükümler)',
    '5271_sayili_ceza_muhakemesi_kanunu.json': '5271 Sayılı Ceza Muhakemesi Kanunu',
    '5326_sayili_kabahatler_kanunu.json': '5326 Sayılı Kabahatler Kanunu',
    '5510_sayili_sosyal_sigortalar_ve_genel_saglik_sigortasi_kanunu.json': '5510 Sayılı Sosyal Sigortalar Kanunu',
    '5718_sayili_milletler_arasi_ozel_hukuk_ve_usul_hukuku_hakkinda_kanun.json': '5718 Sayılı MÖHUK',
    '5901_sayili_turk_vatandasligi_kanunu.json': '5901 Sayılı Türk Vatandaşlığı Kanunu',
    '5941_sayili_cek_kanunu.json': '5941 Sayılı Çek Kanunu',
    '6098_sayili_turk_borclar_kanunu_genel_hukumler.json': '6098 Sayılı TBK (Genel Hükümler)',
    '6098_sayili_turk_borclar_kanunu_ozel_hukumler.json': '6098 Sayılı TBK (Özel Hükümler)',
    '6100_sayili_hukuk_muhakemeleri_kanunu.json': '6100 Sayılı Hukuk Muhakemeleri Kanunu',
    '6356_sayili_sendikalar_ve_toplu_is_sozlesmeleri_kanunu.json': '6356 Sayılı Sendikalar ve TİS Kanunu',
    '657_sayili_devlet_memurlari_kanunu.json': '657 Sayılı Devlet Memurları Kanunu',
    '6698_sayili_kisisel_verilerin_korunmasi_kanunu.json': '6698 Sayılı KVKK',
    'aile_hukuku.json': 'Aile Hukuku',
    'baslangic_hukumleri_ve_kisiler_hukuku.json': 'Başlangıç Hükümleri ve Kişiler Hukuku',
    'baslangic_hukumleri_ve_ticari_isletme_hukuku.json': 'Ticari İşletme Hukuku',
    'deniz_ticareti_hukuku.json': 'Deniz Ticareti Hukuku',
    'esya_hukuku.json': 'Eşya Hukuku',
    'genel_kamu_hukuku.json': 'Genel Kamu Hukuku',
    'hukuk_felsefesi_ve_sosyolojisi.json': 'Hukuk Felsefesi ve Sosyolojisi',
    'kiymetli_evrak_hukuku.json': 'Kıymetli Evrak Hukuku',
    'milletler_arasi_hukuk.json': 'Milletlerarası Hukuk',
    'miras_hukuku.json': 'Miras Hukuku',
    'sigorta_hukuku.json': 'Sigorta Hukuku',
    'tasima_isleri_hukuku.json': 'Taşıma İşleri Hukuku',
    'tc_anayasasi.json': 'T.C. Anayasası',
    'ticaret_sirketleri_hukuku.json': 'Ticaret Şirketleri Hukuku',
    'turk_hukuk_tarihi.json': 'Türk Hukuk Tarihi',
}

def get_topics():
    files = glob.glob(os.path.join(JSON_DIR, '*.json'))
    files.sort()
    return files

def format_konu_adi(filename):
    fname = os.path.basename(filename)
    if fname in TOPIC_NAMES:
        return TOPIC_NAMES[fname]
    name = os.path.splitext(fname)[0].replace('_', ' ')
    return name.title()

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'r', encoding='utf-8') as f:
            state = json.load(f)
            if 'topic_progress' not in state:
                state['topic_progress'] = {}
            return state
    return {
        "current_topic_index": 0,
        "current_question_index": 0,
        "topic_progress": {}
    }

def save_state(state):
    with open(STATE_FILE, 'w', encoding='utf-8') as f:
        json.dump(state, f, indent=2, ensure_ascii=False)

def is_question_suitable(soru_obj):
    soru = (soru_obj.get('soru', '') or '').strip()
    secenekler = [(o or '').strip() for o in soru_obj.get('secenekler', {}).values()]
    
    if not soru or len(secenekler) < 4:
        return False
        
    if len(soru) > MAX_QUESTION_LEN:
        return False
        
    if any(len(opt) > MAX_OPTION_LEN for opt in secenekler):
        return False
        
    if len(soru) + sum(len(opt) for opt in secenekler) > MAX_TOTAL_LEN:
        return False
        
    return True

def render_html_to_png(html_content, output_png):
    tmp_path = os.path.join(OUT_DIR, 'temp_render.html')
    with open(tmp_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
        
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1080, "height": 1920}, device_scale_factor=2)
        page.goto(f"file://{tmp_path}")
        page.wait_for_load_state('networkidle')
        page.screenshot(path=output_png, full_page=True)
        browser.close()
        
    if os.path.exists(tmp_path):
        os.remove(tmp_path)

def generate_next():
    topics = get_topics()
    if not topics:
        print("HATA: JSON dosyası bulunamadı.")
        return

    state = load_state()
    topic_idx = state.get('current_topic_index', 0)
    topic_progress = state.get('topic_progress', {})

    with open(TEMPLATE_SORU, 'r', encoding='utf-8') as f:
        soru_html_template = f.read()

    with open(TEMPLATE_CEVAP, 'r', encoding='utf-8') as f:
        cevap_html_template = f.read()

    attempts = 0
    while attempts < len(topics):
        if topic_idx >= len(topics):
            topic_idx = 0

        filepath = topics[topic_idx]
        fname = os.path.basename(filepath)

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception:
            topic_idx += 1
            attempts += 1
            continue

        sorular = data.get('KLASIKSORULAR', [])
        total_questions = len(sorular)

        if total_questions == 0:
            topic_idx += 1
            attempts += 1
            continue

        start_search_idx = topic_progress.get(fname, 0)
        found_soru = None
        found_idx = -1

        for offset in range(total_questions):
            curr_idx = (start_search_idx + offset) % total_questions
            candidate = sorular[curr_idx]
            if is_question_suitable(candidate):
                found_soru = candidate
                found_idx = curr_idx
                break

        if found_soru is not None:
            konu_adi = format_konu_adi(filepath)

            # Değişkenleri Hazırla
            soru_metni = html.escape(found_soru.get('soru', ''))
            secenekler = found_soru.get('secenekler', {})
            sec_a = html.escape(secenekler.get('A', ''))
            sec_b = html.escape(secenekler.get('B', ''))
            sec_c = html.escape(secenekler.get('C', ''))
            sec_d = html.escape(secenekler.get('D', ''))
            sec_e = html.escape(secenekler.get('E', ''))
            dogru_cevap = found_soru.get('dogru_cevap', '')
            gerekce = html.escape(found_soru.get('gerekce', ''))
            dogru_cevap_metni = html.escape(secenekler.get(dogru_cevap, ''))

            s_html = soru_html_template.replace('{{ ders_adi }}', konu_adi)
            s_html = s_html.replace('{{ soru }}', soru_metni.replace('\n', '<br>'))
            s_html = s_html.replace('{{ secenek_a }}', sec_a)
            s_html = s_html.replace('{{ secenek_b }}', sec_b)
            s_html = s_html.replace('{{ secenek_c }}', sec_c)
            s_html = s_html.replace('{{ secenek_d }}', sec_d)
            s_html = s_html.replace('{{ secenek_e }}', sec_e)

            c_html = cevap_html_template.replace('{{ ders_adi }}', konu_adi)
            c_html = c_html.replace('{{ soru }}', soru_metni.replace('\n', '<br>'))
            c_html = c_html.replace('{{ dogru_cevap_harf }}', dogru_cevap)
            c_html = c_html.replace('{{ dogru_cevap_metin }}', dogru_cevap_metni)
            c_html = c_html.replace('{{ gerekce }}', gerekce.replace('\n', '<br>'))

            print(f"Hazırlanıyor: {konu_adi} (Soru İndeksi: {found_idx + 1})")
            render_html_to_png(s_html, os.path.join(OUT_DIR, 'siradaki_soru.png'))
            render_html_to_png(c_html, os.path.join(OUT_DIR, 'siradaki_cevap.png'))

            # Durumu Güncelle
            topic_progress[fname] = (found_idx + 1) % total_questions
            state['topic_progress'] = topic_progress
            state['current_topic_index'] = (topic_idx + 1) % len(topics)
            save_state(state)

            print(f"BAŞARILI: {konu_adi} - Soru {found_idx + 1} oluşturuldu.")
            return

        topic_idx += 1
        attempts += 1

    print("HATA: Hiçbir mevzuatta uygun soru bulunamadı.")

if __name__ == "__main__":
    generate_next()
