import numpy as np
import pandas as pd

def to_2d_array(arr):
    """
    Converts a 1-dimensional array or Pandas Series to a 2-dimensional array with the same number of rows.
    Handles cases where the input array may have 0 or 1 row.

    Parameters:
    arr (np.array or pd.Series): The 1-dimensional numpy array or Pandas Series to be converted.
 
    Returns:
    np.array: A 2-dimensional numpy array.
    """
    # Convert Pandas Series to NumPy array if necessary
    if isinstance(arr, pd.Series):
        arr = arr.to_numpy()

    # Check if the input array is already 2-dimensional
    if arr.ndim == 2:
        return arr

    # Check for an empty array
    if arr.size == 0:
        return np.array([[]])  # Return an empty 2D array
        #return 0

    # Reshape the array to have rows equal to the number of elements in the array
    return arr.reshape(-1, 1)


if __name__ == "__main__":  
    
    # Example usage
    arr1 = np.array([1, 2, 3])
    arr2 = np.array([4])
    arr3 = np.array([])

    print("Original array:", arr1)
    print("2D array:", to_2d_array(arr1))
    print("Original array:", arr2)
    print("2D array:", to_2d_array(arr2))
    print("Original array:", arr3)
    print("2D array:", to_2d_array(arr3))
