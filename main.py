import tkinter as tk
from tkinter import ttk, messagebox
import threading
from datetime import datetime, timedelta

from bnr_rates import get_rates
from converter import convert, ConversionError


class CurrencyConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Currency Converter (BNR)")
        self.root.resizable(False, False)
        self.root.geometry("420x300")

        self.data = None
        self.rates = {}
        self.using_cached = False

        self.build_ui()
        self.load_rates_async(auto=True)

    def build_ui(self):
        padding = {"padx": 10, "pady": 5}

        ttk.Label(self.root, text="Amount").grid(row=0, column=0, **padding)
        self.amount_entry = ttk.Entry(self.root, width=20)
        self.amount_entry.grid(row=0, column=1, **padding)

        ttk.Label(self.root, text="From").grid(row=1, column=0, **padding)
        self.from_currency = ttk.Combobox(self.root, state="readonly", width=17)
        self.from_currency.grid(row=1, column=1, **padding)

        ttk.Label(self.root, text="To").grid(row=2, column=0, **padding)
        self.to_currency = ttk.Combobox(self.root, state="readonly", width=17)
        self.to_currency.grid(row=2, column=1, **padding)

        self.swap_btn = ttk.Button(self.root, text="↔", width=3, command=self.swap_currencies)
        self.swap_btn.grid(row=1, column=2, rowspan=2, padx=5)

        self.convert_btn = ttk.Button(self.root, text="Convert", command=self.convert_action)
        self.convert_btn.grid(row=3, column=0, columnspan=2, pady=10)

        self.result_label = ttk.Label(self.root, text="Result: -", font=("Segoe UI", 11, "bold"))
        self.result_label.grid(row=4, column=0, columnspan=3, pady=5)

        self.banner_label = ttk.Label(self.root, text="", foreground="red", font=("Segoe UI", 9))
        self.banner_label.grid(row=5, column=0, columnspan=3)

        ttk.Separator(self.root).grid(row=6, column=0, columnspan=3, sticky="ew", pady=5)

        self.refresh_btn = ttk.Button(self.root, text="Refresh rates", command=self.load_rates_async)
        self.refresh_btn.grid(row=7, column=0, **padding)

        self.update_label = ttk.Label(self.root, text="Last update: -", font=("Segoe UI", 9))
        self.update_label.grid(row=7, column=1, columnspan=2, sticky="w", **padding)

    def load_rates_async(self, auto=False):
        self.refresh_btn.config(state="disabled")
        threading.Thread(target=self.load_rates, args=(auto,), daemon=True).start()

    def load_rates(self, auto):
        try:
            data = get_rates()
            self.using_cached = False
            self.root.after(0, self.update_rates_ui, data)
        except Exception:
            self.using_cached = True
            self.root.after(0, self.show_cached_warning)

    def update_rates_ui(self, data):
        self.data = data
        self.rates = data["rates"]

        currencies = sorted(self.rates.keys())
        self.from_currency["values"] = currencies
        self.to_currency["values"] = currencies

        if not self.from_currency.get():
            self.from_currency.set("RON")
        if not self.to_currency.get() and "EUR" in currencies:
            self.to_currency.set("EUR")

        self.update_label.config(text=f"Last update: {data['timestamp']}")
        self.banner_label.config(text="")
        self.refresh_btn.config(state="normal")

    def show_cached_warning(self):
        self.banner_label.config(text="Offline mode: using cached rates")
        self.refresh_btn.config(state="normal")

    def swap_currencies(self):
        from_cur = self.from_currency.get()
        to_cur = self.to_currency.get()

        if from_cur and to_cur:
            self.from_currency.set(to_cur)
            self.to_currency.set(from_cur)

    def convert_action(self):
        try:
            amount = float(self.amount_entry.get())
            from_cur = self.from_currency.get()
            to_cur = self.to_currency.get()

            result = convert(amount, from_cur, to_cur, self.rates)
            self.result_label.config(text=f"Result: {result}")

        except ValueError:
            messagebox.showwarning("Invalid input", "Please enter a numeric amount.")
        except ConversionError as e:
            messagebox.showwarning("Conversion error", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    app = CurrencyConverterApp(root)
    root.mainloop()