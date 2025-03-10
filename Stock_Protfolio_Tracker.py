import tkinter as tk
from tkinter import ttk, messagebox
import requests
import re
from bs4 import BeautifulSoup

# Portfolio dictionary to store stock data
portfolio = {}

def get_stock_price(symbol):
    url = f"https://www.google.com/finance/quote/{symbol}:NASDAQ"
    headers = {"User-Agent": "Mozilla/5.0"}  # Prevent blocking
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        price_tag = soup.find("div", class_="YMlKec fxKbKc")
        
        if price_tag:
            price = re.sub(r'[^0-9.]', '', price_tag.text)  # Extract numeric value
            return float(price) if price else None
    
    messagebox.showerror("Error", "Stock price not found! Please check the symbol.")
    return None

def add_stock():
    symbol = stock_entry.get().upper()
    shares = shares_entry.get()
    
    if not symbol or not shares.isdigit():
        messagebox.showerror("Input Error", "Please enter a valid stock symbol and number of shares.")
        return
    
    shares = int(shares)
    price = get_stock_price(symbol)
    
    if price is None:
        return
    
    portfolio[symbol] = {"Shares": shares, "Price": price}
    update_portfolio()

def remove_stock():
    selected = portfolio_tree.selection()
    if not selected:
        messagebox.showerror("Selection Error", "Please select a stock to remove.")
        return
    
    for item in selected:
        symbol = portfolio_tree.item(item)['values'][0]
        del portfolio[symbol]
    update_portfolio()

def update_portfolio():
    portfolio_tree.delete(*portfolio_tree.get_children())
    total_portfolio_value = 0
    
    for symbol, data in portfolio.items():
        total_value = data["Shares"] * data["Price"]
        total_portfolio_value += total_value
        portfolio_tree.insert("", "end", values=(symbol, data["Shares"], f"${data["Price"]:.2f}", f"${total_value:.2f}"))
    
    total_value_label.config(text=f"Total Portfolio Value: ${total_portfolio_value:.2f}")

# GUI Setup
root = tk.Tk()
root.title("Stock Portfolio Tracker")
root.geometry("800x500")
root.configure(bg="#282C35")

frame = tk.Frame(root, bg="#282C35")
frame.pack(pady=20)

stock_label = tk.Label(frame, text="Stock Symbol:", fg="white", bg="#282C35")
stock_label.grid(row=0, column=0, padx=5, pady=5)
stock_entry = tk.Entry(frame)
stock_entry.grid(row=0, column=1, padx=5, pady=5)

shares_label = tk.Label(frame, text="Shares:", fg="white", bg="#282C35")
shares_label.grid(row=0, column=2, padx=5, pady=5)
shares_entry = tk.Entry(frame)
shares_entry.grid(row=0, column=3, padx=5, pady=5)

add_button = tk.Button(frame, text="Add Stock", command=add_stock, bg="#66B2FF", fg="white")
add_button.grid(row=0, column=4, padx=5, pady=5)
remove_button = tk.Button(frame, text="Remove Stock", command=remove_stock, bg="#FF9999", fg="white")
remove_button.grid(row=0, column=5, padx=5, pady=5)

portfolio_frame = tk.Frame(root, bg="#282C35")
portfolio_frame.pack(pady=20)

portfolio_tree = ttk.Treeview(portfolio_frame, columns=("Stock", "Shares", "Price", "Total Value"), show="headings")
portfolio_tree.heading("Stock", text="Stock")
portfolio_tree.heading("Shares", text="Shares")
portfolio_tree.heading("Price", text="Price")
portfolio_tree.heading("Total Value", text="Total Value")
portfolio_tree.pack(pady=10)

total_value_label = tk.Label(root, text="Total Portfolio Value: $0.00", fg="white", bg="#282C35", font=("Arial", 12, "bold"))
total_value_label.pack(pady=20)

root.mainloop()