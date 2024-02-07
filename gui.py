import tkinter as tk
from tkinter import ttk 
from ftplib import FTP
import os
import datetime
import schedule
import time

class FTPUploaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("FTP")

        # Apply styling
        style = ttk.Style()
        style.configure("TLabel", font=("Helvetica", 12))
        style.configure("TButton", font=("Helvetica", 12))

        # Create FTP details inputs
        self.ftp_host_label = ttk.Label(root, text="FTP Host:")
        self.ftp_host_label.pack(pady=10) 

        self.ftp_host_entry = ttk.Entry(root)
        self.ftp_host_entry.pack(pady=10)  

        self.ftp_user_label = ttk.Label(root, text="FTP Потребител:")
        self.ftp_user_label.pack(pady=10)

        self.ftp_user_entry = ttk.Entry(root)
        self.ftp_user_entry.pack(pady=10)

        self.ftp_pass_label = ttk.Label(root, text="FTP Парола:")
        self.ftp_pass_label.pack(pady=10)

        self.ftp_pass_entry = ttk.Entry(root, show="*")
        self.ftp_pass_entry.pack(pady=10)

        self.local_file_label = ttk.Label(root, text="Път до Папка:")
        self.local_file_label.pack(pady=10)

        self.local_file_entry = ttk.Entry(root)
        self.local_file_entry.pack(pady=10)

        # Create time input
        self.time_label = ttk.Label(root, text="Час на изпълнение (ЧЧ:ММ):")
        self.time_label.pack(pady=10)

        self.time_entry = ttk.Entry(root)
        self.time_entry.pack(pady=2)

        # Create Run button
        self.run_button = ttk.Button(root, text="Изпълни", command=self.schedule_ftp_upload)
        self.run_button.pack(pady=15) 

    def run_ftp_upload(self):
        ftp_host = self.ftp_host_entry.get()
        ftp_user = self.ftp_user_entry.get()
        ftp_pass = self.ftp_pass_entry.get()
        folder_path = self.local_file_entry.get()

        current_date = datetime.date.today()
        formatted_date = current_date.strftime("%d/%m/%Y")

        try:
            # Connect to FTP
            ftp = FTP(ftp_host)
            ftp.login(user=ftp_user, passwd=ftp_pass)

            # Change to the desired remote folder
            ftp.cwd(ftp_folder)

            # Get the latest file path in the specified folder
            latest_file_path = self.get_latest_file_path_in_folder(folder_path)

            # Get the original filename from the local file path
            original_file_name = os.path.basename(latest_file_path)

            # Upload the content of the local file with the original filename
            with open(latest_file_path, "rb") as local_file:
                ftp.storbinary("STOR " + original_file_name, local_file)

            print("Успешно качен файл!" + formatted_date)

            # Close the FTP connection
            ftp.quit()
        except Exception as e:
            print("Error:", e)

    def get_latest_file_path_in_folder(self, folder_path):
        try:
            # List all files in the folder
            files = os.listdir(folder_path)

            # Filter out directories and get creation timestamps
            file_timestamps = [(os.path.join(folder_path, f), os.path.getctime(os.path.join(folder_path, f))) for f in files if os.path.isfile(os.path.join(folder_path, f))]

            # Find the path of the latest file using max() function
            latest_file_path = max(file_timestamps, key=lambda x: x[1])[0]

            return latest_file_path
        except Exception as e:
            print("Error:", e)

    def schedule_ftp_upload(self):
        execution_time = self.time_entry.get()
        try:
            # Schedule the script to run every day at the specified time
            schedule.every().day.at(execution_time).do(self.run_ftp_upload)

            # Keep the script running
            while True:
                schedule.run_pending()
                time.sleep(1)
        except Exception as e:
            print("Error:", e)        

if __name__ == "__main__":
    ftp_folder = "/"
    root = tk.Tk()
    app = FTPUploaderApp(root)
    root.mainloop()
