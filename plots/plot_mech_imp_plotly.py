# Import
import numpy as np
import plotly as py
import plotly.subplots as sp
import plotly.graph_objects as go
import plotly.express as px
from get_parameters import param_dict_extract

def plot_mech_imp_fwd(z_in_front, z_in_piezo, z_in_back, f, f_min, f_max):
    """
    Plot the mechanical impedance seen towards the backing (load -> piezo -> backing)
    """   
    # Plotting function
    fig = sp.make_subplots(rows=2, cols=2)

    f = f / 1e6  # convert to MHz
    f_min = f_min / 1e6
    f_max = f_max / 1e6

    line_width = 1

    # Function to get color from color scale
    color_scale = px.colors.sequential.Jet
    def get_color_from_scale(index, total_elements, color_scale):
        return color_scale[int((index / total_elements) * (len(color_scale) - 1))]

    # Plot z_in_front
    z_in_front = z_in_front / 1e6

    for i, row in enumerate(z_in_front):
        color = get_color_from_scale(i, len(z_in_front), color_scale)
        
        fig.add_trace(go.Scatter(x=list(f), y=np.real(row), mode='lines', name=f'Front layer {i+1}', line=dict(color=color, width=line_width), showlegend=True), row=1, col=1)
        fig.add_trace(go.Scatter(x=list(f), y=np.abs(row), mode='lines', name=f'Absolute value {i+1}', line=dict(color=color, width=line_width), showlegend=False), row=1, col=2)
        fig.add_trace(go.Scatter(x=list(f), y=np.imag(row), mode='lines', name=f'Imaginary part {i+1}', line=dict(color=color, width=line_width), showlegend=False), row=2, col=1)
        fig.add_trace(go.Scatter(x=list(f), y=np.angle(row, deg=True), mode='lines', name=f'Phase {i+1}', line=dict(color=color, width=line_width), showlegend=False), row=2, col=2)

    # Set the x-axis limits and titles
    fig.update_xaxes(range=[f_min, f_max], row=1, col=1)
    fig.update_xaxes(range=[f_min, f_max], row=1, col=2)
    fig.update_xaxes(range=[f_min, f_max], title_text='<b>Frequency [MHz]</b>', row=2, col=1)
    fig.update_xaxes(range=[f_min, f_max], title_text='<b>Frequency [MHz]</b>', row=2, col=2)

    # Set the y-axis titles
    fig.update_yaxes(title_text='<b>Re{z_in_front} [MRayl]</b>', row=1, col=1)
    fig.update_yaxes(title_text='<b>|z_in_front| [MRayl]</b>', row=1, col=2)
    fig.update_yaxes(title_text='<b>Im{z_in_front} [MRayl]</b>', row=2, col=1)
    fig.update_yaxes(title_text='<b>Phase [deg]</b>', row=2, col=2)

    # Plot z_in_piezo
    z_in_piezo = z_in_piezo / 1e6

    line_color = 'blue'  # Using a single color for all z_in_piezo lines

    for i, row in enumerate(z_in_piezo):
        fig.add_trace(go.Scatter(x=list(f), y=np.real(row), mode='lines', name=f'Piezo layer {i+1}', line=dict(color=line_color, width=line_width), showlegend=True), row=1, col=1)
        fig.add_trace(go.Scatter(x=list(f), y=np.abs(row), mode='lines', name=f'Absolute value (piezo) {i+1}', line=dict(color=line_color, width=line_width), showlegend=False), row=1, col=2)
        fig.add_trace(go.Scatter(x=list(f), y=np.imag(row), mode='lines', name=f'Imaginary part (piezo) {i+1}', line=dict(color=line_color, width=line_width), showlegend=False), row=2, col=1)
        fig.add_trace(go.Scatter(x=list(f), y=np.angle(row, deg=True), mode='lines', name=f'Phase (piezo) {i+1}', line=dict(color=line_color, width=line_width), showlegend=False), row=2, col=2)

    # Plot z_in_back
    z_in_back = z_in_back / 1e6

    for i, row in enumerate(z_in_back):
        color = get_color_from_scale(i, len(z_in_back), color_scale)
        
        fig.add_trace(go.Scatter(x=list(f), y=np.real(row), mode='lines', name=f'Back layer {i+1}', line=dict(color=color, width=line_width), showlegend=True), row=1, col=1)
        fig.add_trace(go.Scatter(x=list(f), y=np.abs(row), mode='lines', name=f'Absolute value {i+1}', line=dict(color=color, width=line_width), showlegend=False), row=1, col=2)
        fig.add_trace(go.Scatter(x=list(f), y=np.imag(row), mode='lines', name=f'Imaginary part {i+1}', line=dict(color=color, width=line_width), showlegend=False), row=2, col=1)
        fig.add_trace(go.Scatter(x=list(f), y=np.angle(row, deg=True), mode='lines', name=f'Phase {i+1}', line=dict(color=color, width=line_width), showlegend=False), row=2, col=2)

    # Configure figure layout
    fig.update_layout(title='<b>Impedance seen towards the load</b>', title_x=0.5)
    fig.update_layout(font=dict(size=12))#increase the font size of the y-axis titles
    fig.update_layout(height=1200, width=1700)#increase the figure size

    return fig

def plot_mech_imp_rev(z_in_front_reverse, z_in_piezo_reverse, z_in_back_reverse, f, f_min, f_max):
    """
    Plot the mechanical impedance seen towards the load (backing -> piezo -> load)
    """
    fig = sp.make_subplots(rows=2, cols=2)

    f = f / 1e6  # convert to MHz
    f_min = f_min / 1e6
    f_max = f_max / 1e6

    line_width = 1

    # Function to get color from color scale
    color_scale = px.colors.sequential.Jet
    def get_color_from_scale(index, total_elements, color_scale):
        return color_scale[int((index / total_elements) * (len(color_scale) - 1))]

    # Plot z_in_front_reverse
    z_in_front_reverse = z_in_front_reverse / 1e6

    for i, row in enumerate(z_in_front_reverse):
        color = get_color_from_scale(i, len(z_in_front_reverse), color_scale)
        
        fig.add_trace(go.Scatter(x=list(f), y=np.real(row), mode='lines', name=f'Front layer {i+1}', line=dict(color=color, width=line_width), showlegend=True), row=1, col=1)
        fig.add_trace(go.Scatter(x=list(f), y=np.abs(row), mode='lines', name=f'Absolute value {i+1}', line=dict(color=color, width=line_width), showlegend=False), row=1, col=2)
        fig.add_trace(go.Scatter(x=list(f), y=np.imag(row), mode='lines', name=f'Imaginary part {i+1}', line=dict(color=color, width=line_width), showlegend=False), row=2, col=1)
        fig.add_trace(go.Scatter(x=list(f), y=np.angle(row, deg=True), mode='lines', name=f'Phase {i+1}', line=dict(color=color, width=line_width), showlegend=False), row=2, col=2)

    # Plot z_in_piezo_reverse
    z_in_piezo_reverse = z_in_piezo_reverse / 1e6

    line_color = 'blue'  # Using a single color for all z_in_piezo_reverse lines

    for i, row in enumerate(z_in_piezo_reverse):
        fig.add_trace(go.Scatter(x=list(f), y=np.real(row), mode='lines', name=f'Piezo layer {i+1}', line=dict(color=line_color, width=line_width), showlegend=True), row=1, col=1)
        fig.add_trace(go.Scatter(x=list(f), y=np.abs(row), mode='lines', name=f'Absolute value (piezo) {i+1}', line=dict(color=line_color, width=line_width), showlegend=False), row=1, col=2)
        fig.add_trace(go.Scatter(x=list(f), y=np.imag(row), mode='lines', name=f'Imaginary part (piezo) {i+1}', line=dict(color=line_color, width=line_width), showlegend=False), row=2, col=1)
        fig.add_trace(go.Scatter(x=list(f), y=np.angle(row, deg=True), mode='lines', name=f'Phase (piezo) {i+1}', line=dict(color=line_color, width=line_width), showlegend=False), row=2, col=2)

    # Plot z_in_back_reverse
    z_in_back_reverse = z_in_back_reverse / 1e6

    for i, row in enumerate(z_in_back_reverse):
        color = get_color_from_scale(i, len(z_in_back_reverse), color_scale)
        
        fig.add_trace(go.Scatter(x=list(f), y=np.real(row), mode='lines', name=f'Back layer {i+1}', line=dict(color=color, width=line_width), showlegend=True), row=1, col=1)
        fig.add_trace(go.Scatter(x=list(f), y=np.abs(row), mode='lines', name=f'Absolute value {i+1}', line=dict(color=color, width=line_width), showlegend=False), row=1, col=2)
        fig.add_trace(go.Scatter(x=list(f), y=np.imag(row), mode='lines', name=f'Imaginary part {i+1}', line=dict(color=color, width=line_width), showlegend=False), row=2, col=1)
        fig.add_trace(go.Scatter(x=list(f), y=np.angle(row, deg=True), mode='lines', name=f'Phase {i+1}', line=dict(color=color, width=line_width), showlegend=False), row=2, col=2)

    # Configure figure layout
    fig.update_layout(title='<b>Impedance seen towards the load</b>', title_x=0.5)
    fig.update_layout(font=dict(size=12))#increase the font size of the y-axis titles
    fig.update_layout(height=1200, width=1700)#increase the figure size
    
    return fig
    
def plot_mech_imp(z_load_to_backing, z_backing_to_load, parameter_dict):
    
    # ==================================
    # Extracting variables
    # ==================================
    (f, f_min, f_max, f_c, w, column_labels, z_elport_termination, len_load, len_front_layers,
        len_piezo, len_back_layers, len_backing, len_layers, len_f, c_load, z_c_load,
        d_load, q_load, c_front_layers, z_c_front_layers, d_front_layers, q_front_layers,
        c_piezo, z_c_piezo, d_piezo, h, eps_r, q_piezo, c_back_layers, z_c_back_layers,
        d_back_layers, q_back_layers, c_backing, z_c_backing, d_backing, q_backing
        ) = param_dict_extract(parameter_dict)
    
    
    # #stack the arrays
    # # [-1] = Layer interfacing load, [0] = Layer interfacing backing, [len_back_layers] = Piezo layer
    # if z_in_back.size != 0:
    #     z_load_to_backing = np.vstack([z_in_back, z_in_piezo, z_in_front])
    # else:
    #     z_load_to_backing = np.vstack([z_in_piezo, z_in_front])
    # # Stack the arrays in reverse order
    # # [-1] = Layer interfacing backing, [0] = Layer interfacing load, [len_back_layers] = Piezo layer
    # z_backing_to_load = np.vstack([z_in_front_reverse, z_in_piezo_reverse, z_in_back_reverse])

    
    # # [-1] = Layer interfacing load, [0] = Layer interfacing backing, [len_back_layers] = Piezo layer
    # z_in_front = z_load_to_backing[-1:len_front_layers] #picking out front layers
    # z_in_piezo = z_load_to_backing[len_back_layers] #picking out piezo layer
    # z_in_back = z_load_to_backing[len_back_layers+1:] #picking out backing layers
    
    # # [-1] = Layer interfacing backing, [0] = Layer interfacing load, [len_back_layers] = Piezo layer
    # z_in_front_reverse = z_backing_to_load[len_back_layers+1:]
    # z_in_piezo_reverse = z_backing_to_load[-len_back_layers]
    # z_in_back_reverse = z_backing_to_load[-1:len_back_layers]
    
    # Assuming the structure of z_load_to_backing array is:
    # [-1] = Layer interfacing load, [0] = Layer interfacing backing, [len_back_layers] = Piezo layer

    # Extract the front layers. From the layer interfacing load to just before the piezo layer
    z_in_front = z_load_to_backing[-1:-(len_front_layers+1):-1]
    # Extract the piezo layer
    z_in_piezo = z_load_to_backing[len_back_layers:len_back_layers+1]
    # Extract the back layers
    z_in_back = z_load_to_backing[:len_back_layers] #From the start of the array up to the piezo layer

    # Assuming the structure of z_backing_to_load array is:
    # [-1] = Layer interfacing backing, [0] = Layer interfacing load, [len_back_layers] = Piezo layer

    # Corrected indexing for reverse
    # Extract the front layers in reverse order
    z_in_front_reverse = z_backing_to_load[:len_front_layers]  # From the start up to the length of front layers
    # Extract the piezo layer in reverse order
    z_in_piezo_reverse = z_backing_to_load[len_front_layers:len_back_layers]  # The piezo layer is after the front layers
    # Extract the back layers in reverse order
    z_in_back_reverse = z_backing_to_load[len_front_layers+1:]  # From after the piezo layer to the end
    
    z_fwd_fig = plot_mech_imp_fwd(z_in_front, z_in_piezo, z_in_back, f, f_min, f_max)
    z_bwd_fig = plot_mech_imp_rev(z_in_front_reverse, z_in_piezo_reverse, z_in_back_reverse, f, f_min, f_max)
    
    return z_fwd_fig, z_bwd_fig
    