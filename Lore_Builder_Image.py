import os
import sys
import zlib

# Class for receiving lore and then building the container file
class ContainerLore():
    def __init__(self):
        self.ref_file = ".Ref"
        self.extension = ".Lore"
        self.folder = "Character_Images"
        self.user_file = None
        self.ref_lore = None
        self.image_files = []
        self.updated_value = None # this will hold a value of 1 if the Lore file is set to update
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
        os.makedirs(self.folder, exist_ok=True)
        self.counting = 0 # for the number of characters that are finished being added
        valid_answers = {'update', 'replace'}
        try:
            self.lore_file = input("What do you want the name of your Lore file to be(A file that stores Lore on characters you add)?: ")
            self.user_file = self.lore_file + self.extension
            user_ref = self.lore_file + self.ref_file
            if os.path.isfile(self.user_file):
                while True:
                    user_answer = input(f"Uh oh, the Lore file {self.user_file} already exists, do you want to update or replace it? (update/replace): ")
                    if user_answer.lower() not in valid_answers:
                        print(f"Error: The answer given '{user_answer}' was not a valid answer.")
                        continue
                    if user_answer.lower() == 'replace':
                        os.remove(self.user_file)
                        os.remove(user_ref)
                        print(f"The file {self.user_file} has been deleted, a new file will be made.")
                    else:
                        self.updated_value = 1
                        print(f"The file {self.user_file} will be updated to support more characters.")
                    break
                
            self.info1 = int(input("How many characters will you be adding? "))
        except ValueError:
            input("Invalid number of characters.")
        for i in range(self.info1):
            self.info2 = input("Enter the name of the character: ") # character name
            self.info3 = input("Enter the description of the character: ") # character description
            if not self.info2 or not self.info3:
                print("Character name and description cannot be empty.")
                continue
            image_file = input("Please enter the image file you want to use with the character: ")
            self.image_files.append(image_file)
            
            # Check if the file exists
            if os.path.isfile(os.path.join(self.folder, image_file)):
                print(f"Image file found.")

            else:
                print("No image file found for the character.")
                sys.exit()
            
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

        self.container(self.updated_value) # call the container building function

    def write_character_data(self, file_handle):
        """Writes character and description data to the given file handle."""
        for index, image_files in enumerate(self.image_files):
            with open(os.path.join(self.folder, image_files), "rb") as f1:
                image_size = os.path.getsize(os.path.join(self.folder, image_files))
                image_data = f1.read()
                # Extract data for the current character
                a = self.character_len[index]
                b = self.description_len[index]
                c = self.name_markers[index]
                d = self.description_markers[index]
                e = self.character_data[index]
                f = self.description_data[index]

                lore_offset = file_handle.tell()
                file_handle.write(a.to_bytes(self.size2, "little"))
                file_handle.write(b.to_bytes(self.size2, "little"))
                file_handle.write(c)
                file_handle.write(d)
                file_handle.write(e)
                file_handle.write(f)
                file_handle.write(image_size.to_bytes(4, "little"))
                file_handle.write(image_data)
                self.reference(lore_offset)

    def container_updater(self): # update container instead
        with open(self.user_file, "r+b") as f1: # open the container file
            file_size = os.path.getsize(self.user_file)
            return_to_update = f1.tell() # return to this offset to update with the new character count
            current_character_count = int.from_bytes(f1.read(self.size2), "little")
            total_characters = current_character_count + self.info1
            f1.seek(return_to_update) # return for writing the new character count
            f1.write(total_characters.to_bytes(self.size2, "little")) # write the new character count
            f1.seek(file_size) # seek the end of the file for adding new characters
            self.write_character_data(f1)
                
    def container(self, file_action: int): # container file building function
        self.user_file = self.lore_file + self.extension
        self.ref_lore = self.lore_file + self.ref_file
        lore_offset = None
        with open(self.user_file, "ab") as f1: # open the container file
            if file_action != 1:
                f1.write(self.info1.to_bytes(self.size2, "little")) # write the amount of characters added
                self.write_character_data(f1)
            else:
                f1.close()
                self.container_updater() # call updater function if updating lore file
                    
    def reference(self, data: int): # Used for creating the reference file(stores offsets)
        with open(self.ref_lore, "ab") as f1: # open Lore reference file
            f1.write(data.to_bytes(self.size3, "little")) # write offsets to character data

if __name__ == "__main__":
    ContainerLore()
    input("Task finished, you may exit now.")


