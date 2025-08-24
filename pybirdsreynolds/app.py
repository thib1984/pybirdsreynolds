import tkinter as tk
import random
import math
from pybirdsreynolds.args import compute_args, display_range, get_description, get_epilog, get_help_text
import signal
import sys
import copy
from importlib.metadata import version
import time
from tkinter import font
import types
import pybirdsreynolds.const as const
from pybirdsreynolds.draw import draw_paused, draw_fps, draw_hidden, draw_rectangle, draw_canvas, draw_canvas_hiden, draw_points, draw_status, draw_all, maximize_minimize, add_canvas_tooltip, add_widget_tooltip, is_maximized, update
import pybirdsreynolds.draw as draw
import pybirdsreynolds.reynolds as reynolds
from pybirdsreynolds.reynolds import generate_points_and_facultative_move

# variables
version_prog = version("pybirdsreynolds")
options = compute_args()
for var_name in dir(const):
    if var_name.endswith("_DEFAULT"):
        option_name = var_name[:-8]
        default_value = getattr(const, var_name)
        value = getattr(options, option_name.lower(), default_value)
        setattr(const, option_name, value)



trans_hiden=False
last_time = time.time()

fonts=[]
count= not const.PAUSED
resizing = False

shift_pressed = False
width_before_maximized=const.WIDTH
heigth_before_maximized=const.HEIGHT
if not const.COLOR:
    const.CANVAS_BG = "black"
    const.FILL_COLOR = "white"
    const.OUTLINE_COLOR = "black"
else:
    const.CANVAS_BG = "#87CEEB"
    const.FILL_COLOR = "black"
    const.OUTLINE_COLOR = "white" 

start_button = None
refresh_button = None
generation_button = None

# deep copy
max_speed_init = copy.deepcopy(const.MAX_SPEED)
neighbor_radius_init = copy.deepcopy(const.NEIGHBOR_RADIUS)
num_birds_init = copy.deepcopy(const.NUM_BIRDS)
width_init = copy.deepcopy(const.WIDTH)
height_init = copy.deepcopy(const.HEIGHT)
refresh_ms_init = copy.deepcopy(const.REFRESH_MS)
random_speed_init = copy.deepcopy(const.RANDOM_SPEED)
random_angle_init = copy.deepcopy(const.RANDOM_ANGLE)
sep_weight_init = copy.deepcopy(const.SEP_WEIGHT)
align_weight_init = copy.deepcopy(const.ALIGN_WEIGHT)
coh_weight_init = copy.deepcopy(const.COH_WEIGHT)
size_init = copy.deepcopy(const.SIZE)
font_size_init = copy.deepcopy(const.FONT_SIZE)
font_type_init = copy.deepcopy(const.FONT_TYPE)
triangles_init = copy.deepcopy(const.TRIANGLES)
free_init = copy.deepcopy(const.FREE)
color_init= copy.deepcopy(const.COLOR)
repeating = {"active": False, "job": None}

def app():

    param_docs = {
        name.removesuffix("_DOC"): value
        for name, value in vars(const).items()
        if name.endswith("_DOC")
        and getattr(const, f"{name[:-4]}_HIDEN", 1) == 0 
    }
    param_order = list(param_docs.keys())

    def restore_options():

        global fonts
 
        const.MAX_SPEED = copy.deepcopy(max_speed_init)
        const.NEIGHBOR_RADIUS = copy.deepcopy(neighbor_radius_init)
        const.NUM_BIRDS = copy.deepcopy(num_birds_init)
        const.WIDTH = copy.deepcopy(width_init)
        const.HEIGHT = copy.deepcopy(height_init)
        const.REFRESH_MS = copy.deepcopy(refresh_ms_init)
        const.RANDOM_SPEED = copy.deepcopy(random_speed_init)
        const.ANDOM_ANGLE = copy.deepcopy(random_angle_init)
        const.SEP_WEIGHT = copy.deepcopy(sep_weight_init)
        const.ALIGN_WEIGHT = copy.deepcopy(align_weight_init)
        const.COH_WEIGHT = copy.deepcopy(coh_weight_init)
        const.SIZE = copy.deepcopy(size_init)
        const.COLOR = copy.deepcopy(color_init)
        const.FREE = copy.deepcopy(free_init)
        const.TRIANGLES = copy.deepcopy(triangles_init)
        const.FONT_TYPE = copy.deepcopy(font_type_init)   

        if not const.COLOR:
            const.CANVAS_BG = "black"
            const.FILL_COLOR = "white"
            const.OUTLINE_COLOR = "black"
        else:
            const.CANVAS_BG = "#87CEEB"
            const.FILL_COLOR = "black"
            const.OUTLINE_COLOR = "white" 

    def start_repeat(ligne, direction):
        def repeat():
            on_click(ligne, direction)
            if repeating["active"]:
                repeating["job"] = draw.canvas.after(100, repeat)
        repeating["active"] = True
        repeat()

    def stop_repeat():
        repeating["active"] = False
        if repeating["job"]:
            draw.canvas.after_cancel(repeating["job"])
            repeating["job"] = None

    def on_shift_press(event):
        global shift_pressed
        shift_pressed = True

    def on_shift_release(event):
        global shift_pressed
        shift_pressed = False

    def toggle_pause(event=None):
        const.BLINK_STATE = True
        const.PAUSED = not const.PAUSED
        draw_status(draw.canvas,False, False, on_other_key,start_repeat , stop_repeat)
        draw_paused(draw.canvas)

    def change_value(type, val, free):
        value = getattr(const, type, None)
        prefix = type.upper()
        default       = getattr(const, f"{prefix}_DEFAULT", None)
        min_value     = getattr(const, f"{prefix}_MIN", None)
        max_value     = getattr(const, f"{prefix}_MAX", None)
        min_free_value = getattr(const, f"{prefix}_FREE_MIN", None)
        max_free_value = getattr(const, f"{prefix}_FREE_MAX", None)                
        value += val
        if not free:
            if max_value is not None:
                value = min(value, max_value)
            if min_value is not None:
                value = max(value, min_value)
        else:
            if max_free_value is not None:
                value = min(value, max_free_value)
            if min_free_value is not None:
                value = max(value, min_free_value)     
        return value

    def on_other_key(event):
        global fonts
        global shift_pressed
        shift = getattr(event, "state", None)        
        if shift is not None:
            shift = (shift & 0x1) != 0
        else:
            shift = shift_pressed
        if const.SHIFT_HIDEN==0:
            shift =False    
        mult = 10 if shift else 1
        val = mult if event.keysym == "Right" else 1*-mult
        param = param_order[const.SELECTED_INDEX]
        if (param == "WIDTH" or param == "HEIGHT") and is_maximized(draw.root):
            val=0
        if event.keysym == "Up" and const.ARROWS_HIDEN<2:
            const.SELECTED_INDEX = (const.SELECTED_INDEX - 1) % len(param_order)
        elif event.keysym == "Down" and const.ARROWS_HIDEN<2:
            const.SELECTED_INDEX = (const.SELECTED_INDEX + 1) % len(param_order)
        elif (event.keysym == "Right"  or event.keysym == "Left") and const.ARROWS_HIDEN<=1:
            if param == "TRIANGLES":
                const.TRIANGLES = not const.TRIANGLES
                draw_all(draw.canvas, draw.root, on_other_key,start_repeat , stop_repeat)
            elif param == "FONT_TYPE":
                current_index = fonts.index(const.FONT_TYPE)
                const.FONT_TYPE = fonts[(current_index + val) % len(fonts)]
                draw_all(draw.canvas, draw.root, on_other_key,start_repeat , stop_repeat)
                draw_status(draw.canvas,True, True, on_other_key,start_repeat , stop_repeat)              
            elif param == "COLOR":
                COLOR = not COLOR 
                if not COLOR:
                    const.CANVAS_BG = "black"
                    const.FILL_COLOR = "white"
                    const.OUTLINE_COLOR = "black"
                else:
                    const.CANVAS_BG = "#87CEEB"
                    const.FILL_COLOR = "black"
                    const.OUTLINE_COLOR = "white" 
                draw_canvas(draw.canvas,draw.root)
                draw_all(draw.canvas, draw.root, on_other_key,start_repeat , stop_repeat)
            elif param == "FREE":
                const.FREE = not const.FREE
                for paramm in param_order:
                    if paramm not in ["FREE", "COLOR" , "TRIANGLES", "FONT_TYPE"]:
                        setattr(const, paramm, change_value(paramm, 0, const.FREE))                                                   
            else:  
                setattr(const, param, change_value(param, val, const.FREE))

            if param == "NUM_BIRDS":
                generate_points_and_facultative_move(False, False)
                draw_points()                 
            elif param == "WIDTH":  
                generate_points_and_facultative_move(False, False)
                draw_status(draw.canvas,False, True, on_other_key,start_repeat , stop_repeat)
                draw_canvas(draw.canvas,draw.root)  
                draw_all(draw.canvas, draw.root, on_other_key,start_repeat , stop_repeat)
            elif param == "HEIGHT":  
                generate_points_and_facultative_move(False, False)
                draw_status(draw.canvas,False, True, on_other_key,start_repeat , stop_repeat)
                draw_canvas(draw.canvas,draw.root)
                draw_all(draw.canvas, draw.root, on_other_key,start_repeat , stop_repeat)
            elif param == "FREE":
                generate_points_and_facultative_move(False, False)
                draw_all(draw.canvas, draw.root, on_other_key,start_repeat , stop_repeat)                       
            elif param == "SIZE":
                generate_points_and_facultative_move(False, False)
                draw_all(draw.canvas, draw.root, on_other_key,start_repeat , stop_repeat)
            elif param =="FONT_SIZE" or param =="FONT_TYPE":
                draw_status(draw.canvas,True, True, on_other_key,start_repeat , stop_repeat)     
        elif getattr(event, "keysym", "").lower() == str(const.RESET_COMMAND) and const.RESET_HIDEN<=1:
            restore_options()
            generate_points_and_facultative_move(False, False)
            draw_all(draw.canvas, draw.root, on_other_key,start_repeat , stop_repeat)
            draw_canvas(draw.canvas,draw.root)
            draw_status(draw.canvas,False, True, on_other_key,start_repeat , stop_repeat)
            draw.root.state('normal')
            draw.root.focus_force()
            draw.root.focus_set()
        elif getattr(event, "keysym", "").lower() == str(const.REGENERATION_COMMAND) and const.REGENERATION_HIDEN<=1:
            reynolds.velocities = []
            reynolds.birds= [] 
            generate_points_and_facultative_move(False, False)
            draw_points() 
        elif getattr(event, "keysym", "").lower() == str(const.TOOGLE_FPS_COMMAND) and const.TOOGLE_FPS_HIDEN<=1:
            const.FPS = not const.FPS
            draw_fps(draw.canvas)
        elif getattr(event, "keysym", "").lower() == str(const.TOOGLE_START_PAUSE_COMMAND) and const.TOOGLE_START_PAUSE_HIDEN<=1:
            toggle_pause()
        elif getattr(event, "keysym", "").lower() == str(const.NEXT_FRAME_COMMAND) and const.NEXT_FRAME_HIDEN<=1:
            next_frame()
        elif getattr(event, "keysym", "").lower() == str(const.TOOGLE_MAXIMIZE_COMMAND) and const.TOOGLE_MAXIMIZE_HIDEN<=1:
            maximize_minimize(False)
        elif getattr(event, "keysym", "").lower() == str(const.DOC_COMMAND) and const.DOC_HIDEN<=1:
            help = f"pybirdsreynolds {version_prog}\n\n"+get_help_text()
            popin = tk.Toplevel(draw.canvas)
            popin.title("Documentation - pybirdreynolds")
            popin.transient(draw.canvas.winfo_toplevel())  
            popin.geometry("+200+200")  
            popin.configure(bg="gray") 

            frame = tk.Frame(popin, bg="gray")
            frame.pack(padx=10, pady=10)

            text_widget = tk.Text(
                frame,
                wrap="word",
                width=80,
                height=20,
                bg="gray",
                fg="black",
                insertbackground="black",
                highlightthickness=0,
                bd=0
            )
            text_widget.insert("1.0", help)
            text_widget.config(state="disabled")  
            text_widget.pack(side="left", fill="both", expand=True)

            scrollbar = tk.Scrollbar(frame, command=text_widget.yview)
            scrollbar.pack(side="right", fill="y")
            text_widget.config(yscrollcommand=scrollbar.set)
            popin.wait_visibility()
            popin.grab_set() 


        elif getattr(event, "keysym", "").lower() == str(const.HIDE_COMMAND) and const.HIDE_HIDEN<=1:
            if not const.HIDDEN:
                if is_maximized(draw.root):
                    maximize_minimize(True)
                global trans_hiden
                trans_hiden=True
                const.WIDTH_PARAMS=0
                const.WIDTH_CONTROLS=0
                draw_status(draw.canvas,True, True, on_other_key,start_repeat , stop_repeat)
                generate_points_and_facultative_move(False, True)
                draw_canvas_hiden(draw.root)
                const.HIDDEN=True
                draw_all(draw.canvas, draw.root, on_other_key,start_repeat , stop_repeat)
            else:
                const.WIDTH_PARAMS=const.WIDTH_PARAMS_DEFAULT
                const.WIDTH_CONTROLS=const.WIDTH_CONTROLS_DEFAULT
                if is_maximized(draw.root):
                    const.WIDTH=draw.root.winfo_width()-const.WIDTH_PARAMS-const.WIDTH_CONTROLS
                draw_status(draw.canvas,True, True, on_other_key,start_repeat , stop_repeat)
                generate_points_and_facultative_move(False, True)
                draw_canvas(draw.canvas,draw.root)
                const.HIDDEN=False
                draw_all(draw.canvas, draw.root, on_other_key,start_repeat , stop_repeat)
        draw_status(draw.canvas,False, False, on_other_key,start_repeat , stop_repeat)

    def on_resize(event):
        global trans_hiden
        if trans_hiden:
            const.WIDTH = max(event.width - const.WIDTH_PARAMS - const.WIDTH_CONTROLS,const.WIDTH_MIN)
            const.HEIGHT = max(event.height,const.HEIGHT_PARAMS_CONTROLS_DEFAULT) 
            generate_points_and_facultative_move(False, False)
            draw_points()
            draw_rectangle(draw.canvas, draw.root)
            draw_fps(draw.canvas)
            trans_hiden=False
            return
        #TODO BUGIFX
        const.WIDTH = max(event.width - const.WIDTH_PARAMS - const.WIDTH_CONTROLS -2,const.WIDTH_MIN)
        const.HEIGHT = max(event.height,const.HEIGHT_PARAMS_CONTROLS_DEFAULT) 
        #const.WIDTH = max(event.width - const.WIDTH_PARAMS - const.WIDTH_CONTROLS,const.WIDTH_MIN)
        #const.HEIGHT = max(event.height,const.HEIGHT_PARAMS_CONTROLS_DEFAULT) 
        generate_points_and_facultative_move(False, False)
        draw_status(draw.canvas,False, True, on_other_key,start_repeat , stop_repeat)
        draw_points()
        draw_rectangle(draw.canvas, draw.root)
        draw_fps(draw.canvas)

    def on_click(l, sens):
        first_word = l.split()[0] if l.split() else None
        lines = [
            f"{name.removesuffix('_DOC'):15} :    {str(getattr(const, name.removesuffix('_DOC'))).split(maxsplit=1)[0]}"
            for name in vars(const)
            if name.endswith("_DOC")
            and getattr(const, f"{name[:-4]}_HIDEN", 1) == 0
        ] + [
            f"{name.removesuffix('_TEXT'):15} :    {getattr(const, name)} [{getattr(const, name.replace('_TEXT', '_COMMAND'), '')}]"
            for name in vars(const)
            if name.endswith("_TEXT")
            and getattr(const, f"{name[:-5]}_HIDEN", 1) == 0
        ]
        const.SELECTED_INDEX = next(
            (i for i, line in enumerate(lines) if line.split(":")[0].strip() == first_word),
            0
        )
        on_other_key(types.SimpleNamespace(keysym=sens))

    def next_frame():
        if const.PAUSED:
            generate_points_and_facultative_move(True, False)
            draw_points()

    def signal_handler(sig, frame):
        print("Interrupted! Closing application...")
        draw.root.destroy() 
        sys.exit(0)
            
    def rustine_1():
        #TODO BUGFIX
        draw.root.geometry(f"{const.WIDTH_PARAMS + const.WIDTH +1+ const.WIDTH_CONTROLS}x{max(const.HEIGHT -1, const.HEIGHT_PARAMS_CONTROLS_DEFAULT)}")
        #draw.root.geometry(f"{const.WIDTH_PARAMS + const.WIDTH + const.WIDTH_CONTROLS}x{max(const.HEIGHT , const.HEIGHT_PARAMS_CONTROLS_DEFAULT)}")

    def rustine_2():
        #TODO BUGFIX
        draw.root.geometry(f"{const.WIDTH_PARAMS + const.WIDTH +3+ const.WIDTH_CONTROLS}x{max(const.HEIGHT -3, const.HEIGHT_PARAMS_CONTROLS_DEFAULT)}")
        #draw.root.geometry(f"{const.WIDTH_PARAMS + const.WIDTH + const.WIDTH_CONTROLS}x{max(const.HEIGHT , const.HEIGHT_PARAMS_CONTROLS_DEFAULT)}")

    draw.root = tk.Tk()
    draw.root.title(f"pybirdsreynolds")
    draw.root.minsize(const.WIDTH_PARAMS+ const.WIDTH_MIN+const.WIDTH_CONTROLS, max(const.HEIGHT,const.HEIGHT_PARAMS_CONTROLS_DEFAULT))
    draw.canvas = tk.Canvas(draw.root, width=const.WIDTH_PARAMS+const.WIDTH+const.WIDTH_CONTROLS, height=const.HEIGHT, bg=const.CANVAS_BG)
    draw.canvas.pack(fill="both", expand=True, padx=0, pady=0)
    
    default_fonts = [f for f in const.FONT_TYPE_LIST if f in font.families()] 
    available_fonts = font.families()
    global fonts
    fonts = []
    for f in default_fonts:
        if f not in fonts:
            fonts.append(f)

    if const.FONT_TYPE not in fonts:
        const.FONT_TYPE = fonts[0]  

    generate_points_and_facultative_move(True, False)
    draw_all(draw.canvas, draw.root, on_other_key,start_repeat , stop_repeat)
    draw_status(draw.canvas,True, True, on_other_key,start_repeat , stop_repeat)
    draw_paused(draw.canvas)
    draw.root.bind('p', toggle_pause)
    draw.root.bind("<Key>", on_other_key)
    draw.root.bind_all("<Shift_L>", on_shift_press)
    draw.root.bind_all("<Shift_R>", on_shift_press)
    draw.root.bind_all("<KeyRelease-Shift_L>", on_shift_release)
    draw.root.bind_all("<KeyRelease-Shift_R>", on_shift_release)

    draw.canvas.bind("<Configure>", on_resize)
    
    signal.signal(signal.SIGINT, signal_handler)
    update()
    global last_x, last_y
    last_x = draw.root.winfo_x()
    last_y = draw.root.winfo_y()

    draw.root.after(100, rustine_1)
    draw.root.after(200, rustine_2)
    draw.root.update()
    draw.root.mainloop()           


