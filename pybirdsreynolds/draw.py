import pybirdsreynolds.const as const
import tkinter as tk


canvas=None

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

def draw_fps(pcanvas, fps_value):
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
    proot.geometry(f"{const.WIDTH+2}x{max(const.HEIGHT, const.HEIGHT_PARAMS_CONTROLS_DEFAULT)}")
    proot.minsize(const.WIDTH+2, const.HEIGHT)
    proot.maxsize(const.WIDTH+2, const.HEIGHT)
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