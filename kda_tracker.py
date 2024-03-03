import tkinter as tk
from tkinter import messagebox, filedialog
import datetime
import pandas as pd
import matplotlib.pyplot as plt

class KDATrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("KDA Tracker")
        
        # Center the window
        window_width = 400
        window_height = 300
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        center_x = int(screen_width/2 - window_width / 2)
        center_y = int(screen_height/2 - window_height / 2)
        self.root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        
        # User name
        self.name_label = tk.Label(root, text="Enter Your Name:")
        self.name_label.pack()
        self.name_entry = tk.Entry(root)
        self.name_entry.pack()
        
        # Kills
        self.kills_label = tk.Label(root, text="Enter Kills:")
        self.kills_label.pack()
        self.kills_entry = tk.Entry(root)
        self.kills_entry.pack()
        
        # Deaths
        self.deaths_label = tk.Label(root, text="Enter Deaths:")
        self.deaths_label.pack()
        self.deaths_entry = tk.Entry(root)
        self.deaths_entry.pack()
        
        # Assists
        self.assists_label = tk.Label(root, text="Enter Assists:")
        self.assists_label.pack()
        self.assists_entry = tk.Entry(root)
        self.assists_entry.pack()
        
        # Submit Button
        self.submit_button = tk.Button(root, text="Submit", command=self.calculate_and_save_kda)
        self.submit_button.pack()
        
        # Show KDA Graph Button
        self.plot_button = tk.Button(root, text="Show KDA Graph", command=self.load_and_plot_kda)
        self.plot_button.pack()
        
    def calculate_and_save_kda(self):
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showerror("Error", "Please enter your name.")
            return
        try:
            kills = int(self.kills_entry.get())
            deaths = int(self.deaths_entry.get())
            assists = int(self.assists_entry.get())
            kda = (kills + assists) / max(1, deaths)  # Prevent division by zero
            current_time = datetime.datetime.now()
            date_str_csv = current_time.strftime("%Y|%m|%d")
            date_str_txt = current_time.strftime("%Y-%m-%d")
            time_str_txt = current_time.strftime("%I:%M:%S %p")  # 12-hour format with AM/PM
            filename_csv = f"{name.replace(' ', '_')}_KDA.csv"
            filename_txt = f"{date_str_txt}_{name.replace(' ', '_')}.txt"
            
            # Append data to CSV with the new date format
            with open(filename_csv, "a") as file:
                file.write(f"{date_str_csv},{kills},{deaths},{assists},{kda:.2f}\n")
            
            # Create or append to the text file with standard time format
            data_str = f"Time: {time_str_txt}, Kills: {kills}, Deaths: {deaths}, Assists: {assists}, KDA: {kda:.2f}\n"
            try:
                with open(filename_txt, "r") as file:
                    if date_str_txt in file.read():
                        append_data = True
                    else:
                        append_data = False
            except FileNotFoundError:
                append_data = False
                
            with open(filename_txt, "a" if append_data else "w") as file:
                if not append_data:
                    file.write(f"Date: {date_str_txt}, Player: {name}\n")
                file.write(data_str)
            
            messagebox.showinfo("KDA Result", f"Your KDA is: {kda:.2f}\nDetails saved to {filename_csv} and {filename_txt}")
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for kills, deaths, and assists.")


    
    def load_and_plot_kda(self):
        filepath = filedialog.askopenfilename(title="Select your KDA data file", filetypes=(("CSV files", "*.csv"), ("All files", "*.*")))
        if not filepath:
            return
        
        data = pd.read_csv(filepath, names=['Date', 'Kills', 'Deaths', 'Assists', 'KDA'], parse_dates=['Date'])
        
        plt.figure(figsize=(10, 5))
        plt.plot(data['Date'], data['KDA'], marker='o', linestyle='-', color='b')
        plt.title('KDA Over Time')
        plt.xlabel('Date')
        plt.ylabel('KDA Ratio')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    root = tk.Tk()
    app = KDATrackerApp(root)
    root.mainloop()
