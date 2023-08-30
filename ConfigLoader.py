import json

class ConfigLoader:
    @staticmethod
    def load_config(filename):
        try:
            with open(filename, 'r') as config_file:
                config = json.load(config_file)
            return config
        except FileNotFoundError:
            print(f"Error: Config file '{filename}' not found.")
            return {}
        except json.JSONDecodeError:
            print(f"Error: Unable to parse JSON from config file '{filename}'.")
            return {}