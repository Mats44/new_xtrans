# GUI for program

import tkinter as tk
from get_parameters import get_parameters, param_dict_extract

def gui(parameter_dict):
    
    # Initiate Variables
    (
        (
            f,
            f_min,
            f_max,
            f_c,
            w,
            column_labels,
            z_elport_termination,
            len_load,
            len_front_layers,
            len_piezo,
            len_back_layers,
            len_backing,
            len_layers,
            len_f,
            load_params,
            front_layers_params,
            piezo_params,
            back_layers_params,
            backing_params,
            c_load,
            z_c_load,
            d_load,
            q_load,
            c_front_layers,
            z_c_front_layers,
            d_front_layers,
            q_front_layers,
            c_piezo,
            z_c_piezo,
            d_piezo,
            h,
            eps_r,
            q_piezo,
            c_back_layers,
            z_c_back_layers,
            d_back_layers,
            q_back_layers,
            c_backing,
            z_c_backing,
            d_backing,
            q_backing,
        )
    ) = param_dict_extract(parameter_dict)
    
    d_backing *= 1e3
    d_back_layers = [d * 1e3 for d in d_back_layers]
    d_piezo *= 1e3
    d_front_layers = [d * 1e3 for d in d_front_layers]
    d_load *= 1e3

    z_c_backing /= 1e6
    z_c_back_layers = [z_c / 1e6 for z_c in z_c_back_layers]
    z_c_piezo /= 1e6
    z_c_front_layers = [z_c / 1e6 for z_c in z_c_front_layers]
    z_c_load /= 1e6
    
    h /= 1e9
    
    mat_backing = backing_params["Materials"]
    mat_back_layers = back_layers_params["Materials"]
    mat_piezo = piezo_params["Materials"]
    mat_front_layers = front_layers_params["Materials"]
    mat_load = load_params["Materials"]
    
    # Update the 'backing' list to include 'mat_backing' at the start
    backing = [mat_backing, c_backing, z_c_backing, d_backing, q_backing]

    # For back_layers, piezo, and front_layers, prepend the materials name similarly if needed
    back_layers = [
        [mat_back_layers[i], c_back_layers[i], z_c_back_layers[i], d_back_layers[i], q_back_layers[i]]
        for i in range(len(c_back_layers))
    ][::-1]  # Assuming you want to reverse the order for some reason

    piezo = [mat_piezo, c_piezo, z_c_piezo, d_piezo, q_piezo, h, eps_r]

    front_layers = [
        [mat_front_layers[i], c_front_layers[i], z_c_front_layers[i], d_front_layers[i], q_front_layers[i]]
        for i in range(len(c_front_layers))
    ]
    
    load = [mat_load, c_load, z_c_load, d_load, q_load]
        
    # Initialize main window
    root = tk.Tk()
    root.title("Layered Structure GUI")
    root.geometry("1000x600")

    # Track all rows for dynamic updates
    all_rows = []

    def create_header_row(parent):
        column_names = ["", "Materials", "c [m/s]", "z_c [Mrayl]", "d [mm]", "Q_m", "h [10^9 V/m]", "eps_rel"]  # Add an empty string for the first column
        for col, name in enumerate(column_names):
            tk.Label(parent, text=name, font=('Arial', 12, 'bold'), borderwidth=2, relief="solid").grid(row=0, column=col, sticky="nsew", padx=1, pady=1)

    def add_row_below(current_row, parent, row_data, all_rows):
        # Increment the row indices for existing rows below the current row
        for row in all_rows:
            if row['index'] > current_row:
                row['index'] += 1
                # Update the grid position for all widgets in this row
                for widget in row['widgets']:
                    widget.grid(row=row['index'])

        # Insert the new row at the current_row + 1
        new_row_index = current_row + 1
        new_row_widgets = []  # Keep track of widgets in the new row for future adjustments

        # Add the necessary row with dynamic content, similar to create_row logic
        create_row(parent, "", new_row_index, values=row_data, all_rows=all_rows, is_grayed_out=False, show_plus_button=True)
        
        # Sort all_rows based on the updated indices to maintain order
        all_rows.sort(key=lambda x: x['index'])

    def create_plus_button(row, parent, all_rows):
        def on_click():
            add_row_below(row, parent, ["New Material", "0", "0", "0", "0"], all_rows)

        plus_button = tk.Button(parent, text="+", command=on_click)
        plus_button.grid(row=row, column=0, sticky="nsew", padx=1, pady=1)
        all_rows.append({'index': row, 'widgets': [plus_button]})  # Track the "+" button row

    def create_row(parent, text, row, values=None, is_heading=False, is_grayed_out=False, show_plus_button=False, all_rows=None):
        if show_plus_button:
            create_plus_button(row, parent, all_rows)
        
        if is_heading:
            # Create a header label, but skip the first column as it's for the "+" button
            label = tk.Label(parent, text=text, font=('Arial', 12, 'bold'), borderwidth=1, relief="solid")
            label.grid(row=row, column=1, columnspan=7, sticky="nsew", padx=1, pady=1)
            widgets = [label]
        else:
            widgets = []
            # Make the "Materials" column interactive for non-header rows
            material_entry = tk.Entry(parent, borderwidth=1, relief="solid")
            material_entry.grid(row=row, column=1, sticky="nsew", padx=1, pady=1)
            material_entry.insert(0, values[0] if values else "")  # Pre-fill with the material name, if provided
            widgets.append(material_entry)

            # Continue with the rest of the columns as before
            for col in range(2, 8):  # Adjust loop to start from 2 due to the new "+" button column
                entry = tk.Entry(parent, borderwidth=1, relief="solid")
                entry.grid(row=row, column=col, sticky="nsew", padx=1, pady=1)
                if values and col - 1 < len(values):  # Adjust for the presence of the "+" button and the material entry
                    entry.insert(0, str(values[col - 1]))  # Adjust index for values
                else:
                    entry.insert(0, "N/A" if not is_heading else "")
                    if is_grayed_out:
                        entry.config(state='readonly')
                widgets.append(entry)

        if all_rows is not None:
            all_rows.append({'index': row, 'widgets': widgets})

    create_header_row(root)  # Create header row at the very top

    current_row = 1  # Start from the first row after the header

    # Initialize rows for dynamic update tracking
    all_rows = []

    # Add Backing
    create_row(root, "Backing", current_row, is_heading=True, all_rows=all_rows)
    current_row += 1
    create_row(root, "", current_row, values=backing, all_rows=all_rows)
    current_row += 1

    # Add Back Layers
    create_row(root, "Back Layers", current_row, is_heading=True, all_rows=all_rows)
    current_row += 1
    for back_layer_values in back_layers:
        create_row(root, "", current_row, values=back_layer_values, show_plus_button=True, all_rows=all_rows)
        current_row += 1

    # Add Piezo Layer
    create_row(root, "Piezo Layer", current_row, is_heading=True, all_rows=all_rows)
    current_row += 1
    create_row(root, "", current_row, values=piezo, all_rows=all_rows)
    current_row += 1

    # Add Front Layers
    create_row(root, "Front Layers", current_row, is_heading=True, all_rows=all_rows)
    current_row += 1
    for front_layer_values in front_layers:
        create_row(root, "", current_row, values=front_layer_values, show_plus_button=True, all_rows=all_rows)
        current_row += 1

    # Add Load Header Row
    create_row(root, "Load", current_row, is_heading=True, all_rows=all_rows)
    current_row += 1
    create_row(root, "", current_row, values=load, all_rows=all_rows)
    current_row += 1

    for col in range(7):  # Adjust grid column configuration for equal width
        root.grid_columnconfigure(col, weight=1)

    root.mainloop()


if __name__ == "__main__":
    # Get variables
    #struct_filename = "struct_params_1back_3front_air_water.xlsx"
    struct_filename = "struct_params_3back_3front_air_water.xlsx"
    materials_data, parameter_dict = get_parameters(struct_filename)
    
    gui(parameter_dict)