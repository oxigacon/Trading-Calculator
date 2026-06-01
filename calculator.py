"""
Запуск программы:
Для запуска убедитесь, что у вас установлен Python (обычно с ним идет библиотека tkinter, которая нужна для интерфейса).
Сохраните этот код в файл с расширением .py (например, calculator.py) и выполните в командной строке или терминале:
python calculator.py
"""

import tkinter as tk
from tkinter import messagebox
import os
import sys
import json

# Fix for Tcl/Tk not found error on some Windows Python installations
if sys.platform == 'win32':
    python_dir = sys.base_prefix
    tcl_dir = os.path.join(python_dir, 'tcl', 'tcl8.6')
    tk_dir = os.path.join(python_dir, 'tcl', 'tk8.6')
    
    # Fallback just in case sys.base_prefix is somehow incorrect but we can extract it from tkinter module path
    if not os.path.exists(tcl_dir):
        try:
            import tkinter
            tkinter_dir = os.path.dirname(tkinter.__file__) # e.g. ...\Lib\tkinter
            lib_dir = os.path.dirname(tkinter_dir) # e.g. ...\Lib
            python_dir_fallback = os.path.dirname(lib_dir) # e.g. ...\Python314
            tcl_dir = os.path.join(python_dir_fallback, 'tcl', 'tcl8.6')
            tk_dir = os.path.join(python_dir_fallback, 'tcl', 'tk8.6')
        except Exception:
            pass

    if os.path.exists(tcl_dir):
        os.environ['TCL_LIBRARY'] = tcl_dir
    if os.path.exists(tk_dir):
        os.environ['TK_LIBRARY'] = tk_dir

def get_config_path():
    if getattr(sys, 'frozen', False):
        base_dir = os.path.dirname(sys.executable)
    else:
        base_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_dir, 'config.json')

def load_config():
    try:
        with open(get_config_path(), 'r', encoding='utf-8') as f:
            data = json.load(f)
            return float(data.get('steam_commission', 15.0)), float(data.get('third_party_commission', 5.0))
    except Exception:
        return 15.0, 5.0

def save_config(steam_comm, third_party_comm):
    try:
        with open(get_config_path(), 'w', encoding='utf-8') as f:
            json.dump({'steam_commission': steam_comm, 'third_party_commission': third_party_comm}, f)
    except Exception:
        pass

def calc_third_party_to_steam(buy_price, sell_price, commission_pct):
    commission = sell_price * (commission_pct / 100.0)
    profit = (sell_price - commission) - buy_price
    return commission, profit

def calc_steam_to_third_party(buy_price, sell_price, commission_pct):
    commission = sell_price * (commission_pct / 100.0)
    profit = (sell_price - commission) - buy_price
    return commission, profit

def calculate(op_type, buy_entry, sell_entry, comm_entry, result_label, other_comm_entry):
    try:
        buy_str = buy_entry.get().strip()
        buy_price = float(buy_str) if buy_str else None
        sell_price = float(sell_entry.get())
        commission_pct = float(comm_entry.get())
        
        if op_type == "to_steam":
            commission, profit = calc_third_party_to_steam(buy_price if buy_price is not None else 0.0, sell_price, commission_pct)
            op_name = "Сторонний сайт → Steam"
            try:
                other_comm = float(other_comm_entry.get())
                save_config(commission_pct, other_comm)
            except ValueError:
                save_config(commission_pct, 5.0)
        else:
            commission, profit = calc_steam_to_third_party(buy_price if buy_price is not None else 0.0, sell_price, commission_pct)
            op_name = "Steam → сторонний сайт"
            try:
                other_comm = float(other_comm_entry.get())
                save_config(other_comm, commission_pct)
            except ValueError:
                save_config(15.0, commission_pct)
            
        result_text = f"Операция: {op_name}\n"
        if buy_price is not None:
            result_text += f"Покупка: {buy_price:.2f}\n"
        result_text += f"Продажа: {sell_price:.2f}\n"
        result_text += f"Комиссия ({commission_pct}%): {commission:.2f}\n"
        result_text += f"Итог продажи (чистыми): {sell_price - commission:.2f}\n"
        
        if buy_price is not None:
            profit_pct_str = ""
            if buy_price > 0:
                profit_pct = (profit / buy_price) * 100
                profit_pct_str = f" ({profit_pct:.2f}%)"
                
            if profit > 0:
                result_text += f"Прибыль: {profit:.2f}{profit_pct_str}"
            elif profit < 0:
                result_text += f"Убыток: {abs(profit):.2f}{profit_pct_str}"
            else:
                result_text += f"Прибыль: {profit:.2f}{profit_pct_str}"
            result_color = "green" if profit > 0 else "red" if profit < 0 else "black"
        else:
            result_color = "black"
            
        result_label.config(text=result_text, fg=result_color)
    except ValueError:
        messagebox.showerror("Ошибка", "Пожалуйста, введите корректные числа.")

def main():
    root = tk.Tk()
    root.title("CS2 Trade Calculator")
    root.geometry("480x540")
    root.resizable(True, True)

    steam_default_comm, third_party_default_comm = load_config()

    # Операция: Сторонний сайт -> Steam
    frame1 = tk.LabelFrame(root, text="Сторонний сайт → Steam", padx=10, pady=10)
    frame1.pack(padx=10, pady=10, fill="x")

    tk.Label(frame1, text="Сумма покупки:").grid(row=0, column=0, sticky="w", pady=5)
    buy_entry1 = tk.Entry(frame1, width=20)
    buy_entry1.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(frame1, text="Сумма продажи:").grid(row=1, column=0, sticky="w", pady=5)
    sell_entry1 = tk.Entry(frame1, width=20)
    sell_entry1.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(frame1, text="Комиссия (%):").grid(row=2, column=0, sticky="w", pady=5)
    comm_entry1 = tk.Entry(frame1, width=20)
    comm_entry1.insert(0, str(steam_default_comm))
    comm_entry1.grid(row=2, column=1, padx=10, pady=5)

    res_label1 = tk.Label(frame1, text="", justify="left", font=("Arial", 10))

    # Операция: Steam -> Сторонний сайт
    frame2 = tk.LabelFrame(root, text="Steam → сторонний сайт", padx=10, pady=10)
    frame2.pack(padx=10, pady=10, fill="x")

    tk.Label(frame2, text="Сумма покупки:").grid(row=0, column=0, sticky="w", pady=5)
    buy_entry2 = tk.Entry(frame2, width=20)
    buy_entry2.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(frame2, text="Сумма продажи:").grid(row=1, column=0, sticky="w", pady=5)
    sell_entry2 = tk.Entry(frame2, width=20)
    sell_entry2.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(frame2, text="Комиссия (%):").grid(row=2, column=0, sticky="w", pady=5)
    comm_entry2 = tk.Entry(frame2, width=20)
    comm_entry2.insert(0, str(third_party_default_comm))
    comm_entry2.grid(row=2, column=1, padx=10, pady=5)

    res_label2 = tk.Label(frame2, text="", justify="left", font=("Arial", 10))

    # Buttons
    calc_btn1 = tk.Button(frame1, text="Рассчитать", command=lambda: calculate("to_steam", buy_entry1, sell_entry1, comm_entry1, res_label1, comm_entry2))
    calc_btn1.grid(row=3, column=0, columnspan=2, pady=10)
    res_label1.grid(row=4, column=0, columnspan=2, sticky="w")

    calc_btn2 = tk.Button(frame2, text="Рассчитать", command=lambda: calculate("to_third", buy_entry2, sell_entry2, comm_entry2, res_label2, comm_entry1))
    calc_btn2.grid(row=3, column=0, columnspan=2, pady=10)
    res_label2.grid(row=4, column=0, columnspan=2, sticky="w")


    def on_closing():
        try:
            steam_comm = float(comm_entry1.get())
            third_party_comm = float(comm_entry2.get())
            save_config(steam_comm, third_party_comm)
        except ValueError:
            pass
        root.destroy()
        
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()
