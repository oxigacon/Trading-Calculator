"""
Запуск программы:
Для запуска убедитесь, что у вас установлен Python (обычно с ним идет библиотека tkinter, которая нужна для интерфейса).
Сохраните этот код в файл с расширением .py (например, calculator.py) и выполните в командной строке или терминале:
python calculator.py
"""

import tkinter as tk
from tkinter import messagebox

def calc_third_party_to_steam(buy_price, sell_price):
    commission = sell_price * 0.15
    profit = (sell_price - commission) - buy_price
    return commission, profit

def calc_steam_to_third_party(buy_price, sell_price):
    commission = sell_price * 0.05
    profit = (sell_price - commission) - buy_price
    return commission, profit

def calculate(op_type, buy_entry, sell_entry, result_label):
    try:
        buy_price = float(buy_entry.get())
        sell_price = float(sell_entry.get())
        
        if op_type == "to_steam":
            commission, profit = calc_third_party_to_steam(buy_price, sell_price)
            op_name = "Сторонний сайт → Steam"
        else:
            commission, profit = calc_steam_to_third_party(buy_price, sell_price)
            op_name = "Steam → сторонний сайт"
            
        result_text = f"Операция: {op_name}\n"
        result_text += f"Покупка: {buy_price:.2f}\n"
        result_text += f"Продажа: {sell_price:.2f}\n"
        result_text += f"Комиссия: {commission:.2f}\n"
        result_text += f"Итог продажи (чистыми): {sell_price - commission:.2f}\n"
        
        if profit > 0:
            result_text += f"Прибыль: {profit:.2f}"
        elif profit < 0:
            result_text += f"Убыток: {abs(profit):.2f}"
        else:
            result_text += f"Прибыль: {profit:.2f}"
            
        result_label.config(text=result_text, fg="green" if profit > 0 else "red" if profit < 0 else "black")
    except ValueError:
        messagebox.showerror("Ошибка", "Пожалуйста, введите корректные числа.")

def main():
    root = tk.Tk()
    root.title("CS2 Trade Calculator")
    root.geometry("480x580")
    root.resizable(True, True)

    # Операция: Сторонний сайт -> Steam
    frame1 = tk.LabelFrame(root, text="Сторонний сайт → Steam (Комиссия 15%)", padx=10, pady=10)
    frame1.pack(padx=10, pady=10, fill="x")

    tk.Label(frame1, text="Сумма покупки:").grid(row=0, column=0, sticky="w", pady=5)
    buy_entry1 = tk.Entry(frame1, width=20)
    buy_entry1.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(frame1, text="Сумма продажи:").grid(row=1, column=0, sticky="w", pady=5)
    sell_entry1 = tk.Entry(frame1, width=20)
    sell_entry1.grid(row=1, column=1, padx=10, pady=5)

    res_label1 = tk.Label(frame1, text="", justify="left", font=("Arial", 10))
    
    calc_btn1 = tk.Button(frame1, text="Рассчитать", command=lambda: calculate("to_steam", buy_entry1, sell_entry1, res_label1))
    calc_btn1.grid(row=2, column=0, columnspan=2, pady=10)
    res_label1.grid(row=3, column=0, columnspan=2, sticky="w")

    # Операция: Steam -> Сторонний сайт
    frame2 = tk.LabelFrame(root, text="Steam → сторонний сайт (Комиссия 5%)", padx=10, pady=10)
    frame2.pack(padx=10, pady=10, fill="x")

    tk.Label(frame2, text="Сумма покупки:").grid(row=0, column=0, sticky="w", pady=5)
    buy_entry2 = tk.Entry(frame2, width=20)
    buy_entry2.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(frame2, text="Сумма продажи:").grid(row=1, column=0, sticky="w", pady=5)
    sell_entry2 = tk.Entry(frame2, width=20)
    sell_entry2.grid(row=1, column=1, padx=10, pady=5)

    res_label2 = tk.Label(frame2, text="", justify="left", font=("Arial", 10))

    calc_btn2 = tk.Button(frame2, text="Рассчитать", command=lambda: calculate("to_third", buy_entry2, sell_entry2, res_label2))
    calc_btn2.grid(row=2, column=0, columnspan=2, pady=10)
    res_label2.grid(row=3, column=0, columnspan=2, sticky="w")

    root.mainloop()

if __name__ == "__main__":
    main()
