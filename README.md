# Lore-App
A small and simple offline based Lore app that doesn't require an internet connection like online websites that contain Lore on characters in Anime, games, etc. There is nothing wrong with those websites, this is merely an attempt at making a small offline based one that uses Python and Tkinter. Credit goes to God(Christian) and I(for the coding). Currently the Lore_Container_Builder script is console based while the Lore_App script has a GUI using Python's Tkinter.

Current features for the Container Builder script(console based):

1. The Container Builder script will create Lore file(.Lore file) after asking what you want the name of the file to be.

2. It will ask for the amount of characters you want to add along with the name and description of each character.

3. It will compress the character names and descriptions using ZLIB if it detects the compressed size of the text will be smaller than the original size.

4. Creates the reference file(.Ref file) for the Lore file created.

Current features for the Lore App script(GUI based using Tkinter):

1. Selecting a Lore file using the "Select Lore File" button

2. Usage of a combobox that stores all of the character names in the selected Lore file

3. A Textbox that displays the description of the currently selected character

How the Container file works:

The Container file(the .Lore file) is a custom container file that will store all of the character names and descriptions. Each character has a few bytes worth of metadata for the Lore App's file reader to use in reading the character data.
The metadata is the character's name length, description length, character name marker that specifies if compression was used, and description marker that specifies if compression was used. The reference file(.Ref file) is essentially a metadata file that holds offsets for character data in the Lore file.

The Lore App is as I said, small and simple but it was something I wanted to make and share with everyone.
