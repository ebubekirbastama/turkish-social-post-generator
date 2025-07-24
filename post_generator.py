import stanza
import re
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import yake

# Stanza pipeline (önceden tr modeli indirilmeli: stanza.download('tr'))
nlp = stanza.Pipeline('tr', processors='tokenize,ner', verbose=False)

BASE_HASHTAGS = ["#Beykoz", "#Gündem", "#İstanbulHaber", "#YerelHaber", "#SonDakika"]

def extract_entities(text):
    doc = nlp(text)
    entities = set()
    for sent in doc.sentences:
        for ent in sent.ents:
            entities.add(ent.text)
    return list(entities)

def extract_keywords(text, max_keywords=5):
    kw_extractor = yake.KeywordExtractor(lan="tr", n=1, top=max_keywords)
    keywords = kw_extractor.extract_keywords(text)
    return [kw[0] for kw in keywords]

def generate_hashtags(text):
    hashtags = set(BASE_HASHTAGS)
    
    # 1. NER ile entitylerden hashtag yap
    entities = extract_entities(text)
    for ent in entities:
        tag = "#" + "".join(ent.title().split())
        hashtags.add(tag)
    
    # 2. Anahtar kelimelerden hashtag yap
    keywords = extract_keywords(text)
    for kw in keywords:
        tag = "#" + "".join(kw.title().split())
        hashtags.add(tag)
    
    return list(hashtags)

def parse_input(input_text):
    hashtag_pattern = r"(#SonDakika)"
    url_pattern = r"(https?://\S+)"
    hashtag_match = re.search(hashtag_pattern, input_text)
    url_match = re.search(url_pattern, input_text)
    hashtag = hashtag_match.group(1) if hashtag_match else "#SonDakika"
    url = url_match.group(1) if url_match else ""
    title_part = input_text[:url_match.start()].strip() if url_match else input_text
    title_clean = title_part.replace(hashtag, "").strip()
    return hashtag, title_clean, url

def extract_kurum_kisi(title):
    entities = extract_entities(title)
    if entities:
        # Öncelikli: kurum (ORG) ve kişi (PERSON) değil, tüm entityler zaten liste halinde,
        # ama senin kodda zaten sadece text var, bu yüzden direkt ilk entity kullanabiliriz.
        return entities[0]
    else:
        parts = title.split()
        return " ".join(parts[:2]) if len(parts) >= 2 else title

def extract_haber_basligi(title, kurum_kisi):
    if kurum_kisi and kurum_kisi in title:
        haber = title.replace(kurum_kisi, "").strip(" :–-")
        return haber
    else:
        return title

def create_post(kurum_kisi, haber_basligi, url, hashtags):
    hashtags_str = " ".join(hashtags)
    post = f"""🔥 #SonDakika | {kurum_kisi}:
📝 “{haber_basligi}”

🌲 Detaylar ve gelişmeler için:
👉 {url}

🔖 Hashtagler: {hashtags_str}
"""
    return post

class PostGeneratorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sosyal Medya Post Oluşturucu")
        self.geometry("720x570")
        self.configure(bg="#F3F3F3")  # Açık gri arkaplan, Windows 11 uyumlu

        self.style = ttk.Style(self)
        self.style.theme_use('clam')

        # Stil ayarları
        self.style.configure("TLabel",
                             background="#F3F3F3",
                             foreground="#1C1C1E",
                             font=("Segoe UI Variable", 12))
        self.style.configure("TButton",
                             font=("Segoe UI Variable", 12, "bold"),
                             foreground="#FFFFFF",
                             background="#0078D7",
                             borderwidth=0,
                             focusthickness=3,
                             focuscolor='none')
        self.style.map("TButton",
                       background=[('active', '#005A9E'), ('disabled', '#A6A6A6')])

        # Başlık
        self.label = ttk.Label(self, text="Haber Metni (#SonDakika ... link):")
        self.label.pack(padx=20, pady=(20, 8), anchor="w")

        # Girdi metin kutusu
        self.input_text = scrolledtext.ScrolledText(self, height=6, font=("Segoe UI Variable", 12), wrap=tk.WORD, relief="flat", bd=1)
        self.input_text.pack(fill=tk.X, padx=20, pady=(0, 20))

        # Buton çerçevesi (post oluşturma ve kopyalama yan yana)
        btn_frame = ttk.Frame(self, style="TFrame")
        btn_frame.pack(padx=20, pady=(0, 20), fill=tk.X)

        # Post oluştur butonu
        self.button_generate = ttk.Button(btn_frame, text="📝 Post Oluştur", command=self.generate_post)
        self.button_generate.pack(side=tk.LEFT, ipadx=12, ipady=6)

        # Kopyala butonu
        self.button_copy = ttk.Button(btn_frame, text="📋 Kopyala", command=self.copy_post)
        self.button_copy.pack(side=tk.LEFT, padx=12, ipadx=12, ipady=6)

        # Çıktı başlığı
        self.output_label = ttk.Label(self, text="Oluşan Post:")
        self.output_label.pack(padx=20, pady=(10, 8), anchor="w")

        # Çıktı metin kutusu
        self.output_text = scrolledtext.ScrolledText(self, height=14, font=("Segoe UI Variable", 12), wrap=tk.WORD, relief="flat", bd=1, state="disabled", bg="white")
        self.output_text.pack(fill=tk.BOTH, padx=20, pady=(0, 20), expand=True)

    def generate_post(self):
        input_str = self.input_text.get("1.0", tk.END).strip()
        if not input_str:
            messagebox.showwarning("Uyarı", "Lütfen haber metni girin.")
            return
        try:
            hashtag, title_clean, url = parse_input(input_str)
            kurum_kisi = extract_kurum_kisi(title_clean)
            haber_basligi = extract_haber_basligi(title_clean, kurum_kisi)
            hashtags = generate_hashtags(title_clean)  # <-- Burada sözlük yerine otomatik hashtag üretim fonksiyonu
            post = create_post(kurum_kisi, haber_basligi, url, hashtags)

            self.output_text.config(state="normal")
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert(tk.END, post)
            self.output_text.config(state="disabled")
        except Exception as e:
            messagebox.showerror("Hata", f"Bir hata oluştu:\n{e}")

    def copy_post(self):
        post_text = self.output_text.get("1.0", tk.END).strip()
        if post_text:
            self.clipboard_clear()
            self.clipboard_append(post_text)
            messagebox.showinfo("Başarılı", "Post kopyalandı! 📋")
        else:
            messagebox.showwarning("Uyarı", "Kopyalanacak post bulunamadı.")

if __name__ == "__main__":
    app = PostGeneratorApp()
    app.mainloop()
