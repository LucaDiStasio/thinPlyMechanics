from pywinauto.application import Application
# Run a target application
app = Application().start("notepad.exe")
# Select a menu item
app.UntitledNotepad.menu_select("Help->About Notepad")
# Click on a button
app.AboutNotepad.OK.click()
# Type a text string
app.UntitledNotepad.Edit.type_keys("pywinauto Works!", with_spaces = True)
