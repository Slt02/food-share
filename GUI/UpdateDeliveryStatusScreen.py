# GUI/UpdateDeliveryStatusScreen.py
import tkinter as tk
from tkinter import ttk, messagebox
from DeliveryController import DeliveryController

class UpdateDeliveryStatusScreen:
    def __init__(self, parent, agent_id):
        self.parent = parent
        self.agent_id = agent_id
        self.controller = DeliveryController()

        self.window = tk.Toplevel(parent)
        self.window.title("Update Delivery Status")
        self.window.geometry("450x400")

        self.build_ui()
        self.refresh_list()

    def build_ui(self):
        ttk.Label(self.window, text="My Deliveries",
                  font=("Helvetica", 14, "bold")).pack(pady=10)

        cols = ("Delivery ID", "Request ID", "Status", "ETA")
        self.tree = ttk.Treeview(self.window, columns=cols, show="headings", height=8)
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, anchor="center")
        self.tree.pack(fill="both", expand=True, padx=10)

        form = ttk.Frame(self.window)
        form.pack(pady=15)

        ttk.Label(form, text="New Status").grid(row=0, column=0, padx=5, pady=2)
        self.status_var = tk.StringVar(value="in_transit")
        status_cb = ttk.Combobox(form, textvariable=self.status_var,
                                 values=["pending","in_transit","completed"], state="readonly")
        status_cb.grid(row=0, column=1, padx=5)

        ttk.Label(form, text="ETA (YYYY-MM-DD HH:MM)").grid(row=1, column=0, padx=5, pady=2)
        self.eta_entry = ttk.Entry(form, width=20)
        self.eta_entry.grid(row=1, column=1, padx=5)

        ttk.Button(self.window, text="Update Selected",
                   command=self.on_update).pack(pady=10)

    def refresh_list(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for rec in self.controller.list_my_deliveries(self.agent_id):
            eta_fmt = rec["eta"].strftime("%Y-%m-%d %H:%M") if rec["eta"] else "-"
            self.tree.insert("", "end",
                             values=(rec["delivery_id"], rec["request_id"],
                                     rec["status"], eta_fmt))

    def on_update(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("No selection", "Please select a delivery.")
            return
        delivery_id = self.tree.item(sel[0])["values"][0]

        ok, msg = self.controller.update_status(
            delivery_id,
            self.status_var.get(),
            self.eta_entry.get().strip() or None
        )
        messagebox.showinfo("Update", msg)
        if ok:
            self.refresh_list()
