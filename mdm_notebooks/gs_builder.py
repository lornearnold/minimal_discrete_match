# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "marimo>=0.13",
#     "numpy",
# ]
# ///

import marimo

__generated_with = "0.23.5"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _imports():
    import marimo as mo
    import numpy as np


    return mo, np


@app.cell(hide_code=True)
def _title(mo):
    mo.md(r"""
    # Build $G$ and $S$ by hand

    Two indexed sets:

    - **$G$** (grain size distribution) — sizes $X_G$ ascending and retained masses $M_G$
      (last entry pinned to 0 by **Cond1**).
    - **$S$** (sample) — sizes $X_S$ ascending and integer quantities $Q_S$.

    Cond1 is enforced mechanically. **Cond2** (range coverage: $\min X_G < \min X_S$ and
    $\max X_G \ge \max X_S$) and **Cond3** (articulate: a $G$-size between every consecutive
    pair in $X_S$) are reported as status badges below — adjust the values until both pass.
    """)
    return


@app.cell
def _sizes(mo):
    n_G = mo.ui.slider(start=3, stop=6, step=1, value=4, label=r"$n_G$ (sizes in $G$)", show_value=True)
    n_S = mo.ui.slider(start=1, stop=5, step=1, value=3, label=r"$n_S$ (sizes in $S$)", show_value=True)
    mo.hstack([n_G, n_S], justify="start", gap=2)

    return n_G, n_S


@app.cell
def _g_widgets(mo, n_G):
    _xg_init = [[round(0.5 * (i + 1) ** 2, 3)] for i in range(n_G.value)]
    _mg_init = [[round(1.0 / max(n_G.value - 1, 1), 4)] for _ in range(n_G.value - 1)] + [[0.0]]
    _mg_disabled = [[False] for _ in range(n_G.value - 1)] + [[True]]

    X_G_in = mo.ui.matrix(
        value=_xg_init,
        min_value=0.0,
        step=0.1,
        column_labels=["X_G (mm)"],
        row_labels=[f"j={j}" for j in range(n_G.value)],
        label="$G$ sizes",
        precision=3,
    )
    M_G_in = mo.ui.matrix(
        value=_mg_init,
        min_value=0.0,
        step=0.05,
        disabled=_mg_disabled,
        column_labels=["M_G"],
        row_labels=[f"j={j}" for j in range(n_G.value)],
        label="$G$ masses (last = 0, Cond1)",
        precision=4,
    )
    mo.hstack([X_G_in, M_G_in], justify="start", gap=1, align="start")

    return M_G_in, X_G_in


@app.cell
def _s_widgets(mo, n_S):
    _xs_init = [[round(0.5 * (i + 1) ** 2 + 0.25, 3)] for i in range(n_S.value)]
    _qs_init = [[1] for _ in range(n_S.value)]

    X_S_in = mo.ui.matrix(
        value=_xs_init,
        min_value=0.0,
        step=0.1,
        column_labels=["X_S (mm)"],
        row_labels=[f"i={i}" for i in range(n_S.value)],
        label="$S$ sizes",
        precision=3,
    )
    Q_S_in = mo.ui.matrix(
        value=_qs_init,
        min_value=1,
        step=1,
        column_labels=["Q_S"],
        row_labels=[f"i={i}" for i in range(n_S.value)],
        label="$S$ quantities (positive integers)",
        precision=0,
    )
    mo.hstack([X_S_in, Q_S_in], justify="start", gap=1, align="start")

    return Q_S_in, X_S_in


@app.cell(hide_code=True)
def _read(M_G_in, Q_S_in, X_G_in, X_S_in, np):
    X_G = np.sort(np.array([row[0] for row in X_G_in.value], dtype=float))
    M_G = np.array([row[0] for row in M_G_in.value], dtype=float)
    M_G[-1] = 0.0  # Cond1
    X_S = np.sort(np.array([row[0] for row in X_S_in.value], dtype=float))
    Q_S = np.array([int(row[0]) for row in Q_S_in.value], dtype=int)

    return M_G, X_G, X_S


@app.cell(hide_code=True)
def _status(M_G, X_G, X_S, mo, np):
    def _badge(ok, label):
        color = "#2e7d32" if ok else "#c62828"
        sym = "PASS" if ok else "FAIL"
        return (
            f'<span style="background:{color};color:white;padding:2px 8px;'
            f'border-radius:4px;font-family:monospace;font-size:0.85em;">'
            f'{sym}</span> &nbsp;{label}'
        )

    _cond1 = M_G[-1] == 0.0
    _cond2 = (X_G.min() < X_S.min()) and (X_G.max() >= X_S.max())

    # Cond3: between every consecutive (x_i, x_{i+1}) in X_S there is x_j in X_G with x_i < x_j <= x_{i+1}
    def _cond3(X_G, X_S):
        if len(X_S) < 2:
            return True
        for a, b in zip(X_S[:-1], X_S[1:]):
            if not np.any((X_G > a) & (X_G <= b)):
                return False
        return True

    _cond3_ok = _cond3(X_G, X_S)

    mo.md(
        "### Conditions\n\n"
        + _badge(_cond1, r"**Cond1** &nbsp; $m_{n_G} = 0$") + "<br>"
        + _badge(_cond2, r"**Cond2** &nbsp; $\min X_G < \min X_S \;\wedge\; \max X_G \ge \max X_S$") + "<br>"
        + _badge(_cond3_ok, r"**Cond3** &nbsp; articulate &mdash; a $G$-size between every consecutive pair in $X_S$")
    )

    return


if __name__ == "__main__":
    app.run()
