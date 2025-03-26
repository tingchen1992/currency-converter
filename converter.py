import tkinter as tk
from tkinter import messagebox
import requests
import config


def get_exchange_rate(base_currency, target_currency):
    api_key = config.API_KEY
    url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/{base_currency}"
    response = requests.get(url)
    print(f"API 回應狀態碼: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        rate = data["conversion_rates"].get(target_currency)
        if rate:
            return rate
        else:
            messagebox.showerror("錯誤", "無法找到指定的貨幣代碼")
            return None
    else:
        messagebox.showerror("錯誤", "無法獲取匯率，請檢查網路連線。")
        return None


def convert_currency():
    base_currency = base_currency_entry.get().upper()
    target_currency = target_currency_entry.get().upper()
    try:
        amount = float(amount_entry.get())
    except ValueError:
        messagebox.showerror("錯誤", "請輸入有效的數字")
        return

    rate = get_exchange_rate(base_currency, target_currency)

    if rate:
        converted_amount = amount * rate
        result_label.config(
            text=f"{amount} {base_currency} = {converted_amount:.2f} {target_currency}"
        )
    else:
        result_label.config(text="轉換失敗，請檢查貨幣代碼")


root = tk.Tk()
root.title("貨幣轉換器")
root.geometry("300x200")

tk.Label(root, text="基礎貨幣:").pack()
base_currency_entry = tk.Entry(root)
base_currency_entry.pack()

tk.Label(root, text="目標貨幣:").pack()
target_currency_entry = tk.Entry(root)
target_currency_entry.pack()

tk.Label(root, text="金額:").pack()
amount_entry = tk.Entry(root)
amount_entry.pack()

convert_button = tk.Button(root, text="轉換", command=convert_currency)
convert_button.pack()

result_label = tk.Label(root, text="", font=("Arial", 14))
result_label.pack()

root.mainloop()
