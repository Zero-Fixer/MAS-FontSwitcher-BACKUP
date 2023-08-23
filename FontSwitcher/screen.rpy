#===========================================================================================
# Screen Base
#===========================================================================================

# This screen handles font switching settings.
screen _font_switcher_submod():
    $ tooltip = renpy.get_screen("submods", "screens").scope["tooltip"]

    vbox:
        style_prefix "check"
        box_wrap False
        xfill True
        xmaximum 1000

        # Display selected font's name.
        label _("Font : {0}").format(persistent._font_settings_["name"]):
            xpos 0.3

        null height 10

        # Sort and display font options in groups of four.
        $ font_keys = sorted(JS_font_switcher.keys(), key=lambda k: JS_font_switcher[k]["name"])

        for i in range(0, len(font_keys), 4):
            hbox:
                for j in range(i, min(i+4, len(font_keys))):
                    $ key = font_keys[j]
                    $ font_name = JS_font_switcher[key]["name"]

                    # Button to select a font.
                    textbutton _(font_name):
                        action SetField(persistent, "_save_font_", key)
                        hovered tooltip.Action(JS_font_switcher[key]["description"])
                        selected persistent._save_font_ == key
            null height 10

        null height 10

        # Buttons for applying, disabling, previewing, and restarting font changes.
        hbox:
            spacing 5

            textbutton _("Apply"):
                style "navigation_button"
                action Show(screen="dialog", message="To apply the changes, the game will be closed.\nFont to apply : {0}\nRange : {1}".format(
                    JS_font_switcher[persistent._save_font_]["name"], persistent._font_switcher_change.capitalize()),
                    ok_action=Function(FS_apply_style))
                
            textbutton _("Disable"):
                style "navigation_button"
                action Show(screen="dialog", message="Disabling has been successful.\nThe game will now be closed.",
                            ok_action=Function(FS_reset_style))
                sensitive persistent._font_settings_["applied"]

            textbutton _("Preview"):
                style "navigation_button"
                action Function(renpy.call_in_new_context, '_fs_preview')
                hovered tooltip.Action("Here is a preview of the font you want to apply.")
                
            textbutton _("Restart"):
                style "navigation_button"
                action Show(screen="dialog", message="Old Range : {0}\nNew Range : {1}".format(
                    font_switcher_old_change.capitalize(), persistent._font_switcher_change.capitalize()),
                    ok_action=Function(FS_monika_restart))
                    
                sensitive persistent._font_settings_["applied"] and not font_switcher_old_change == persistent._font_switcher_change
                hovered tooltip.Action("It is necessary to manually restart or close the game to apply the range change.")
                    
            null height 20
            hbox:
                spacing 10

                # Options for font switcher range.
                $ font_switcher_options = [
                    ("Low", "Apply a minimum change."),
                    ("Medium", "Applies balanced changes."),
                    ("High", " Applies changes to the entire interface (Except for: Check Button).")
                ]

                for option_label, option_tooltip in font_switcher_options:
                    textbutton _(option_label):
                        action SetField(persistent, "_font_switcher_change", option_label.lower())
                        hovered tooltip.Action(option_tooltip)
                        selected persistent._font_switcher_change == option_label.lower()

#===========================================================================================
# Preview
#===========================================================================================
# Label to display font preview.
label _fs_preview:
    hide monika
    python:
        disable_esc()
        mas_MUMURaiseShield()
        font_settings = JS_font_switcher[persistent._save_font_]
        size_default = font_settings["size_default"]
        size_button = font_settings["size_button"]
        path_default = font_settings["font_default"]
        path_label = font_settings["font_label"]
        path_button = font_settings["font_button"]
        preview_text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit.\n1 2 3 4 5 6 7 8 9 0 ! ? . , : ; _\nJust click on the textbox or anywhere on the screen to exit the preview."
    $ fake_name = "{size=[size_default]}{font=[path_default]}Name{/font}{/size}"

    # Show font preview overlay.
    show screen fake_overlay
    fake_name "{size=[size_default]}{font=[path_default]}[preview_text]{/font}{/size}"
    show monika
    python:
        enable_esc()
        mas_MUMUDropShield()
    hide screen fake_overlay
    return

# Overlay screen for font preview.
screen fake_overlay():
    zorder 50

    vbox:
        style_prefix "check"
        xpos 0.050
        ypos 0.0
        label "{size=[size_default]}{font=[path_label]}Note:{/font}{/size}"
        text "{size=[size_default]}{font=[path_default]}Just Monika{/font}{/size}" outlines [(2, "#808080", 0, 0)]

    vbox:
        style_prefix "hkb"
        xpos 0.05
        yanchor 1.0
        ypos 715

        for button_text in ["Talk", "Extra", "Music", "Play"]:
            textbutton "{size=[size_button]}{font=[path_button]}[button_text]{/font}{/size}":
                action NullAction()

    vbox:
        style_prefix "talk_choice"
        $ items = [
            "Bookmarks",
            "Hey, {0}...".format(m_name),
            "Repeat conversation",
            "I love you!",
            "I feel...",
            "Goodbye",
            "Nevermind"
        ]

        for _menu in items:
            textbutton "{size=[size_button]}{font=[path_button]}[_menu]{/font}{/size}":
                action NullAction()
