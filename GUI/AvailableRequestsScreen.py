class AvailableRequestsScreen:
    def __init__(self, parent, agent_id):
        self.ctrl  = DeliveryController()
        self.agent_id = agent_id
        self.win = tk.Toplevel(parent)
        self.win.title("Available Requests")
        self.win.geometry("500x380")
        # treeview
        cols = ("Request ID", "Customer", "Address", "People")
        self.tree = ttk.Treeview(self.win, columns=cols, show="headings", height=10)
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, anchor="center")
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)
        ttk.Button(self.win, text="Assign Selected", command=self.on_assign).pack(pady=8)
        self.refresh()

    def refresh(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for rec in self.ctrl.list_available_requests():
            self.tree.insert("", "end", values=(rec["request_id"], rec["customer_id"], rec["address"], rec["people"]))
        if not self.tree.get_children():
            messagebox.showinfo("Info", "No pending requests at this time.")

    def on_assign(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("No selection", "Please select a request to assign.")
            return
        req_id = self.tree.item(sel[0])["values"][0]
        ok, msg = self.ctrl.assign_request(req_id, self.agent_id)
        messagebox.showinfo("Assign", msg)
        if ok:
            self.refresh()