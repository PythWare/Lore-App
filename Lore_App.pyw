import os
import zlib
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

class LoreApp():
    """Class for handling the file reading and GUI logic"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Lore App")
        self.root.minsize(1000, 700)
        self.root.resizable(False, False)

        self.ref_file = ".Ref" # Reference file extension
        self.extension = "*.Lore;" # Extension allowed for the file dialog
        self.compression_used = b'\x01' # A 1 byte marker that specifies compression was used
        self.compression_skipped = b'\x00' # A 1 byte marker that specifies compression was not used
        self.size1 = 1 # used for a max size of 1 byte
        self.size2 = 2 # used for a max size of 2 bytes
        self.size3 = 4 # used for a max size of 4 bytes(mainly for reference files)
        self.gui() # call GUI function

        
    def file_handling(self):
        """This functions handles the initial file reading logic of the user selected Lore file"""
        
        self.characters() # Call characters function
        self.filename = filedialog.askopenfilename(
            initialdir = os.getcwd(),
            title = "Select Lore File",
            filetypes=(
                ("Supported Files", self.extension),
            ))
        try:
            if self.filename:
                base_name = os.path.splitext(self.filename)[0] # Strip the lore extension
                self.ref_lore = base_name + self.ref_file # Add the .Ref extension to access the .Ref file that matches the .Lore file
                with open(self.filename, "rb") as f1: # Open the Lore file
                    character_count = int.from_bytes(f1.read(self.size2), "little") # get the total amount of characters in the Lore file
                    self.character_data = [] # Holds character names
                    for i in range(character_count): # loop
                        name_len = int.from_bytes(f1.read(self.size2), "little") # Character name length
                        desc_len = int.from_bytes(f1.read(self.size2), "little") # Character description length
                        name_marker = f1.read(self.size1) # Read character name marker that specifies if compression was used or not
                        desc_marker = f1.read(self.size1) # Read character description marker that specifies if compression was used or not
                        char_name = f1.read(name_len) # read character name
                        desc_info = f1.read(desc_len) # read character description
                        # Decode based on marker
                        if name_marker == self.compression_used: # if compression was used
                            char_name = zlib.decompress(char_name).decode() # decompress and decode character name
                        else: # If compression was not used
                            char_name = char_name.decode() # decode character name
                        
                        self.character_data.append(char_name)  # Store the decoded name
                    self.slot_combobox['values'] = self.character_data  # Update combobox values
                    if self.character_data:
                        self.selected_slot.set(self.character_data[0])  # Default to the first character
        except FileNotFoundError:
            input(f"Error: The file {self.filename} does not exist.")
        except PermissionError:
                input(f"Error: Permission denied for file {self.filename}.")
        except IOError as e:
                input(f"Error. An I/O error occured. Details: {e}")
        self.data_search() # run data_search function
        
    def data_search(self):
        """This function is used for character name and description reading"""
        
        self.text_info.config(state="normal")
        self.text_info.delete(1.0, tk.END)  # Clear previous data
        selected_name = self.selected_slot.get() # get the currently selected character
        if selected_name in self.character_data: # if the character's name is in character_data
            character_index = self.character_data.index(selected_name) # get the position number
        with open(self.filename, "rb") as f1: # open the Lore file
            with open(self.ref_lore, "rb") as f2: # open the Lore metadata file(.Ref file)
                useroffset = character_index * self.size3 # get the offset needed for the selected character in the .Ref file
                f2.seek(useroffset) # seek the offset
                user_info = int.from_bytes(f2.read(self.size3), "little") # get the offset that will be used for the .Lore file
                f1.seek(user_info) # go to the offset in the .Lore file
                name_len = int.from_bytes(f1.read(self.size2), "little") # Read the name length
                info_len = int.from_bytes(f1.read(self.size2), "little") # Read the description length
                name_check = f1.read(self.size1) # Read the name marker that says if the character name is compressed or not
                info_check = f1.read(self.size1) # Read the description marker that says if the description is compressed or not
                char_name = f1.read(name_len) # Read the character name
                char_info = f1.read(info_len) # Read the description of the character
                if info_check == self.compression_used: # If the description is compressed
                    zdata = zlib.decompress(char_info) # decompress description
                    dec_info = zdata.decode() # decode description
                    self.text_info.insert(tk.END, dec_info) # insert the decoded text
                else: # If compression is not used
                    odata = char_info.decode() # decode description
                    self.text_info.insert(tk.END, odata) # insert description
        self.text_info.config(state="disabled")
        
    def characters(self):
        """Function used for characters(may be updated in the future or removed though)"""
        
        self.character_data = [] # list for storing the character name

    def gui(self):
        """this function is used for the GUI logic and handling"""
        
        self.characters() # Call characters function
        self.selected_slot = tk.StringVar(self.root) # Used for holding character names
        self.selected_slot.set("")  # Default value
        self.slot_combobox = ttk.Combobox(self.root, textvariable=self.selected_slot, values=self.character_data, width = 40)
        self.slot_combobox.bind("<<ComboboxSelected>>", self.slot_selected)
        self.slot_combobox.place(x=700, y=10)
        tk.Label(self.root, text="Character Description:").place(x=200, y=170)
        tk.Label(self.root, text="Lore Entries").place(x=620, y=10)
        self.text_info = tk.Text(self.root, wrap = "word", state = "disabled", height = 5, width = 80)
        self.text_info.place(x = 200, y = 200)
        tk.Button(self.root, text="Select Lore File", command=self.file_handling, height=5, width=30).place(x=10, y=10)
        
    def slot_selected(self, event=None):
        """This function is used for updating display data"""
        
        selected_name = self.selected_slot.get() # Get the currently selected name
        if selected_name in self.character_data: # If the selected name is in character_data
            character_index = self.character_data.index(selected_name)
            self.data_search()
        
def runner():
    root = tk.Tk()
    Lore_App = LoreApp(root)
    root.mainloop()
if __name__ == "__main__":
    runner()
