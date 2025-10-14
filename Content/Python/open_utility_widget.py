"""

    Example of extending a menu in Unreal using Python

"""

import unreal

@unreal.uclass()
class MyEntryScript(unreal.ToolMenuEntryScript):
    @unreal.ufunction(override=True)
    def execute(self, context):
        # Reemplaza 'YourWidgetName' con el nombre real de tu Utility Widget
        widget_path = "/Game/read_json"  # Ajusta la ruta según tu estructura de carpetas
        
        try:
            # Cargar el asset del widget
            widget_asset = unreal.EditorAssetLibrary.load_asset(widget_path)
            
            if widget_asset:
                # Crear y mostrar el widget
                editor_utility_subsystem = unreal.get_editor_subsystem(unreal.EditorUtilitySubsystem)
                editor_utility_subsystem.spawn_and_register_tab(widget_asset)
                print(f"Widget '{widget_path}' opened successfully!")
            else:
                print(f"Failed to load widget at path: {widget_path}")
                
        except Exception as e:
            print(f"Error opening widget: {str(e)}")

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
        name = "OpenUtilityWidget",
        label = "Open Utility Widget",
        tool_tip = "Opens the utility widget"
    )
    myentry_script_1.register_menu_entry()

    menus.refresh_all_widgets()

if __name__ == '__main__':
    main()