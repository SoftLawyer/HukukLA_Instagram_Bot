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
  <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,600;0,700;0,800;0,900;1,700&family=Plus+Jakarta+Sans:wght@400;500;600;700;800;900&family=Outfit:wght@600;700;800;900&display=swap" rel="stylesheet">
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
      background-color: #060913;
      color: #FFFFFF;
    }
    .font-serif-title {
      font-family: 'Playfair Display', Georgia, serif;
    }
    .font-heading {
      font-family: 'Outfit', sans-serif;
    }
    .text-gold {
      color: #FBBF24;
    }
    .text-red {
      color: #F87171;
    }
    .text-emerald {
      color: #34D399;
    }
    .text-cyan {
      color: #38BDF8;
    }
    .glass-pill {
      background: rgba(255, 255, 255, 0.07);
      backdrop-filter: blur(14px);
      -webkit-backdrop-filter: blur(14px);
      border: 1px solid rgba(255, 255, 255, 0.14);
    }
    .glass-card {
      background: rgba(15, 23, 42, 0.78);
      backdrop-filter: blur(20px);
      -webkit-backdrop-filter: blur(20px);
      border: 1px solid rgba(255, 255, 255, 0.11);
      box-shadow: 0 24px 60px rgba(0, 0, 0, 0.5), inset 0 1px 0 rgba(255, 255, 255, 0.12);
    }
    .glass-card-accent {
      background: linear-gradient(145deg, rgba(30, 41, 59, 0.85) 0%, rgba(15, 23, 42, 0.95) 100%);
      border: 1px solid rgba(245, 158, 11, 0.25);
      box-shadow: 0 20px 50px rgba(0, 0, 0, 0.6), 0 0 30px rgba(245, 158, 11, 0.08);
    }
  </style>
</head>
<body class="relative flex flex-col justify-between selection:bg-amber-500">
  <!-- Dynamic Ambient Glows -->
  <div class="absolute -top-36 -left-36 w-[620px] h-[620px] bg-blue-600/18 rounded-full blur-[140px] pointer-events-none"></div>
  <div class="absolute top-[38%] -right-36 w-[560px] h-[560px] bg-indigo-600/20 rounded-full blur-[150px] pointer-events-none"></div>
  <div class="absolute -bottom-36 left-[18%] w-[620px] h-[620px] bg-amber-600/12 rounded-full blur-[150px] pointer-events-none"></div>
  <div class="absolute inset-0 bg-[linear-gradient(to_right,rgba(255,255,255,0.02)_1px,transparent_1px),linear-gradient(to_bottom,rgba(255,255,255,0.02)_1px,transparent_1px)] bg-[size:52px_52px] pointer-events-none"></div>

  <!-- Content Injection -->
  {{CONTENT}}
</body>
</html>
"""

def generate_dots(current_idx, total_slides):
    dots = []
    for i in range(total_slides):
        if i == current_idx:
            dots.append('<span class="w-8 h-3 rounded-full bg-amber-400 transition-all duration-300"></span>')
        else:
            dots.append('<span class="w-3 h-3 rounded-full bg-slate-700/80"></span>')
    return "".join(dots)

def build_cover_slide(topic, total_slides):
    dots_html = generate_dots(0, total_slides)
    content = f"""
    <div class="relative z-10 flex flex-col justify-between h-full p-16">
      <!-- Header -->
      <div class="flex items-center justify-between">
        <div class="flex items-center gap-3.5">
          <div class="w-11 h-11 rounded-2xl bg-gradient-to-br from-indigo-500 via-purple-600 to-amber-500 flex items-center justify-center font-black text-2xl shadow-xl shadow-indigo-500/30">
            ⚖️
          </div>
          <div class="flex flex-col">
            <span class="text-2xl font-black tracking-tight text-white font-heading">HukukLA</span>
            <span class="text-[11px] font-semibold text-slate-400 tracking-wider uppercase">Geleceğin Hukuk Platformu</span>
          </div>
        </div>
        
        <!-- Instagram Carousel Icon Pill -->
        <div class="glass-pill px-4 py-2 rounded-xl flex items-center gap-2">
          <svg class="w-5 h-5 text-amber-400" fill="currentColor" viewBox="0 0 24 24">
            <path d="M4 6a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v9a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6zm13-2h1a2 2 0 0 1 2 2v9a2 2 0 0 1-2 2h-1V4z"/>
          </svg>
          <span class="text-xs font-bold tracking-wider text-slate-200 uppercase">Kaydırmalı</span>
        </div>
      </div>

      <!-- Center Hero / Hook -->
      <div class="flex flex-col my-auto py-6">
        <!-- Category Pill -->
        <div class="inline-flex items-center gap-2.5 px-5 py-2.5 rounded-full glass-pill border-amber-500/30 w-max mb-10 shadow-lg shadow-amber-500/10">
          <span class="text-lg">{topic['badge_icon']}</span>
          <span class="text-sm font-extrabold tracking-widest uppercase text-amber-300 font-heading">{topic['badge_text']}</span>
        </div>

        <!-- Hook Headline -->
        <h1 class="text-[64px] font-bold leading-[1.12] tracking-tight mb-8 font-serif-title">
          {topic['hook_title_html']}
        </h1>

        <!-- Curiosity Subtext -->
        <p class="text-2xl text-slate-300 italic font-medium leading-relaxed max-w-3xl border-l-3 border-amber-400/50 pl-6 py-1">
          {topic['curiosity_subtext']}
        </p>
      </div>

      <!-- Footer -->
      <div class="pt-8 border-t border-slate-800/80 flex items-center justify-between">
        <div class="flex items-center gap-2">
          {dots_html}
        </div>
        <div class="flex items-center gap-3">
          <div class="glass-pill px-6 py-3 rounded-full flex items-center gap-2 text-slate-200 text-sm font-bold tracking-wide shadow-md">
            <span>Kaydır</span>
            <span class="text-amber-400">➡️</span>
            <span class="text-slate-400 font-normal text-xs">(1/{total_slides})</span>
          </div>
        </div>
      </div>

      <!-- Watermark -->
      <div class="absolute bottom-5 left-1/2 -translate-x-1/2 text-xs text-slate-600 font-semibold tracking-widest uppercase">
        hukukla.app
      </div>
    </div>
    """
    return BASE_HTML_WRAPPER.replace("{{CONTENT}}", content)

def build_content_slide(topic, slide, slide_idx, total_slides):
    dots_html = generate_dots(slide_idx, total_slides)
    content = f"""
    <div class="relative z-10 flex flex-col justify-between h-full p-16">
      <!-- Header -->
      <div class="flex items-center justify-between">
        <div class="flex items-center gap-3.5">
          <div class="w-11 h-11 rounded-2xl bg-gradient-to-br from-indigo-500 via-purple-600 to-amber-500 flex items-center justify-center font-black text-2xl shadow-xl shadow-indigo-500/30">
            ⚖️
          </div>
          <span class="text-2xl font-black tracking-tight text-white font-heading">HukukLA</span>
        </div>
        
        <!-- Slide Count Pill -->
        <div class="glass-pill px-4 py-2 rounded-xl flex items-center gap-2">
          <span class="text-xs font-bold tracking-widest text-amber-400 font-heading">SLIDE {slide_idx+1:02d} / {total_slides:02d}</span>
        </div>
      </div>

      <!-- Main Body -->
      <div class="flex flex-col my-auto space-y-6">
        <!-- Step Badge -->
        <div class="inline-flex items-center gap-2 px-4 py-1.5 rounded-full glass-pill border-slate-700 w-max">
          <span class="w-2 h-2 rounded-full bg-amber-400"></span>
          <span class="text-xs font-extrabold tracking-widest uppercase text-slate-300 font-heading">{slide.get('step_badge', 'ÖNEMLİ DETAY')}</span>
        </div>

        <!-- Slide Title -->
        <h2 class="text-5xl font-extrabold tracking-tight leading-tight text-white font-heading">
          {slide['title']}
        </h2>

        <!-- Cards Container -->
        <div class="space-y-4 pt-2">
          <!-- Problem / Warning Card -->
          <div class="glass-card rounded-3xl p-7 border-l-4 border-l-red-500/80">
            <div class="text-xs font-extrabold tracking-wider text-red-400 uppercase mb-2 font-heading">
              {slide['problem_title']}
            </div>
            <div class="text-xl text-slate-300 leading-relaxed font-normal">
              {slide['problem_desc']}
            </div>
          </div>

          <!-- Solution / Golden Rule Card -->
          <div class="glass-card rounded-3xl p-7 border-l-4 border-l-emerald-500/80">
            <div class="text-xs font-extrabold tracking-wider text-emerald-400 uppercase mb-2 font-heading">
              {slide['solution_title']}
            </div>
            <div class="text-xl text-slate-200 leading-relaxed font-medium">
              {slide['solution_desc']}
            </div>
          </div>

          <!-- Tactic Box -->
          <div class="glass-card-accent rounded-2xl p-5 flex items-start gap-4">
            <div class="text-2xl mt-0.5">💡</div>
            <div class="text-lg text-amber-200 font-medium leading-relaxed">
              {slide['tactic']}
            </div>
          </div>
        </div>
      </div>

      <!-- Footer -->
      <div class="pt-8 border-t border-slate-800/80 flex items-center justify-between">
        <div class="flex items-center gap-2">
          {dots_html}
        </div>
        <div class="flex items-center gap-3">
          <div class="glass-pill px-6 py-3 rounded-full flex items-center gap-2 text-slate-200 text-sm font-bold tracking-wide">
            <span>Kaydır</span>
            <span class="text-amber-400">➡️</span>
            <span class="text-slate-400 font-normal text-xs">({slide_idx+1}/{total_slides})</span>
          </div>
        </div>
      </div>

      <!-- Watermark -->
      <div class="absolute bottom-5 left-1/2 -translate-x-1/2 text-xs text-slate-600 font-semibold tracking-widest uppercase">
        hukukla.app
      </div>
    </div>
    """
    return BASE_HTML_WRAPPER.replace("{{CONTENT}}", content)

def build_cta_slide(topic, slide, slide_idx, total_slides):
    dots_html = generate_dots(slide_idx, total_slides)
    content = f"""
    <div class="relative z-10 flex flex-col justify-between h-full p-16">
      <!-- Header -->
      <div class="flex items-center justify-between">
        <div class="flex items-center gap-3.5">
          <div class="w-11 h-11 rounded-2xl bg-gradient-to-br from-indigo-500 via-purple-600 to-amber-500 flex items-center justify-center font-black text-2xl shadow-xl shadow-indigo-500/30">
            ⚖️
          </div>
          <span class="text-2xl font-black tracking-tight text-white font-heading">HukukLA</span>
        </div>
        
        <div class="glass-pill px-4 py-2 rounded-xl flex items-center gap-2">
          <span class="text-xs font-bold tracking-widest text-emerald-400 font-heading">FİNAL SLIDE</span>
        </div>
      </div>

      <!-- Center Content -->
      <div class="flex flex-col my-auto space-y-8">
        <!-- Badge -->
        <div class="inline-flex items-center gap-2.5 px-5 py-2 rounded-full glass-pill border-amber-500/30 w-max shadow-lg shadow-amber-500/10">
          <span class="text-lg">🎯</span>
          <span class="text-sm font-extrabold tracking-widest uppercase text-amber-300 font-heading">{slide.get('badge_text', 'ÖZET & AKSİYON')}</span>
        </div>

        <!-- Title -->
        <h2 class="text-5xl font-extrabold tracking-tight leading-tight text-white font-serif-title max-w-2xl">
          {slide['title']}
        </h2>

        <!-- Action Items Grid -->
        <div class="grid grid-cols-2 gap-5 pt-2">
          <!-- Kaydet -->
          <div class="glass-card rounded-3xl p-6 flex flex-col justify-between border-t-2 border-t-amber-500/60">
            <div class="flex items-center gap-3 mb-3">
              <span class="text-3xl">🔖</span>
              <h4 class="text-2xl font-bold text-white font-heading">{slide['action_1_title']}</h4>
            </div>
            <p class="text-base text-slate-300 leading-relaxed">
              {slide['action_1_desc']}
            </p>
          </div>

          <!-- Paylaş -->
          <div class="glass-card rounded-3xl p-6 flex flex-col justify-between border-t-2 border-t-indigo-500/60">
            <div class="flex items-center gap-3 mb-3">
              <span class="text-3xl">👥</span>
              <h4 class="text-2xl font-bold text-white font-heading">{slide['action_2_title']}</h4>
            </div>
            <p class="text-base text-slate-300 leading-relaxed">
              {slide['action_2_desc']}
            </p>
          </div>
        </div>

        <!-- HukukLA App Banner -->
        <div class="glass-card-accent rounded-3xl p-8 flex items-center gap-6">
          <div class="w-20 h-20 rounded-2xl bg-gradient-to-br from-indigo-500 to-amber-500 flex items-center justify-center text-4xl shadow-2xl flex-shrink-0">
            📱
          </div>
          <div class="flex flex-col space-y-1">
            <div class="text-2xl font-black text-white font-heading tracking-tight">{slide['app_title']}</div>
            <div class="text-base text-slate-300 font-medium leading-relaxed">{slide['app_desc']}</div>
            <div class="pt-2 flex items-center gap-4 text-xs font-bold text-amber-300 tracking-wider uppercase">
              <span>App Store</span>
              <span class="text-slate-500">•</span>
              <span>Google Play</span>
              <span class="text-slate-500">•</span>
              <span>hukukla.app</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Footer -->
      <div class="pt-8 border-t border-slate-800/80 flex items-center justify-between">
        <div class="flex items-center gap-2">
          {dots_html}
        </div>
        <div class="flex items-center gap-3">
          <div class="glass-pill px-6 py-3 rounded-full flex items-center gap-2 text-amber-300 text-sm font-extrabold tracking-wider uppercase">
            <span>HukukLA App</span>
            <span>📲</span>
          </div>
        </div>
      </div>

      <!-- Watermark -->
      <div class="absolute bottom-5 left-1/2 -translate-x-1/2 text-xs text-slate-600 font-semibold tracking-widest uppercase">
        hukukla.app
      </div>
    </div>
    """
    return BASE_HTML_WRAPPER.replace("{{CONTENT}}", content)

def render_topic_carousel(topic_id, topics_path="carousel_topics.json", downloads_dir=None):
    if downloads_dir is None:
        downloads_dir = DOWNLOADS_BASE

    with open(topics_path, "r", encoding="utf-8") as f:
        topics = json.load(f)

    target_topic = None
    for t in topics:
        if t["id"] == topic_id:
            target_topic = t
            break

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
            time.sleep(0.1) # Small render settling
            dest_path = os.path.join(output_folder, filename)
            page.screenshot(path=dest_path)
            generated_files.append(dest_path)
            print(f"  [+] Rendered {filename}")

        browser.close()

    if os.path.exists(temp_html_path):
        os.remove(temp_html_path)

    # Update status in topics file
    target_topic["status"] = "completed"
    target_topic["generated_at"] = datetime.now().isoformat()
    target_topic["output_dir"] = output_folder

    with open(topics_path, "w", encoding="utf-8") as f:
        json.dump(topics, f, ensure_ascii=False, indent=2)

    return target_topic, output_folder, generated_files
