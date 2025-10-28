# peluditos_app.py
import customtkinter as ctk
from PIL import Image, ImageTk
import webbrowser
import os
import sys
from urllib.parse import quote_plus
import tkinter as tk

# --------------------------
# Ajustes visuales generales
# --------------------------
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("green")  # esquema base (usaremos colores personalizados en widgets)

# Colores principales
CORAL = "#F05A28"
WHITESMOKE = "#FFFFFF"
CARD_BORDER = "#e6e6e6"
TEXT_MUTED = "#666666"

# --------------------------
# Datos de ejemplo (modelo)
# --------------------------
MASCOTAS = [
    {
        "nombre": "Luna",
        "edad": "1 año",
        "especie": "Gato",
        "descripcion": "Tímida, busca un hogar tranquilo y sin otros gatos. Ideal para personas que teletrabajan.",
        "raza": "Maine Coon",
        "sexo": "♀",
        "foto_path": "assets/gato2.jpeg",
        "contacto_wpp": "5492964600521"
    },
    {
        "nombre": "Rocky",
        "edad": "8 años",
        "especie": "Perro",
        "descripcion": "Energético, necesita espacio y ejercicio diario. Muy leal y protector.",
        "raza": "Husky Siberiano",
        "sexo": "♂",
        "foto_path": "assets/Oso.jpg",
        "contacto_wpp": "5492964600521"
    },
    {
        "nombre": "Bella",
        "edad": "7 meses",
        "especie": "Gato",
        "descripcion": "Juguetona y muy curiosa. Ideal para familias con niños pequeños.",
        "raza": "Mestizo",
        "sexo": "♀",
        "foto_path": "assets/manchas.jpg",
        "contacto_wpp": "5492964600521"
    },
    {
        "nombre": "Max",
        "edad": "2 años",
        "especie": "Perro",
        "descripcion": "Muy amigable y leal. Le encanta jugar a la pelota.",
        "raza": "Labrador",
        "sexo": "♂",
        "foto_path": "assets/perro2.jpeg",
        "contacto_wpp": "5492964600521"
    }
]

# --------------------------
# Helper functions
# --------------------------
def resource_path(relative_path):
    """Soporta PyInstaller: devuelve ruta absoluta si se empaqueta."""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def open_whatsapp(contact_number: str, pet_name: str):
    """Abre WhatsApp Web / App con mensaje prellenado."""
    message = f"Hola! Estoy interesadx en adoptar a {pet_name}. ¿Me dan más información?"
    encoded = quote_plus(message)
    # usar wa.me con numero internacional sin signos (ej: 549296...)
    url = f"https://wa.me/{contact_number}?text={encoded}"
    webbrowser.open(url)

def load_image_safe(path, size=None):
    """Carga imagen con PIL; devuelve PhotoImage o None si falla."""
    try:
        pil = Image.open(resource_path(path))
        if size:
            pil = pil.resize(size, Image.LANCZOS)
        return ImageTk.PhotoImage(pil)
    except Exception:
        return None

# --------------------------
# Splash Screen
# --------------------------
class SplashScreen(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Peluditos en Adopción - Iniciando")
        self.geometry("420x740")
        self.overrideredirect(True)

        # centrar
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        x = (sw//2) - (420//2)
        y = (sh//2) - (740//2)
        self.geometry(f"420x740+{x}+{y}")

        # Layout: cabecera coral + contenido blanco inferior en curva simulada
        self.grid_rowconfigure((0,1,2), weight=1)
        self.grid_columnconfigure(0, weight=1)

        top = ctk.CTkFrame(self, fg_color=CORAL, corner_radius=0)
        top.grid(row=0, column=0, sticky="nsew")

        # Logo/title centro
        title = ctk.CTkLabel(top, text="Peluditos\nen Adopción", font=ctk.CTkFont(size=34, weight="bold"),
                             text_color="white", justify="center")
        title.place(relx=0.5, rely=0.25, anchor="center")

        # optional: colocar varios PNGs decorativos si existen en assets/ (no obligatorios)
        deco1 = load_image_safe("assets/deco1.png", (80,80))
        if deco1:
            lbl = ctk.CTkLabel(top, image=deco1, text="")
            lbl.image = deco1
            lbl.place(relx=0.2, rely=0.6, anchor="center")
        deco2 = load_image_safe("assets/deco2.png", (80,80))
        if deco2:
            lbl2 = ctk.CTkLabel(top, image=deco2, text="")
            lbl2.image = deco2
            lbl2.place(relx=0.8, rely=0.6, anchor="center")

        # Welcome frame (blanco)
        bottom = ctk.CTkFrame(self, fg_color=WHITESMOKE, corner_radius=30)
        bottom.grid(row=1, column=0, sticky="nsew", padx=20, pady=0)
        bottom.grid_rowconfigure(0, weight=1)
        bottom.grid_columnconfigure(0, weight=1)

        lbl_w = ctk.CTkLabel(bottom, text="¡Encontrá a tu compañero ideal!", font=ctk.CTkFont(size=16, weight="bold"),
                             text_color="#333")
        lbl_w.place(relx=0.5, rely=0.25, anchor="center")

        desc = ctk.CTkLabel(bottom, text="Explorá perfiles, mirá fotos y contactá por WhatsApp.",
                            wraplength=320, justify="center", text_color=TEXT_MUTED)
        desc.place(relx=0.5, rely=0.4, anchor="center")

        # Progressbar
        self.progress = ctk.CTkProgressBar(bottom, mode="indeterminate", height=8)
        self.progress.place(relx=0.5, rely=0.6, anchor="center", relwidth=0.8)
        self.progress.start()

        # small credits
        foot = ctk.CTkLabel(bottom, text="Peluditos - Comunidad de adopción", text_color="#999", font=ctk.CTkFont(size=10))
        foot.place(relx=0.5, rely=0.85, anchor="center")

        # iniciar app principal luego de 1800ms
        self.after(1800, self.launch_main)

    def launch_main(self):
        self.progress.stop()
        self.destroy()
        app = AppAdopcion()
        app.mainloop()

# --------------------------
# Main App
# --------------------------
class AppAdopcion(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Peluditos en Adopción")
        self.geometry("920x760")
        self.minsize(600, 600)

        # top bar
        header = ctk.CTkFrame(self, fg_color=CORAL)
        header.grid(row=0, column=0, sticky="ew")
        header.grid_columnconfigure(0, weight=1)

        title = ctk.CTkLabel(header, text="🐾 Peluditos en Adopción", font=ctk.CTkFont(size=22, weight="bold"),
                             text_color="white")
        title.grid(row=0, column=0, padx=20, pady=14, sticky="w")

        # scrollable frame (catálogo)
        content = ctk.CTkFrame(self, fg_color=WHITESMOKE)
        content.grid(row=1, column=0, sticky="nsew", padx=12, pady=12)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # etiqueta "Favoritos" o "¡Conócelos!"
        lbl_section = ctk.CTkLabel(content, text="Peludos en Adopción", font=ctk.CTkFont(size=18, weight="bold"),
                                   text_color=CORAL)
        lbl_section.pack(anchor="nw", padx=10, pady=(6, 2))

        # ScrollableFrame con tarjetas
        self.scroll = ctk.CTkScrollableFrame(content, width=800, height=600, fg_color=WHITESMOKE, corner_radius=10)
        self.scroll.pack(fill="both", expand=True, padx=10, pady=6)
        self.scroll.grid_columnconfigure((0,1), weight=1)

        # Cargar icono de whatsapp (assets/icon.png)
        self.wpp_icon_img = load_image_safe("assets/icon.png", (22,22))

        # crear las tarjetas
        self.load_pet_cards()

    def load_pet_cards(self):
        # limpiar hijos si recarga
        for w in self.scroll.winfo_children():
            w.destroy()

        # crear tarjetas en 2 columnas
        for idx, pet in enumerate(MASCOTAS):
            r = idx // 2
            c = idx % 2
            card = self.make_card(self.scroll, pet)
            card.grid(row=r, column=c, padx=12, pady=12, sticky="nsew")

    def make_card(self, parent, pet):
        # Card frame blanco con esquina redondeada
        card = ctk.CTkFrame(parent, corner_radius=12, fg_color="white", border_width=1, border_color=CARD_BORDER)
        card.grid_columnconfigure(0, weight=1)

        # imagen (thumbnail)
        img_w, img_h = 320, 180
        img = load_image_safe(pet.get("foto_path", ""), (img_w, img_h))
        if img:
            img_label = ctk.CTkLabel(card, image=img, text="")
            img_label.image = img
        else:
            placeholder = ctk.CTkLabel(card, text="Imagen\nno encontrada", width=img_w, height=img_h,
                                       fg_color="#f0f0f0", text_color="#888", justify="center")
            img_label = placeholder
        img_label.grid(row=0, column=0, padx=10, pady=(10,6))

        # info: nombre + edad + especie en una banda coral debajo de la imagen
        band = ctk.CTkFrame(card, fg_color=CORAL, corner_radius=8)
        band.grid(row=1, column=0, sticky="ew", padx=10, pady=(0,8))
        band.grid_columnconfigure((0,1), weight=1)

        left_txt = f"{pet['nombre']}\n{pet['edad']}"
        lbl_name = ctk.CTkLabel(band, text=left_txt, font=ctk.CTkFont(size=13, weight="bold"),
                                text_color="white", anchor="w")
        lbl_name.grid(row=0, column=0, padx=8, pady=8, sticky="w")

        lbl_species = ctk.CTkLabel(band, text=pet["especie"], font=ctk.CTkFont(size=12, weight="bold"),
                                   text_color="white")
        lbl_species.grid(row=0, column=1, padx=8, sticky="e")

        # al hacer click en la imagen o en la tarjeta abrimos el detalle
        def open_detail(event=None):
            DetailWindow(self, pet, wpp_icon=self.wpp_icon_img)
        # enlazar tanto imagen como card
        img_label.bind("<Button-1>", open_detail)
        band.bind("<Button-1>", open_detail)
        card.bind("<Button-1>", open_detail)

        return card

# --------------------------
# Ventana de detalle
# --------------------------
class DetailWindow(ctk.CTkToplevel):
    def __init__(self, parent, pet_data, wpp_icon=None):
        super().__init__(parent)
        self.title(pet_data["nombre"])
        self.geometry("560x700")
        self.transient(parent)
        self.grab_set()

        # Layout
        self.grid_columnconfigure(0, weight=1)
        # Imagen grande arriba
        img = load_image_safe(pet_data.get("foto_path", ""), (520, 360))
        if img:
            lbl_img = ctk.CTkLabel(self, image=img, text="")
            lbl_img.image = img
            lbl_img.grid(row=0, column=0, padx=14, pady=(14,8))
        else:
            lbl_img = ctk.CTkLabel(self, text="Imagen no disponible", width=48, height=12,
                                   fg_color="#f5f5f5", text_color="#888")
            lbl_img.grid(row=0, column=0, padx=14, pady=(14,8))

        # Info frame
        info = ctk.CTkFrame(self, fg_color=WHITESMOKE)
        info.grid(row=1, column=0, sticky="nsew", padx=12, pady=(6,12))
        info.grid_columnconfigure(0, weight=1)

        # Nombre (grande) y detalles pequeños
        title = ctk.CTkLabel(info, text=f"{pet_data['nombre']}, {pet_data['edad']}",
                             font=ctk.CTkFont(size=20, weight="bold"), text_color=CORAL)
        title.grid(row=0, column=0, sticky="w", padx=12, pady=(6,4))

        small = ctk.CTkLabel(info, text=f"Raza: {pet_data.get('raza','N/D')}    Sexo: {pet_data.get('sexo','')}",
                             font=ctk.CTkFont(size=12), text_color="#444")
        small.grid(row=1, column=0, sticky="w", padx=12)

        # descripción
        desc = ctk.CTkLabel(info, text=pet_data.get("descripcion","Sin descripción"), wraplength=500, justify="left",
                            text_color=TEXT_MUTED)
        desc.grid(row=2, column=0, sticky="w", padx=12, pady=(10,12))

        # botones: Contactar WhatsApp + Cerrar
        btn_frame = ctk.CTkFrame(info, fg_color="transparent")
        btn_frame.grid(row=3, column=0, sticky="ew", padx=12, pady=(6,12))
        btn_frame.grid_columnconfigure((0,1), weight=1)

        # Botón WhatsApp con icono (verde)
        def on_wpp():
            open_whatsapp(pet_data.get("contacto_wpp",""), pet_data.get("nombre",""))

        if wpp_icon:
            wpp_btn = ctk.CTkButton(btn_frame, text=" Contactar por WhatsApp", command=on_wpp,
                                    image=wpp_icon, compound="left", fg_color="#25D366", hover_color="#128C7E",
                                    font=ctk.CTkFont(size=13, weight="bold"))
        else:
            # si no hay icon, botón solo texto
            wpp_btn = ctk.CTkButton(btn_frame, text="Contactar por WhatsApp", command=on_wpp,
                                    fg_color="#25D366", hover_color="#128C7E", font=ctk.CTkFont(size=13, weight="bold"))

        wpp_btn.grid(row=0, column=0, sticky="ew", padx=(0,8))

        close_btn = ctk.CTkButton(btn_frame, text="Cerrar", command=self.destroy,
                                  fg_color="#e0e0e0", hover_color="#d0d0d0", text_color="#444",
                                  font=ctk.CTkFont(size=13))
        close_btn.grid(row=0, column=1, sticky="ew")

# --------------------------
# Ejecutar aplicación
# --------------------------
if __name__ == "__main__":
    # Verificación mínima: assets/icon.png debe existir (si no, no se rompe; botón aparece sin icono)
    icon_path = resource_path("assets/icon.png")
    if not os.path.exists(icon_path):
        print("Aviso: no se encontró assets/icon.png — el botón de WhatsApp se mostrará sin ícono.")
    # Lanza splash -> luego app principal
    splash = SplashScreen()
    splash.mainloop()
