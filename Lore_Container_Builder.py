import os
import zlib

# Class for receiving lore and then building the container file
class ContainerLore():
    def __init__(self):
        self.ref_file = ".Ref"
        self.extension = ".Lore"
        self.character_len = [] # list for storing the size of the character name
        self.description_len = [] # list for storing the size of the description
        self.compressed_name = None # used for compressed name length
        self.compressed_description = None # used for commpressed description length
        self.character_data = [] # list for storing the character name
        self.description_data = [] # list for storing the description of the character
        self.name_markers = []
        self.description_markers = []
        self.offsets = [] # will be used later
        self.size1 = 1 # used for a max size of 1 byte
        self.size2 = 2 # used for a max size of 2 bytes
        self.size3 = 4 # used for a max size of 4 bytes(mainly for reference files)
        self.orig_mark = 0 # used if the data written is not compressed
        self.comp_mark = 1 # used if the data written is compressed
        self.characters() # call characters function
    def characters(self): # handles the character and description data
        self.counting = 0 # for the number of characters that are finished being added
        try:
            self.lore_file = input("What do you want the name of your Lore file to be(A file that stores Lore on characters you add)?: ")
            self.info1 = int(input("How many characters will you be adding? "))
        except ValueError:
            input("Invalid number of characters.")
        for i in range(self.info1):
            self.info2 = input("Enter the name of the character: ") # character name
            self.info3 = input("Enter the description of the character: ") # character description
            if not self.info2 or not self.info3:
                print("Character name and description cannot be empty.")
                continue
            self.counting += 1
            print(f"Character number {self.counting} is finished.")
            comp_name = zlib.compress(self.info2.encode(), 9)
            comp_description = zlib.compress(self.info3.encode(), 9)
            
            if len(comp_name) > len(self.info2): # if compressed name is larger
                self.character_data.append(self.info2.encode()) # store the encoded name
                self.character_len.append(len(self.info2)) # store the size of the character name
                self.name_markers.append(self.orig_mark.to_bytes(self.size1, "little")) # store original marker
            else:
                self.character_data.append(comp_name) # store the compressed name
                self.character_len.append(len(comp_name)) # store the compressed size of the character name
                self.name_markers.append(self.comp_mark.to_bytes(self.size1, "little")) # store compressed marker
                
            if len(comp_description) > len(self.info3): # if compressed description is larger
                self.description_data.append(self.info3.encode()) # store the encoded description
                self.description_len.append(len(self.info3)) # store the size of the character description
                self.description_markers.append(self.orig_mark.to_bytes(self.size1, "little")) # store original marker
            else:
                self.description_data.append(comp_description) # store compressed description
                self.description_len.append(len(comp_description)) # store the compressed size of the character description
                self.description_markers.append(self.comp_mark.to_bytes(self.size1, "little")) # store compressed marker
            #repeat = input("Would you like to add another character? (yes/no): ") # ask to continue
            #if repeat.lower() != 'yes':
            #break
        self.container() # call the container building function
    def container(self): # container file building function
        self.user_file = self.lore_file + self.extension
        self.ref_lore = self.lore_file + self.ref_file
        lore_offset = None
        with open(self.user_file, "ab") as f1: # open the container file
            f1.write(self.info1.to_bytes(1, "little")) # write the amount of characters added
            for a, b, c, d, e, f in zip(self.character_len, self.description_len, self.name_markers, self.description_markers,
                                        self.character_data, self.description_data): # add the character and description data
                lore_offset = f1.tell()
                f1.write(a.to_bytes(self.size2, "little"))
                f1.write(b.to_bytes(self.size2, "little"))
                f1.write(c)
                f1.write(d)
                f1.write(e)
                f1.write(f)
                self.reference(lore_offset)
                    
    def reference(self, data: int): # Used for creating the reference file(stores offsets)
        with open(self.ref_lore, "ab") as f1: # open Lore reference file
            f1.write(data.to_bytes(self.size3, "little")) # write offsets to character data

if __name__ == "__main__":
    ContainerLore()
    input("Task finished, you may exit now.")


