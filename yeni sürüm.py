import os

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import datetime
import platform
import subprocess

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CUSTOMER_PRESET_DIR = os.path.join(SCRIPT_DIR, "Musteri_Listesi")
ÖN_TANIMLI_MÜŞTERİLER = [
    "AliYılmaz", 
    "AyşeDemir", 
    "MehmetKaya", 
    "MensurKoçyiğit", 
    "Mendoza Gürkan", 
    "ŞükrüKaya", 
]
PRESET_COLUMNS = 4
def sanitize_filename(name: str) -> str: 
    """ Dosya adlarında geçersiz olan karakterleri alt çizgilerle değiştirin.""" 
    geçersiz = '<>:"/\\|?*'
    sanitized = ''.join('_' eğer c geçersizse, c adındaysa)
    sanitized.strip()' i döndür
def load_customer_presets():
    try:
        os.path.isdir(CUSTOMER_PRESET_DIR) değilse : 
            os.makedirs(MÜŞTERİ_ÖN_AYAR_DİZİNİ, exist_ok=True) 

        dosya adları = [n for n in os.listdir(CUSTOMER_PRESET_DIR)
                     eğer os.path.isfile(os.path.join(MÜŞTERİ_ÖN AYAR_DİZİNİ, n))] 
        isimler = []
        dosya adlarındaki fname için : 
            yol = os.path.join(MÜŞTERİ_ÖN_AYAR_DİZİNİ, fname)
            denemek :
                open(path, "r", kodlama="utf-8") ile f olarak: 
                    içerik = f.read().strip()
                names.append(içerik veya fname) 
            İstisna hariç : 
            isimler.append(fname)

        eğer isimler değilse: 
            DEFAULT_CUSTOMERS'daki isim için : 
                sterilize edilmiş = sanitize_filename(name)
                yol = os.path.join(MÜŞTERİ_ÖN AYAR_DİZİNİ, temizlendi)
                open(path, "w", kodlama="utf-8") ile f olarak: 
                    f.write(isim)
            isimler = DEFAULT_CUSTOMERS
        isimleri geri döndür 
    except Exception:
       DEFAULT_CUSTOMERS'ı döndür 
def save_customer_presets(presets):
    try:
         os.makedirs(MÜŞTERİ_ÖN_AYAR_DİZİNİ, exist_ok=True) 
        os.listdir(CUSTOMER_PRESET_DIR) dosyasındaki dosya adı için : 
            yol = os.path.join(MÜŞTERİ_ÖN_AYAR_DİZİNİ, dosya adı)
            eğer os.path.isfile(yol): 
                os.remove(yol)

        ön ayarlardaki isim için : 
            sterilize edilmiş = sanitize_filename(name)
            yol = os.path.join(MÜŞTERİ_ÖN AYAR_DİZİNİ, temizlendi)
            open(path, "w", kodlama="utf-8") ile f olarak: 
                f.write(isim)
    except Exception as e:
        print("Kaydetme hatası:", e)

class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tipwindow = None
        widget.bind("<Enter>", self.show)
        widget.bind("<Leave>", self.hide)
    def show(self, _=None):
        if self.tipwindow or not self.text:
            return
        x = self.widget.winfo_rootx() + 20
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 5
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(tw, text=self.text, justify="left", background="#ffffe0", relief="solid", borderwidth=1,
                         font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)
    def hide(self, _=None):
        if self.tipwindow:
            self.tipwindow.destroy()
            self.tipwindow = None

class ReceiptApp:
    ROLE_VAT_MAP = {
        "Pazarcı Esnafı": 0.02,
        "Hal İçi / Ortacı": 0.01
    }

    def __init__(self, master: tk.Tk):
        self.master = master
        master.title("Sebze-Meyve Fiş Uygulaması (KDV Rol Bazlı)")
        self.customer_presets = load_customer_presets()

        master.geometry("880x650")
        master.minsize(800, 600)
        master.resizable(True, True)

        # Variables
        self.customer_name_var = tk.StringVar()
        self.item_type_var = tk.StringVar()
        self.piece_count_var = tk.StringVar()
        self.weight_var = tk.StringVar()
        self.price_per_kg_var = tk.StringVar()
        self.total_var = tk.StringVar(value="0.00")
        self.role_var = tk.StringVar(value="Pazarcı Esnafı")
        self.new_customer_var = tk.StringVar()
        self.category_var = tk.StringVar(value="MEYVE")
        self.subitem_var = tk.StringVar()

        # Data lists
        self.fruits = ["ŞEFTALİ", "NEKTARİ", "PORTAKAL", "MANDALİNA", "ELMA", "NAR", "ÇİLEK", "MUZ", "DİĞER"]
        self.vegetables = ["FASULYE", "DOMATES", "DİĞER"]

        # ==== HEADER AREA ====
        header = ttk.Frame(master, padding=(8,8))
        header.pack(fill="x", padx=5, pady=3)
        header.columnconfigure(0, weight=2)
        header.columnconfigure(1, weight=3)
        header.columnconfigure(2, weight=2)

        # Customer info panel (left)
        customer_frame = ttk.LabelFrame(header, text="Müşteri Bilgisi", padding=6)
        customer_frame.grid(row=0, column=0, sticky="nsew", padx=4, pady=2)
        customer_frame.columnconfigure(1, weight=1)
        ttk.Label(customer_frame, text="Müşteri Adı:").grid(row=0, column=0, sticky="e", padx=2, pady=2)
        name_entry = ttk.Entry(customer_frame, textvariable=self.customer_name_var, width=25)
        name_entry.grid(row=0, column=1, sticky="ew", padx=2, pady=2)
        name_entry.bind("<KeyRelease>", self._on_name_typing)
        name_entry.bind("<Down>", self._focus_suggestions)
        # Autocomplete suggestion box
        self.suggestion_box = tk.Listbox(customer_frame, height=4)
        self.suggestion_box.grid(row=1, column=1, sticky="ew", padx=2)
        self.suggestion_box.bind("<<ListboxSelect>>", self._apply_suggestion)
        self.suggestion_box.bind("<Return>", self._apply_suggestion)
        self.suggestion_box.grid_remove()
        # Quick presets inside same area below
        preset_label = ttk.Label(customer_frame, text="Müşteri Listesi:")
        preset_label.grid(row=2, column=0, sticky="nw", padx=2, pady=(6,2))
        preset_container = ttk.Frame(customer_frame)
        preset_container.grid(row=2, column=1, sticky="ew", padx=2, pady=(6,2))
        # Preset canvas with scroll bars
        self.preset_canvas = tk.Canvas(preset_container, height=90, highlightthickness=0)
        self.v_scroll = ttk.Scrollbar(preset_container, orient="vertical", command=self.preset_canvas.yview)
        self.h_scroll = ttk.Scrollbar(preset_container, orient="horizontal", command=self.preset_canvas.xview)
        self.preset_canvas.configure(yscrollcommand=self.v_scroll.set, xscrollcommand=self.h_scroll.set)
        self.preset_canvas.grid(row=0, column=0, sticky="nsew")
        self.v_scroll.grid(row=0, column=1, sticky="ns")
        self.h_scroll.grid(row=1, column=0, sticky="ew")
        self.preset_buttons_frame = ttk.Frame(self.preset_canvas)
        self.preset_window = self.preset_canvas.create_window((0,0), window=self.preset_buttons_frame, anchor="nw")
        self.preset_buttons_frame.bind("<Configure>", lambda e: self.preset_canvas.configure(scrollregion=self.preset_canvas.bbox("all")))
        self._refresh_customer_preset_buttons()
        # Add new customer
        add_frame = ttk.Frame(customer_frame)
        add_frame.grid(row=3, column=1, sticky="w", padx=2, pady=(2,4))
        ttk.Entry(add_frame, textvariable=self.new_customer_var, width=18).grid(row=0, column=0, padx=(0,4))
        ttk.Button(add_frame, text="Ekle", command=self._add_new_preset).grid(row=0, column=1)

        # Item selection panel (center)
        item_frame = ttk.LabelFrame(header, text="Ürün Seçimi", padding=6)
        item_frame.grid(row=0, column=1, sticky="nsew", padx=4, pady=2)
        for i in range(4):
            item_frame.columnconfigure(i, weight=1)
        # Category & subitem
        ttk.Label(item_frame, text="Kategori:").grid(row=0, column=0, sticky="e", padx=2, pady=2)
        # Radio buttons instead of combobox for Kategori
        kat_frame = ttk.Frame(item_frame)
        kat_frame.grid(row=0, column=1, sticky="w", padx=2, pady=2)
        for val in ["MEYVE", "SEBZE"]:
            ttk.Radiobutton(kat_frame, text=val, variable=self.category_var, value=val,
                            command=self._on_category_changed).pack(side="left", padx=4)

        ttk.Label(item_frame, text="Alt Cinsi:").grid(row=0, column=2, sticky="e", padx=2, pady=2)
        self.subitem_combobox = ttk.Combobox(item_frame, textvariable=self.subitem_var, state="readonly",
                                             values=self.fruits, width=18)
        self.subitem_combobox.grid(row=0, column=3, sticky="w", padx=2, pady=2)
        self.subitem_combobox.bind("<<ComboboxSelected>>", self._on_subitem_selected)

        ttk.Label(item_frame, text="Malın Cinsi:").grid(row=1, column=0, sticky="e", padx=2, pady=4)
        item_entry = ttk.Entry(item_frame, textvariable=self.item_type_var, width=30, state="readonly")
        item_entry.grid(row=1, column=1, columnspan=3, sticky="w", padx=2, pady=4)

        # Role and VAT (right)
        role_frame = ttk.LabelFrame(header, text="İşlem Bilgisi", padding=6)
        role_frame.grid(row=0, column=2, sticky="nsew", padx=4, pady=2)
        role_frame.columnconfigure(1, weight=1)
        ttk.Label(role_frame, text="Müşteri Türü:").grid(row=0, column=0, sticky="w", padx=2, pady=2)
        self.role_selector = ttk.Combobox(role_frame, textvariable=self.role_var, state="readonly",
                                          values=list(self.ROLE_VAT_MAP.keys()), width=20)
        self.role_selector.grid(row=0, column=1, sticky="w", padx=2, pady=2)
        self.role_selector.bind("<<ComboboxSelected>>", lambda e: self.calculate_total())

        # ==== MAIN FORM ====
        form_wrapper = ttk.Frame(master)
        form_wrapper.pack(fill="both", expand=True, padx=5, pady=(4,2))

        self.form_canvas = tk.Canvas(form_wrapper, highlightthickness=0)
        self.form_canvas.pack(side="left", fill="both", expand=True)
        form_scroll = ttk.Scrollbar(form_wrapper, orient="vertical", command=self.form_canvas.yview)
        form_scroll.pack(side="right", fill="y")
        self.form_canvas.configure(yscrollcommand=form_scroll.set)

        self.form_frame = ttk.Frame(self.form_canvas, padding=6)
        self.form_window = self.form_canvas.create_window((0,0), window=self.form_frame, anchor="nw")
        self.form_frame.bind("<Configure>", lambda e: self.form_canvas.configure(scrollregion=self.form_canvas.bbox("all")))

        # Numeric and total fields grouped
        ttk.Label(self.form_frame, text="Parça Adedi:").grid(row=0, column=0, sticky="e", padx=5, pady=6)
        ttk.Entry(self.form_frame, textvariable=self.piece_count_var, width=12).grid(row=0, column=1, sticky="w", padx=5, pady=6)
        ttk.Label(self.form_frame, text="Kilo (kg):").grid(row=1, column=0, sticky="e", padx=5, pady=6)
        ttk.Entry(self.form_frame, textvariable=self.weight_var, width=12).grid(row=1, column=1, sticky="w", padx=5, pady=6)
        ttk.Label(self.form_frame, text="Birim Fiyat (kg başına):").grid(row=2, column=0, sticky="e", padx=5, pady=6)
        ttk.Entry(self.form_frame, textvariable=self.price_per_kg_var, width=12).grid(row=2, column=1, sticky="w", padx=5, pady=6)
        ttk.Label(self.form_frame, text="Toplam (KDV dahil):").grid(row=3, column=0, sticky="e", padx=5, pady=6)
        ttk.Entry(self.form_frame, textvariable=self.total_var, width=20, state="readonly").grid(row=3, column=1, sticky="w", padx=5, pady=6)

        for var in (self.weight_var, self.price_per_kg_var, self.role_var):
            var.trace_add("write", lambda *args: self.calculate_total())

        # Bottom actions
        action_frame = ttk.Frame(master, padding=6)
        action_frame.pack(fill="x", padx=5, pady=8)
        ttk.Button(action_frame, text="Fişi Yazdır / Kaydet", command=self.print_receipt).pack(side="left", padx=6)
        ttk.Button(action_frame, text="Çıkış", command=master.quit).pack(side="right", padx=6)

        # Initialize state
        self._on_category_changed()

    def _refresh_customer_preset_buttons(self):
        for child in self.preset_buttons_frame.winfo_children():
            child.destroy()
        sorted_presets = sorted(self.customer_presets, key=lambda s: s.lower())
        for idx, name in enumerate(sorted_presets):
            row = idx // PRESET_COLUMNS
            col = idx % PRESET_COLUMNS
            btn = ttk.Button(self.preset_buttons_frame, text=name,
                             command=lambda n=name: self.customer_name_var.set(n))
            btn.grid(row=row, column=col, padx=2, pady=2, sticky="ew")
            ToolTip(btn, name)
            btn.bind("<Button-3>", lambda e, n=name: self._remove_preset(n))
        for c in range(PRESET_COLUMNS):
            self.preset_buttons_frame.columnconfigure(c, weight=1)

    def _add_new_preset(self):
        name = self.new_customer_var.get().strip()
        if not name:
            return
        if name in self.customer_presets:
            messagebox.showinfo("Bilgi", "Bu müşteri zaten mevcut.")
            return
        self.customer_presets.append(name)
        save_customer_presets(self.customer_presets)
        self.new_customer_var.set("")
        self._refresh_customer_preset_buttons()

    def _remove_preset(self, name):
        if messagebox.askyesno("Sil", f"'{name}' presetini silmek istiyor musunuz?" ):
            self.customer_presets = [n for n in self.customer_presets if n != name]
            save_customer_presets(self.customer_presets)
            self._refresh_customer_preset_buttons()

    def _on_category_changed(self, event=None):
        cat = self.category_var.get()
        if cat == "MEYVE":
            self.subitem_combobox.configure(values=self.fruits, state="readonly")
            self.subitem_var.set(self.fruits[0])
        elif cat == "SEBZE":
            self.subitem_combobox.configure(values=self.vegetables, state="readonly")
            self.subitem_var.set(self.vegetables[0])
        self._apply_subitem_to_item()

    def _on_subitem_selected(self, event=None):
        self._apply_subitem_to_item()

    def _apply_subitem_to_item(self):
        val = self.subitem_var.get()
        if val == "DİĞER":
            custom = simpledialog.askstring("Diğer Alt Cinsi", "Alt cinsi giriniz:")
            if custom:
                self.item_type_var.set(custom.upper())
        elif val:
            self.item_type_var.set(val)

    def calculate_total(self):
        try:
            weight = float(self.weight_var.get().replace(',', '.')) if self.weight_var.get() else 0.0
            price = float(self.price_per_kg_var.get().replace(',', '.')) if self.price_per_kg_var.get() else 0.0
        except ValueError:
            return
        net_total = weight * price
        vat_rate = self.ROLE_VAT_MAP.get(self.role_var.get(), 0.0)
        total_with_vat = net_total + net_total * vat_rate
        self.total_var.set(f"{total_with_vat:.2f}")

    def print_receipt(self):
        customer_name = self.customer_name_var.get().strip()
        item_type = self.item_type_var.get().strip()
        piece_count = self.piece_count_var.get().strip()
        try:
            weight = float(self.weight_var.get().replace(',', '.')) if self.weight_var.get() else 0.0
            price = float(self.price_per_kg_var.get().replace(',', '.')) if self.price_per_kg_var.get() else 0.0
        except ValueError:
            messagebox.showerror("Hata", "Kilo ve fiyat alanlarına sayısal değer giriniz.")
            return
        net_total = weight * price
        vat_rate = self.ROLE_VAT_MAP.get(self.role_var.get(), 0.0)
        vat_amount = net_total * vat_rate
        total_with_vat = net_total + vat_amount
        filename = f"fis_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        file_path = os.path.join(os.getcwd(), filename)
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write("=== SEBZE-MEYVE FİŞİ ===\n")
                f.write(f"Tarih: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Müşteri Türü: {self.role_var.get()}\n")
                f.write(f"Müşteri Adı: {customer_name}\n")
                f.write(f"Malın Cinsi: {item_type}\n")
                f.write(f"Parça Adedi: {piece_count}\n")
                f.write(f"Kilo: {weight:.2f} kg\n")
                f.write(f"Birim Fiyat: {price:.2f}\n")
                f.write(f"Net Tutar: {net_total:.2f}\n")
                f.write(f"KDV (%{vat_rate*100:.0f}): {vat_amount:.2f}\n")
                f.write(f"Toplam: {total_with_vat:.2f}\n")
            printed = False
            if platform.system() == "Windows":
                try:
                    os.startfile(file_path, "print")
                    printed = True
                except Exception:
                    pass
            else:
                try:
                    subprocess.run(["lpr", file_path], check=True)
                    printed = True
                except Exception:
                    pass
            if printed:
                messagebox.showinfo("Başarılı", f"Fiş yazıcıya gönderildi ve kaydedildi:\n{file_path}")
            else:
                messagebox.showinfo("Kaydedildi", f"Fiş kaydedildi ama yazdırılamadı:\n{file_path}")
        except Exception as e:
            messagebox.showerror("Hata", f"Fiş oluşturulurken bir hata oldu:\n{e}")

    def _on_name_typing(self, event):
        typed = self.customer_name_var.get()
        if not typed:
            self.suggestion_box.grid_remove()
            return
        matches = [c for c in self.customer_presets if c.lower().startswith(typed.lower())]
        if matches:
            self.suggestion_box.delete(0, tk.END)
            for m in matches:
                self.suggestion_box.insert(tk.END, m)
            self.suggestion_box.grid()
        else:
            self.suggestion_box.grid_remove()

    def _focus_suggestions(self, event):
        if self.suggestion_box.winfo_ismapped():
            self.suggestion_box.focus_set()
            self.suggestion_box.selection_set(0)
        return "break"

    def _apply_suggestion(self, event=None):
        sel = None
        if self.suggestion_box.curselection():
            sel = self.suggestion_box.get(self.suggestion_box.curselection())
        elif event and hasattr(event, 'widget') and isinstance(event.widget, tk.Listbox):
            sel = event.widget.get(0)
        if sel:
            self.customer_name_var.set(sel)
        self.suggestion_box.grid_remove()

def main():
    root = tk.Tk()
    ReceiptApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
