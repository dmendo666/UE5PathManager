import unreal
import json
import os

@unreal.uclass()
class JsonReaderBFL(unreal.BlueprintFunctionLibrary):
    """
    Blueprint Function Library for reading JSON files and logging their contents
    """
    
    @unreal.ufunction(static=True, params=[str], ret=bool, meta=dict(category="JSON Utilities"))
    def read_and_log_json_file(file_path: str) -> bool:
        """
        Read a JSON file and log all its values to the console
        
        Args:
            file_path: Path to the JSON file (relative to project or absolute)
            
        Returns:
            bool: True if successful, False if failed
        """
        try:
            # Convert relative path to absolute if needed
            if not os.path.isabs(file_path):
                # Get the project directory
                project_dir = unreal.Paths.project_dir()
                full_path = os.path.join(project_dir, file_path)
            else:
                full_path = file_path
            
            # Check if file exists
            if not os.path.exists(full_path):
                unreal.log_error(f"JSON file not found: {full_path}")
                return False
            
            # Read and parse JSON file
            with open(full_path, 'r', encoding='utf-8') as file:
                json_data = json.load(file)
            
            # Log the file path
            unreal.log(f"=== JSON File Contents: {file_path} ===")
            
            # Log all values recursively
            JsonReaderBFL._log_json_values(json_data, "")
            
            unreal.log("=== End JSON File Contents ===")
            return True
            
        except json.JSONDecodeError as e:
            unreal.log_error(f"Invalid JSON format in file {file_path}: {str(e)}")
            return False
        except Exception as e:
            unreal.log_error(f"Error reading JSON file {file_path}: {str(e)}")
            return False
    
    @unreal.ufunction(static=True, params=[str], ret=str, meta=dict(category="JSON Utilities"))
    def read_json_file_as_string(file_path: str) -> str:
        """
        Read a JSON file and return its contents as a formatted string
        
        Args:
            file_path: Path to the JSON file
            
        Returns:
            str: JSON contents as formatted string, or empty string if failed
        """
        try:
            # Convert relative path to absolute if needed
            if not os.path.isabs(file_path):
                project_dir = unreal.Paths.project_dir()
                full_path = os.path.join(project_dir, file_path)
            else:
                full_path = file_path
            
            if not os.path.exists(full_path):
                unreal.log_error(f"JSON file not found: {full_path}")
                return ""
            
            with open(full_path, 'r', encoding='utf-8') as file:
                json_data = json.load(file)
            
            return json.dumps(json_data, indent=2, ensure_ascii=False)
            
        except Exception as e:
            unreal.log_error(f"Error reading JSON file {file_path}: {str(e)}")
            return ""
    
    @unreal.ufunction(static=True, params=[str, str], ret=str, meta=dict(category="JSON Utilities"))
    def get_json_value_by_path(file_path: str, key_path: str) -> str:
        """
        Get a specific value from JSON file using dot notation path
        
        Args:
            file_path: Path to the JSON file
            key_path: Dot-separated path to the value (e.g., "player.stats.health")
            
        Returns:
            str: Value as string, or empty string if not found
        """
        try:
            # Convert relative path to absolute if needed
            if not os.path.isabs(file_path):
                project_dir = unreal.Paths.project_dir()
                full_path = os.path.join(project_dir, file_path)
            else:
                full_path = file_path
            
            if not os.path.exists(full_path):
                unreal.log_error(f"JSON file not found: {full_path}")
                return ""
            
            with open(full_path, 'r', encoding='utf-8') as file:
                json_data = json.load(file)
            
            # Navigate through the key path
            current_data = json_data
            keys = key_path.split('.')
            
            for key in keys:
                if isinstance(current_data, dict) and key in current_data:
                    current_data = current_data[key]
                elif isinstance(current_data, list) and key.isdigit():
                    index = int(key)
                    if 0 <= index < len(current_data):
                        current_data = current_data[index]
                    else:
                        unreal.log_error(f"Index {index} out of range for array")
                        return ""
                else:
                    unreal.log_error(f"Key '{key}' not found in JSON data")
                    return ""
            
            # Convert result to string
            if isinstance(current_data, (dict, list)):
                return json.dumps(current_data, indent=2, ensure_ascii=False)
            else:
                return str(current_data)
                
        except Exception as e:
            unreal.log_error(f"Error getting value from JSON file: {str(e)}")
            return ""
    
    @unreal.ufunction(static=True, params=[str], ret=bool, meta=dict(category="JSON Utilities"))
    def log_json_string(json_string: str) -> bool:
        """
        Parse and log a JSON string to the console
        
        Args:
            json_string: JSON string to parse and log
            
        Returns:
            bool: True if successful, False if failed
        """
        try:
            json_data = json.loads(json_string)
            
            unreal.log("=== JSON String Contents ===")
            JsonReaderBFL._log_json_values(json_data, "")
            unreal.log("=== End JSON String Contents ===")
            
            return True
            
        except json.JSONDecodeError as e:
            unreal.log_error(f"Invalid JSON format: {str(e)}")
            return False
        except Exception as e:
            unreal.log_error(f"Error parsing JSON string: {str(e)}")
            return False
    
    @staticmethod
    def _log_json_values(data, prefix):
        """
        Recursively log JSON values with proper indentation
        
        Args:
            data: JSON data to log (dict, list, or primitive)
            prefix: Current key path prefix for nested objects
        """
        if isinstance(data, dict):
            for key, value in data.items():
                current_path = f"{prefix}.{key}" if prefix else key
                
                if isinstance(value, (dict, list)):
                    unreal.log(f"{current_path}:")
                    JsonReaderBFL._log_json_values(value, current_path)
                else:
                    unreal.log(f"{current_path}: {value} ({type(value).__name__})")
                    
        elif isinstance(data, list):
            for i, item in enumerate(data):
                current_path = f"{prefix}[{i}]" if prefix else f"[{i}]"
                
                if isinstance(item, (dict, list)):
                    unreal.log(f"{current_path}:")
                    JsonReaderBFL._log_json_values(item, current_path)
                else:
                    unreal.log(f"{current_path}: {item} ({type(item).__name__})")
        else:
            # For primitive values at root level
            unreal.log(f"{prefix}: {data} ({type(data).__name__})")


# Standalone utility functions that can be called directly from Python console
def create_sample_json_file(file_name: str = "sample_data.json") -> bool:
    """
    Create a sample JSON file in the project directory for testing
    
    Args:
        file_name: Name of the JSON file to create
        
    Returns:
        bool: True if successful, False if failed
    """
    try:
        # Sample data structure
        sample_data = {
            "game_info": {
                "title": "My Awesome Game",
                "version": "1.0.0",
                "developer": "Your Studio"
            },
            "player_data": {
                "name": "TestPlayer",
                "level": 42,
                "health": 100,
                "mana": 75,
                "position": {
                    "x": 123.45,
                    "y": 67.89,
                    "z": 0.0
                },
                "inventory": [
                    {"item": "Sword", "quantity": 1, "durability": 85},
                    {"item": "Health Potion", "quantity": 5, "durability": 100},
                    {"item": "Magic Ring", "quantity": 1, "durability": 95}
                ]
            },
            "settings": {
                "graphics": {
                    "resolution": "1920x1080",
                    "quality": "High",
                    "vsync": True
                },
                "audio": {
                    "master_volume": 0.8,
                    "sfx_volume": 0.7,
                    "music_volume": 0.6
                }
            },
            "achievements": [
                "First Steps",
                "Level 10 Reached",
                "Treasure Hunter"
            ]
        }
        
        # Get project directory and create full path
        project_dir = unreal.Paths.project_dir()
        full_path = os.path.join(project_dir, file_name)
        
        # Write JSON file
        with open(full_path, 'w', encoding='utf-8') as file:
            json.dump(sample_data, file, indent=2, ensure_ascii=False)
        
        unreal.log(f"Sample JSON file created at: {full_path}")
        return True
        
    except Exception as e:
        unreal.log_error(f"Error creating sample JSON file: {str(e)}")
        return False

def test_json_functions(file_name: str = "sample_data.json") -> None:
    """
    Test all JSON reader functions with a sample file
    
    Args:
        file_name: Name of the JSON file to test with
    """
    unreal.log("=== Starting JSON Function Tests ===")
    
    # Test 1: Create sample file
    unreal.log("Test 1: Creating sample JSON file...")
    if create_sample_json_file(file_name):
        unreal.log("✓ Sample file created successfully")
    else:
        unreal.log_error("✗ Failed to create sample file")
        return
    
    # Test 2: Read and log entire file
    unreal.log("\nTest 2: Reading and logging entire JSON file...")
    if JsonReaderBFL.read_and_log_json_file(file_name):
        unreal.log("✓ File read and logged successfully")
    else:
        unreal.log_error("✗ Failed to read and log file")
    
    # Test 3: Get specific values by path
    unreal.log("\nTest 3: Getting specific values by path...")
    test_paths = [
        "game_info.title",
        "player_data.level",
        "player_data.position.x",
        "player_data.inventory.0.item",
        "settings.graphics",
        "achievements"
    ]
    
    for path in test_paths:
        value = JsonReaderBFL.get_json_value_by_path(file_name, path)
        if value:
            unreal.log(f"✓ {path}: {value}")
        else:
            unreal.log_error(f"✗ Failed to get value for path: {path}")
    
    # Test 4: Read file as string
    unreal.log("\nTest 4: Reading file as formatted string...")
    json_string = JsonReaderBFL.read_json_file_as_string(file_name)
    if json_string:
        unreal.log("✓ File read as string successfully")
        unreal.log("First 200 characters:")
        unreal.log(json_string[:200] + "..." if len(json_string) > 200 else json_string)
    else:
        unreal.log_error("✗ Failed to read file as string")
    
    unreal.log("\n=== JSON Function Tests Completed ===")

# Quick test function
def quick_test() -> None:
    """Quick test function that can be called from Python console"""
    test_json_functions()
    
# Example of how to call the functions from Python console:
# import json_blueprint
# json_blueprint.quick_test()