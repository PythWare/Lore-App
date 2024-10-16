# Lore-App
A small and simple offline based Lore app that doesn't require an internet connection like online websites that contain Lore on characters in Anime, games, etc. There is nothing wrong with those websites, this is merely an attempt at making a small offline based one that uses Python and Tkinter. Credit goes to God(Christian) and I(for the coding). Currently the Builder script is console based while the Lore_App script has a GUI using Python's Tkinter. I have included two versions, the text based version and the image based version of the Lore App. The difference is that the image based version supports displaying images of characters created with the Builder script while the text based version is for anyone that doesn't want images displayed within the Lore App.

Current features for the Builder script(console based):

1. The Container Builder script will create Lore file(.Lore file) after asking what you want the name of the file to be.

2. If the file is detected it will offer updating or replacing
   
3. It will ask for the amount of characters you want to add along with the name and description of each character.

4. Asks for image to be used with the entered character.

5. It will compress the character names and descriptions using ZLIB if it detects the compressed size of the text will be smaller than the original size.

6. Creates the reference file(.Ref file) for the Lore file created.

Current features for the Lore App script(GUI based using Tkinter):

1. Selecting a Lore file using the "Select Lore File" button

2. Usage of a combobox that stores all of the character names in the selected Lore file

3. A Textbox that displays the description of the currently selected character

4. Image display of characters created with the Lore App

5. Down scales or upscales images stored within the Lore file automatically to a specific width and height so that you don't have to.

To use images with the characters you need to have images placed within the folder created by the builder script. The images are then packed into the .Lore file which is a custom container format I designed.
