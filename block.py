import tkinter as tk


class Block:
    def __init__(self, parent, block_name, color, params: list[dict], is_template=False):
        self.dragging = False
        self.block_name = block_name
        self.color = color
        self.is_template = is_template
        self.params = params

        width = 200 if not is_template else 140

        # Main container (THE BLOCK)
        self.widget = tk.Frame(
            parent,
            bg=color,
            bd=2,
            relief="raised",
            width=200
        )

        self.widget.pack_propagate(True)

        # Title label
        self.title = tk.Label(
            self.widget,
            text=block_name,
            bg=color,
            fg="white",
            font=("Arial", 10, "bold")
        )
        self.title.pack(anchor="w", padx=1, pady=(4, 2))

        self.param_entry_widget = {}

        params_frame = tk.Frame(self.widget, bg=self.color)
        params_frame.pack(anchor="w", padx=6, pady=(4, 6), fill="x")

        for param in params:
            name = param.get("name", "param")
            default = param.get("default", "")

            row = tk.Frame(params_frame, bg=self.color)
            row.pack(fill="x", pady=2)

            label = tk.Label(
                row,
                text=name + ":",
                bg=self.color,
                fg="white",
                font=("Arial", 9)
            )
            label.pack(side="left")

            entry = tk.Entry(row, textvariable=tk.StringVar(
                value=default), width=12)

            entry.pack(side="left", padx=4)

            entry.bind("<Button-1>", lambda e, ent=entry: ent.focus_set())

            self.param_entry_widget[name] = entry

        for block_segment in (self.widget, self.title):
            block_segment.bind("<ButtonPress-1>", self.on_press)
            block_segment.bind("<ButtonRelease-1>", self.on_release)

        self.drag_start = None
        self.drop_callback = None

    def pack(self, **kwargs):
        self.widget.pack(**kwargs)

    def on_press(self, event):
        self.dragging = True
        self.drag_start = (event.x_root, event.y_root)

    def on_release(self, event):
        if not self.dragging:
            return

        self.dragging = False

        if self.drop_callback:
            self.drop_callback(self, event.x_root, event.y_root)

    def get_params_dict(self):
        """retrive the current entered parameters as a dict"""
        current_params = {}

        for param in self.param_entry_widget:
            current_params[param] = self.param_entry_widget[param].get()

        print("Current parameters for block", self.block_name)
        print(current_params)

        return current_params

    def clone(self, new_parent):
        return Block(
            parent=new_parent,
            block_name=self.block_name,
            color=self.color,
            params=self.params,
            is_template=False
        )

    def destroy(self):
        self.widget.destroy()
