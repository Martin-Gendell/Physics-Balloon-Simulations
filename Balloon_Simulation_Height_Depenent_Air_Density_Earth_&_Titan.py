import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, RadioButtons

r_balloon = 5.0
gas_density = 0.18
L = 0.7
g = 9.81
t_end = 7.0
dt = 0.01

def simulate(r_balloon, g, L, gas_density, t_end, dt, planet='titan'):
    C = 0.4
    A = np.pi * r_balloon ** 2
    V = 1.33 * np.pi * r_balloon ** 3
    m = 4 * np.pi * L * r_balloon ** 2 + 1.33 * np.pi * r_balloon ** 3 * gas_density
    t = 0.0
    h = 0.0
    v = 0.0
    t_values = []
    h_values = []
    v_values = []
    a_values = []
    v_terminal_values = []
    while t <= t_end:
        if planet == 'earth':
            rho = 1.225 * (0.999888 ** h)
        else:
            rho = 5.34 * (0.9999683 ** h)

        drag = 0.5 * rho * C * A * v * abs(v)

        a = (g * (rho * V - m) - drag) / m
        v = v + a * dt
        h = h + v * dt

        vt_num = 2 * g * (rho * V - m)
        vt_den = rho * C * A
        v_terminal = np.sqrt(abs(vt_num / vt_den))

        t_values.append(t)
        h_values.append(h)
        v_values.append(v)
        a_values.append(a)
        v_terminal_values.append(v_terminal)
        t += dt
    return np.array(t_values), np.array(h_values), np.array(v_values), np.array(a_values), np.array(v_terminal_values)

t_values, h_values, v_values, a_values, v_terminal_values = simulate(r_balloon, g, L, gas_density, t_end, dt)

fig = plt.figure(figsize=(14, 5))
gs = fig.add_gridspec(1, 3, width_ratios=[1.0, 1.0, 0.35])
ax1 = fig.add_subplot(gs[0, 0])
ax2 = fig.add_subplot(gs[0, 1])
ax3 = fig.add_subplot(gs[0, 2])
plt.subplots_adjust(left=0.06, right=0.98, top=0.93, bottom=0.46, wspace=0.375)

line_v_time, = ax1.plot(t_values, v_values, color="tab:blue", label="Velocity")
ax1.set_xlabel("Time (s)")
ax1.set_ylabel("Velocity (m/s)", color="tab:blue")
ax1.tick_params(axis="y", labelcolor="tab:blue")
ax1.set_title("Velocity vs Time")
ax1b = ax1.twinx()
line_a_time, = ax1b.plot(t_values, a_values, color="tab:red", label="Acceleration")
ax1b.set_ylabel("Acceleration (m/s^2)", color="tab:red")
ax1b.tick_params(axis="y", labelcolor="tab:red")
lines1, labels1 = ax1.get_legend_handles_labels()
lines1b, labels1b = ax1b.get_legend_handles_labels()
ax1.legend(lines1 + lines1b, labels1 + labels1b, loc="best")

line_v_height, = ax2.plot(h_values, v_values, color="tab:blue", label="Velocity")
line_vt_height, = ax2.plot(h_values, v_terminal_values, color="tab:green", linestyle="--", label="Terminal Velocity")
ax2.set_xlabel("Height (m)")
ax2.set_ylabel("Velocity (m/s)", color="tab:blue")
ax2.tick_params(axis="y", labelcolor="tab:blue")
ax2.set_title("Velocity vs Height")
ax2b = ax2.twinx()
line_a_height, = ax2b.plot(h_values, a_values, color="tab:red", label="Acceleration")
ax2b.set_ylabel("Acceleration (m/s^2)", color="tab:red")
ax2b.tick_params(axis="y", labelcolor="tab:red")
lines2, labels2 = ax2.get_legend_handles_labels()
lines2b, labels2b = ax2b.get_legend_handles_labels()
ax2.legend(lines2 + lines2b, labels2 + labels2b, loc="best")

line_h_time, = ax3.plot([], [], color="tab:purple", linewidth=1, label="Height")
ax3.set_xlabel("Time (s)")
ax3.set_ylabel("Height (m)")
ax3.tick_params(axis="y", labelcolor="tab:purple")
ax3.set_title("Height Vs Velocity")

axcolor = "lightgoldenrodyellow"
planet_w = 0.10
planet_h = 0.05
planet_x = 0.5 - planet_w / 2
planet_y = 0.27
ax_planet = plt.axes([planet_x, planet_y, planet_w, planet_h], facecolor=axcolor)
planet_radio = RadioButtons(ax_planet, ("Earth", "Titan"), active=1)

planet_defaults = {
    'earth': {'g': 9.81},
    'titan': {'g': 1.352}
}

def planet_changed(label):
    p = label.lower()
    d = planet_defaults.get(p)
    if d is None:
        return
    try:
        s_g.set_val(d['g'])
    except Exception:
        pass
    update(None)

planet_radio.on_clicked(planet_changed)

slider_x = 0.15
slider_w = 0.70
slider_h = 0.03
gap = 0.01
y0 = 0.03
ax_r = plt.axes([slider_x, y0 + 5*(slider_h+gap), slider_w, slider_h], facecolor=axcolor)
ax_g = plt.axes([slider_x, y0 + 4*(slider_h+gap), slider_w, slider_h], facecolor=axcolor)
ax_L = plt.axes([slider_x, y0 + 3*(slider_h+gap), slider_w, slider_h], facecolor=axcolor)
ax_gas = plt.axes([slider_x, y0 + 2*(slider_h+gap), slider_w, slider_h], facecolor=axcolor)
ax_tend = plt.axes([slider_x, y0 + 1*(slider_h+gap), slider_w, slider_h], facecolor=axcolor)
ax_tend2 = plt.axes([slider_x, y0 + 0*(slider_h+gap), slider_w, slider_h], facecolor=axcolor)
s_r_denom = 1.33 * (1.225 - gas_density)
if s_r_denom <= 0:
    s_r_min = 0.1
else:
    s_r_min = (4.0 * L) / s_r_denom
if s_r_min <= 0:
    s_r_min = 0.1
s_r_max = 30.0
s_r_init = max(r_balloon, s_r_min)
s_r = Slider(ax_r, "Balloon Radius", 0.0, 30.0, valinit=s_r_init, valstep=0.1)
s_g = Slider(ax_g, "Gravity", 1.0, 20.0, valinit=g)
s_L = Slider(ax_L, "Balloon Material Density", 0.01, 5.0, valinit=L, valstep=0.01)
s_gas = Slider(ax_gas, "Balloon Gas Density", 0.01, 1.0, valinit=gas_density, valstep=0.01)
s_tend = Slider(ax_tend, "time end", 1.0, 200.0, valinit=t_end, valstep=0.1)
s_tend_coarse = Slider(ax_tend2, "time end coarse", 100.0, 20000.0, valinit=100.0, valstep=100.0)

vt_time_vline, = ax1.plot([], [], linestyle='--', color='tab:purple', linewidth=1.2)
vt_time_marker, = ax1.plot([], [], marker='o', color='tab:purple')
vt_height_marker, = ax2.plot([], [], marker='o', color='tab:purple')

annot_by_ax = {}

def format_xy(x, y, ax=None):

    def infer_name(label):
        if not label:
            return 'x'
        lab = label.lower()
        if 'time' in lab:
            return 't'
        if 'height' in lab:
            return 'h'
        if 'terminal' in lab:
            return 'vt'
        if 'velocity' in lab:
            return 'v'
        if 'accel' in lab or 'acceleration' in lab:
            return 'a'
        return lab.strip()[0]

    try:
        if ax is not None:
            xlabel = ax.get_xlabel()
            if not xlabel:
                for other in ax.figure.axes:
                    try:
                        if ax.get_shared_x_axes().joined(ax, other):
                            ox = other.get_xlabel()
                            if ox:
                                xlabel = ox
                                break
                    except Exception:
                        pass
            xname = infer_name(xlabel)
            yname = infer_name(ax.get_ylabel())
        else:
            xname, yname = 'x', 'y'
        return f"{xname}={x:.4g}\n{yname}={y:.4g}"
    except Exception:
        return f"x={x}\ny={y}"

def on_motion(event):
    ax = event.inaxes
    if ax is None:
        for a in annot_by_ax.values():
            a.set_visible(False)
        fig.canvas.draw_idle()
        return

    if ax not in annot_by_ax:
        annot = ax.annotate('', xy=(0,0), xytext=(15,15), textcoords='offset points',
                            bbox=dict(boxstyle='round', fc='w'), fontsize=8)
        annot.set_visible(False)
        annot_by_ax[ax] = annot
    else:
        annot = annot_by_ax[ax]

    lines = [ln for ln in ax.get_lines() if ln.get_xdata().size]
    if not lines:
        annot.set_visible(False)
        fig.canvas.draw_idle()
        return

    min_dist = float('inf')
    nearest = None
    ex, ey = event.x, event.y

    axes_under = [a for a in fig.axes if a.bbox.contains(ex, ey)]
    all_lines = []
    for a in axes_under:
        all_lines.extend([ln for ln in a.get_lines() if np.asarray(ln.get_xdata()).size])

    for ln in all_lines:
        xdata = np.asarray(ln.get_xdata())
        ydata = np.asarray(ln.get_ydata())
        if xdata.size == 0:
            continue
        idx = 0
        if event.xdata is not None:
            try:
                idx = np.abs(xdata - event.xdata).argmin()
            except Exception:
                idx = 0
        xd, yd = xdata[idx], ydata[idx]
        disp = ln.axes.transData.transform((xd, yd))
        dx = disp[0] - ex
        dy = disp[1] - ey
        dist = (dx*dx + dy*dy) ** 0.5
        if dist < min_dist:
            min_dist = dist
            nearest = (ln, xd, yd)

    PIXEL_THRESHOLD = 25
    if nearest is not None and min_dist < PIXEL_THRESHOLD:
        ln, xd, yd = nearest
        label = ln.get_label() if ln.get_label() else 'line'
        target_ax = ln.axes
        if target_ax not in annot_by_ax:
            annot = target_ax.annotate('', xy=(0,0), xytext=(15,15), textcoords='offset points',
                                      bbox=dict(boxstyle='round', fc='w'), fontsize=8)
            annot.set_visible(False)
            annot_by_ax[target_ax] = annot
        else:
            annot = annot_by_ax[target_ax]
        annot.xy = (xd, yd)
        annot.set_text(f"{label}\n" + format_xy(xd, yd, ax=target_ax))
        annot.get_bbox_patch().set_alpha(0.9)
        annot.set_visible(True)
        for a, aa in annot_by_ax.items():
            if a is not target_ax:
                aa.set_visible(False)
    else:
        for a in annot_by_ax.values():
            a.set_visible(False)

    fig.canvas.draw_idle()

fig.canvas.mpl_connect('motion_notify_event', on_motion)

def find_vt_crossing(t_vals, h_vals, v_vals, vt_vals):
    diff = v_vals - vt_vals
    idxs = np.where(np.isclose(v_vals, vt_vals, rtol=1e-3, atol=1e-3))[0]
    if idxs.size:
        return idxs[0]
    signs = np.sign(diff)
    change = np.where(signs[1:] != signs[:-1])[0]
    if change.size:
        return change[0] + 1
    return None

def update(val):
    r = s_r.val
    gg = s_g.val
    LL = s_L.val
    gas = s_gas.val
    T = s_tend.val
    planet_choice = planet_radio.value_selected.lower() if 'planet_radio' in globals() else 'titan'
    t_vals, h_vals, v_vals, a_vals, vt_vals = simulate(r, gg, LL, gas, T, dt, planet=planet_choice)
    line_v_time.set_data(t_vals, v_vals)
    line_a_time.set_data(t_vals, a_vals)
    ax1.set_xlim(t_vals.min(), t_vals.max())
    ymin = min(v_vals.min(), 0)
    ymax = v_vals.max() + 2
    ax1.set_ylim(ymin, ymax)
    line_v_height.set_data(h_vals, v_vals)
    line_vt_height.set_data(h_vals, vt_vals)
    line_a_height.set_data(h_vals, a_vals)
    ax2.set_xlim(min(h_vals.min(), 0), h_vals.max())
    ymin2 = min(v_vals.min(), vt_vals.min(), 0)
    ymax2 = max(v_vals.max(), vt_vals.max()) + 2
    ax2.set_ylim(ymin2, ymax2)
    idx = find_vt_crossing(t_vals, h_vals, v_vals, vt_vals)
    if idx is not None:
        t_cross = t_vals[idx]
        h_cross = h_vals[idx]
        v_cross = v_vals[idx]
        ymin, ymax = ax1.get_ylim()
        vt_time_vline.set_data([t_cross, t_cross], [ymin, ymax])
        vt_time_marker.set_data([t_cross], [v_cross])
        vt_height_marker.set_data([h_cross], [v_cross])
    else:
        vt_time_vline.set_data([], [])
        vt_time_marker.set_data([], [])
        vt_height_marker.set_data([], [])
    line_h_time.set_data(t_vals, h_vals)
    if t_vals.size:
        ax3.set_xlim(t_vals.min(), t_vals.max())
    if h_vals.size:
        ax3.set_ylim(min(h_vals.min(), 0), h_vals.max() + 2)
    fig.canvas.draw_idle()

s_r.on_changed(update)
s_g.on_changed(update)
s_L.on_changed(update)
s_gas.on_changed(update)
s_tend.on_changed(update)

def coarse_changed(val):
    s_tend.set_val(val)

s_tend_coarse.on_changed(coarse_changed)

update(None)

plt.show()