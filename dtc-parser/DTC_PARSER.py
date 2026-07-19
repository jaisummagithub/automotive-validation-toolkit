import os
import re
import tkinter as tk
from tkinter import filedialog, ttk

# Function to parse the log files
def parse_dtc_logs(folder_path):
    dtc_info = []

    for filename in os.listdir(folder_path):
        if filename.startswith("DTC_") and filename.endswith(".txt"):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r') as file:
                content = file.read()

                # Match the ECU name and code
                ecu_matches = re.findall(r'Reading DTCs from\s+(.*)\n\s+Filter set OK for ECU:\s+(\w+)', content)

                for ecu_match in ecu_matches:
                    ecu_name = ecu_match[0].strip()
                    ecu_code = ecu_match[1].strip()

                    # Adjusted regex pattern to capture broader cases
                    #dtc_matches = re.findall(r'ECU Reports\s+(\d+)\s+DTCs\n+(.*?)\s+([A-Z0-9]{7})\s+[(]', content, re.DOTALL)
                    dtc_matches = re.findall(r'ECU Reports\s+(\d+)\s+DTCs\s+([A-Z][0-9]{6})\s+[(]', content, re.DOTALL)


                    for dtc_match in dtc_matches:
                        occurrence_count = int(dtc_match[0].strip())
                        dtc_code = dtc_match[2].strip()

                        # Append each parsed data instance
                        dtc_info.append((ecu_name, ecu_code, dtc_code, occurrence_count, filename, file_path))

    # Sort by file name and then by occurrences (descending order)
    dtc_info.sort(key=lambda x: (x[4], -x[3]))

    return dtc_info

# Function to browse folders
def browse_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        # Clear the treeview
        for i in tree.get_children():
            tree.delete(i)

        dtc_info = parse_dtc_logs(folder_path)

        # Insert data into the treeview
        for info in dtc_info:
            tree.insert("", tk.END, values=info)

# Set up the main application window
root = tk.Tk()
root.title("DTC Log Parser")
root.geometry("1500x500")

# Add a button to browse for the folder
browse_button = tk.Button(root, text="Browse Folder", command=browse_folder)
browse_button.pack(pady=10)

# Set up a frame for the Treeview and scrollbar
frame = tk.Frame(root)
frame.pack(fill=tk.BOTH, expand=True)    

# Add the Treeview widget
columns = ("ECU Name", "ECU Code", "DTC Code", "Occurrences", "File Name", "File Path")
tree = ttk.Treeview(frame, columns=columns, show="headings")

# Define headings with custom widths
tree.heading("ECU Name", text="ECU Name")
tree.column("ECU Name", width=200)  # Set custom width for ECU Name

tree.heading("ECU Code", text="ECU Code")
tree.column("ECU Code", width=50)  # Set custom width for ECU Code

tree.heading("DTC Code", text="DTC Code")
tree.column("DTC Code", width=50)  # Set custom width for DTC Code

tree.heading("Occurrences", text="Occurrences")
tree.column("Occurrences", width=50)  # Set custom width for Occurrences

tree.heading("File Name", text="File Name")
tree.column("File Name", width=250)  # Set custom width for File Name

tree.heading("File Path", text="File Path")
tree.column("File Path", width=470)  # Set custom width for File Path


# Add a vertical scrollbar
scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Pack the Treeview widget into the frame
tree.pack(fill=tk.BOTH, expand=True)

# Start the GUI event loop
root.mainloop()





# import os
# import re
# import tkinter as tk
# from tkinter import filedialog, ttk

# # Function to parse the log files
# def parse_dtc_logs(folder_path):
#     dtc_info = []

#     for filename in os.listdir(folder_path):
#         if filename.startswith("DTC_") and filename.endswith(".txt"):
#             file_path = os.path.join(folder_path, filename)
#             with open(file_path, 'r') as file:
#                 content = file.read()

#                 # Match the ECU name and code
#                 ecu_matches = re.findall(r'Reading DTCs from\s+(.*)\n\s+Filter set OK for ECU:\s+(\w+)', content)

#                 for ecu_match in ecu_matches:
#                     ecu_name = ecu_match[0].strip()
#                     ecu_code = ecu_match[1].strip()

#                     # Adjust regex pattern to accommodate tabs
#                     dtc_matches = re.findall(r'(\d+)\s+DTCs\n+(.*?)\s+([A-Z0-9]+)\s+DTC information record not found', content, re.DOTALL)
                    
#                     for dtc_match in dtc_matches:
#                         occurrence_count = int(dtc_match[0].strip())
#                         dtc_code = dtc_match[2].strip()

#                         # Append each parsed data instance
#                         dtc_info.append((ecu_name, ecu_code, dtc_code, occurrence_count, filename, file_path))

#     # Sort by file name and then by occurrences (descending order)
#     dtc_info.sort(key=lambda x: (x[4], -x[3]))

#     return dtc_info

# # Function to browse folders
# def browse_folder():
#     folder_path = filedialog.askdirectory()
#     if folder_path:
#         # Clear the treeview
#         for i in tree.get_children():
#             tree.delete(i)

#         dtc_info = parse_dtc_logs(folder_path)

#         # Insert data into the treeview
#         for info in dtc_info:
#             tree.insert("", tk.END, values=info)

# # Set up the main application window
# root = tk.Tk()
# root.title("DTC Log Parser")
# root.geometry("1500x500")

# # Add a button to browse for the folder
# browse_button = tk.Button(root, text="Browse Folder", command=browse_folder)
# browse_button.pack(pady=10)

# # Set up a frame for the Treeview and scrollbar
# frame = tk.Frame(root)
# frame.pack(fill=tk.BOTH, expand=True)    

# # Add the Treeview widget
# columns = ("ECU Name", "ECU Code", "DTC Code", "Occurrences", "File Name", "File Path")
# tree = ttk.Treeview(frame, columns=columns, show="headings")

# # Define headings with custom widths
# tree.heading("ECU Name", text="ECU Name")
# tree.column("ECU Name", width=200)  # Set custom width for ECU Name

# tree.heading("ECU Code", text="ECU Code")
# tree.column("ECU Code", width=50)  # Set custom width for ECU Code

# tree.heading("DTC Code", text="DTC Code")
# tree.column("DTC Code", width=50)  # Set custom width for DTC Code

# tree.heading("Occurrences", text="Occurrences")
# tree.column("Occurrences", width=50)  # Set custom width for Occurrences

# tree.heading("File Name", text="File Name")
# tree.column("File Name", width=250)  # Set custom width for File Name

# tree.heading("File Path", text="File Path")
# tree.column("File Path", width=470)  # Set custom width for File Path

# # Add a vertical scrollbar
# scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
# tree.configure(yscrollcommand=scrollbar.set)
# scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# # Pack the Treeview widget into the frame
# tree.pack(fill=tk.BOTH, expand=True)

# # Start the GUI event loop
# root.mainloop()




# # import os
# # import re
# # import tkinter as tk
# # from tkinter import filedialog, ttk

# # # Function to parse the log files
# # def parse_dtc_logs(folder_path):
# #     dtc_info = []

# #     for filename in os.listdir(folder_path):
# #         if filename.startswith("DTC_") and filename.endswith(".txt"):
# #             file_path = os.path.join(folder_path, filename)
# #             with open(file_path, 'r') as file:
# #                 content = file.read()

# #                 # Match the ECU name and code
# #                 ecu_matches = re.findall(r'Reading DTCs from\s+(.*)\n\s+Filter set OK for ECU:\s+(\w+)', content)

# #                 for ecu_match in ecu_matches:
# #                     ecu_name = ecu_match[0].strip()
# #                     ecu_code = ecu_match[1].strip()

# #                     # Adjust regex pattern to accommodate tabs
# #                     dtc_matches = re.findall(r'(\d+)\s+DTCs\n+(.*?)\s+([A-Z0-9]+)\s+DTC information record not found', content, re.DOTALL)
                    
# #                     for dtc_match in dtc_matches:
# #                         occurrence_count = int(dtc_match[0].strip())
# #                         dtc_code = dtc_match[2].strip()

# #                         # Append each parsed data instance
# #                         dtc_info.append((ecu_name, ecu_code, dtc_code, occurrence_count, filename, file_path))

# #     # Sort by file name and then by occurrences (descending order)
# #     dtc_info.sort(key=lambda x: (x[4], -x[3]))

# #     return dtc_info

# # # Function to browse folders
# # def browse_folder():
# #     folder_path = filedialog.askdirectory()
# #     if folder_path:
# #         # Clear the treeview
# #         for i in tree.get_children():
# #             tree.delete(i)

# #         dtc_info = parse_dtc_logs(folder_path)

# #         # Insert data into the treeview
# #         for info in dtc_info:
# #             tree.insert("", tk.END, values=info)

# #         # Auto-fit column widths
# #         auto_fit_columns(tree, dtc_info)

# # # Function to auto-fit column widths
# # def auto_fit_columns(treeview, data):
# #     for col in treeview["columns"]:
# #         max_width = max(len(str(row[col_idx])) for row_idx, row in enumerate(data) for col_idx, column in enumerate(treeview["columns"]) if column == col)
# #         max_width = max(max_width, len(col))  # Include header in width calculation
# #         treeview.column(col, width=(max_width + 2) * 10)  # Add padding for better spacing

# # # Set up the main application window
# # root = tk.Tk()
# # root.title("DTC Log Parser")
# # root.geometry("1500x500")

# # # Add a button to browse for the folder
# # browse_button = tk.Button(root, text="Browse Folder", command=browse_folder)
# # browse_button.pack(pady=10)

# # # Set up a frame for the Treeview and scrollbar
# # frame = tk.Frame(root)
# # frame.pack(fill=tk.BOTH, expand=True)    

# # # Add the Treeview widget
# # columns = ("ECU Name", "ECU Code", "DTC Code", "Occurrences", "File Name", "File Path")
# # tree = ttk.Treeview(frame, columns=columns, show="headings")

# # # Define headings
# # for col in columns:
# #     tree.heading(col, text=col)
# #     tree.column(col, minwidth=0, width=150)

# # # Add a vertical scrollbar
# # scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
# # tree.configure(yscrollcommand=scrollbar.set)
# # scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# # # Pack the Treeview widget into the frame
# # tree.pack(fill=tk.BOTH, expand=True)

# # # Start the GUI event loop
# # root.mainloop()








# # # import os
# # # import re
# # # import tkinter as tk
# # # from tkinter import filedialog, ttk

# # # # Function to parse the log files
# # # def parse_dtc_logs(folder_path):
# # #     dtc_info = []

# # #     for filename in os.listdir(folder_path):
# # #         if filename.startswith("DTC_") and filename.endswith(".txt"):
# # #             file_path = os.path.join(folder_path, filename)
# # #             with open(file_path, 'r') as file:
# # #                 content = file.read()

# # #                 # Match the ECU name and code
# # #                 ecu_matches = re.findall(r'Reading DTCs from\s+(.*)\n\s+Filter set OK for ECU:\s+(\w+)', content)

# # #                 for ecu_match in ecu_matches:
# # #                     ecu_name = ecu_match[0].strip()
# # #                     ecu_code = ecu_match[1].strip()

# # #                     # Adjust regex pattern to accommodate tabs
# # #                     dtc_matches = re.findall(r'(\d+)\s+DTCs\n+(.*?)\s+([A-Z0-9]+)\s+DTC information record not found', content, re.DOTALL)
                    
# # #                     for dtc_match in dtc_matches:
# # #                         occurrence_count = int(dtc_match[0].strip())
# # #                         dtc_code = dtc_match[2].strip()

# # #                         # Append each parsed data instance
# # #                         dtc_info.append((file_path, filename, ecu_name, ecu_code, dtc_code, occurrence_count))

# # #     # Sort by file name and then by occurrences (descending order)
# # #     dtc_info.sort(key=lambda x: (x[1], -x[5]))

# # #     return dtc_info

# # # # Function to browse folders
# # # def browse_folder():
# # #     folder_path = filedialog.askdirectory()
# # #     if folder_path:
# # #         # Clear the treeview
# # #         for i in tree.get_children():
# # #             tree.delete(i)

# # #         dtc_info = parse_dtc_logs(folder_path)

# # #         # Insert data into the treeview
# # #         for info in dtc_info:
# # #             tree.insert("", tk.END, values=info)

# # #         # Auto-fit column widths
# # #         auto_fit_columns(tree, dtc_info)

# # # # Function to auto-fit column widths
# # # def auto_fit_columns(treeview, data):
# # #     for col in treeview["columns"]:
# # #         max_width = max(len(str(row[col_idx])) for row_idx, row in enumerate(data) for col_idx, column in enumerate(treeview["columns"]) if column == col)
# # #         max_width = max(max_width, len(col))  # Include header in width calculation
# # #         treeview.column(col, width=(max_width + 2) * 10)  # Add padding for better spacing

# # # # Set up the main application window
# # # root = tk.Tk()
# # # root.title("DTC Log Parser")
# # # root.geometry("1500x500")

# # # # Add a button to browse for the folder
# # # browse_button = tk.Button(root, text="Browse Folder", command=browse_folder)
# # # browse_button.pack(pady=10)

# # # # Set up a frame for the Treeview and scrollbar
# # # frame = tk.Frame(root)
# # # frame.pack(fill=tk.BOTH, expand=True)    
# # # # Add the Treeview widget
# # # columns = ("File Path", "File Name", "ECU Name", "ECU Code", "DTC Code", "Occurrences")
# # # tree = ttk.Treeview(frame, columns=columns, show="headings")

# # # # Define headings
# # # for col in columns:
# # #     tree.heading(col, text=col)
# # #     tree.column(col, minwidth=0, width=150)

# # # # Add a vertical scrollbar
# # # scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
# # # tree.configure(yscrollcommand=scrollbar.set)
# # # scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# # # # Pack the Treeview widget into the frame
# # # tree.pack(fill=tk.BOTH, expand=True)

# # # # Start the GUI event loop
# # # root.mainloop()



# # # # import os
# # # # import re
# # # # import tkinter as tk
# # # # from tkinter import filedialog, ttk

# # # # # Function to parse the log files
# # # # def parse_dtc_logs(folder_path):
# # # #     dtc_info = []

# # # #     for filename in os.listdir(folder_path):
# # # #         if filename.startswith("DTC_") and filename.endswith(".txt"):
# # # #             file_path = os.path.join(folder_path, filename)
# # # #             with open(file_path, 'r') as file:
# # # #                 content = file.read()

# # # #                 # Match the ECU name and code
# # # #                 ecu_matches = re.findall(r'Reading DTCs from\s+(.*)\n\s+Filter set OK for ECU:\s+(\w+)', content)

# # # #                 for ecu_match in ecu_matches:
# # # #                     ecu_name = ecu_match[0].strip()
# # # #                     ecu_code = ecu_match[1].strip()

# # # #                     # Match the DTC codes and occurrence counts
# # # #                     dtc_matches = re.findall(r'ECU Reports\s+(\d+)\s+DTCs\s+(.*?)([A-Z0-9]+)\s+DTC information record not found', content, re.DOTALL)
                    
# # # #                     for dtc_match in dtc_matches:
# # # #                         occurrence_count = int(dtc_match[0].strip())
# # # #                         dtc_code = dtc_match[2].strip()

# # # #                         # Append each parsed data instance
# # # #                         dtc_info.append((file_path, filename, ecu_name, ecu_code, dtc_code, occurrence_count))

# # # #     # Sort by file name and then by occurrences (descending order)
# # # #     dtc_info.sort(key=lambda x: (x[1], -x[5]))

# # # #     return dtc_info

# # # # # Function to browse folders
# # # # def browse_folder():
# # # #     folder_path = filedialog.askdirectory()
# # # #     if folder_path:
# # # #         # Clear the treeview
# # # #         for i in tree.get_children():
# # # #             tree.delete(i)

# # # #         dtc_info = parse_dtc_logs(folder_path)

# # # #         # Insert data into the treeview
# # # #         for info in dtc_info:
# # # #             tree.insert("", tk.END, values=info)

# # # #         # Auto-fit column widths
# # # #         auto_fit_columns(tree, dtc_info)

# # # # # Function to auto-fit column widths
# # # # def auto_fit_columns(treeview, data):
# # # #     for col in treeview["columns"]:
# # # #         max_width = max(len(str(row[col_idx])) for row_idx, row in enumerate(data) for col_idx, column in enumerate(treeview["columns"]) if column == col)
# # # #         max_width = max(max_width, len(col))  # Include header in width calculation
# # # #         treeview.column(col, width=(max_width + 2) * 10)  # Add padding for better spacing

# # # # # Set up the main application window
# # # # root = tk.Tk()
# # # # root.title("DTC Log Parser")
# # # # root.geometry("1000x500")

# # # # # Add a button to browse for the folder
# # # # browse_button = tk.Button(root, text="Browse Folder", command=browse_folder)
# # # # browse_button.pack(pady=10)

# # # # # Set up a frame for the Treeview and scrollbar
# # # # frame = tk.Frame(root)
# # # # frame.pack(fill=tk.BOTH, expand=True)

# # # # # Add the Treeview widget
# # # # columns = ("File Path", "File Name", "ECU Name", "ECU Code", "DTC Code", "Occurrences")
# # # # tree = ttk.Treeview(frame, columns=columns, show="headings")

# # # # # Define headings
# # # # for col in columns:
# # # #     tree.heading(col, text=col)
# # # #     tree.column(col, minwidth=0, width=150)

# # # # # Add a vertical scrollbar
# # # # scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
# # # # tree.configure(yscrollcommand=scrollbar.set)
# # # # scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# # # # # Pack the Treeview widget into the frame
# # # # tree.pack(fill=tk.BOTH, expand=True)

# # # # # Start the GUI event loop
# # # # root.mainloop()




# # # # # import os
# # # # # import re
# # # # # import tkinter as tk
# # # # # from tkinter import filedialog, ttk

# # # # # # Function to parse the log files
# # # # # def parse_dtc_logs(folder_path):
# # # # #     dtc_info = []

# # # # #     for filename in os.listdir(folder_path):
# # # # #         if filename.startswith("DTC_") and filename.endswith(".txt"):
# # # # #             file_path = os.path.join(folder_path, filename)
# # # # #             with open(file_path, 'r') as file:
# # # # #                 content = file.read()

# # # # #                 # Match the ECU name and code
# # # # #                 ecu_matches = re.findall(r'Reading DTCs from\s+(.*)\n\s+Filter set OK for ECU:\s+(\w+)', content)

# # # # #                 for ecu_match in ecu_matches:
# # # # #                     ecu_name = ecu_match[0].strip()
# # # # #                     ecu_code = ecu_match[1].strip()

# # # # #                     # Match the DTC codes and occurrence counts
# # # # #                     dtc_matches = re.findall(r'ECU Reports\s+(\d+)\s+DTCs\s+(.*?)([A-Z0-9]+)\s+DTC information record not found', content, re.DOTALL)
                    
# # # # #                     for dtc_match in dtc_matches:
# # # # #                         occurrence_count = int(dtc_match[0].strip())
# # # # #                         dtc_code = dtc_match[2].strip()

# # # # #                         # Append each parsed data instance
# # # # #                         dtc_info.append((file_path, filename, ecu_name, ecu_code, dtc_code, occurrence_count))

# # # # #     # Sort by file name and then by occurrences within each file
# # # # #     dtc_info.sort(key=lambda x: (x[1], x[5]))

# # # # #     return dtc_info

# # # # # # Function to browse folders
# # # # # def browse_folder():
# # # # #     folder_path = filedialog.askdirectory()
# # # # #     if folder_path:
# # # # #         # Clear the treeview
# # # # #         for i in tree.get_children():
# # # # #             tree.delete(i)

# # # # #         dtc_info = parse_dtc_logs(folder_path)

# # # # #         # Insert data into the treeview
# # # # #         for info in dtc_info:
# # # # #             tree.insert("", tk.END, values=info)

# # # # #         # Auto-fit column widths
# # # # #         auto_fit_columns(tree, dtc_info)

# # # # # # Function to auto-fit column widths
# # # # # def auto_fit_columns(treeview, data):
# # # # #     for col in treeview["columns"]:
# # # # #         max_width = max(len(str(row[col_idx])) for row_idx, row in enumerate(data) for col_idx, column in enumerate(treeview["columns"]) if column == col)
# # # # #         max_width = max(max_width, len(col))  # Include header in width calculation
# # # # #         treeview.column(col, width=(max_width + 2) * 10)  # Add padding for better spacing

# # # # # # Set up the main application window
# # # # # root = tk.Tk()
# # # # # root.title("DTC Log Parser")
# # # # # root.geometry("1000x500")

# # # # # # Add a button to browse for the folder
# # # # # browse_button = tk.Button(root, text="Browse Folder", command=browse_folder)
# # # # # browse_button.pack(pady=10)

# # # # # # Set up a frame for the Treeview and scrollbar
# # # # # frame = tk.Frame(root)
# # # # # frame.pack(fill=tk.BOTH, expand=True)

# # # # # # Add the Treeview widget
# # # # # columns = ("File Path", "File Name", "ECU Name", "ECU Code", "DTC Code", "Occurrences")
# # # # # tree = ttk.Treeview(frame, columns=columns, show="headings")

# # # # # # Define headings
# # # # # for col in columns:
# # # # #     tree.heading(col, text=col)
# # # # #     tree.column(col, minwidth=0, width=150)

# # # # # # Add a vertical scrollbar
# # # # # scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
# # # # # tree.configure(yscrollcommand=scrollbar.set)
# # # # # scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# # # # # # Pack the Treeview widget into the frame
# # # # # tree.pack(fill=tk.BOTH, expand=True)

# # # # # # Start the GUI event loop
# # # # # root.mainloop()




# # # # # # import os
# # # # # # import re
# # # # # # import tkinter as tk
# # # # # # from tkinter import filedialog, ttk

# # # # # # # Function to parse the log files
# # # # # # def parse_dtc_logs(folder_path):
# # # # # #     dtc_info = []

# # # # # #     for filename in os.listdir(folder_path):
# # # # # #         if filename.startswith("DTC_") and filename.endswith(".txt"):
# # # # # #             file_path = os.path.join(folder_path, filename)
# # # # # #             with open(file_path, 'r') as file:
# # # # # #                 content = file.read()

# # # # # #                 # Match the ECU name and code
# # # # # #                 ecu_matches = re.findall(r'Reading DTCs from\s+(.*)\n\s+Filter set OK for ECU:\s+(\w+)', content)

# # # # # #                 for ecu_match in ecu_matches:
# # # # # #                     ecu_name = ecu_match[0].strip()
# # # # # #                     ecu_code = ecu_match[1].strip()

# # # # # #                     # Match the DTC codes and occurrence counts
# # # # # #                     dtc_matches = re.findall(r'ECU Reports\s+(\d+)\s+DTCs\s+(.*?)([A-Z0-9]+)\s+DTC information record not found', content, re.DOTALL)
                    
# # # # # #                     for dtc_match in dtc_matches:
# # # # # #                         occurrence_count = dtc_match[0].strip()
# # # # # #                         dtc_code = dtc_match[2].strip()

# # # # # #                         # Append each parsed data instance
# # # # # #                         dtc_info.append((file_path, filename, ecu_name, ecu_code, dtc_code, occurrence_count))

# # # # # #     return dtc_info

# # # # # # # Function to browse folders
# # # # # # def browse_folder():
# # # # # #     folder_path = filedialog.askdirectory()
# # # # # #     if folder_path:
# # # # # #         # Clear the treeview
# # # # # #         for i in tree.get_children():
# # # # # #             tree.delete(i)

# # # # # #         dtc_info = parse_dtc_logs(folder_path)

# # # # # #         # Insert data into the treeview
# # # # # #         for info in dtc_info:
# # # # # #             tree.insert("", tk.END, values=info)

# # # # # #         # Auto-fit column widths
# # # # # #         auto_fit_columns(tree, dtc_info)

# # # # # # # Function to auto-fit column widths
# # # # # # def auto_fit_columns(treeview, data):
# # # # # #     for col in treeview["columns"]:
# # # # # #         max_width = max(len(str(row[col_idx])) for row_idx, row in enumerate(data) for col_idx, column in enumerate(treeview["columns"]) if column == col)
# # # # # #         max_width = max(max_width, len(col))  # Include header in width calculation
# # # # # #         treeview.column(col, width=(max_width + 2) * 10)  # Add padding for better spacing

# # # # # # # Set up the main application window
# # # # # # root = tk.Tk()
# # # # # # root.title("DTC Log Parser")
# # # # # # root.geometry("1000x500")

# # # # # # # Add a button to browse for the folder
# # # # # # browse_button = tk.Button(root, text="Browse Folder", command=browse_folder)
# # # # # # browse_button.pack(pady=10)

# # # # # # # Set up the Treeview widget
# # # # # # columns = ("File Path", "File Name", "ECU Name", "ECU Code", "DTC Code", "Occurrences")
# # # # # # tree = ttk.Treeview(root, columns=columns, show="headings")

# # # # # # # Define headings
# # # # # # for col in columns:
# # # # # #     tree.heading(col, text=col)
# # # # # #     tree.column(col, minwidth=0, width=150)

# # # # # # # Add the Treeview to the window
# # # # # # tree.pack(fill=tk.BOTH, expand=True)

# # # # # # # Start the GUI event loop
# # # # # # root.mainloop()




# # # # # # # import os
# # # # # # # import re
# # # # # # # import tkinter as tk
# # # # # # # from tkinter import filedialog, ttk

# # # # # # # # Function to parse the log files
# # # # # # # def parse_dtc_logs(folder_path):
# # # # # # #     dtc_info = []

# # # # # # #     for filename in os.listdir(folder_path):
# # # # # # #         if filename.startswith("DTC_") and filename.endswith(".txt"):
# # # # # # #             file_path = os.path.join(folder_path, filename)
# # # # # # #             with open(file_path, 'r') as file:
# # # # # # #                 content = file.read()

# # # # # # #                 # Match the ECU name and code
# # # # # # #                 ecu_match = re.search(r'Reading DTCs from\s+(.*)\n\s+Filter set OK for ECU:\s+(\w+)', content)
# # # # # # #                 if ecu_match:
# # # # # # #                     ecu_name = ecu_match.group(1).strip()
# # # # # # #                     ecu_code = ecu_match.group(2).strip()

# # # # # # #                     # Match the DTC code and occurrence count
# # # # # # #                     dtc_match = re.search(r'ECU Reports\s+(\d+)\s+DTCs\s+(.*?)([A-Z0-9]+)\s+DTC information record not found', content, re.DOTALL)
# # # # # # #                     if dtc_match:
# # # # # # #                         occurrence_count = dtc_match.group(1).strip()
# # # # # # #                         dtc_code = dtc_match.group(3).strip()

# # # # # # #                         # Append the parsed data
# # # # # # #                         dtc_info.append((file_path, filename, ecu_name, ecu_code, dtc_code, occurrence_count))

# # # # # # #     return dtc_info

# # # # # # # # Function to browse folders
# # # # # # # def browse_folder():
# # # # # # #     folder_path = filedialog.askdirectory()
# # # # # # #     if folder_path:
# # # # # # #         # Clear the treeview
# # # # # # #         for i in tree.get_children():
# # # # # # #             tree.delete(i)

# # # # # # #         dtc_info = parse_dtc_logs(folder_path)

# # # # # # #         # Insert data into the treeview
# # # # # # #         for info in dtc_info:
# # # # # # #             tree.insert("", tk.END, values=info)

# # # # # # #         # Auto-fit column widths
# # # # # # #         auto_fit_columns(tree, dtc_info)

# # # # # # # # Function to auto-fit column widths
# # # # # # # def auto_fit_columns(treeview, data):
# # # # # # #     for col in treeview["columns"]:
# # # # # # #         max_width = max(len(str(row[col_idx])) for row_idx, row in enumerate(data) for col_idx, column in enumerate(treeview["columns"]) if column == col)
# # # # # # #         max_width = max(max_width, len(col))  # Include header in width calculation
# # # # # # #         treeview.column(col, width=(max_width + 2) * 10)  # Add padding for better spacing

# # # # # # # # Set up the main application window
# # # # # # # root = tk.Tk()
# # # # # # # root.title("DTC Log Parser")
# # # # # # # root.geometry("1000x500")

# # # # # # # # Add a button to browse for the folder
# # # # # # # browse_button = tk.Button(root, text="Browse Folder", command=browse_folder)
# # # # # # # browse_button.pack(pady=10)

# # # # # # # # Set up the Treeview widget
# # # # # # # columns = ("File Path", "File Name", "ECU Name", "ECU Code", "DTC Code", "Occurrences")
# # # # # # # tree = ttk.Treeview(root, columns=columns, show="headings")

# # # # # # # # Define headings
# # # # # # # for col in columns:
# # # # # # #     tree.heading(col, text=col)
# # # # # # #     tree.column(col, minwidth=0, width=150)

# # # # # # # # Add the Treeview to the window
# # # # # # # tree.pack(fill=tk.BOTH, expand=True)

# # # # # # # # Start the GUI event loop
# # # # # # # root.mainloop()













# # # # # # # # import os
# # # # # # # # import re
# # # # # # # # import tkinter as tk
# # # # # # # # from tkinter import filedialog, ttk

# # # # # # # # # Function to parse the log files
# # # # # # # # def parse_dtc_logs(folder_path):
# # # # # # # #     dtc_info = []

# # # # # # # #     for filename in os.listdir(folder_path):
# # # # # # # #         if filename.startswith("DTC_") and filename.endswith(".txt"):
# # # # # # # #             file_path = os.path.join(folder_path, filename)
# # # # # # # #             with open(file_path, 'r') as file:
# # # # # # # #                 content = file.read()

# # # # # # # #                 # Match the ECU name and code
# # # # # # # #                 ecu_match = re.search(r'Reading DTCs from\s+(.*)\n\s+Filter set OK for ECU:\s+(\w+)', content)
# # # # # # # #                 if ecu_match:
# # # # # # # #                     ecu_name = ecu_match.group(1).strip()
# # # # # # # #                     ecu_code = ecu_match.group(2).strip()

# # # # # # # #                     # Match the DTC code and occurrence count
# # # # # # # #                     dtc_match = re.search(r'ECU Reports\s+(\d+)\s+DTCs\s+(.*?)([A-Z0-9]+)\s+DTC information record not found', content, re.DOTALL)
# # # # # # # #                     if dtc_match:
# # # # # # # #                         occurrence_count = dtc_match.group(1).strip()
# # # # # # # #                         dtc_code = dtc_match.group(3).strip()

# # # # # # # #                         # Append the parsed data
# # # # # # # #                         dtc_info.append((file_path, filename, ecu_name, ecu_code, dtc_code, occurrence_count))

# # # # # # # #     return dtc_info

# # # # # # # # # Function to browse folders
# # # # # # # # def browse_folder():
# # # # # # # #     folder_path = filedialog.askdirectory()
# # # # # # # #     if folder_path:
# # # # # # # #         # Clear the treeview
# # # # # # # #         for i in tree.get_children():
# # # # # # # #             tree.delete(i)

# # # # # # # #         dtc_info = parse_dtc_logs(folder_path)

# # # # # # # #         # Insert data into the treeview
# # # # # # # #         for info in dtc_info:
# # # # # # # #             tree.insert("", tk.END, values=info)

# # # # # # # # # Set up the main application window
# # # # # # # # root = tk.Tk()
# # # # # # # # root.title("DTC Log Parser")
# # # # # # # # root.geometry("1000x500")

# # # # # # # # # Add a button to browse for the folder
# # # # # # # # browse_button = tk.Button(root, text="Browse Folder", command=browse_folder)
# # # # # # # # browse_button.pack(pady=10)

# # # # # # # # # Set up the Treeview widget
# # # # # # # # columns = ("File Path", "File Name", "ECU Name", "ECU Code", "DTC Code", "Occurrences")
# # # # # # # # tree = ttk.Treeview(root, columns=columns, show="headings")

# # # # # # # # # Define headings
# # # # # # # # for col in columns:
# # # # # # # #     tree.heading(col, text=col)
# # # # # # # #     tree.column(col, minwidth=0, width=150)

# # # # # # # # # Add the Treeview to the window
# # # # # # # # tree.pack(fill=tk.BOTH, expand=True)

# # # # # # # # # Start the GUI event loop
# # # # # # # # root.mainloop()


















































# # # # # # # # # import os
# # # # # # # # # import re
# # # # # # # # # import tkinter as tk
# # # # # # # # # from tkinter import filedialog, scrolledtext

# # # # # # # # # # Function to parse the log files
# # # # # # # # # def parse_dtc_logs(folder_path):
# # # # # # # # #     dtc_info = []

# # # # # # # # #     for filename in os.listdir(folder_path):
# # # # # # # # #         if filename.startswith("DTC_") and filename.endswith(".txt"):
# # # # # # # # #             with open(os.path.join(folder_path, filename), 'r') as file:
# # # # # # # # #                 content = file.read()

# # # # # # # # #                 # Match the ECU name and code
# # # # # # # # #                 ecu_match = re.search(r'Reading DTCs from\s+(.*)\n\s+Filter set OK for ECU:\s+(\w+)', content)
# # # # # # # # #                 if ecu_match:
# # # # # # # # #                     ecu_name = ecu_match.group(1).strip()
# # # # # # # # #                     ecu_code = ecu_match.group(2).strip()

# # # # # # # # #                     # Match the DTC code and occurrence count
# # # # # # # # #                     dtc_match = re.search(r'ECU Reports\s+(\d+)\s+DTCs\s+(.*?)([A-Z0-9]+)\s+DTC information record not found', content, re.DOTALL)
# # # # # # # # #                     if dtc_match:
# # # # # # # # #                         occurrence_count = dtc_match.group(1).strip()
# # # # # # # # #                         dtc_code = dtc_match.group(3).strip()

# # # # # # # # #                         # Append the parsed data
# # # # # # # # #                         dtc_info.append(f"ECU Name: {ecu_name}, ECU Code: {ecu_code}, DTC Code: {dtc_code}, Occurrences: {occurrence_count}")

# # # # # # # # #     return dtc_info

# # # # # # # # # # Function to browse folders
# # # # # # # # # def browse_folder():
# # # # # # # # #     folder_path = filedialog.askdirectory()
# # # # # # # # #     if folder_path:
# # # # # # # # #         result.delete(1.0, tk.END)  # Clear the text box
# # # # # # # # #         dtc_info = parse_dtc_logs(folder_path)
# # # # # # # # #         for info in dtc_info:
# # # # # # # # #             result.insert(tk.END, info + "\n")

# # # # # # # # # # Set up the main application window
# # # # # # # # # root = tk.Tk()
# # # # # # # # # root.title("DTC Log Parser")
# # # # # # # # # root.geometry("800x500")

# # # # # # # # # # Add a button to browse for the folder
# # # # # # # # # browse_button = tk.Button(root, text="Browse Folder", command=browse_folder)
# # # # # # # # # browse_button.pack(pady=10)

# # # # # # # # # # Add a scrolled text box to display the results
# # # # # # # # # result = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=100, height=20)
# # # # # # # # # result.pack(pady=10)

# # # # # # # # # # Start the GUI event loop
# # # # # # # # # root.mainloop()
