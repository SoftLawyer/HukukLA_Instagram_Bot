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

def get_topics():
    # Klasördeki jsonları alfabetik sırayla al (sabit bir sıra olsun)
    files = glob.glob(os.path.join(JSON_DIR, '*.json'))
    files.sort()
    return files

def format_konu_adi(filename):
    name = os.path.splitext(os.path.basename(filename))[0]
    name = name.replace('_', ' ').title()
    return name

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'r') as f:
            return json.load(f)
    return {
        "current_topic_index": 0,
        "current_question_index": 0
    }

def save_state(state):
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f)

def render_html_to_png(html_content, output_png):
    # Geçici HTML dosyası oluştur
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
    topic_idx = state['current_topic_index']
    q_idx = state['current_question_index']
    
    with open(TEMPLATE_SORU, 'r', encoding='utf-8') as f:
        soru_html_template = f.read()

    with open(TEMPLATE_CEVAP, 'r', encoding='utf-8') as f:
        cevap_html_template = f.read()
        
    found = False
    start_topic_idx = topic_idx
    start_q_idx = q_idx
    
    while not found:
        # Eğer topic index listeyi aştıysa, başa dön ve soru indexini 1 artır
        if topic_idx >= len(topics):
            topic_idx = 0
            q_idx += 1
            
        # Eğer bu turda (bütün topicleri gezip) hiçbirinde soru bulamazsak sonsuz döngüyü kır
        # Pratikte çok fazla topic var, eğer hepsi bittiyse program dursun
        if q_idx > 10000: # Güvenlik
            print("Tüm sorular bitti!")
            return
            
        filepath = topics[topic_idx]
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception:
            topic_idx += 1
            continue
            
        sorular = data.get('KLASIKSORULAR', [])
        
        # Bu mevzuatta istenilen index'te soru var mı?
        if q_idx < len(sorular):
            found = True
            soru_obj = sorular[q_idx]
            konu_adi = format_konu_adi(filepath)
            
            # Üretim Yap
            soru_metni = html.escape(soru_obj.get('soru', ''))
            secenekler = soru_obj.get('secenekler', {})
            sec_a = html.escape(secenekler.get('A', ''))
            sec_b = html.escape(secenekler.get('B', ''))
            sec_c = html.escape(secenekler.get('C', ''))
            sec_d = html.escape(secenekler.get('D', ''))
            sec_e = html.escape(secenekler.get('E', ''))
            dogru_cevap = soru_obj.get('dogru_cevap', '')
            gerekce = html.escape(soru_obj.get('gerekce', ''))
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
            
            print(f"Hazırlanıyor: {konu_adi} (Soru {q_idx + 1})")
            render_html_to_png(s_html, os.path.join(OUT_DIR, 'siradaki_soru.png'))
            render_html_to_png(c_html, os.path.join(OUT_DIR, 'siradaki_cevap.png'))
            
            # Durumu Güncelle (Bir sonraki çağrı için topic'i 1 artır)
            state['current_topic_index'] = topic_idx + 1
            state['current_question_index'] = q_idx
            save_state(state)
            
            print(f"BAŞARILI: {konu_adi} - Soru {q_idx + 1} oluşturuldu.")
            return
            
        else:
            # Bu mevzuatta bu index'te soru yok (örneğin bu mevzuatta 10 soru var ama biz 11.yi arıyoruz)
            # Sonraki mevzuata geç
            topic_idx += 1

if __name__ == "__main__":
    generate_next()
