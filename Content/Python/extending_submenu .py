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

    entry = unreal.ToolMenuEntry(
        name = "MyEntry",
        type = unreal.MultiBlockType.MENU_ENTRY, # If you pass a type that is not supported Unreal will let you know,
        insert_position = unreal.ToolMenuInsert("Delete", unreal.ToolMenuInsertType.AFTER) # this will tell unreal to insert this entry after the 'Delete' menu item, if found in section we define later,
    )

    entry.set_label("My Entry")
    entry.set_tool_tip("This is a Tool Menu Entry made in Python!")
    if not edit:
        print("Failed to find the 'Edit' menu")

    edit.add_menu_entry("EditMain", entry) # section name, ToolMenuInsert, Unreal will add the section name if it can't find it, otherwise call AddEntry for the found section,

 # section name, ToolMenuInsert, Unreal will add the section name if it can't find it, otherwise call AddEntry for the found section,

################### PART 2 ###################

    my_menu = edit.add_sub_menu(
        owner=edit.menu_name, 
        section_name="MySubmenu",
        name="MySubmenu",
        label="My Submenu"
    )

    myentry_script = MyEntryScript()  
    myentry_script.init_entry(
        owner_name = my_menu.menu_name,
        menu = my_menu.menu_name,
        section = "",
        name = "PrintHelloWorld",
        label = "Print Hello World",
        tool_tip = "Prints hello world to the output log"
    )

    my_menu.add_menu_entry_object(myentry_script)

    # for name in ["Foo", "Bar", "Baz"]:
    #     e = unreal.ToolMenuEntry(
    #         name = name,
    #         type = unreal.MultiBlockType.MENU_ENTRY, # If you pass a type that is not supported Unreal will let you know,
    #     )
    #     e.set_label(name)
    #     my_menu.add_menu_entry("Items", e)

    menus.refresh_all_widgets()

if __name__ == '__main__':
    main()