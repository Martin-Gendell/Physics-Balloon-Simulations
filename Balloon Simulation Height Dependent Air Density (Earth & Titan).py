import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, RadioButtons

r_balloon = 5.0
gas_density = 0.18
L = 0.7
g = 1.352
t_end = 7.0
dt = 0.01
payload_mass = 0
payload_density = 100


def simulate(r_balloon, g, L, gas_density, t_end, dt, payload_mass=0, payload_density=500.0, planet="titan"):
    C = 0.4
    A = np.pi * r_balloon ** 2
    V_balloon = 1.33 * np.pi * r_balloon ** 3
    V_payload = payload_mass / payload_density if payload_density > 0 else 0.0
    V = V_balloon + V_payload
    m_balloon = 4 * np.pi * L * r_balloon ** 2 + 1.33 * np.pi * r_balloon ** 3 * gas_density
    m = m_balloon + payload_mass

    t = 0.0
    h = 0.0
    v = 0.0

    t_values = []
    h_values = []
    v_values = []
    a_values = []
    v_terminal_values = []

    while t <= t_end:
        if planet == "earth":
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

    return (
        np.array(t_values),
        np.array(h_values),
        np.array(v_values),
        np.array(a_values),
        np.array(v_terminal_values),
        V_balloon,
        V_payload,
        m_balloon,
    )


t_values, h_values, v_values, a_values, v_terminal_values, V_balloon0, V_payload0, m_balloon0 = simulate(
    r_balloon, g, L, gas_density, t_end, dt, payload_mass, payload_density
)

fig = plt.figure(figsize=(14, 5))
gs = fig.add_gridspec(1, 3, width_ratios=[1.0, 1.0, 0.35])
ax1 = fig.add_subplot(gs[0, 0])
ax2 = fig.add_subplot(gs[0, 1])
ax3 = fig.add_subplot(gs[0, 2])
plt.subplots_adjust(left=0.06, right=0.98, top=0.93, bottom=0.52, wspace=0.375)

(line_v_time,) = ax1.plot(t_values, v_values, color="tab:blue", label="Velocity")
ax1.set_xlabel("Time (s)")
ax1.set_ylabel("Velocity (m/s)", color="tab:blue")
ax1.tick_params(axis="y", labelcolor="tab:blue")
ax1.set_title("Velocity vs Time")

ax1b = ax1.twinx()
(line_a_time,) = ax1b.plot(t_values, a_values, color="tab:red", label="Acceleration")
ax1b.set_ylabel("Acceleration (m/s^2)", color="tab:red")
ax1b.tick_params(axis="y", labelcolor="tab:red")

lines1, labels1 = ax1.get_legend_handles_labels()
lines1b, labels1b = ax1b.get_legend_handles_labels()
ax1.legend(lines1 + lines1b, labels1 + labels1b, loc="best")

(line_v_height,) = ax2.plot(h_values, v_values, color="tab:blue", label="Velocity")
(line_vt_height,) = ax2.plot(
    h_values, v_terminal_values, color="tab:green", linestyle="--", label="Terminal Velocity"
)
ax2.set_xlabel("Height (m)")
ax2.set_ylabel("Velocity (m/s)", color="tab:blue")
ax2.tick_params(axis="y", labelcolor="tab:blue")
ax2.set_title("Velocity vs Height")

ax2b = ax2.twinx()
(line_a_height,) = ax2b.plot(h_values, a_values, color="tab:red", label="Acceleration")
ax2b.set_ylabel("Acceleration (m/s^2)", color="tab:red")
ax2b.tick_params(axis="y", labelcolor="tab:red")

lines2, labels2 = ax2.get_legend_handles_labels()
lines2b, labels2b = ax2b.get_legend_handles_labels()
ax2.legend(lines2 + lines2b, labels2 + labels2b, loc="best")

(line_h_time,) = ax3.plot([], [], color="tab:purple", linewidth=1, label="Height")
ax3.set_xlabel("Time (s)")
ax3.set_ylabel("Height (m)")
ax3.tick_params(axis="y", labelcolor="tab:purple")
ax3.set_title("Height Vs Time")

axcolor = "lightgoldenrodyellow"

box_y = 0.355
box_h = 0.088
box_gap = 0.01
info_w = 0.42
planet_w = 0.07
mass_w = 0.42
info_x = (1.0 - info_w - box_gap - planet_w - box_gap - mass_w) / 2
planet_x = info_x + info_w + box_gap
mass_x = planet_x + planet_w + box_gap

ax_info = plt.axes([info_x, box_y, info_w, box_h], facecolor="#f0f4ff")
ax_info.set_xticks([])
ax_info.set_yticks([])
for spine in ax_info.spines.values():
    spine.set_edgecolor("#aaaacc")
    spine.set_linewidth(1.2)

info_text = ax_info.text(
    0.5, 0.5, "",
    transform=ax_info.transAxes,
    ha="center", va="center",
    fontsize=11,
    linespacing=1.5,
    color="#111133",
)

ax_planet = plt.axes([planet_x, box_y, planet_w, box_h], facecolor=axcolor)
planet_radio = RadioButtons(ax_planet, ("Earth", "Titan"), active=1)
for lbl in planet_radio.labels:
    lbl.set_ha("center")
    lbl.set_position((0.55, lbl.get_position()[1]))

ax_mass = plt.axes([mass_x, box_y, mass_w, box_h], facecolor="#f0fff4")
ax_mass.set_xticks([])
ax_mass.set_yticks([])
for spine in ax_mass.spines.values():
    spine.set_edgecolor("#aaccaa")
    spine.set_linewidth(1.2)

mass_text = ax_mass.text(
    0.5, 0.5, "",
    transform=ax_mass.transAxes,
    ha="center", va="center",
    fontsize=11,
    linespacing=1.5,
    color="#113311",
)

planet_defaults = {
    "earth": {"g": 9.81},
    "titan": {"g": 1.352},
}


def planet_changed(label):
    p = label.lower()
    d = planet_defaults.get(p)
    if d is None:
        return
    try:
        s_g.set_val(d["g"])
    except Exception:
        pass
    update(None)


planet_radio.on_clicked(planet_changed)

slider_x = 0.15
slider_w = 0.70
slider_h = 0.03
gap = 0.01
y0 = 0.03

ax_r = plt.axes([slider_x, y0 + 7 * (slider_h + gap), slider_w, slider_h], facecolor=axcolor)
ax_g = plt.axes([slider_x, y0 + 6 * (slider_h + gap), slider_w, slider_h], facecolor=axcolor)
ax_L = plt.axes([slider_x, y0 + 5 * (slider_h + gap), slider_w, slider_h], facecolor=axcolor)
ax_gas = plt.axes([slider_x, y0 + 4 * (slider_h + gap), slider_w, slider_h], facecolor=axcolor)
ax_payload = plt.axes([slider_x, y0 + 3 * (slider_h + gap), slider_w, slider_h], facecolor=axcolor)
ax_payload_density = plt.axes([slider_x, y0 + 2 * (slider_h + gap), slider_w, slider_h], facecolor=axcolor)
ax_tend = plt.axes([slider_x, y0 + 1 * (slider_h + gap), slider_w, slider_h], facecolor=axcolor)
ax_tend2 = plt.axes([slider_x, y0 + 0 * (slider_h + gap), slider_w, slider_h], facecolor=axcolor)

s_r_denom = 1.33 * (1.225 - gas_density)
s_r_min = (4.0 * L) / s_r_denom if s_r_denom > 0 else 0.1
s_r_min = max(s_r_min, 0.1)
s_r_init = max(r_balloon, s_r_min)

s_r = Slider(ax_r, "Balloon Radius", 0.0, 30.0, valinit=s_r_init, valstep=0.1)
s_g = Slider(ax_g, "Gravity", 1.0, 20.0, valinit=g)
s_L = Slider(ax_L, "Balloon Material Density", 0.01, 5.0, valinit=L, valstep=0.01)
s_gas = Slider(ax_gas, "Balloon Gas Density", 0.01, 1.0, valinit=gas_density, valstep=0.01)
s_payload = Slider(ax_payload, "Payload Mass (kg)", 0.0, 500.0, valinit=payload_mass, valstep=0.5)
s_payload_density = Slider(ax_payload_density, "Payload Density (kg/m3)", 1.0, 5000.0, valinit=payload_density, valstep=1.0)
s_tend = Slider(ax_tend, "Time End", 1.0, 200.0, valinit=t_end, valstep=0.1)
s_tend_coarse = Slider(ax_tend2, "Time End Coarse", 100.0, 20000.0, valinit=100.0, valstep=100.0)

(vt_time_vline,) = ax1.plot([], [], linestyle="--", color="tab:purple", linewidth=1.2)
(vt_time_marker,) = ax1.plot([], [], marker="o", color="tab:purple")
(vt_height_marker,) = ax2.plot([], [], marker="o", color="tab:purple")

annot_by_ax = {}

def format_xy(x, y, ax=None):
    def infer_name(label):
        if not label:
            return "x"
        lab = label.lower()
        if "time" in lab:
            return "t"
        if "height" in lab:
            return "h"
        if "terminal" in lab:
            return "vt"
        if "velocity" in lab:
            return "v"
        if "accel" in lab or "acceleration" in lab:
            return "a"
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
            xname, yname = "x", "y"
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
        annot = ax.annotate(
            "",
            xy=(0, 0),
            xytext=(15, 15),
            textcoords="offset points",
            bbox=dict(boxstyle="round", fc="w"),
            fontsize=8,
        )
        annot.set_visible(False)
        annot_by_ax[ax] = annot
    else:
        annot = annot_by_ax[ax]

    lines = [ln for ln in ax.get_lines() if ln.get_xdata().size]
    if not lines:
        annot.set_visible(False)
        fig.canvas.draw_idle()
        return

    min_dist = float("inf")
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
        dist = (dx * dx + dy * dy) ** 0.5
        if dist < min_dist:
            min_dist = dist
            nearest = (ln, xd, yd)

    PIXEL_THRESHOLD = 25
    if nearest is not None and min_dist < PIXEL_THRESHOLD:
        ln, xd, yd = nearest
        label = ln.get_label() if ln.get_label() else "line"
        target_ax = ln.axes
        if target_ax not in annot_by_ax:
            annot = target_ax.annotate(
                "",
                xy=(0, 0),
                xytext=(15, 15),
                textcoords="offset points",
                bbox=dict(boxstyle="round", fc="w"),
                fontsize=8,
            )
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

fig.canvas.mpl_connect("motion_notify_event", on_motion)

def find_vt_crossing(t_vals, h_vals, v_vals, vt_vals):
    idxs = np.where(np.isclose(v_vals, vt_vals, rtol=1e-3, atol=1e-3))[0]
    if idxs.size:
        return idxs[0]
    signs = np.sign(v_vals - vt_vals)
    change = np.where(signs[1:] != signs[:-1])[0]
    if change.size:
        return change[0] + 1
    return None

def compute_stats(t_vals, h_vals, v_vals, vt_vals):
    vt_idx = find_vt_crossing(t_vals, h_vals, v_vals, vt_vals)

    if vt_idx is not None:
        t_vt = t_vals[vt_idx]
        h_vt = h_vals[vt_idx]
    else:
        t_vt = None
        h_vt = None

    zero_crossings = np.where(np.diff(np.sign(v_vals)))[0]
    if zero_crossings.size:
        first_zero_idx = zero_crossings[0] + 1
        t_zero = t_vals[first_zero_idx]
        h_zero = h_vals[first_zero_idx]
    else:
        t_zero = None
        h_zero = None

    if zero_crossings.size >= 2:
        start = zero_crossings[-2]
        end = zero_crossings[-1] + 1
        h_tail = h_vals[start:end]
        if h_tail.size > 0:
            resting_h = np.mean(h_tail)
            amplitude = (np.max(h_tail) - np.min(h_tail)) / 2.0
        else:
            resting_h = None
            amplitude = None
    elif zero_crossings.size == 0 and v_vals[-1] > 0:
        resting_h = None
        amplitude = None
    else:
        resting_h = None
        amplitude = None

    return t_vt, h_vt, t_zero, h_zero, resting_h, amplitude

def build_info_text(t_vt, h_vt, t_zero, h_zero, resting_h, amplitude):
    def fmt(val, unit):
        return f"{val:.1f} {unit}" if val is not None else "N/A (extend time)"

    line1 = f"Time until v = vt :  {fmt(t_vt, 's')}    Height at v = vt :  {fmt(h_vt, 'm')}"
    line2 = f"Time until v = 0  :  {fmt(t_zero, 's')}    Height at v = 0  :  {fmt(h_zero, 'm')}"
    if resting_h is not None and amplitude is not None:
        line3 = f"Resting height    :  {resting_h:.1f} m  +-  {amplitude:.3f} m  (amplitude)"
    else:
        line3 = "Resting height    :  N/A (extend time or balloon still rising)"
    return f"{line1}\n{line2}\n{line3}"

def build_mass_text(V_balloon, V_payload, m_balloon, payload_mass):
    line1 = f"Balloon  Volume: {V_balloon:.2f} m^3    Mass: {m_balloon:.2f} kg"
    line2 = f"Payload  Volume: {V_payload:.3f} m^3    Mass: {payload_mass:.1f} kg"
    return f"{line1}\n{line2}"

def update(val):
    r = s_r.val
    gg = s_g.val
    LL = s_L.val
    gas = s_gas.val
    pm = s_payload.val
    pd = s_payload_density.val
    T = s_tend.val
    planet_choice = (
        planet_radio.value_selected.lower() if "planet_radio" in globals() else "titan"
    )

    t_vals, h_vals, v_vals, a_vals, vt_vals, V_balloon, V_payload, m_balloon = simulate(
        r, gg, LL, gas, T, dt, payload_mass=pm, payload_density=pd, planet=planet_choice
    )

    line_v_time.set_data(t_vals, v_vals)
    line_a_time.set_data(t_vals, a_vals)
    ax1.set_xlim(t_vals.min(), t_vals.max())
    ax1.set_ylim(min(v_vals.min(), 0), v_vals.max() + 2)

    line_v_height.set_data(h_vals, v_vals)
    line_vt_height.set_data(h_vals, vt_vals)
    line_a_height.set_data(h_vals, a_vals)
    ax2.set_xlim(min(h_vals.min(), 0), h_vals.max())
    ax2.set_ylim(min(v_vals.min(), vt_vals.min(), 0), max(v_vals.max(), vt_vals.max()) + 2)

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

    t_vt, h_vt, t_zero, h_zero, resting_h, amplitude = compute_stats(t_vals, h_vals, v_vals, vt_vals)
    info_text.set_text(build_info_text(t_vt, h_vt, t_zero, h_zero, resting_h, amplitude))
    mass_text.set_text(build_mass_text(V_balloon, V_payload, m_balloon, pm))

    fig.canvas.draw_idle()

s_r.on_changed(update)
s_g.on_changed(update)
s_L.on_changed(update)
s_gas.on_changed(update)
s_payload.on_changed(update)
s_payload_density.on_changed(update)
s_tend.on_changed(update)

def coarse_changed(val):
    s_tend.set_val(val)

s_tend_coarse.on_changed(coarse_changed)

update(None)
plt.show()