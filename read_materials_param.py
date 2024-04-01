# Imports
import pandas as pd

def read_materials_param(filename):

    # Define the path to the file
    file_path = 'parameters/' + filename
    
    # Read the Excel file into a DataFrame
    df = pd.read_excel(file_path, engine='openpyxl')
    
    return df