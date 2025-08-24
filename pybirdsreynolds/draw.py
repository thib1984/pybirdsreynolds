import pybirdsreynolds.const as const
import pybirdsreynolds.reynolds as reynolds
import tkinter as tk
import math
from tkinter import font
from pybirdsreynolds.reynolds import generate_points_and_facultative_move
from pybirdsreynolds.args import compute_args, display_range, get_description, get_epilog, get_help_text
import types
import time

frame_count = 0
fps_value = 0
root = None
tip_window = None
canvas=None
point_ids = []

def update():
    update_tmp(canvas, root)

def update_tmp(pcanvas, proot):
    global frame_count, last_time, count, fps_value
    if not const.PAUSED:
        generate_points_and_facultative_move(True, False)
        draw_points()
        draw_fps(pcanvas)
        frame_count += 1
        now = time.time()
        if not count:
            last_time = now
            count = True
        #add delay to stabilize fps    
        if now - last_time >= 1.0: 
            fps_value = frame_count / (now - last_time)
            frame_count = 0
            last_time = now 
    #reset fps        
    else:
        frame_count = 0
        count = False
        fps_value = 0          

    proot.after(const.REFRESH_MS, update)

def draw_all(pcanvas, proot, on_other_key,start_repeat , stop_repeat):
    draw_status(pcanvas,False, False, on_other_key,start_repeat , stop_repeat)
    draw_points()
    draw_rectangle(pcanvas, proot)
    draw_fps(pcanvas)
    draw_hidden(pcanvas)

def draw_status(pcanvas, fullRefreshParams, fullRefreshControls, on_other_key,start_repeat , stop_repeat):
    global start_button, refresh_button, generation_button
    # récupérer toutes les variables _DEFAULT dans const
    base_globals = [
        var_name[:-8]  # enlever le "_DEFAULT"
        for var_name in vars(const)
        if var_name.endswith("_DEFAULT")
    ]


    normal_font = font.Font(family=const.FONT_TYPE, size=const.FONT_SIZE, weight="normal")
    bold_font   = font.Font(family=const.FONT_TYPE, size=const.FONT_SIZE, weight="bold")
    italic_font = font.Font(family=const.FONT_TYPE, size=const.FONT_SIZE, slant="italic")

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
    x_text = 10
    y_text = 10
    pcanvas.delete("controls")
    pcanvas.delete("params")
    if const.WIDTH_PARAMS==0 and const.WIDTH_CONTROLS==0:
        pcanvas.delete("params_button")
        pcanvas.delete("controls_button")
        for name in dir(const):
            if name.endswith(("_BUTTON", "_BUTTON_UP", "_BUTTON_DOWN")):
                setattr(const, name, None)
        return 

    i_param=-1
    i_control=-1 
    y_pos_control=0 
    for i, line in enumerate(lines):
        key = line.split()[0]
        font_to_use = normal_font
        fill = const.FILL_COLOR

        if i == const.SELECTED_INDEX and const.ARROWS_HIDEN<2:
            i_param=i_param+1
            fill = "red"
            item= pcanvas.create_text(
                x_text +  const.WIDTH_CONTROLS + const.WIDTH,
                y_text + i_param * 2.3 * const.FONT_SIZE,
                anchor="nw",
                fill=fill,
                font=font_to_use,
                tags="params",
                text=line.lower(),
            )
            add_canvas_tooltip(
                item,
                getattr(const, key.upper() + "_DOC") + " (" + display_range(key.upper()) + ")")
        elif "[" in line:
            i_control=i_control+1
        elif not "[" in line:    
            i_param=i_param+1               
            item = pcanvas.create_text(
                x_text  +  const.WIDTH_CONTROLS + const.WIDTH,
                y_text + i_param * 2.3 * const.FONT_SIZE,
                anchor="nw",
                fill=const.FILL_COLOR,
                font=font_to_use,
                tags="params",
                text=line.lower(),
            )
            add_canvas_tooltip(
                item,
                getattr(const, key.upper() + "_DOC") + " (" + display_range(key.upper()) + ")"
)

        y_pos_control = y_text + i_control * 2.1 * 2 * const.FONT_SIZE
        y_pos_param = y_text + i_param * 2.3 * const.FONT_SIZE
        
        
        if fullRefreshControls:         
            first_colon_index = line.find(":") + 1 
            f = font.Font(font=font_to_use)
            x_offset = 0
            if "[" in line:
                key = line.split()[0]
                btn_font = (const.FONT_TYPE, const.FONT_SIZE*2)
                btn_width = 2
                btn_height = 1
                highlight_color = "black"
                highlight_thickness = 2

                name_button = key + "_BUTTON"
                key = line.split()[0]
                icon = getattr(const, key.upper() + "_ICON")
                cmd  = getattr(const, key.upper() + "_COMMAND")

                lbl_btn_tmp = tk.Label(
                    pcanvas, text=icon, fg="black", bg="white",
                    font=btn_font, width=btn_width, height=btn_height, anchor="center",
                    highlightbackground=highlight_color, highlightthickness=highlight_thickness
                )

                tooltip_text = f"{getattr(const, key.upper() + '_TEXT')} [{getattr(const, key.upper() + '_COMMAND')}]"
                add_widget_tooltip(lbl_btn_tmp, tooltip_text)

                lbl_btn_tmp.bind("<Button-1>", lambda e, c=cmd: on_other_key(types.SimpleNamespace(keysym=c)))

                # Création du bouton
                if getattr(const, name_button, None) is None:
                    setattr(
                        const,
                        name_button,
                        pcanvas.create_window(
                            x_text + x_offset + 2,
                            y_pos_control,
                            anchor="nw",
                            window=lbl_btn_tmp,
                            tags=("controls_button",)
                        )
                    )
                else:
                    pcanvas.coords(
                        getattr(const, name_button),
                        x_text + x_offset + 2,
                        y_pos_control
                    )

            first_colon_index = line.find(":") + 1 
            f = font.Font(font=font_to_use)
            x_offset = f.measure(line[:first_colon_index])
            if "[" not in line and const.ARROWS_HIDEN<2:
                highlight_color = "black"
                highlight_thickness = 1                    
                name_button_up=key+"_BUTTON_UP"
                name_button_down=key+"_BUTTON_DOWN"
                lbl_left = tk.Label(pcanvas, text="<", fg="black", bg="white", font=font_to_use , highlightbackground=highlight_color, highlightthickness=highlight_thickness)
                lbl_left.bind("<ButtonPress-1>", lambda e, l=line: start_repeat(l, "Left"))
                lbl_left.bind("<ButtonRelease-1>", lambda e: stop_repeat())                                  
                if not hasattr(const, name_button_down) or getattr(const, name_button_down) is None: 
                    setattr(
                        const,
                        name_button_down,
                        pcanvas.create_window(
                            x_text + x_offset + 1 + const.WIDTH_CONTROLS + const.WIDTH,
                            y_pos_param,
                            anchor="nw",
                            window=lbl_left,
                            tags=("params_button",)
                        )
                    )

                else:
                    pcanvas.coords(getattr(const, name_button_down), x_text + x_offset + 1 + const.WIDTH_CONTROLS + const.WIDTH, y_pos_param)
                lbl_right = tk.Label(pcanvas, text=">", fg="black", bg="white", font=font_to_use , highlightbackground=highlight_color, highlightthickness=highlight_thickness)
                lbl_right.bind("<ButtonPress-1>", lambda e, l=line: start_repeat(l, "Right"))
                lbl_right.bind("<ButtonRelease-1>", lambda e: stop_repeat()) 
                if not hasattr(const, name_button_up) or getattr(const, name_button_up) is None: 
                    setattr(
                        const,
                        name_button_up,
                        pcanvas.create_window(
                            x_text + x_offset + 18 + const.WIDTH_CONTROLS + const.WIDTH,
                            y_pos_param,
                            anchor="nw",
                            window=lbl_right,
                            tags=("params_button",)
                        )
                    )
                else:
                    pcanvas.coords(getattr(const, name_button_up), x_text + x_offset + 18 + const.WIDTH_CONTROLS + const.WIDTH, y_pos_param)


def draw_paused(pcanvas):
    pcanvas.delete("paused")
    if const.PAUSED:
        if const.BLINK_STATE:
            pcanvas.create_text(
                const.WIDTH_CONTROLS,
                max(const.HEIGHT, const.HEIGHT_PARAMS_CONTROLS_DEFAULT),
                anchor="sw",
                fill="red",
                font=(const.FONT_TYPE, const.FONT_SIZE, "bold"),
                tags="paused",
                text=" PAUSED "
            )
        const.BLINK_STATE = not const.BLINK_STATE
        pcanvas.after(500, lambda: draw_paused(pcanvas))

def draw_fps(pcanvas):
    global fps_value
    pcanvas.delete("fps")
    if const.FPS:
        if not const.PAUSED:
            if fps_value == 0:
                value="..."
            else:    
                value = f"{fps_value:.1f}"
        else:
            value = "NA"
        pcanvas.create_text(
            const.WIDTH_CONTROLS,
            0,            
            anchor="nw",  
            fill="yellow",
            font=(const.FONT_TYPE, const.FONT_SIZE, "bold"),
            tags="fps",
            text=f" FPS : {value}"
    ) 

def draw_hidden(pcanvas):
    pcanvas.delete("hidden")
    if const.HIDDEN:
        pcanvas.create_text(
            const.WIDTH_CONTROLS+const.WIDTH,
            max(const.HEIGHT, const.HEIGHT_PARAMS_CONTROLS_DEFAULT),
            anchor="se",
            fill="gray",
            font=(const.FONT_TYPE, const.FONT_SIZE), 
            tags="hidden",
            text="h to restore panels "
        )           

def draw_rectangle(pcanvas, proot):
    if not is_maximized(proot):
        global width_before_maximized
        global heigth_before_maximized  
        width_before_maximized=const.WIDTH 
        heigth_before_maximized=const.HEIGHT         
    pcanvas.delete("boundary")
    pcanvas.create_rectangle(
        const.WIDTH_CONTROLS, 0, const.WIDTH_CONTROLS + const.WIDTH, const.HEIGHT,
        outline=const.FILL_COLOR, width=const.MARGIN,
        tags="boundary"
    )        

def draw_canvas_hiden(proot):
    #TODO BUG FIX
    #proot.geometry(f"{const.WIDTH+2}x{max(const.HEIGHT, const.HEIGHT_PARAMS_CONTROLS_DEFAULT)}")
    #proot.minsize(const.WIDTH+2, const.HEIGHT)
    #proot.maxsize(const.WIDTH+2, const.HEIGHT)
    proot.geometry(f"{const.WIDTH}x{max(const.HEIGHT, const.HEIGHT_PARAMS_CONTROLS_DEFAULT)}")
    proot.minsize(const.WIDTH, const.HEIGHT)
    proot.maxsize(const.WIDTH, const.HEIGHT)
    width_tmp=const.WIDTH
    height_tmp=const.HEIGHT        
    proot.update()
    proot.minsize(const.WIDTH_MIN, const.HEIGHT_MIN)
    proot.maxsize(10000, 10000)
    proot.update()
    const.WIDTH=width_tmp
    const.HEIGHT=height_tmp       
    return

def draw_canvas(pcanvas, proot):
    proot.geometry(f"{const.WIDTH_PARAMS+const.WIDTH+const.WIDTH_CONTROLS+2}x{max(const.HEIGHT, const.HEIGHT_PARAMS_CONTROLS_DEFAULT)}")
    pcanvas.config(width=const.WIDTH_PARAMS+const.WIDTH+const.WIDTH_CONTROLS+2, height=max(const.HEIGHT,const.HEIGHT_PARAMS_CONTROLS_DEFAULT), bg=const.CANVAS_BG)


def is_maximized(proot):
    if proot.tk.call('tk', 'windowingsystem') == 'aqua':
        return bool(proot.attributes("-fullscreen"))
    if proot.state() == "zoomed":
        return True
    try:
        if proot.attributes('-zoomed'):
            return True
    except tk.TclError:
        pass
    return (
        proot.winfo_width() >= proot.winfo_screenwidth() and
        proot.winfo_height() >= proot.winfo_screenheight()
    )

def draw_points():
    global point_ids
    for pid in point_ids:
        canvas.delete(pid)
    point_ids.clear()

    triangle_size = 6*const.SIZE
    triangle_width = 4*const.SIZE
    for (x, y), (vx, vy) in zip(reynolds.birds, reynolds.velocities):
        if not const.TRIANGLES: 
            pid = canvas.create_oval(
                x - const.SIZE, y - const.SIZE,
                x + const.SIZE, y + const.SIZE,
                fill=const.FILL_COLOR, outline=const.OUTLINE_COLOR)
        else:
            angle = math.atan2(vy, vx)
            tip_x = x + math.cos(angle) * triangle_size
            tip_y = y + math.sin(angle) * triangle_size
            left_angle = angle + math.radians(150)
            right_angle = angle - math.radians(150)

            left_x = x + math.cos(left_angle) * triangle_width
            left_y = y + math.sin(left_angle) * triangle_width

            right_x = x + math.cos(right_angle) * triangle_width
            right_y = y + math.sin(right_angle) * triangle_width

            pid = canvas.create_polygon(
                tip_x, tip_y,
                left_x, left_y,
                right_x, right_y,
                fill=const.FILL_COLOR, outline=const.OUTLINE_COLOR
            )
        point_ids.append(pid) 

def maximize_minimize(force):
    global width_before_maximized
    global heigth_before_maximized
    if is_maximized(root):
        root.state("normal")
        try:
            root.attributes('-zoomed', False)
        except tk.TclError:
            pass
        if not force:
            const.WIDTH=width_before_maximized
            const.HEIGHT=heigth_before_maximized
    else:
        width_before_maximized=const.WIDTH 
        heigth_before_maximized=const.HEIGHT          

        wm = root.tk.call('tk', 'windowingsystem')
        if wm == 'aqua':  # macOS
            root.attributes("-fullscreen", True)
        elif wm == 'win32':  # Windows
            root.state("zoomed")
        else:  # Linux
            try:
                root.attributes('-zoomed', True)
            except tk.TclError:
                root.attributes("-fullscreen", True)
    root.focus_force()
    root.focus_set() 

def show_tip(widget, text, event=None, dx=10, dy=10, wraplength=200):
    global tip_window

    # Si un tooltip est déjà affiché → le détruire
    if tip_window is not None:
        try:
            tip_window.destroy()
        except:
            pass
        tip_window = None

    if not text:
        return

    # Position du tooltip
    if event:  # cas des événements <Enter> sur un Canvas
        x = widget.winfo_rootx() + event.x + dx
        y = widget.winfo_rooty() + event.y + dy
    else:  # cas d’un widget normal
        x = widget.winfo_rootx() + dx
        y = widget.winfo_rooty() + widget.winfo_height() + dy

    tip_window = tw = tk.Toplevel(widget)
    tw.wm_overrideredirect(True)
    tw.wm_geometry(f"+{x}+{y}")
    label = tk.Label(
        tw,
        text=text,
        background="yellow",
        relief="solid",
        borderwidth=1,
        font=(const.FONT_TYPE, const.FONT_SIZE),
        wraplength=wraplength
    )
    label.pack(ipadx=4, ipady=2)

def hide_tip(event=None):
    global tip_window
    if tip_window:
        tip_window.destroy()
        tip_window = None

def add_canvas_tooltip(item, text):
    canvas.tag_bind(item, "<Enter>", lambda e: show_tip(canvas, text, e))
    canvas.tag_bind(item, "<Leave>", hide_tip)

def add_widget_tooltip(widget, text):
    widget.bind("<Enter>", lambda e: show_tip(widget, text))
    widget.bind("<Leave>", hide_tip)             