import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime, timedelta
import random
import pandas as pd

class TekXSimulator:
    def __init__(self):
        self.A = 0
        self.B = 0
        self.DO1 = 0
        self.DO2 = 0
        self.Tx = 25.0  

    def generate_random_values(self):
        self.A = random.randint(0, 1)
        self.B = random.randint(0, 1)
        self.DO1 = random.randint(0, 1)
        self.DO2 = random.randint(0, 1)
        self.Tx += random.uniform(-1, 1)

    def get_current_status(self):
        return {'A': self.A, 'B': self.B, 'DO1': self.DO1, 'DO2': self.DO2, 'Tx': self.Tx}

    def observe_trends_over_week(self):
        trends = []
        current_time = datetime.now()
        for _ in range(7):
            trends.append((current_time.strftime("%Y-%m-%d %H:%M:%S"), self.get_current_status()))
            current_time -= timedelta(days=1)
            self.generate_random_values()
        return trends

    def configure_A_B_settings(self, A_value, B_value):
        self.A = A_value
        self.B = B_value

class DeviceManagerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("TekX Device Manager")
        self.geometry("500x300")
        
        self.tekx_simulator = TekXSimulator()

        
        self.status_label = ttk.Label(self, text="Current Status")
        self.status_label.pack()

        self.status_frame = ttk.Frame(self)
        self.status_frame.pack()

        self.do1_label = ttk.Label(self.status_frame, text="DO1:")
        self.do1_label.grid(row=0, column=0)
        self.do1_value = ttk.Label(self.status_frame, text="")
        self.do1_value.grid(row=0, column=1)

        self.do2_label = ttk.Label(self.status_frame, text="DO2:")
        self.do2_label.grid(row=1, column=0)
        self.do2_value = ttk.Label(self.status_frame, text="")
        self.do2_value.grid(row=1, column=1)

        self.tx_label = ttk.Label(self.status_frame, text="Temperature:")
        self.tx_label.grid(row=2, column=0)
        self.tx_value = ttk.Label(self.status_frame, text="")
        self.tx_value.grid(row=2, column=1)

        self.observe_button = ttk.Button(self, text="Observe Trends", command=self.observe_trends)
        self.observe_button.pack()

        self.config_frame = ttk.LabelFrame(self, text="Configure A & B")
        self.config_frame.pack()

        self.a_label = ttk.Label(self.config_frame, text="A:")
        self.a_label.grid(row=0, column=0)
        self.a_entry = ttk.Entry(self.config_frame)
        self.a_entry.grid(row=0, column=1)

        self.b_label = ttk.Label(self.config_frame, text="B:")
        self.b_label.grid(row=1, column=0)
        self.b_entry = ttk.Entry(self.config_frame)
        self.b_entry.grid(row=1, column=1)

        self.config_button = ttk.Button(self.config_frame, text="Apply", command=self.configure_a_b)
        self.config_button.grid(row=2, columnspan=2)

        self.export_button = ttk.Button(self, text="Export XL Report", command=self.export_xl_report)
        self.export_button.pack()

        
        self.update_status()

    def update_status(self):
        current_status = self.tekx_simulator.get_current_status()
        self.do1_value.config(text=current_status['DO1'])
        self.do2_value.config(text=current_status['DO2'])
        self.tx_value.config(text=f"{current_status['Tx']} °C / {current_status['Tx']*9/5+32} °F")

    def observe_trends(self):
        trends = self.tekx_simulator.observe_trends_over_week()
        for date, status in trends:
            print(f"Date: {date}, Status: {status}")
        messagebox.showinfo("Trends Observation", "Trends observed successfully. Check console.")

    def configure_a_b(self):
        try:
            A_value = int(self.a_entry.get())
            B_value = int(self.b_entry.get())
            if A_value not in [0, 1] or B_value not in [0, 1]:
                raise ValueError
            self.tekx_simulator.configure_A_B_settings(A_value, B_value)
            messagebox.showinfo("Configuration", "A & B settings configured successfully.")
            self.update_status()  
        except ValueError:
            messagebox.showerror("Error", "Invalid input for A or B. Please enter 0 or 1.")

    def export_xl_report(self):
        trends = self.tekx_simulator.observe_trends_over_week()
        df = pd.DataFrame(trends, columns=['Timestamp', 'Status'])
        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
        if file_path:
            df.to_excel(file_path, index=False)
            messagebox.showinfo("Export Successful", f"XL report exported successfully to:\n{file_path}")

if __name__ == "__main__":
    app = DeviceManagerApp()
    app.mainloop()
