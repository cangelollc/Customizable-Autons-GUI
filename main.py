import json
import time
import tkinter as tk
from enum import Enum
from sequence_area import SequenceArea
from block import Block
from block_types import *
import nt_interface


class BlockTypes(Enum):
    TEST_ONE = "Test Block One"
    TEST_TWO = "Test Block Two"
    TEST_THREE = "Test Block Three"


# networktables will configure this for us eventually and we will build this dynamically

template_blocks = [
    (BlockTypes.TEST_ONE, "blue"),
    (BlockTypes.TEST_TWO, "blue"),
    (BlockTypes.TEST_THREE, "blue")
]

nt = nt_interface.NTInterface()

root = tk.Tk()
root.geometry("800x400")
root.title("Configurable Autonomous Program Builder")

# template boxes live here
palette = tk.Frame(root, width=450, bg="#dddddd")
palette.pack(side="left", fill="y")

program_container = tk.Frame(root)
program_container.pack(side="right", fill="both", expand=True)

sequence_area = SequenceArea(program_container)

dump_program_btn = tk.Button(
    program_container,
    text="Dump Program to Robot",
    bg="green",
    height=1,
    font=("Arial", 15, "bold"),
    command=lambda: nt.publish_routine_json(sequence_area.dump_program())
)

dump_program_btn.pack(
    side="top",
    fill="x",
    pady=5
)

# after the button *important*
sequence_area.frame.pack(fill="both", expand=True)


def handle_drop(block, x, y):
    """When the block is dropped in the sequence area, clone a non template block there."""
    print(f"Dropped block {block.block_name} at ({x}, {y})")

    if block.is_template:
        if sequence_area.contains(x, y):
            new_block = block.clone(sequence_area.frame)
            new_block.drop_callback = handle_drop
            sequence_area.add_block(new_block)
    else:
        if not sequence_area.contains(x, y):
            block.destroy()
            sequence_area.blocks.remove(block)

    # nt.publish_routine_json(sequence_area.dump_program())


blocks_json = nt.get_block_types_json()

blocks_json = json.loads(blocks_json)

print("Block Types JSON from NT:", blocks_json)
print()

# create blocks from the json data
for block_info in blocks_json:
    block_name = str(block_info)
    print(block_name)

    params_dict_lst = blocks_json.get(block_name).get(
        "params", {})  # List of param dicts

    for param in params_dict_lst:
        print(param)

    block = Block(palette, block_name=block_name, color="red",
                  params=params_dict_lst, is_template=True)

    block.drop_callback = handle_drop
    block.pack(pady=15, padx=15, fill="x")

    print()

root.mainloop()
