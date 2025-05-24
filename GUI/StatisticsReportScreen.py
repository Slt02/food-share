# StatisticsReportScreen.py
import tkinter as tk
from tkinter import messagebox, scrolledtext
from StatisticsReportController import StatisticsReportController


class StatisticsReportScreen:
    """Παράθυρο που εμφανίζει το report ή μήνυμα αν απουσιάζουν δεδομένα."""

    def __init__(self, parent, admin_id):
        self.window = tk.Toplevel(parent)
        self.window.title("Statistics & Reports")
        self.window.geometry("500x600")

        controller = StatisticsReportController()
        report = controller.build_report(admin_id)

        if report is None:  # Εναλλακτική Ροή 1
            messagebox.showinfo(
                "Statistics & Reports", "No statistics or reports available."
            )
            self.window.destroy()
            return

        txt = scrolledtext.ScrolledText(self.window, wrap="word", font=("Helvetica", 11))
        txt.insert("1.0", report.content)
        txt.configure(state="disabled")
        txt.pack(expand=True, fill="both", padx=20, pady=20)

        tk.Button(self.window, text="Close", command=self.window.destroy).pack(pady=10)
