# Lore-App
A small and simple offline based Lore app that doesn't require an internet connection like online websites that contain Lore on characters in Anime, games, etc. There is nothing wrong with those websites, this is merely an attempt at making an offline based one that uses Python and Tkinter. Credit goes to God(Christian) and I(for the coding). Currently the Lore_Container_Builder script is console based while the Lore_App script has a GUI using Python's Tkinter.

Current features for the Container Builder script(console based):

1. The Container Builder script will create Lore files(.Lore and .Ref) after asking what you want the name of the file to be.

2. It will ask for the amount of characters you want to add along with the name and description of each character.

3. It will compress the character names and descriptions using ZLIB if it detects the compressed size of the text will be smaller than the original size.

4. Adds necessary markers with each character name and description to specify for the Lore App if compression was used.
5. 
Current features for the Lore App script(GUI based using Tkinter):

1. Selecting a Lore file using the "Select Lore File" button

2. Usage of a combobox that stores all of the character names in the selected Lore file

3. A Textbox that displays the description of the currently selected character
