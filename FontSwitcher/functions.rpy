init -1 python:
    # Apply the selected font style and trigger a game restart.
    def FS_apply_style():
        FS_get_data = JS_font_switcher[persistent._save_font_]
        persistent._font_settings_ = {
            "id": persistent._save_font_,
            "name": FS_get_data["name"],
            "applied": True
        }
        FS_monika_restart()

    # Reset font style settings to default and trigger a game restart.
    def FS_reset_style():
        persistent._font_settings_ = {
            "id": "justmonika",
            "name": "Inactive",
            "applied": False
        }
        FS_monika_restart()

    # Restart the game by setting a flag and quitting Ren'Py.
    def FS_monika_restart():
        persistent.closed_self = True
        renpy.quit()

    # Load fonts data from JSON files in the designated folder.
    def FS_load_fonts():
        json_folder = renpy.config.basedir + "/game/submods/FontSwitcher/json"
        
        try:
            json_files = [os.path.join(json_folder, filename) for filename in os.listdir(json_folder) if filename.endswith('.json')]
        except OSError:
            return {
                "justmonika": {
                    "name": "Monika",
                    "font_default": "mod_assets/font/m1_fixed.ttf",
                    "font_label": "mod_assets/font/m1_fixed.ttf",
                    "font_button": "mod_assets/font/m1_fixed.ttf",
                    "size_default": 30,
                    "size_button": 30,
                    "padding": 3,
                    "description": "I'm glad to see you here, [player]~"
                }
            }

        fonts_data = {}
        
        for filepath in json_files:
            with open(filepath, "r") as file:
                json_data = json.load(file)
            fonts_data.update(json_data)

        return fonts_data

    # Check if a font file exists at the given path.
    def is_font_available(font_path):
        return os.path.isfile(font_path)
