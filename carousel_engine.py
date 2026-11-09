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
  <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@700;800;900&family=Plus+Jakarta+Sans:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
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
      background: radial-gradient(circle at 85% 18%, #102B40 0%, #0B1422 45%, #070D16 100%);
      color: #FFFFFF;
    }
    .font-hook {
      font-family: 'Montserrat', sans-serif;
      font-weight: 900;
      line-height: 0.98;
      letter-spacing: -0.02em;
    }
    .text-gold {
      color: #FBBF24;
    }
    .text-cyan {
      color: #22D3EE;
    }
    .glass-card {
      background: rgba(15, 29, 47, 0.82);
      backdrop-filter: blur(20px);
      -webkit-backdrop-filter: blur(20px);
      border: 1px solid rgba(255, 255, 255, 0.1);
      box-shadow: 0 20px 50px rgba(0, 0, 0, 0.5);
    }
    .glass-card-accent {
      background: linear-gradient(145deg, rgba(16, 43, 64, 0.9) 0%, rgba(11, 20, 34, 0.95) 100%);
      border: 1px solid rgba(34, 211, 238, 0.3);
      box-shadow: 0 20px 50px rgba(0, 0, 0, 0.6), 0 0 30px rgba(34, 211, 238, 0.08);
    }
  </style>
</head>
<body class="relative flex flex-col justify-between p-20 selection:bg-cyan-500">
  {{CONTENT}}
</body>
</html>
"""

def generate_dots(current_idx, total_slides):
    dots = []
    for i in range(total_slides):
        if i == current_idx:
            dots.append('<span class="w-8 h-3 rounded-full bg-[#22D3EE] transition-all"></span>')
        elif i < current_idx:
            dots.append('<span class="w-8 h-3 rounded-full bg-[#22D3EE]/80"></span>')
        else:
            dots.append('<span class="w-2.5 h-2.5 rounded-full bg-slate-700"></span>')
    return "".join(dots)

def build_cover_slide(topic, total_slides):
    dots_html = generate_dots(0, total_slides)
    
    hook_lines = topic.get("hook_lines", ["ÇOĞU", "HUKUKÇU", "BUNU", "BİLMİYOR:"])
    highlight_idx = topic.get("highlight_line_idx", 1)
    
    formatted_lines = []
    for idx, line in enumerate(hook_lines):
        if idx == highlight_idx:
            formatted_lines.append(f'<span class="text-[#FBBF24]">{line}</span>')
        else:
            formatted_lines.append(line)
    hook_html = "<br>\n      ".join(formatted_lines)

    content = f"""
    <div class="flex flex-col space-y-7 mt-8">
      <!-- Huge Impact Hook -->
      <div class="font-hook text-[100px] uppercase text-white tracking-tight">
        {hook_html}
      </div>

      <!-- Cyan Topic Title -->
      <div class="text-[44px] font-extrabold text-[#22D3EE] tracking-tight leading-tight">
        {topic['topic_cyan_title']}
      </div>

      <!-- Uppercase Principle -->
      <div class="text-[21px] font-bold text-slate-400 tracking-wider uppercase max-w-3xl leading-snug">
        {topic['core_principle_upper']}
      </div>

      <!-- Explanatory Hook Sentence -->
      <div class="text-[26px] text-slate-200 leading-relaxed max-w-3xl pt-1 font-normal">
        {topic['hook_desc']}
      </div>

      <!-- Pushpin Text -->
      <div class="text-[24px] text-slate-300 font-medium pt-3 flex items-center gap-2">
        {topic['pin_text']}
      </div>
    </div>

    <!-- Footer Bar -->
    <div class="flex items-center justify-between pt-10 border-t border-slate-800/80 mb-2">
      <div class="flex items-center gap-2.5">
        {dots_html}
      </div>

      <div class="text-[28px] font-extrabold text-[#22D3EE] flex items-center gap-2 tracking-wide font-hook">
        <span>Kaydır</span>
        <span>➔</span>
      </div>
    </div>
    """
    return BASE_HTML_WRAPPER.replace("{{CONTENT}}", content)

def build_content_slide(topic, slide, slide_idx, total_slides):
    dots_html = generate_dots(slide_idx, total_slides)
    
    content = f"""
    <!-- Top Header -->
    <div class="flex items-center justify-between pt-4">
      <div class="flex items-center gap-3">
        <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-cyan-500 to-indigo-600 flex items-center justify-center font-black text-xl shadow-lg shadow-cyan-500/20">
          ⚖️
        </div>
        <span class="text-2xl font-black tracking-tight text-white font-hook">HukukLA</span>
      </div>
      
      <div class="px-4 py-1.5 rounded-full bg-[#132B3C] border border-[#22D3EE]/30 text-[#22D3EE] text-xs font-bold tracking-widest uppercase">
        {slide.get('step_badge', f'{slide_idx}. ADIM')}
      </div>
    </div>

    <!-- Main Content Area -->
    <div class="flex flex-col my-auto space-y-6 py-4">
      <!-- Slide Title -->
      <h2 class="text-[44px] font-extrabold tracking-tight leading-tight text-white font-hook">
        {slide['title']}
      </h2>

      <!-- Problem Card -->
      <div class="glass-card rounded-3xl p-7 border-l-4 border-l-red-500/80">
        <div class="text-xs font-extrabold tracking-wider text-red-400 uppercase mb-2 font-hook">
          {slide['problem_title']}
        </div>
        <div class="text-[22px] text-slate-200 leading-relaxed font-normal">
          {slide['problem_desc']}
        </div>
      </div>

      <!-- Solution Card -->
      <div class="glass-card rounded-3xl p-7 border-l-4 border-l-[#22D3EE]">
        <div class="text-xs font-extrabold tracking-wider text-[#22D3EE] uppercase mb-2 font-hook">
          {slide['solution_title']}
        </div>
        <div class="text-[22px] text-slate-100 leading-relaxed font-medium">
          {slide['solution_desc']}
        </div>
      </div>

      <!-- Tactic Callout Box -->
      <div class="glass-card-accent rounded-2xl p-5 flex items-start gap-4">
        <div class="text-2xl mt-0.5">💡</div>
        <div class="text-[19px] text-[#FBBF24] font-medium leading-relaxed">
          {slide['tactic']}
        </div>
      </div>
    </div>

    <!-- Footer Bar -->
    <div class="flex items-center justify-between pt-8 border-t border-slate-800/80 mb-2">
      <div class="flex items-center gap-2.5">
        {dots_html}
      </div>

      <div class="text-[28px] font-extrabold text-[#22D3EE] flex items-center gap-2 tracking-wide font-hook">
        <span>Kaydır</span>
        <span>➔</span>
      </div>
    </div>
    """
    return BASE_HTML_WRAPPER.replace("{{CONTENT}}", content)

def build_cta_slide(topic, slide, slide_idx, total_slides):
    dots_html = generate_dots(slide_idx, total_slides)

    content = f"""
    <!-- Top Header -->
    <div class="flex items-center justify-between pt-4">
      <div class="flex items-center gap-3">
        <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-cyan-500 to-indigo-600 flex items-center justify-center font-black text-xl shadow-lg shadow-cyan-500/20">
          ⚖️
        </div>
        <span class="text-2xl font-black tracking-tight text-white font-hook">HukukLA</span>
      </div>
      
      <div class="px-4 py-1.5 rounded-full bg-[#132B3C] border border-[#22D3EE]/30 text-[#22D3EE] text-xs font-bold tracking-widest uppercase">
        SONUÇ
      </div>
    </div>

    <!-- Center Content -->
    <div class="flex flex-col my-auto space-y-8 py-4">
      <!-- Title -->
      <h2 class="text-[48px] font-extrabold tracking-tight leading-tight text-white font-hook max-w-2xl">
        {slide['title']}
      </h2>

      <!-- Action Cards -->
      <div class="grid grid-cols-2 gap-5">
        <div class="glass-card rounded-3xl p-7 border-t-2 border-t-[#FBBF24]">
          <div class="flex items-center gap-3 mb-3">
            <span class="text-3xl">🔖</span>
            <h4 class="text-2xl font-bold text-white font-hook">{slide['action_1_title']}</h4>
          </div>
          <p class="text-lg text-slate-300 leading-relaxed font-normal">
            {slide['action_1_desc']}
          </p>
        </div>

        <div class="glass-card rounded-3xl p-7 border-t-2 border-t-[#22D3EE]">
          <div class="flex items-center gap-3 mb-3">
            <span class="text-3xl">👥</span>
            <h4 class="text-2xl font-bold text-white font-hook">{slide['action_2_title']}</h4>
          </div>
          <p class="text-lg text-slate-300 leading-relaxed font-normal">
            {slide['action_2_desc']}
          </p>
        </div>
      </div>

      <!-- App Banner -->
      <div class="glass-card-accent rounded-3xl p-8 flex items-center gap-6">
        <div class="w-20 h-20 rounded-2xl bg-gradient-to-br from-[#22D3EE] to-indigo-600 flex items-center justify-center text-4xl shadow-xl flex-shrink-0">
          📱
        </div>
        <div class="flex flex-col space-y-1">
          <div class="text-2xl font-black text-white font-hook tracking-tight">{slide['app_title']}</div>
          <div class="text-base text-slate-300 font-normal leading-relaxed">{slide['app_desc']}</div>
          <div class="pt-2 flex items-center gap-4 text-xs font-bold text-[#22D3EE] tracking-wider uppercase">
            <span>App Store</span>
            <span class="text-slate-500">•</span>
            <span>Google Play</span>
            <span class="text-slate-500">•</span>
            <span>hukukla.app</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Footer Bar -->
    <div class="flex items-center justify-between pt-8 border-t border-slate-800/80 mb-2">
      <div class="flex items-center gap-2.5">
        {dots_html}
      </div>

      <div class="text-[28px] font-extrabold text-[#22D3EE] flex items-center gap-2 tracking-wide font-hook">
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
