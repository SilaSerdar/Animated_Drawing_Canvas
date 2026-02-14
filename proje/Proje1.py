import tkinter as tk
import random
from PIL import Image, ImageTk, ImageColor

TUVAL_GENISLIK = 600
TUVAL_YUKSEKLIK = 500
TOP_BOYUTLARI = {"kucuk": 10, "orta": 20, "buyuk": 30}
TEMEL_HIZ = 2 

RENK_ARKAPLAN = "#222222"
RENK_TUVAL = "#000000"
RENK_YAZI = "#FFFFFF"
RENK_BUTON = "#333333"
RENK_BUTON_USTUNE_GELINCE = "#444444"
RENK_VURGU = "#00BFFF"
RENK_GRI_DAIRE = "#555555"

TEMEL_RESIM = Image.open("football.png").convert("RGBA") 
RESIM_ONBELLEGI = {}

top_sozlugu = {}
top_id_sayaci = 0
animasyon_calisiyor = False

def renkli_top_resmi_getir(yariCap, renk_adi):
    cap = yariCap * 2
    onbellek_anahtari = (cap, renk_adi) 

    if onbellek_anahtari not in RESIM_ONBELLEGI:
        
        renkli_resim = TEMEL_RESIM.copy()
        
        hedef_renk_rgba = ImageColor.getrgb(renk_adi) + (255,) 

        for x in range(renkli_resim.width):
            for y in range(renkli_resim.height):
                r, g, b, a = renkli_resim.getpixel((x, y))
                if a > 0 and (r < 100 and g < 100 and b < 100): 
                    renkli_resim.putpixel((x, y), hedef_renk_rgba)
        
        yeniden_boyutlu_resim = renkli_resim.resize((cap, cap), Image.Resampling.LANCZOS)
        
        RESIM_ONBELLEGI[onbellek_anahtari] = ImageTk.PhotoImage(yeniden_boyutlu_resim)
    
    return RESIM_ONBELLEGI[onbellek_anahtari]


class Top:
    def __init__(self, canvas, yariCap, renk_adi): 
        self.canvas = canvas
        self.yariCap = yariCap
        self.renk_adi = renk_adi 
        
        self.resim_tk = renkli_top_resmi_getir(self.yariCap, self.renk_adi) 
        
        x = random.randint(self.yariCap, TUVAL_GENISLIK - self.yariCap)
        y = random.randint(self.yariCap, TUVAL_YUKSEKLIK - self.yariCap)

        yon_x = random.choice([-1, 1])
        yon_y = random.choice([-1, 1])
        self.dx = yon_x * random.uniform(TEMEL_HIZ, TEMEL_HIZ * 1.5)
        self.dy = yon_y * random.uniform(TEMEL_HIZ, TEMEL_HIZ * 1.5)

        self.kimlik = canvas.create_image(
            x, y,
            image=self.resim_tk, 
            anchor=tk.CENTER
        )

    def hareket_et(self):
        konum = self.canvas.coords(self.kimlik)
        if not konum: return
        
        x, y = konum[0], konum[1] 

        if (x - self.yariCap) <= 0 or (x + self.yariCap) >= TUVAL_GENISLIK: 
            self.dx *= -1
        if (y - self.yariCap) <= 0 or (y + self.yariCap) >= TUVAL_YUKSEKLIK: 
            self.dy *= -1
            
        self.canvas.move(self.kimlik, self.dx, self.dy)

    def hizlan(self):
        self.dx *= 1.25
        self.dy *= 1.25

    def sil(self):
        self.canvas.delete(self.kimlik)


def top_ekle(boyut_anahtari):
    global top_id_sayaci 
    yariCap = TOP_BOYUTLARI[boyut_anahtari]
    renk_adi = secili_renk.get() 
    
    yeni_top = Top(canvas, yariCap, renk_adi) 
    
    top_sozlugu[top_id_sayaci] = yeni_top
    top_id_sayaci += 1 

def animasyonu_baslat():
    global animasyon_calisiyor
    if not animasyon_calisiyor:
        animasyon_calisiyor = True
        animasyon_dongusu()

def animasyonu_durdur(): 
    global animasyon_calisiyor
    animasyon_calisiyor = False

def animasyonu_sifirla():
    global animasyon_calisiyor, top_sozlugu, top_id_sayaci
    animasyonu_durdur()
    
    for top in top_sozlugu.values():
        top.sil()
        
    top_sozlugu.clear() 
    top_id_sayaci = 0 

def animasyonu_hizlandir():
    for top in top_sozlugu.values():
        top.hizlan()

def animasyon_dongusu():
    if animasyon_calisiyor:
        for top in top_sozlugu.values():
            top.hareket_et()
            
        root.after(16, animasyon_dongusu)


def btn_uzerine_gir(event, button): button.config(bg=RENK_BUTON_USTUNE_GELINCE)
def btn_uzerinden_ayril(event, button): button.config(bg=RENK_BUTON)
def boyut_uzerine_gir(event, canvas_widget): canvas_widget.itemconfig("oval", outline=RENK_VURGU, width=2)
def boyut_uzerinden_ayril(event, canvas_widget): canvas_widget.itemconfig("oval", outline="", width=1)
def boyut_basildi(event, canvas_widget): canvas_widget.itemconfig("oval", fill=RENK_VURGU) 
def boyut_birakildi(event, canvas_widget, boyut_anahtari):
    canvas_widget.itemconfig("oval", fill=RENK_GRI_DAIRE) 
    top_ekle(boyut_anahtari)


root = tk.Tk()
root.title("Renkli Futbol Topu Animasyonu (Final Sürüm)") 
root.resizable(False, False)
root.configure(bg=RENK_ARKAPLAN)

secili_renk = tk.StringVar(value="red")

canvas = tk.Canvas(root, width=TUVAL_GENISLIK, height=TUVAL_YUKSEKLIK, bg=RENK_TUVAL, highlightthickness=0)
canvas.pack()

kontrol_cercevesi = tk.Frame(root, pady=10, bg=RENK_ARKAPLAN)
kontrol_cercevesi.pack()

renk_cercevesi = tk.Frame(kontrol_cercevesi, bg=RENK_ARKAPLAN)
renk_cercevesi.pack()

tk.Label(renk_cercevesi, text="Top Rengi Seç:", bg=RENK_ARKAPLAN, fg=RENK_YAZI).pack(side=tk.LEFT, padx=5)

tk.Radiobutton(
    renk_cercevesi, text="Kırmızı", variable=secili_renk, value="red",
    indicatoron=0, bg="red", fg="white", selectcolor="#E00000", width=8, relief="flat", bd=0
).pack(side=tk.LEFT)
tk.Radiobutton(
    renk_cercevesi, text="Mavi", variable=secili_renk, value="blue",
    indicatoron=0, bg="blue", fg="white", selectcolor="#0000E0", width=8, relief="flat", bd=0
).pack(side=tk.LEFT)
tk.Radiobutton(
    renk_cercevesi, text="Sarı", variable=secili_renk, value="yellow",
    indicatoron=0, bg="yellow", fg="black", selectcolor="#E0E000", width=8, relief="flat", bd=0
).pack(side=tk.LEFT)

top_ekle_cercevesi = tk.Frame(kontrol_cercevesi, bg=RENK_ARKAPLAN)
top_ekle_cercevesi.pack(pady=5)

tk.Label(top_ekle_cercevesi, text="Boyut Seç:", bg=RENK_ARKAPLAN, fg=RENK_YAZI).pack(side=tk.LEFT, padx=5)

BUTON_TUVAL_BOYUTU = 64
MERKEZ = BUTON_TUVAL_BOYUTU / 2

boyut_secenekleri = [
    {"key": "kucuk", "radius": TOP_BOYUTLARI["kucuk"]},
    {"key": "orta", "radius": TOP_BOYUTLARI["orta"]},
    {"key": "buyuk", "radius": TOP_BOYUTLARI["buyuk"]}
]

for secenek in boyut_secenekleri:
    boyut_anahtari = secenek["key"]; yariCap = secenek["radius"]
    boyut_tuvali = tk.Canvas(top_ekle_cercevesi, width=BUTON_TUVAL_BOYUTU, height=BUTON_TUVAL_BOYUTU, bg=RENK_ARKAPLAN, highlightthickness=0)
    
    boyut_tuvali.create_oval(MERKEZ - yariCap, MERKEZ - yariCap, MERKEZ + yariCap, MERKEZ + yariCap, fill=RENK_GRI_DAIRE, outline="", tags="oval")
    
    onizleme_resmi = renkli_top_resmi_getir(yariCap, "grey")
    
    boyut_tuvali.image_reference = onizleme_resmi 
    
    boyut_tuvali.create_image(MERKEZ, MERKEZ, image=onizleme_resmi)
    
    boyut_tuvali.bind("<Enter>", lambda e, c=boyut_tuvali: boyut_uzerine_gir(e, c))
    boyut_tuvali.bind("<Leave>", lambda e, c=boyut_tuvali: boyut_uzerinden_ayril(e, c))
    boyut_tuvali.bind("<Button-1>", lambda e, c=boyut_tuvali: boyut_basildi(e, c))
    boyut_tuvali.bind("<ButtonRelease-1>", lambda e, c=boyut_tuvali, sk=boyut_anahtari: boyut_birakildi(e, c, sk))
    boyut_tuvali.pack(side=tk.LEFT, padx=5)

eylem_buton_cercevesi = tk.Frame(kontrol_cercevesi, bg=RENK_ARKAPLAN)
eylem_buton_cercevesi.pack(pady=5)

buton_secenekleri = [
    {"text": "BAŞLAT", "command": animasyonu_baslat},
    {"text": "DURDUR", "command": animasyonu_durdur},
    {"text": "SIFIRLA", "command": animasyonu_sifirla},
    {"text": "HIZLANDIR", "command": animasyonu_hizlandir}
]

for secenek in buton_secenekleri:
    buton = tk.Button(
        eylem_buton_cercevesi, text=secenek["text"], command=secenek["command"], width=8,
        bg=RENK_BUTON, fg=RENK_YAZI, relief="flat",
        activebackground=RENK_VURGU, activeforeground=RENK_ARKAPLAN
    )
    buton.bind("<Enter>", lambda e, b=buton: btn_uzerine_gir(e, b))
    buton.bind("<Leave>", lambda e, b=buton: btn_uzerinden_ayril(e, b))
    buton.pack(side=tk.LEFT, padx=5)

root.mainloop()