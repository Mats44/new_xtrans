import tkinter as tk
import plotly.graph_objs as go
import webview

# Create a Plotly figure
fig = go.Figure(data=go.Bar(y=[2, 3, 1]))

# Convert the figure to HTML
plot_html = fig.to_html(full_html=False)

# Create a Tkinter window
root = tk.Tk()
root.title("Plotly in Tkinter")

# Function to open the plot in a webview
def open_plot():
    webview.create_window("Plotly Plot", html=plot_html)
    webview.start()

# Add a button to the Tkinter window to display the plot
button = tk.Button(root, text="Show Plot", command=open_plot)
button.pack()

# Start the Tkinter event loop
root.mainloop()
