# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "marimo>=0.13",
#     "numpy",
#     "matplotlib",
#     "scipy",
#     "wigglystuff",
# ]
# ///

import marimo

__generated_with = "0.23.5"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _imports():
    import marimo as mo
    import numpy as np
    import matplotlib.pyplot as plt
    from wigglystuff import ChartPuck


    return ChartPuck, mo, np, plt


@app.cell(hide_code=True)
def _title(mo):
    mo.md(r"""
    # GSD by direct manipulation

    Drag the **purple pucks** to shape the cumulative grain-size distribution. Each puck sits over a sieve;
    the curve is a piecewise-linear interpolation through the puck positions plus the two pinned
    black anchors (0% at the smallest sieve, 100% at the largest, per Cond1).

    > **v1 behavior:** pucks can drift horizontally within the active sieve range. On read we sort by x
    > and use the puck (x, y) as control points for `np.interp`. A future version will lock x to sieves
    > and add a 2D-mode toggle.
    """)
    return


@app.cell(hide_code=True)
def _constants(np):
    SIEVES_MM = np.array([0.075, 0.425, 2.0, 4.75, 9.5, 19.0, 37.5, 75.0])
    INTERIOR_SIEVES = SIEVES_MM[1:-1]
    LOG_SIEVES = np.log10(SIEVES_MM)
    X_MIN, X_MAX = float(LOG_SIEVES[0]), float(LOG_SIEVES[-1])

    return INTERIOR_SIEVES, LOG_SIEVES, SIEVES_MM, X_MAX, X_MIN


@app.cell(hide_code=True)
def _initial(INTERIOR_SIEVES, np):
    from scipy.stats import norm as _norm
    _z = (np.log(INTERIOR_SIEVES) - np.log(2.0)) / np.log(3.0)
    INIT_Y = (100.0 * _norm.cdf(_z)).tolist()
    INIT_X = np.log10(INTERIOR_SIEVES).tolist()

    return INIT_X, INIT_Y


@app.cell
def _puck_chart(
    ChartPuck,
    INIT_X,
    INIT_Y,
    LOG_SIEVES,
    SIEVES_MM,
    X_MAX,
    X_MIN,
    mo,
    np,
):
    def _draw(ax, widget):
        ax.clear()
        for ls in LOG_SIEVES:
            ax.axvline(ls, color="0.85", lw=1, zorder=0)
        ax.plot([X_MIN, X_MAX], [0, 100], "ko", ms=8, zorder=3)
        xs = [X_MIN, *list(widget.x), X_MAX]
        ys = [0.0, *list(widget.y), 100.0]
        order = np.argsort(xs)
        xs_sorted = np.array(xs)[order]
        ys_sorted = np.array(ys)[order]
        xx = np.linspace(X_MIN, X_MAX, 400)
        yy = np.interp(xx, xs_sorted, ys_sorted)
        ax.plot(xx, yy, color="C0", lw=2, zorder=2)
        ax.set_xlim(X_MIN - 0.05, X_MAX + 0.05)
        ax.set_ylim(-3, 103)
        ax.set_xticks(LOG_SIEVES)
        ax.set_xticklabels([f"{s:g}" for s in SIEVES_MM])
        ax.set_xlabel("Sieve opening (mm, log scale)")
        ax.set_ylabel("Percent passing (%)")
        ax.set_title("Drag pucks to shape the GSD")
        ax.grid(True, axis="y", alpha=0.3)

    puck = mo.ui.anywidget(
        ChartPuck.from_callback(
            _draw,
            x_bounds=(X_MIN - 0.05, X_MAX + 0.05),
            y_bounds=(-3, 103),
            figsize=(8, 4),
            x=INIT_X,
            y=INIT_Y,
            puck_color="#9c27b0",
            drag_x_bounds=(X_MIN, X_MAX),
            drag_y_bounds=(0.0, 100.0),
        )
    )
    puck

    return (puck,)


@app.cell(hide_code=True)
def _read_pucks(LOG_SIEVES, SIEVES_MM, X_MAX, X_MIN, np, puck):
    _xs = np.array([X_MIN, *list(puck.x), X_MAX])
    _ys = np.array([0.0, *list(puck.y), 100.0])
    _order = np.argsort(_xs)
    _xs_sorted = _xs[_order]
    _ys_sorted = _ys[_order]
    P = np.interp(LOG_SIEVES, _xs_sorted, _ys_sorted)
    P = np.clip(P, 0.0, 100.0)
    M_G = np.zeros_like(SIEVES_MM)
    M_G[:-1] = np.diff(P)
    _total = M_G[:-1].sum()
    if _total > 0:
        M_G = M_G / _total

    return (M_G,)


@app.cell(hide_code=True)
def _mass_plot(M_G, SIEVES_MM, np, plt):
    _fig, _ax = plt.subplots(figsize=(8, 3.6))
    _centers = np.sqrt(SIEVES_MM[:-1] * SIEVES_MM[1:])
    _widths = np.diff(np.log10(SIEVES_MM)) * 0.6
    _ax.bar(np.log10(_centers), M_G[:-1], width=_widths,
            color="C0", alpha=0.7, edgecolor="k")
    _ax.set_xticks(np.log10(SIEVES_MM))
    _ax.set_xticklabels([f"{s:g}" for s in SIEVES_MM], rotation=45, ha="right")
    _ax.set_xlabel("Sieve interval (lower bound, mm)")
    _ax.set_ylabel(r"Relative mass $m_j$")
    _ax.set_title("Mass retained per interval")
    _ax.grid(True, axis="y", alpha=0.3)
    _fig.tight_layout()
    _fig

    return


if __name__ == "__main__":
    app.run()
