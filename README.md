# HukukLA Instagram Story Bot

Bu proje, HukukLA için hazırlanan mevzuat sorularını (JSON formatında) Instagram hikaye boyutlarında (1080x1920) yüksek kaliteli PNG görsellerine dönüştüren bir otomasyon sistemidir.

## Özellikler
- Soruları ve cevapları okunaklı, modern bir tasarımda PNG olarak renderlar.
- HTML şablonları üzerinden çalışır (Playwright kullanılarak `headless` tarayıcıda render edilir).
- **Kaldığı Yeri Hatırlama (State Management):** `cursor_state.json` dosyası, sistemin hangi mevzuatta ve o mevzuatın kaçıncı sorusunda kaldığını kaydeder.

## Yeni Yapay Zeka Asistanı İçin Talimatlar (Agent Instructions)
Eğer bu repoyu yeni bir sohbet penceresinde açtıysanız ve kullanıcı "Kaldığımız yerden devam edelim" veya "Sıradaki soruyu ver" diyorsa:
1. Python yüklü olduğundan emin olun. `venv` oluşturup `playwright` yüklemeniz gerekebilir:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install playwright
   playwright install chromium
   ```
2. Kullanıcıya sıradaki soruyu üretmek için aşağıdaki komutu çalıştırın:
   ```bash
   source venv/bin/activate && python3 get_next_question.py
   ```
3. Script çalıştığında `cursor_state.json` dosyasını okuyacak, kaldığı mevzuattan sıradaki soruyu alacak ve `siradaki_soru.png` ile `siradaki_cevap.png` dosyalarını üretecektir.
4. Çıktı başarılı olduğunda kullanıcıya hangi kanunun kaçıncı sorusunun üretildiğini bildirin. `cursor_state.json` dosyasını GitHub'a geri push etmeyi unutmayın (böylece bir sonraki sohbete geçildiğinde state korunmuş olur).
   ```bash
   git add cursor_state.json
   git commit -m "Update state to next question"
   git push
   ```

## Dosya Yapısı
- `templates/`: Soru ve cevaplar için HTML/CSS tasarım şablonları.
- `HukukLA/HUKUKÇIKTILARI/SORULARINJSONLARI/`: İçerisinde mevzuat isimleriyle kaydedilmiş binlerce soruyu barındıran JSON dosyaları.
- `get_next_question.py`: Her çalıştırıldığında sıradaki soruyu bulup PNG'sini üreten asıl script.
- `cursor_state.json`: Sistemin en son hangi soruyu ürettiğini aklında tuttuğu hafıza dosyası.
