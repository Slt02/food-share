import tkinter as tk
from tkinter import ttk, messagebox
from DeliveryController import DeliveryController

class AvailableRequestsScreen:
    """Λίστα τρεχόντων (pending) αιτημάτων και ανάθεση σε Drop-off Agent."""

    def __init__(self, parent, agent_id: int):
        self.parent = parent
        self.agent_id = agent_id
        self.ctrl = DeliveryController()

        self.win = tk.Toplevel(parent)
        self.win.title("Available Requests")
        self.win.geometry("560x420")

        self._build_ui()
        self.refresh()

    # ------------------------------------------------------------
    # UI
    # ------------------------------------------------------------
    def _build_ui(self):
        ttk.Label(self.win, text="Pending Food-Requests",
                  font=("Helvetica", 15, "bold")).pack(pady=8)

        cols = ("Request ID", "Customer ID", "Address", "People")
        self.tree = ttk.Treeview(self.win, columns=cols,
                                 show="headings", height=12)
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, anchor="center")
        self.tree.pack(fill="both", expand=True, padx=10)

        ttk.Button(self.win, text="Assign selected to me",
                   command=self.on_assign).pack(pady=12)

    # ------------------------------------------------------------
    # Data helpers
    # ------------------------------------------------------------
    def refresh(self):
        """Ανανεώνει τη λίστα με τα διαθέσιμα αιτήματα."""
        for i in self.tree.get_children():
            self.tree.delete(i)

        for r_id, c_id, addr, ppl in self.ctrl.list_available_requests():
            self.tree.insert("", "end", values=(r_id, c_id, addr, ppl))

    def on_assign(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("No selection", "Διάλεξε πρώτα ένα αίτημα.")
            return

        request_id = self.tree.item(sel[0])["values"][0]
        ok = self.ctrl.assign_request(request_id, self.agent_id)

        messagebox.showinfo("Assign",
                            "Ανάθεση ολοκληρώθηκε!" if ok else "Η ανάθεση απέτυχε.")
        if ok:
            self.refresh()
