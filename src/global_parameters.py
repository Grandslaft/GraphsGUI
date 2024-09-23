import darkdetect

# detect light modew
def Light_mode(mode):
    global SYSTEM_LIGHT_MODE
    match mode:
        case 'System':
            SYSTEM_LIGHT_MODE = 'Dark' if darkdetect.isDark() else 'Light'
        case 'Light':
            SYSTEM_LIGHT_MODE = 'Light'
        case 'Dark':
            SYSTEM_LIGHT_MODE = 'Dark'
# current direction of the main
CURRENT_DIR = None
# Corner radius for widgets
CORNER_RADIUS = 10
# outer padding (mostly horizontal)
OUTER_PAD = 20
# inner padding (mostly vertical)
INNER_PAD = 10
# padding for same type elements
ELEMENTS_PAD = 5