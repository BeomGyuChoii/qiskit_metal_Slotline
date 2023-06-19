"""
Slotline qiskit metal code by bgchoi 22.10.15
Slotline

"""


from tkinter import N
from qiskit_metal import draw, Dict
from qiskit_metal.qlibrary.core import QComponent
import numpy as np


class Slotline(QComponent):

    component_metadata = Dict(short_name="cpw", _qgeometry_table_path="True")
    """Component metadata"""

    # Currently setting the primary CPW length based on the coupling_length
    # May want it to be it's own value that the user can control?
    default_options = Dict(
        right_width="cpw_width",
        right_gap="cpw_gap",
        left_width="cpw_width",
        left_gap="cpw_gap",

        first_lower = "150um",#150
        chip_distance = "400um",#400
        slotline_length = "80um",#80
        slotline_fillet="20um",#width + 2 * gap
        fillet = "19.99um",
        slotline_count = 10  #line 개수 + 1
    )

    """Default connector options"""

    def make(self):
        """Build the component."""
        p = self.p
        multiple = 2
        first_lower = p.first_lower
        chip_distance = p.chip_distance
        slotline_count = p.slotline_count

        # Primary CPW
        right_x = p.right_gap + p.right_width / 2

        # Secondary CPW
        left_x = p.left_gap + p.left_width / 2

        right_start_line = draw.LineString(
            [
                [chip_distance / 2 + right_x, p.right_width / 2],
                [chip_distance / 2 + right_x, -p.right_width / 2],
            ]
        )

        right_end_line = draw.LineString(
            [
                [right_x + p.slotline_length / 2, -first_lower - p.slotline_fillet * (3*(slotline_count-1)-3) - p.right_width],
                [right_x + p.slotline_length / 2, -first_lower - p.slotline_fillet * (3*(slotline_count-1)-3) + p.right_width],
            ]
        )

        left_start_line = draw.LineString(
            [
                [-chip_distance / 2 - left_x, p.left_width / 2],
                [-chip_distance / 2 - left_x, -p.left_width / 2],
            ]
        )

        left_end_line = draw.LineString(
            [
                [-left_x + p.slotline_fillet + p.slotline_length / 2 - p.left_width, -first_lower - p.slotline_fillet * (3*(slotline_count-1)-3)],
                [-left_x + p.slotline_fillet + p.slotline_length / 2 + p.left_width, -first_lower - p.slotline_fillet * (3*(slotline_count-1)-3)],
            ]
        )

        pocket = draw.Polygon(
            [
                [-left_x - p.slotline_fillet * 3 - p.slotline_length / 2, -first_lower + p.slotline_fillet * 2],
                [-left_x - p.slotline_fillet * 3 - p.slotline_length / 2, -first_lower - p.slotline_fillet * (3*(slotline_count-1))],
                [right_x + p.slotline_length / 2 + p.slotline_fillet * 4, -first_lower - p.slotline_fillet * (3*(slotline_count-1))],
                [right_x + p.slotline_length / 2 + p.slotline_fillet * 4, -first_lower + p.slotline_fillet * 2],
                [-left_x - p.slotline_fillet * 3 - p.slotline_length / 2, -first_lower + p.slotline_fillet * 2],
            ]
        )
        
        # Rotate and Translate
        c_items = [
            pocket,
            right_start_line,
            right_end_line,
            left_start_line,
            left_end_line,
        ]

        for i in range(slotline_count):
            if i == 0:
                globals()['right{}'.format(i)] = draw.LineString(
                    [
                        [chip_distance / 2 + right_x, 0],
                        [right_x, 0],
                        [right_x, -first_lower],
                        [right_x + p.slotline_length / 2 , -first_lower],
                    ]
                )
                c_items.append(globals()['right{}'.format(i)])
            elif i == 1:
                globals()['right{}'.format(i)] = draw.LineString(
                    [
                        [right_x + p.slotline_length / 2 , -first_lower],
                        [right_x + p.slotline_length / 2 + p.slotline_fillet * multiple, -first_lower],
                        [right_x + p.slotline_length / 2 + p.slotline_fillet * multiple, -first_lower - p.slotline_fillet * 4],
                        [right_x - p.slotline_length / 2 , -first_lower - p.slotline_fillet * 4],
                    ]
                )
                c_items.append(globals()['right{}'.format(i)])
            elif i%2 == 0:
                globals()['right{}'.format(i)] = draw.LineString(
                    [
                        [right_x - p.slotline_length / 2 , -first_lower - p.slotline_fillet * (3*i-2)],
                        [right_x - p.slotline_length / 2 - p.slotline_fillet , -first_lower - p.slotline_fillet * (3*i-2)],
                        [right_x - p.slotline_length / 2 - p.slotline_fillet , -first_lower - p.slotline_fillet * (3*i)],
                        [right_x + p.slotline_length / 2 , -first_lower - p.slotline_fillet * (3*i)],
                            
                    ]
                )
                c_items.append(globals()['right{}'.format(i)])
            elif i == (slotline_count-1):
                globals()['right{}'.format(i)] = draw.LineString(
                    [
                        [right_x + p.slotline_length / 2 , -first_lower - p.slotline_fillet * (3*i-3)],
                        [right_x + p.slotline_length / 2 + right_x, -first_lower - p.slotline_fillet * (3*i-3)],
                        [right_x + p.slotline_length / 2 + right_x, -first_lower - p.slotline_fillet * (3*i-2)],
                        [right_x + p.slotline_length / 2 , -first_lower - p.slotline_fillet * (3*i-2)],
                            
                    ]
                )
                c_items.append(globals()['right{}'.format(i)])
            else:
                globals()['right{}'.format(i)] = draw.LineString(
                    [
                        [right_x + p.slotline_length / 2 , -first_lower - p.slotline_fillet * (3*i-3)],
                        [right_x + p.slotline_length / 2 + p.slotline_fillet * multiple, -first_lower - p.slotline_fillet * (3*i-3)],
                        [right_x + p.slotline_length / 2 + p.slotline_fillet * multiple, -first_lower - p.slotline_fillet * (3*i+1)],
                        [right_x - p.slotline_length / 2 , -first_lower - p.slotline_fillet * (3*i+1)],
                            
                    ]
                )
                c_items.append(globals()['right{}'.format(i)])
        for i in range(slotline_count):
            if i == 0:
                globals()['left{}'.format(i)] = draw.LineString(
                    [
                        [-chip_distance / 2 - left_x, 0],
                        [-left_x, 0],
                        [-left_x, -first_lower + p.slotline_fillet ],
                    ]
                )
                c_items.append(globals()['left{}'.format(i)])
            elif i == 1:
                globals()['left{}'.format(i)] = draw.LineString(
                    [
                        [-left_x, -first_lower + p.slotline_fillet ],
                        [-left_x, -first_lower - p.slotline_fillet],
                        [-left_x + p.slotline_fillet + p.slotline_length / 2 , -first_lower - p.slotline_fillet],
                    ]
                )
                c_items.append(globals()['left{}'.format(i)])
            elif i == 2:
                globals()['left{}'.format(i)] = draw.LineString(
                    [
                        [-left_x + p.slotline_fillet + p.slotline_length / 2 , -first_lower - p.slotline_fillet],
                        [-left_x + p.slotline_fillet + p.slotline_length / 2 + p.slotline_fillet, -first_lower - p.slotline_fillet],
                        [-left_x + p.slotline_fillet + p.slotline_length / 2 + p.slotline_fillet, -first_lower - p.slotline_fillet * 3],
                        [-left_x + p.slotline_fillet - p.slotline_length / 2 , -first_lower - p.slotline_fillet * 3],
                    ]
                )
                c_items.append(globals()['left{}'.format(i)])
            elif i%2 == 0:
                globals()['left{}'.format(i)] = draw.LineString(
                    [
                        [-left_x + p.slotline_fillet + p.slotline_length / 2 , -first_lower - p.slotline_fillet * (3*i-5)],
                        [-left_x + p.slotline_fillet + p.slotline_length / 2 + p.slotline_fillet, -first_lower - p.slotline_fillet * (3*i-5)],
                        [-left_x + p.slotline_fillet + p.slotline_length / 2 + p.slotline_fillet, -first_lower - p.slotline_fillet * (3*i-3)],
                        [-left_x + p.slotline_fillet - p.slotline_length / 2 , -first_lower - p.slotline_fillet * (3*i-3)],
                            
                    ]
                )
                c_items.append(globals()['left{}'.format(i)])
            else:
                globals()['left{}'.format(i)] = draw.LineString(
                    [
                        [-left_x + p.slotline_fillet - p.slotline_length / 2 , -first_lower - p.slotline_fillet * (3*i-6)],
                        [-left_x + p.slotline_fillet - p.slotline_length / 2 - p.slotline_fillet * multiple, -first_lower - p.slotline_fillet * (3*i-6)],
                        [-left_x + p.slotline_fillet - p.slotline_length / 2 - p.slotline_fillet * multiple, -first_lower - p.slotline_fillet * (3*i-2)],
                        [-left_x + p.slotline_fillet + p.slotline_length / 2 , -first_lower - p.slotline_fillet * (3*i-2)],
                            
                    ]
                )
                c_items.append(globals()['left{}'.format(i)])
        c_items_copy = c_items
        c_items = draw.rotate(c_items, p.orientation, origin=(0, 0))
        c_items = draw.translate(c_items, p.pos_x, p.pos_y)
        c_items_copy = c_items

        # Add to qgeometry tables
        for i in range(slotline_count):
            if i == (slotline_count-1):
                self.add_qgeometry(
                    "path", {f"right{i}" : globals()['right{}'.format(i)]}, 
                    width=p.right_width, 
                    fillet=0,
                )
                self.add_qgeometry(
                    "path", {f"right{i}_sub" : globals()['right{}'.format(i)]}, 
                    width=p.right_width + 2 * p.right_gap, 
                    subtract=True, 
                    fillet=0,
                )
            elif i%2 == 1:
                self.add_qgeometry(
                    "path", {f"right{i}" : globals()['right{}'.format(i)]}, 
                    width=p.right_width, 
                    fillet=p.fillet+p.slotline_fillet
                )
                self.add_qgeometry(
                    "path", {f"right{i}_sub" : globals()['right{}'.format(i)]}, 
                    width=p.right_width + 2 * p.right_gap, 
                    subtract=True, 
                    fillet=p.fillet+p.slotline_fillet,
                )
            else:
                self.add_qgeometry(
                    "path", {f"right{i}" : globals()['right{}'.format(i)]}, 
                    width=p.right_width, 
                    fillet=p.fillet
                )
                self.add_qgeometry(
                    "path", {f"right{i}_sub" : globals()['right{}'.format(i)]}, 
                    width=p.right_width + 2 * p.right_gap, 
                    subtract=True, 
                    fillet=p.fillet,
                )

        for i in range(slotline_count):
            if i%2 == 1:
                self.add_qgeometry(
                    "path", {f"left{i}" : globals()['left{}'.format(i)]}, 
                    width=p.left_width, 
                    fillet=p.fillet+p.slotline_fillet
                )
                self.add_qgeometry(
                    "path", {f"left{i}_sub" : globals()['left{}'.format(i)]}, 
                    width=p.left_width + 2 * p.left_gap, 
                    subtract=True, 
                    fillet=p.fillet+p.slotline_fillet,
                )
            else:
                self.add_qgeometry(
                    "path", {f"left{i}" : globals()['left{}'.format(i)]}, 
                    width=p.left_width, 
                    fillet=p.fillet
                )
                self.add_qgeometry(
                    "path", {f"left{i}_sub" : globals()['left{}'.format(i)]}, 
                    width=p.left_width + 2 * p.left_gap, 
                    subtract=True, 
                    fillet=p.fillet,
                )



        self.add_qgeometry('poly', dict(pocket=pocket), subtract=True, layer=p.layer)

        self.add_pin("right_start", points=right_start_line.coords, width=p.right_width)
        self.add_pin("left_start", points=left_start_line.coords, width=p.left_width)
