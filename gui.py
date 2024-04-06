import tkinter as tk
import os as os
from get_parameters import get_parameters, param_dict_extract
from tkinter import filedialog

def gui():
        
    # ==================================
    # Menu and Button functions
    # ==================================
    def open_file():
        # Open the file dialog and get the selected file path
        file_path = filedialog.askopenfilename(title="Open file", filetypes=(("Excel files", "*.xlsx"), ("All files", "*.*")))
        
        if file_path:  # Check if a file was selected
            struct_filename = os.path.basename(file_path)
            materials_data, parameter_dict = get_parameters(struct_filename)
            
            update_gui(parameter_dict)
    
    def save_file():
        pass
    
    def save_file_as():
        pass
    
    def mechanical_impedances(parameter_dict):
        mechanical_impedances(parameter_dict)
    
    def electrical_impedances():
        pass
    
    def transfer_functions():
        pass
    
    # ==================================
    # Create row and column layout
    # ==================================
    
    def update_gui(parameter_dict): # Call function to update the GUI with new parameters
        
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
        
        d_backing = ""  # The backing has infinite thickness
        d_back_layers = [d * 1e3 for d in d_back_layers]
        d_piezo *= 1e3
        d_front_layers = [d * 1e3 for d in d_front_layers]
        d_load = ""  # The load has infinite thickness

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
        
        #=== Start creating the row and column layout
        current_row = 1 # Keep track of the current row

        
        # Header row
        column_names = ["", "Materials", "c [m/s]", "z_c [Mrayl]", "d [mm]", "Q_m", "h [10^9 V/m]", "eps_rel"]
        for col, name in enumerate(column_names):
            tk.Label(root, text=name, font=('Arial', 12, 'bold'), borderwidth=2, relief="solid").grid(row=current_row, column=col, sticky="nsew", padx=1, pady=1)

        current_row += 1
        
        # Backing heading
        tk.Label(root, text="Backing", font=('Arial', 12, 'bold'), borderwidth=2, relief="solid").grid(row=current_row, column=0, columnspan=8, sticky="nsew", padx=1, pady=1)
        current_row += 1

        # Backing layer row
        tk.Label(root, text="", font=('Arial', 10), borderwidth=2, relief="solid").grid(row=current_row, column=0, sticky="nsew", padx=1, pady=1)
        tk.Label(root, text=mat_backing, font=('Arial', 10), borderwidth=2, relief="solid").grid(row=current_row, column=1, sticky="nsew", padx=1, pady=1)
        tk.Label(root, text=str(c_backing), font=('Arial', 10), borderwidth=2, relief="solid").grid(row=current_row, column=2, sticky="nsew", padx=1, pady=1)
        tk.Label(root, text=str(z_c_backing), font=('Arial', 10), borderwidth=2, relief="solid").grid(row=current_row, column=3, sticky="nsew", padx=1, pady=1)
        tk.Label(root, text=str(d_backing), font=('Arial', 10), borderwidth=2, relief="solid", bg="lightgrey").grid(row=current_row, column=4, sticky="nsew", padx=1, pady=1)
        tk.Label(root, text=str(q_backing), font=('Arial', 10), borderwidth=2, relief="solid").grid(row=current_row, column=5, sticky="nsew", padx=1, pady=1)
        tk.Label(root, text="", font=('Arial', 10), borderwidth=2, relief="solid", bg="lightgrey").grid(row=current_row, column=6, sticky="nsew", padx=1, pady=1)
        tk.Label(root, text="", font=('Arial', 10), borderwidth=2, relief="solid", bg="lightgrey").grid(row=current_row, column=7, sticky="nsew", padx=1, pady=1)
        current_row += 1

        # Back heading
        tk.Label(root, text="Back layers", font=('Arial', 12, 'bold'), borderwidth=2, relief="solid").grid(row=current_row, column=0, columnspan=8, sticky="nsew", padx=1, pady=1)
        current_row += 1

        # Back layers rows
        for index, row in back_layers_params.iterrows():
            tk.Label(root, text="", font=('Arial', 10), borderwidth=2, relief="solid").grid(row=current_row, column=0, sticky="nsew", padx=1, pady=1)
            tk.Label(root, text=row["Materials"], font=('Arial', 10), borderwidth=2, relief="solid").grid(row=current_row, column=1, sticky="nsew", padx=1, pady=1)
            tk.Label(root, text=str(row["c[m/s]"]), font=('Arial', 10), borderwidth=2, relief="solid").grid(row=current_row, column=2, sticky="nsew", padx=1, pady=1)
            tk.Label(root, text=str(row["z_c[MRayl]"]), font=('Arial', 10), borderwidth=2, relief="solid").grid(row=current_row, column=3, sticky="nsew", padx=1, pady=1)
            tk.Label(root, text=str(row["d[mm]"]), font=('Arial', 10), borderwidth=2, relief="solid").grid(row=current_row, column=4, sticky="nsew", padx=1, pady=1)
            tk.Label(root, text=str(row["Q_m"]), font=('Arial', 10), borderwidth=2, relief="solid").grid(row=current_row, column=5, sticky="nsew", padx=1, pady=1)
            tk.Label(root, text="", font=('Arial', 10), borderwidth=2, relief="solid", bg="lightgrey").grid(row=current_row, column=6, sticky="nsew", padx=1, pady=1)
            tk.Label(root, text="", font=('Arial', 10), borderwidth=2, relief="solid", bg="lightgrey").grid(row=current_row, column=7, sticky="nsew", padx=1, pady=1)
            current_row += 1

        # Piezo heading
        tk.Label(root, text="Piezo", font=('Arial', 12, 'bold'), borderwidth=2, relief="solid").grid(row=current_row, column=0, columnspan=8, sticky="nsew", padx=1, pady=1)
        current_row += 1

        # Piezo layer row
        tk.Label(root, text="", font=('Arial', 10), borderwidth=2, relief="solid").grid(row=current_row, column=0, sticky="nsew", padx=1, pady=1)
        tk.Label(root, text=mat_piezo, font=('Arial', 10), borderwidth=2, relief="solid").grid(row=current_row, column=1, sticky="nsew", padx=1, pady=1)
        tk.Label(root, text=str(c_piezo), font=('Arial', 10), borderwidth=2, relief="solid").grid(row=current_row, column=2, sticky="nsew", padx=1, pady=1)
        tk.Label(root, text=str(z_c_piezo), font=('Arial', 10), borderwidth=2, relief="solid").grid(row=current_row, column=3, sticky="nsew", padx=1, pady=1)
        tk.Label(root, text=str(d_piezo), font=('Arial', 10), borderwidth=2, relief="solid").grid(row=current_row, column=4, sticky="nsew", padx=1, pady=1)
        tk.Label(root, text=str(q_piezo), font=('Arial', 10), borderwidth=2, relief="solid").grid(row=current_row, column=5, sticky="nsew", padx=1, pady=1)
        tk.Label(root, text=str(h), font=('Arial', 10), borderwidth=2, relief="solid").grid(row=current_row, column=6, sticky="nsew", padx=1, pady=1)
        tk.Label(root, text=str(eps_r), font=('Arial', 10), borderwidth=2, relief="solid").grid(row=current_row, column=7, sticky="nsew", padx=1, pady=1)
        current_row += 1

        # Front heading
        tk.Label(root, text="Front layers", font=('Arial', 12, 'bold'), borderwidth=2, relief="solid").grid(row=current_row, column=0, columnspan=8, sticky="nsew", padx=1, pady=1)
        current_row += 1

        # Front layers rows
        for index, row in front_layers_params.iterrows():
            tk.Label(root, text="", font=('Arial', 10), borderwidth=2, relief="solid").grid(row=current_row, column=0, sticky="nsew", padx=1, pady=1)
            tk.Label(root, text=row["Materials"], font=('Arial', 10), borderwidth=2, relief="solid").grid(row=current_row, column=1, sticky="nsew", padx=1, pady=1)
            tk.Label(root, text=str(row["c[m/s]"]), font=('Arial', 10), borderwidth=2, relief="solid").grid(row=current_row, column=2, sticky="nsew", padx=1, pady=1)
            tk.Label(root, text=str(row["z_c[MRayl]"]), font=('Arial', 10), borderwidth=2, relief="solid").grid(row=current_row, column=3, sticky="nsew", padx=1, pady=1)
            tk.Label(root, text=str(row["d[mm]"]), font=('Arial', 10), borderwidth=2, relief="solid").grid(row=current_row, column=4, sticky="nsew", padx=1, pady=1)
            tk.Label(root, text=str(row["Q_m"]), font=('Arial', 10), borderwidth=2, relief="solid").grid(row=current_row, column=5, sticky="nsew", padx=1, pady=1)
            tk.Label(root, text="", font=('Arial', 10), borderwidth=2, relief="solid", bg="lightgrey").grid(row=current_row, column=6, sticky="nsew", padx=1, pady=1)
            tk.Label(root, text="", font=('Arial', 10), borderwidth=2, relief="solid", bg="lightgrey").grid(row=current_row, column=7, sticky="nsew", padx=1, pady=1)
            current_row += 1

        # Load heading
        tk.Label(root, text="Load", font=('Arial', 12, 'bold'), borderwidth=2, relief="solid").grid(row=current_row, column=0, columnspan=8, sticky="nsew", padx=1, pady=1)
        current_row += 1

        # Load layer row
        tk.Label(root, text="", font=('Arial', 10), borderwidth=2, relief="solid").grid(row=current_row, column=0, sticky="nsew", padx=1, pady=1)
        tk.Label(root, text=mat_load, font=('Arial', 10), borderwidth=2, relief="solid").grid(row=current_row, column=1, sticky="nsew", padx=1, pady=1)
        tk.Label(root, text=str(c_load), font=('Arial', 10), borderwidth=2, relief="solid").grid(row=current_row, column=2, sticky="nsew", padx=1, pady=1)
        tk.Label(root, text=str(z_c_load), font=('Arial', 10), borderwidth=2, relief="solid").grid(row=current_row, column=3, sticky="nsew", padx=1, pady=1)
        tk.Label(root, text=str(d_load), font=('Arial', 10), borderwidth=2, relief="solid", bg="lightgrey").grid(row=current_row, column=4, sticky="nsew", padx=1, pady=1)
        tk.Label(root, text=str(q_load), font=('Arial', 10), borderwidth=2, relief="solid").grid(row=current_row, column=5, sticky="nsew", padx=1, pady=1)
        tk.Label(root, text="", font=('Arial', 10), borderwidth=2, relief="solid", bg="lightgrey").grid(row=current_row, column=6, sticky="nsew", padx=1, pady=1)
        tk.Label(root, text="", font=('Arial', 10), borderwidth=2, relief="solid", bg="lightgrey").grid(row=current_row, column=7, sticky="nsew", padx=1, pady=1)
        current_row += 1

        for col in range(7):  # Adjust grid column configuration for equal width
            root.grid_columnconfigure(col, weight=1)


    def initialize_gui(): # Default values for initializing the GUI
        struct_filename = "struct_1front_1back_water_air.xlsx"
        materials_data, parameter_dict = get_parameters(struct_filename)

        return parameter_dict

    #==================================
    
    root = tk.Tk()
    root.title("Layered Structure GUI")
    root.geometry("1000x600")
    
    parameter_dict = initialize_gui()
    update_gui(parameter_dict)
    
    # Menu
    menu_bar = tk.Menu(root)

    ## Create File menu
    file_menu = tk.Menu(menu_bar, tearoff=0)
    file_menu.add_command(label="Open", command=open_file)
    file_menu.add_command(label="Save")
    file_menu.add_command(label="Save as")
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=root.quit)
    menu_bar.add_cascade(label="File", menu=file_menu)

    ## Create Help menu
    help_menu = tk.Menu(menu_bar, tearoff=0)
    help_menu.add_command(label="About")
    menu_bar.add_cascade(label="Help", menu=help_menu)

    root.config(menu=menu_bar)

    # Button row
    current_row = 0 # Keep track of the current row
        
    button_frame = tk.Frame(root)
    button_frame.grid(row=current_row, column=0, columnspan=8, sticky="nsew", padx=1, pady=1)

    button_names = ["Mechanical Impedance", "Electrical Impedance", "El. Config", "Transfer Functions"]
    for i, name in enumerate(button_names):
        button = tk.Button(button_frame, text=name, font=('Arial', 10), borderwidth=2, relief="solid")
        button.grid(row=0, column=i, sticky="nsew", padx=1, pady=1)
    
    
    
    
    
    root.mainloop()


#=========================
#=========================

if __name__ == "__main__":
    
    gui()