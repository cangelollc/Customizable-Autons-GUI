import tkinter as tk


class Block:
    def __init__(self, parent, block_type, color, is_template=False):
        self.dragging = False

        self.block_type = block_type
        self.color = color
        self.is_template = is_template

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
            text=block_type.value,
            bg=color,
            fg="white",
            font=("Arial", 10, "bold")
        )
        self.title.pack(anchor="w", padx=1, pady=(4, 2))

        # Parameter entries TODO: make this a loop
        self.param1 = tk.Entry(
            self.widget, width=15, bg="white", textvariable=tk.StringVar(value="default"))
        self.param2 = tk.Entry(self.widget, width=16)

        params_frame = tk.Frame(self.widget)
        params_frame.pack(in_=self.widget, anchor="w",
                          padx=6, pady=(4, 6), fill="x")

        self.param1.pack(side="left", padx=(0, 6), ipady=3)
        self.param2.pack(side="left", ipady=3)

        for entry in (self.param1, self.param2):
            entry.bind("<Key>", lambda e: print("typing works"))

            entry.bind("<Button-1>", lambda e, ent=entry: ent.focus_set())

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

    def clone(self, new_parent):
        return Block(
            new_parent,
            self.block_type,
            self.color,
            is_template=False
        )

    def destroy(self):
        self.widget.destroy()
