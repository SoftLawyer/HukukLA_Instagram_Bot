import json
import os
import glob
import html

# Yollar
BASE_DIR = '/Users/elifgurler/Desktop/HukukLA_Instagram'
JSON_DIR = os.path.join(BASE_DIR, 'HukukLA/HUKUKÇIKTILARI/SORULARINJSONLARI')
TEMPLATE_SORU = os.path.join(BASE_DIR, 'templates/template_soru.html')
TEMPLATE_CEVAP = os.path.join(BASE_DIR, 'templates/template_cevap.html')
OUT_DIR = os.path.join(BASE_DIR, 'story_cikti')

# Şablonları oku
with open(TEMPLATE_SORU, 'r', encoding='utf-8') as f:
    soru_html_template = f.read()

with open(TEMPLATE_CEVAP, 'r', encoding='utf-8') as f:
    cevap_html_template = f.read()

# JSON dosyalarını bul
json_files = glob.glob(os.path.join(JSON_DIR, '*.json'))

def format_konu_adi(filename):
    name = os.path.splitext(os.path.basename(filename))[0]
    # Örneğin: tc_anayasasi -> Tc Anayasası
    name = name.replace('_', ' ').title()
    return name

total_questions = 0

for filepath in json_files:
    konu_adi = format_konu_adi(filepath)
    filename_base = os.path.splitext(os.path.basename(filepath))[0]
    
    # Çıktı klasörünü konu için oluştur
    konu_out_dir = os.path.join(OUT_DIR, filename_base)
    os.makedirs(konu_out_dir, exist_ok=True)
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Hata okuma: {filepath} - {e}")
        continue
        
    sorular = data.get('KLASIKSORULAR', [])
    
    for idx, soru_obj in enumerate(sorular, 1):
        soru_metni = html.escape(soru_obj.get('soru', ''))
        secenekler = soru_obj.get('secenekler', {})
        sec_a = html.escape(secenekler.get('A', ''))
        sec_b = html.escape(secenekler.get('B', ''))
        sec_c = html.escape(secenekler.get('C', ''))
        sec_d = html.escape(secenekler.get('D', ''))
        sec_e = html.escape(secenekler.get('E', ''))
        dogru_cevap = soru_obj.get('dogru_cevap', '')
        gerekce = html.escape(soru_obj.get('gerekce', ''))
        
        # Doğru cevabın metnini al
        dogru_cevap_metni = secenekler.get(dogru_cevap, '')
        dogru_cevap_metni = html.escape(dogru_cevap_metni)

        # Soru HTML'i oluştur
        s_html = soru_html_template.replace('{{ ders_adi }}', konu_adi)
        s_html = s_html.replace('{{ soru }}', soru_metni.replace('\n', '<br>'))
        s_html = s_html.replace('{{ secenek_a }}', sec_a)
        s_html = s_html.replace('{{ secenek_b }}', sec_b)
        s_html = s_html.replace('{{ secenek_c }}', sec_c)
        s_html = s_html.replace('{{ secenek_d }}', sec_d)
        s_html = s_html.replace('{{ secenek_e }}', sec_e)
        
        soru_path = os.path.join(konu_out_dir, f'soru_{idx}_1_soru.html')
        with open(soru_path, 'w', encoding='utf-8') as f:
            f.write(s_html)
            
        # Cevap HTML'i oluştur
        c_html = cevap_html_template.replace('{{ ders_adi }}', konu_adi)
        c_html = c_html.replace('{{ soru }}', soru_metni.replace('\n', '<br>'))
        c_html = c_html.replace('{{ dogru_cevap_harf }}', dogru_cevap)
        c_html = c_html.replace('{{ dogru_cevap_metin }}', dogru_cevap_metni)
        c_html = c_html.replace('{{ gerekce }}', gerekce.replace('\n', '<br>'))
        
        cevap_path = os.path.join(konu_out_dir, f'soru_{idx}_2_cevap.html')
        with open(cevap_path, 'w', encoding='utf-8') as f:
            f.write(c_html)
            
        total_questions += 1

print(f"Toplam {len(json_files)} dosyadan {total_questions} adet soru için HTML şablonları başarıyla oluşturuldu!")
print(f"Çıktılar '{OUT_DIR}' klasöründe bulunabilir.")
