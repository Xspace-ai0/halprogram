"""
Malı alan kişinin adını da fişe yazan ve tek düğmeyle fişi
yazdırıp kaydeden sebze‑meyve fiş uygulaması.

Bu sürümde Müşteri Adı (SAYIN ...) alanı eklenmiştir. Kullanıcı
isim, malın cinsi, parça adedi, kilo ve birim fiyatı girdikten
sonra "Fişi Yazdır" düğmesine basarak fişi otomatik olarak
kaydedebilir ve yazıcıdan çıktı alabilir.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import datetime
import os


class ReceiptApp:
    """Müşteri adı dahil fiş yazdırma uygulaması."""

    VAT_RATE = 0.02

    def __init__(self, master: tk.Tk) -> None:
        self.master = master
        master.title("Sebze‑Meyve Fiş Uygulaması")

        # Değişkenler
        self.customer_name_var = tk.StringVar()
        self.item_type_var = tk.StringVar()
        self.piece_count_var = tk.StringVar()
        self.weight_var = tk.StringVar()
        self.price_per_kg_var = tk.StringVar()
        self.total_var = tk.StringVar(value="0.00")

        # Müşteri adı
        ttk.Label(master, text="Müşteri Adı:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        ttk.Entry(master, textvariable=self.customer_name_var, width=30).grid(row=0, column=1, padx=5, pady=5)

        # Malın cinsi
        ttk.Label(master, text="Malın Cinsi:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        ttk.Entry(master, textvariable=self.item_type_var, width=30).grid(row=1, column=1, padx=5, pady=5)
        # Sık kullanılan meyveler için hızlı seçim düğmeleri ekle
        # Kullanıcı bazı meyveleri yazmak yerine tek tıkla seçebilmesi için bir çerçeve oluştur.
        fruits_frame = ttk.Frame(master)
        # Hızlı seçim için eklenecek meyveler listesi
        fruits = ["ŞEFTALİ", "NEKTARİ", "PORTAKAL", "MANDALİNA", "DOMATES"]
        for idx, fruit in enumerate(fruits):
            # Her meyve için bir düğme oluştur; tıklanınca malın cinsi otomatik doldurulur
            ttk.Button(fruits_frame, text=fruit,
                       command=lambda f=fruit: self.item_type_var.set(f)).grid(row=0, column=idx, padx=2, pady=2)
        # Çerçeveyi 'Malın Cinsi' satırının hemen altına yerleştir
        fruits_frame.grid(row=2, column=0, columnspan=3, padx=5, pady=5, sticky="w")

        # Parça adedi
        ttk.Label(master, text="Parça Adedi:").grid(row=3, column=0, sticky="e", padx=5, pady=5)
        ttk.Entry(master, textvariable=self.piece_count_var).grid(row=3, column=1, padx=5, pady=5)

        # Kilo (kg)
        ttk.Label(master, text="Kilo (kg):").grid(row=4, column=0, sticky="e", padx=5, pady=5)
        ttk.Entry(master, textvariable=self.weight_var).grid(row=4, column=1, padx=5, pady=5)

        # Birim fiyat (TL/kg)
        ttk.Label(master, text="Birim Fiyat (TL/kg):").grid(row=5, column=0, sticky="e", padx=5, pady=5)
        ttk.Entry(master, textvariable=self.price_per_kg_var).grid(row=5, column=1, padx=5, pady=5)

        # Hesapla butonu
        ttk.Button(master, text="Hesapla", command=self.calculate_total).grid(row=6, column=0, columnspan=2, pady=10)

        # Toplam tutar etiketi
        ttk.Label(master, text="Toplam Tutar (KDV dâhil) TL:").grid(row=7, column=0, sticky="e", padx=5, pady=5)
        ttk.Label(master, textvariable=self.total_var, foreground="blue").grid(row=7, column=1, sticky="w", padx=5, pady=5)

        # Fiş Yazdır düğmesi
        ttk.Button(master, text="Fişi Yazdır", command=self.print_receipt).grid(row=8, column=0, columnspan=2, pady=10)

        # Çıkış düğmesi
        ttk.Button(master, text="Çıkış", command=master.quit).grid(row=9, column=0, columnspan=2, pady=10)

    def calculate_total(self) -> None:
        try:
            weight = float(self.weight_var.get().replace(',', '.'))
            price = float(self.price_per_kg_var.get().replace(',', '.'))
        except ValueError:
            messagebox.showerror("Hata", "Kilo ve fiyat alanlarına sayısal değer giriniz.")
            return
        net_total = weight * price
        self.total_var.set(f"{(net_total + net_total * self.VAT_RATE):.2f}")

    def print_receipt(self) -> None:
        customer_name = self.customer_name_var.get().strip()
        item_type = self.item_type_var.get().strip()
        piece_count = self.piece_count_var.get().strip()
        try:
            weight = float(self.weight_var.get().replace(',', '.'))
            price = float(self.price_per_kg_var.get().replace(',', '.'))
        except ValueError:
            messagebox.showerror("Hata", "Kilo ve fiyat alanlarına sayısal değer giriniz.")
            return
        net_total = weight * price
        vat_amount = net_total * self.VAT_RATE
        total_with_vat = net_total + vat_amount

        filename = f"fis_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        file_path = os.path.join(os.getcwd(), filename)
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                # Başlık: firma adı
                f.write("GÖKHAN TİCARET\n")
                f.write(f"Tarih: {datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S')}\n\n")
                # Müşteri ismi fişe SAYIN başlığıyla yazılır
                f.write(f"SAYIN         : {customer_name}\n")
                f.write(f"Malın Cinsi   : {item_type}\n")
                f.write(f"Parça Adedi   : {piece_count}\n")
                f.write(f"Kilo (kg)     : {weight:.2f}\n")
                f.write(f"Birim Fiyat   : {price:.2f} TL/kg\n")
                f.write(f"Net Tutar     : {net_total:.2f} TL\n")
                f.write(f"KDV (%2)      : {vat_amount:.2f} TL\n")
                f.write(f"Toplam Tutar  : {total_with_vat:.2f} TL\n")
        except OSError as e:
            messagebox.showerror("Hata", f"Fiş kaydedilemedi:\n{e}")
            return
        printed = False
        try:
            os.startfile(file_path, "print")
            printed = True
        except Exception as e:
            messagebox.showwarning(
                "Yazdırma Hatası",
                f"Fiş kaydedildi, ancak yazdırma sırasında bir hata oluştu:\n{e}\nFişi manuel olarak yazdırabilirsiniz: {file_path}"
            )
        finally:
            if printed:
                messagebox.showinfo("Başarılı", f"Fiş yazıcıya gönderildi ve kaydedildi:\n{file_path}")


def main() -> None:
    root = tk.Tk()
    root.resizable(False, False)
    ReceiptApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
