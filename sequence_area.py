import tkinter as tk


class SequenceArea:
    def __init__(self, parent):
        self.frame = tk.Frame(parent, bg="#f0f0f0")
        self.blocks = []

    def contains(self, x, y):
        px = self.frame.winfo_rootx()
        py = self.frame.winfo_rooty()
        pw = self.frame.winfo_width()
        ph = self.frame.winfo_height()
        # is the widget x,y over the threshold between palatte and sequence area
        return (px < x < px + pw) and (py < y < py + ph)

    def add_block(self, block):
        self.blocks.append(block)
        block.pack(anchor="w", pady=15, padx=50)

    def dump_program(self):  # returns a list of block types in sequence
        program = {}

        for block in self.blocks:
            program[f"block_{self.blocks.index(block)}"] = {
                "type": block.block_name,
                "params": block.get_params_dict()
            }
        return program
