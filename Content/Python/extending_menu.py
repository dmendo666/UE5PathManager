"""

    Example of extending a menu in Unreal using Python

"""

import unreal

@unreal.uclass()
class MyEntryScript(unreal.ToolMenuEntryScript):
    @unreal.ufunction(override=True)
    def execute(self, context):
        print("Hello, World!")

def main():

    menus = unreal.ToolMenus.get()

    # Find the 'edit' menu, this should not fail, 
    # but if we're looking for a menu we're unsure about 'if not' 
    # works as nullptr check,
    edit = menus.find_menu("LevelEditor.MainMenu.Edit")
    main_menu = menus.find_menu("LevelEditor.MainMenu")
    if not edit:
        print("Failed to find the 'Edit' menu")

    myentry_script_1 = MyEntryScript()  
    myentry_script_1.init_entry(
        owner_name = edit.menu_name,
        menu = edit.menu_name,
        section = "EditMain",
        name = "PrintHelloWorld",
        label = "Print hello world",
        tool_tip = "Prints hello world to the output log"
    )
    myentry_script_1.register_menu_entry()

    menus.refresh_all_widgets()

if __name__ == '__main__':
    main()