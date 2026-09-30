import json
import os
import html
from playwright.sync_api import sync_playwright

BASE_DIR = '/Users/elifgurler/Desktop/HukukLA_Instagram'
JSON_FILE = os.path.join(BASE_DIR, 'HukukLA/HUKUKÇIKTILARI/SORULARINJSONLARI/tc_anayasasi.json')
TEMPLATE_SORU = os.path.join(BASE_DIR, 'templates/template_soru.html')
TEMPLATE_CEVAP = os.path.join(BASE_DIR, 'templates/template_cevap.html')
OUT_DIR = BASE_DIR

with open(TEMPLATE_SORU, 'r', encoding='utf-8') as f:
    soru_html_template = f.read()

with open(TEMPLATE_CEVAP, 'r', encoding='utf-8') as f:
    cevap_html_template = f.read()

with open(JSON_FILE, 'r', encoding='utf-8') as f:
    data = json.load(f)

sorular = data.get('KLASIKSORULAR', [])
soru_obj = sorular[0] # İlk soruyu al

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
konu_adi = "T.C. Anayasası"

# HTML'leri oluştur
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

soru_path = os.path.join(OUT_DIR, 'ornek_soru.html')
cevap_path = os.path.join(OUT_DIR, 'ornek_cevap.html')

with open(soru_path, 'w', encoding='utf-8') as f:
    f.write(s_html)
with open(cevap_path, 'w', encoding='utf-8') as f:
    f.write(c_html)

def render_html_to_png(html_path, output_png):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # Instagram story dimension
        page = browser.new_page(viewport={"width": 1080, "height": 1920}, device_scale_factor=2)
        page.goto(f"file://{html_path}")
        # Bekle ki fontlar yüklensin
        page.wait_for_load_state('networkidle')
        page.screenshot(path=output_png, full_page=True)
        browser.close()

print("Soru görseli oluşturuluyor...")
render_html_to_png(soru_path, os.path.join(OUT_DIR, 'ornek_soru.png'))
print("Cevap görseli oluşturuluyor...")
render_html_to_png(cevap_path, os.path.join(OUT_DIR, 'ornek_cevap.png'))

print("Örnek PNG görselleri başarıyla oluşturuldu!")
