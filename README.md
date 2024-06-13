# Data processing of measurements done with the Vilas coagulation analyzer

The code iterates through all files in the specified data path (path). For each file with a .txt extension and a filename that doesn't contain certain keywords (e.g., 'PD', 'CC', 'TEST', 'FREC') -these are the valid measurement files- the code calls the procesar function and writes the output values to the CSV file.
The code parses data files containing pressure measurements over time, extracts various key values through signal processing for each measurement run, and writes the processed data to a CSV file and optionally updates a Google Sheet. Additionally, if enabled, it generates and displays several interactive plots using the Plotly library.
