import os
import json
import time
from datetime import datetime
from playwright.sync_api import sync_playwright

DOWNLOADS_BASE = os.path.expanduser("~/Downloads")

BASE_HTML_WRAPPER = """
<!DOCTYPE html>
<html lang="tr">
<head>
  <meta charset="UTF-8">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@800;900&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <script src="https://cdn.tailwindcss.com"></script>
  <style>
    * {
      box-sizing: border-box;
      -webkit-font-smoothing: antialiased;
    }
    body {
      font-family: 'Plus Jakarta Sans', sans-serif;
      width: 1080px;
      height: 1350px;
      margin: 0;
      padding: 0;
      overflow: hidden;
      background: radial-gradient(circle at 85% 22%, #1C4060 0%, #132A42 45%, #0E1D30 100%);
      color: #FFFFFF;
    }
    .font-hook {
      font-family: 'Montserrat', sans-serif;
      font-weight: 900;
      line-height: 0.98;
      letter-spacing: -0.025em;
    }
    .text-gold {
      color: #FACD54;
    }
    .text-teal {
      color: #31E5DB;
    }
    .badge-teal {
      border: 1.5px solid #31E5DB;
      background: rgba(21, 74, 89, 0.45);
      color: #31E5DB;
    }
  </style>
</head>
<body class="relative flex flex-col justify-between p-24 selection:bg-teal-500">
  <!-- Subtle circular background glow in top right -->
  <div class="absolute -top-32 -right-32 w-[650px] h-[650px] rounded-full bg-[#1A3D5B]/30 blur-[60px] pointer-events-none"></div>

  {{CONTENT}}
</body>
</html>
"""

def generate_dots(current_idx, total_slides):
    dots = []
    for i in range(total_slides):
        if i == current_idx:
            dots.append('<span class="w-8 h-2.5 rounded-full bg-[#31E5DB] transition-all"></span>')
        elif i < current_idx:
            dots.append('<span class="w-8 h-2.5 rounded-full bg-[#31E5DB]/75"></span>')
        else:
            dots.append('<span class="w-2.5 h-2.5 rounded-full bg-[#244563]"></span>')
    return "".join(dots)

def build_cover_slide(topic, total_slides):
    dots_html = generate_dots(0, total_slides)
    
    hook_lines = topic.get("hook_lines", ["ÇOĞU", "HMGS ADAYI", "BUNU", "BİLMİYOR:"])
    highlight_idx = topic.get("highlight_line_idx", 1)
    
    formatted_lines = []
    for idx, line in enumerate(hook_lines):
        if idx == highlight_idx:
            formatted_lines.append(f'<span class="text-gold">{line}</span>')
        else:
            formatted_lines.append(line)
    hook_html = "<br>\n      ".join(formatted_lines)

    content = f"""
    <div class="flex flex-col space-y-7 mt-6 z-10">
      <!-- Huge Impact Hook -->
      <div class="font-hook text-[104px] uppercase text-white tracking-tight">
        {hook_html}
      </div>

      <!-- Cyan/Teal Topic Title -->
      <div class="text-[44px] font-extrabold text-teal tracking-tight leading-tight">
        {topic['topic_cyan_title']}
      </div>

      <!-- Uppercase Principle -->
      <div class="text-[21px] font-bold text-[#8FAEC6] tracking-wider uppercase max-w-3xl leading-snug">
        {topic['core_principle_upper']}
      </div>

      <!-- Explanatory Hook Sentence -->
      <div class="text-[26px] text-slate-100 leading-relaxed max-w-3xl pt-1 font-normal">
        {topic['hook_desc']}
      </div>

      <!-- Pushpin Text -->
      <div class="text-[24px] text-slate-200 font-medium pt-3 flex items-center gap-2">
        {topic['pin_text']}
      </div>
    </div>

    <!-- Footer Bar -->
    <div class="flex items-center justify-between pt-10 border-t border-[#1E3B56] mb-2 z-10">
      <div class="flex items-center gap-2">
        {dots_html}
      </div>

      <div class="text-[30px] font-extrabold text-teal flex items-center gap-2 tracking-wide font-hook">
        <span>Kaydır</span>
        <span>➔</span>
      </div>
    </div>
    """
    return BASE_HTML_WRAPPER.replace("{{CONTENT}}", content)

def build_content_slide(topic, slide, slide_idx, total_slides):
    dots_html = generate_dots(slide_idx, total_slides)
    badge_label = slide.get("step_badge", f"SLAYT {slide_idx}")
    
    bullets = slide.get("bullets", [])
    bullets_html_list = []
    
    for i, b in enumerate(bullets):
        is_last = (i == len(bullets) - 1)
        italic_class = "italic text-slate-300" if is_last else "text-slate-200"
        b_label = b.get("label", "")
        b_text = b.get("text", "")
        
        bullets_html_list.append(f"""
        <p class="{italic_class}">
          <strong class="text-white font-extrabold not-italic">• {b_label}:</strong>
          {b_text}
        </p>
        """)
        
    bullets_content = "".join(bullets_html_list)

    icon_suffix = f" {slide.get('icon', '⚖️')}" if slide.get('icon') else ""

    content = f"""
    <div class="flex flex-col mt-6 z-10">
      <!-- Top Pill Badge -->
      <div class="inline-flex items-center px-6 py-2 rounded-full badge-teal text-[20px] font-bold tracking-wider uppercase mb-10 w-max font-hook">
        {badge_label}
      </div>

      <!-- Title -->
      <h2 class="text-[48px] font-extrabold text-white leading-[1.2] tracking-tight uppercase mb-14 font-hook max-w-4xl">
        {slide['title']}{icon_suffix}
      </h2>

      <!-- Clean Bullet Points -->
      <div class="space-y-12 text-[27px] leading-[1.65] text-slate-200 max-w-4xl">
        {bullets_content}
      </div>
    </div>

    <!-- Footer Bar -->
    <div class="flex items-center justify-between pt-10 border-t border-[#1E3B56] mb-2 z-10">
      <div class="flex items-center gap-2">
        {dots_html}
      </div>

      <div class="text-[30px] font-extrabold text-teal flex items-center gap-2 tracking-wide font-hook">
        <span>Kaydır</span>
        <span>➔</span>
      </div>
    </div>
    """
    return BASE_HTML_WRAPPER.replace("{{CONTENT}}", content)

def build_cta_slide(topic, slide, slide_idx, total_slides):
    dots_html = generate_dots(slide_idx, total_slides)
    badge_label = slide.get("step_badge", "SONUÇ")

    bullets = slide.get("bullets", [
        {"label": "Kaydet", "text": "Deneme öncesi ve tekrar dönemlerinde stratejini hatırlamak için bu gönderiyi kaydet."},
        {"label": "Paylaş", "text": "Birlikte hazırlandığın kütüphane veya çalışma arkadaşına gönder."},
        {"label": "HukukLA App", "text": "Binlerce soru, güncel mevzuat ve yapay zeka destekli sınav analizleri App Store ve Google Play'de cebinde."},
        {"label": "Altın Kural", "text": "HMGS'yi çok çalışanlar değil; yanlışlarını analiz edip doğru stratejiyle çalışanlar kazanır."}
    ])

    bullets_html_list = []
    for i, b in enumerate(bullets):
        is_last = (i == len(bullets) - 1)
        italic_class = "italic text-slate-300" if is_last else "text-slate-200"
        bullets_html_list.append(f"""
        <p class="{italic_class}">
          <strong class="text-white font-extrabold not-italic">• {b['label']}:</strong>
          {b['text']}
        </p>
        """)
    bullets_content = "".join(bullets_html_list)

    content = f"""
    <div class="flex flex-col mt-6 z-10">
      <!-- Top Pill Badge -->
      <div class="inline-flex items-center px-6 py-2 rounded-full badge-teal text-[20px] font-bold tracking-wider uppercase mb-10 w-max font-hook">
        {badge_label}
      </div>

      <!-- Title -->
      <h2 class="text-[48px] font-extrabold text-white leading-[1.2] tracking-tight uppercase mb-14 font-hook max-w-4xl">
        BU BİLGİYİ KAYDET VE ARKADAŞINLA PAYLAŞ 📌
      </h2>

      <!-- Clean Bullet Points -->
      <div class="space-y-11 text-[27px] leading-[1.65] text-slate-200 max-w-4xl">
        {bullets_content}
      </div>
    </div>

    <!-- Footer Bar -->
    <div class="flex items-center justify-between pt-10 border-t border-[#1E3B56] mb-2 z-10">
      <div class="flex items-center gap-2">
        {dots_html}
      </div>

      <div class="text-[30px] font-extrabold text-teal flex items-center gap-2 tracking-wide font-hook">
        <span>HukukLA</span>
        <span>📲</span>
      </div>
    </div>
    """
    return BASE_HTML_WRAPPER.replace("{{CONTENT}}", content)

def generate_caption(topic):
    bullets_text = "\n".join(topic.get("caption_bullets", []))
    mandatory_copy = topic.get("mandatory_copy", "")
    
    caption = f"""{topic['caption_intro']}

Bu carousel'de öne çıkan noktaları topladım:

{bullets_text}

{topic['caption_question']}

{mandatory_copy}

#hmgs #hukuk #hukukfakültesi #avukat #stajyeravukat #hakimlik #icramüdürlüğü #hukukla
"""
    return caption.strip()

def render_topic_carousel(topic_id, topics_path="carousel_topics.json", downloads_dir=None):
    if downloads_dir is None:
        downloads_dir = DOWNLOADS_BASE

    with open(topics_path, "r", encoding="utf-8") as f:
        topics = json.load(f)

    target_topic = next((t for t in topics if t["id"] == topic_id), None)
    if not target_topic:
        raise ValueError(f"Topic with id {topic_id} not found!")

    folder_name = target_topic["folder_name"]
    output_folder = os.path.join(downloads_dir, folder_name)
    os.makedirs(output_folder, exist_ok=True)

    slides = target_topic["slides"]
    total_slides = len(slides)
    generated_files = []

    temp_html_path = os.path.abspath("temp_slide.html")

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1080, "height": 1350})

        for i, slide in enumerate(slides):
            slide_type = slide.get("type", "content")
            if slide_type == "cover":
                html_str = build_cover_slide(target_topic, total_slides)
                filename = "slide_1_kapak.png"
            elif slide_type == "cta":
                html_str = build_cta_slide(target_topic, slide, i, total_slides)
                filename = f"slide_{i+1}_cta.png"
            else:
                html_str = build_content_slide(target_topic, slide, i, total_slides)
                filename = f"slide_{i+1}.png"

            with open(temp_html_path, "w", encoding="utf-8") as tf:
                tf.write(html_str)

            page.goto(f"file://{temp_html_path}", wait_until="networkidle")
            time.sleep(0.1)
            dest_path = os.path.join(output_folder, filename)
            page.screenshot(path=dest_path)
            generated_files.append(dest_path)
            print(f"  [+] Rendered {filename}")

        browser.close()

    if os.path.exists(temp_html_path):
        os.remove(temp_html_path)

    # Generate Caption Files
    caption_content = generate_caption(target_topic)
    aciklama_path = os.path.join(output_folder, "aciklama.txt")
    caption_path = os.path.join(output_folder, "caption.txt")
    with open(aciklama_path, "w", encoding="utf-8") as f:
        f.write(caption_content)
    with open(caption_path, "w", encoding="utf-8") as f:
        f.write(caption_content)
    generated_files.append(aciklama_path)

    # Update status in topics file
    target_topic["status"] = "completed"
    target_topic["generated_at"] = datetime.now().isoformat()
    target_topic["output_dir"] = output_folder

    with open(topics_path, "w", encoding="utf-8") as f:
        json.dump(topics, f, ensure_ascii=False, indent=2)

    return target_topic, output_folder, generated_files, caption_content
