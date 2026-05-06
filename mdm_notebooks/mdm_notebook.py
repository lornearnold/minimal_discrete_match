# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "marimo>=0.13",
#     "numpy",
#     "matplotlib",
#     "scipy",
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
    from scipy.stats import norm

    return mo, norm, np, plt


@app.cell(hide_code=True)
def _title(mo):
    mo.md(r"""
    # Minimal Discrete Matches for Target Grain Size Distributions

    *Lorne Arnold (University of Washington, Tacoma) &middot; Caleb Arnold (Hunt Middle School)*

    *Proceedings of the 21st International Conference on Soil Mechanics and Geotechnical Engineering, Vienna 2026*

    Interactive companion implementing the two algorithms from the paper: the **Fixed Size (FS)**
    and the **Spanned Integer (SI)** algorithm. Adjust the GSD with the sliders below and watch the
    resulting **minimal discrete match (MDM)** update.
    """)
    return


@app.cell(hide_code=True)
def _background(mo):
    mo.md(r"""
    ## What is a minimal discrete match?

    A grain size distribution $G$ specifies the mass retained on a set of sieves. To populate a DEM
    model we need a finite *discrete* set of particles whose sizes and counts reproduce $G$ by mass.
    The **minimal discrete match (MDM)** is the smallest such set.

    | Symbol | Meaning |
    |---|---|
    | $X_G$ | sieve sizes, ascending, length $n_G$ |
    | $M_G$ | masses retained per sieve interval ($m_{n_G} = 0$, Cond1) |
    | $X_S$ | particle sizes in the sample, length $n_S$ |
    | $Q_S$ | integer particle quantities |
    | $\Phi$ | relative masses $\phi_j = m_j / m_{n_G - 1}$, length $n_S$ |
    | $Z$ | volume ratios $\zeta_i = f(x_{n_S}) / f(x_i)$ |
    | $K = \Phi \cdot Z$ | quantity ratios &mdash; relative number of particles per size |

    Mass scaling for uniform spheres of density $\rho$:

    $$
    f(x) \;=\; \frac{\rho \pi}{6}\,x^{3}.
    $$

    For an *articulate accurate* match (Cond4) one $x_i$ is needed per sieve interval, so
    $n_S = n_G - 1$.
    """)
    return


@app.cell(hide_code=True)
def _constants(np):
    # Subset of ASTM D6913 sieve openings (mm). Chosen to keep visuals legible.
    SIEVES_MM = np.array([0.075, 0.425, 2.0, 4.75, 9.5, 19.0, 37.5, 75.0])
    RHO = 2650.0  # kg/m^3, solid density of quartz
    return RHO, SIEVES_MM


@app.cell(hide_code=True)
def _gsd_controls(SIEVES_MM, mo):
    d5 = mo.ui.slider(
        start=float(SIEVES_MM[0]),
        stop=float(SIEVES_MM[-2]),
        step=0.05,
        value=0.3,
        label=r"$D_{5}$ (mm) &mdash; size at 5% passing",
        show_value=True,
    )
    d95 = mo.ui.slider(
        start=float(SIEVES_MM[1]),
        stop=float(SIEVES_MM[-1]),
        step=0.1,
        value=20.0,
        label=r"$D_{95}$ (mm) &mdash; size at 95% passing",
        show_value=True,
    )
    mo.vstack(
        [
            mo.md("### GSD parameters"),
            mo.md("A lognormal curve is fit through these two percentiles."),
            d5,
            d95,
        ]
    )
    return d5, d95


@app.cell
def _build_gsd(SIEVES_MM, d5, d95, norm, np):
    # Fit a lognormal so that P(D5) = 5% and P(D95) = 95%.
    x5 = min(d5.value, d95.value - 0.01)
    x95 = max(d95.value, d5.value + 0.01)
    z5, z95 = norm.ppf(0.05), norm.ppf(0.95)
    sigma_log = (np.log(x95) - np.log(x5)) / (z95 - z5)
    mu_log = np.log(x5) - sigma_log * z5

    # Percent passing at each sieve, anchored to 100% at the largest sieve (Cond1).
    P = 100.0 * norm.cdf((np.log(SIEVES_MM) - mu_log) / sigma_log)
    P[-1] = 100.0
    P[0] = max(0.0, P[0])

    # Mass retained per interval; trailing entry is zero by construction.
    M_G = np.zeros_like(SIEVES_MM)
    M_G[:-1] = np.diff(P)
    _retained = M_G[:-1].sum()
    if _retained > 0:
        M_G = M_G / _retained

    # Trim to the contiguous range of intervals carrying real mass.
    # Intervals below MASS_EPS (default 0.1%% of total) are treated as empty,
    # avoiding pathological K-ranges where phi -> 0 forces no spanned integer.
    MASS_EPS = 1e-3
    _active = np.where(M_G[:-1] > MASS_EPS)[0]
    if len(_active) >= 1:
        _i0, _i1 = int(_active[0]), int(_active[-1])
        SIEVES_ACTIVE = SIEVES_MM[_i0 : _i1 + 2]
        M_G_ACTIVE = np.concatenate([M_G[_i0 : _i1 + 1], [0.0]])
        _s = M_G_ACTIVE.sum()
        if _s > 0:
            M_G_ACTIVE = M_G_ACTIVE / _s
    else:
        SIEVES_ACTIVE = SIEVES_MM.copy()
        M_G_ACTIVE = M_G.copy()
    return M_G, M_G_ACTIVE, P, SIEVES_ACTIVE


@app.cell
def _gsd_plot(M_G, P, SIEVES_MM, np, plt):
    _fig, (_ax1, _ax2) = plt.subplots(1, 2, figsize=(10, 3.6))
    _ax1.semilogx(SIEVES_MM, P, "ko-", lw=1.5, ms=6)
    _ax1.set_xlabel("Particle size (mm)")
    _ax1.set_ylabel("Percent passing (%)")
    _ax1.set_title("GSD - cumulative")
    _ax1.set_ylim(0, 105)
    _ax1.grid(True, which="both", alpha=0.3)

    _centers = np.sqrt(SIEVES_MM[:-1] * SIEVES_MM[1:])
    _widths = np.diff(np.log10(SIEVES_MM)) * 0.6
    _ax2.bar(
        np.log10(_centers),
        M_G[:-1],
        width=_widths,
        color="C0",
        alpha=0.7,
        edgecolor="k",
    )
    _ax2.set_xticks(np.log10(SIEVES_MM))
    _ax2.set_xticklabels([f"{s:g}" for s in SIEVES_MM], rotation=45, ha="right")
    _ax2.set_xlabel("Sieve interval (lower bound, mm)")
    _ax2.set_ylabel(r"Relative mass $m_j$")
    _ax2.set_title("Mass retained per interval")
    _ax2.grid(True, axis="y", alpha=0.3)

    _fig.tight_layout()
    _fig
    return


@app.cell(hide_code=True)
def _phi_section(mo):
    mo.md(r"""
    ## Algorithm 1 &mdash; Fixed Size (FS)

    Pick the particle sizes once (here: the geometric mean of each sieve interval), compute
    $K = \Phi \cdot Z$, and round to integers. Iteration $i$ uses $Q_S = \lfloor (i+1)\,K \rfloor$,
    so the rounding error shrinks as $i$ grows but the total particle count grows linearly.
    """)
    return


@app.cell
def _fs_algorithm(M_G_ACTIVE, RHO, SIEVES_ACTIVE, np):
    def f_mass(x, rho=RHO):
        return rho * np.pi * x**3 / 6.0

    def fs_algorithm(X_G, M_G, n_iter=15):
        """Fixed Size algorithm. Runs n_iter iterations regardless of tolerance,
        so the convergence curve in Fig. 2 is fully visible."""
        X_S = np.sqrt(X_G[:-1] * X_G[1:])
        if M_G[-2] <= 0:
            return {
                "X_S": X_S,
                "phi": np.full(len(X_S), np.nan),
                "z": np.full(len(X_S), np.nan),
                "K": np.full(len(X_S), np.nan),
                "history": [],
                "ok": False,
            }
        phi = M_G[:-1] / M_G[-2]
        z = f_mass(X_S[-1]) / f_mass(X_S)
        K = phi * z
        history = []
        for i in range(n_iter):
            Q = np.floor((i + 1) * K).astype(int)
            predicted = Q * f_mass(X_S)
            target = (i + 1) * phi * f_mass(X_S[-1])
            err = float(np.abs(predicted - target).sum() / target.sum())
            history.append({"i": i, "Q": Q, "N": int(Q.sum()), "err": err})
        return {"X_S": X_S, "phi": phi, "z": z, "K": K, "history": history, "ok": True}

    fs_result = fs_algorithm(SIEVES_ACTIVE, M_G_ACTIVE)
    return f_mass, fs_result


@app.cell(hide_code=True)
def _fs_iter_ui(fs_result, mo):
    n_iters = len(fs_result["history"])
    fs_iter = mo.ui.slider(
        start=0,
        stop=max(0, n_iters - 1),
        step=1,
        value=0,
        label="FS iteration index",
        show_value=True,
    )
    mo.vstack([mo.md(f"**Iterations run:** {n_iters}"), fs_iter])
    return (fs_iter,)


@app.cell
def _fs_plot(fs_iter, fs_result, plt):
    _hist = fs_result["history"]
    _snap = _hist[fs_iter.value]
    _iters = [h["i"] for h in _hist]
    _errs = [h["err"] for h in _hist]

    _fig, (_ax1, _ax2) = plt.subplots(1, 2, figsize=(10, 3.6))

    _ax1.semilogy(_iters, _errs, "k.-", lw=1.2)
    _ax1.semilogy(_snap["i"], _snap["err"], "o", color="C3", ms=10, label=f"i = {_snap['i']}")
    _ax1.set_xlabel("Iteration $i$")
    _ax1.set_ylabel(r"Match error $E$")
    _ax1.set_title("FS convergence")
    _ax1.grid(True, which="both", alpha=0.3)
    _ax1.legend(loc="best")

    _ml, _sl, _bl = _ax2.stem(fs_result["X_S"], _snap["Q"], basefmt=" ")
    plt.setp(_ml, "color", "C0")
    plt.setp(_sl, "color", "C0")
    _ax2.set_xscale("log")
    _ax2.set_yscale("log")
    _ax2.set_xlabel("Particle size (mm)")
    _ax2.set_ylabel(r"Quantity $q_i$")
    _ax2.set_title(f"FS sample at i={_snap['i']}: $N$ = {_snap['N']:,}")
    _ax2.grid(True, which="both", alpha=0.3)

    _fig.tight_layout()
    _fig
    return


@app.cell(hide_code=True)
def _si_intro(mo):
    mo.md(r"""
    ## Algorithm 2 &mdash; Spanned Integer (SI)

    Rather than fix the particle sizes and accept rounding error, the SI algorithm searches over
    the largest particle size $x_{n_S}$ and asks whether an integer fits inside the *range*
    $[K_+,\,K_-]$ for each sieve interval (where $K_-$ uses the smallest allowable size in the
    interval and $K_+$ the largest). When such a "spanned integer" exists for every interval,
    choosing it for $Q_{SI}$ and inverting $f$ gives an exact match:

    $$
    x_i \;=\; f^{-1}\!\left(\,\text{scale}\cdot\phi_i\,\frac{f(x_{n_S})}{q_{SI,i}}\right).
    $$

    The bars below show the achievable $K$-range per interval; red dots are the chosen integers.
    """)
    return


@app.cell
def _si_algorithm(M_G_ACTIVE, RHO, SIEVES_ACTIVE, f_mass, np):
    def si_algorithm(X_G, M_G, n_x_grid=200, max_scale=20):
        """Spanned Integer algorithm. Sweeps x_nS from low to high; first valid
        x_nS yields the minimal-N solution because Q_SI[i] = ceil(K_+,i) is
        monotone non-decreasing in x_nS. If no x_nS works at the current scale,
        the algorithm scales the quantity ratios by an integer factor and retries
        (paper, Step SI_4)."""
        nG = len(X_G)
        nS = nG - 1
        if M_G[-2] <= 0:
            return {"success": False, "reason": "m_{n_G - 1} = 0"}
        eps = 1e-9
        phi = M_G[:-1] / M_G[-2]
        f_inv = lambda v: (6.0 * v / (RHO * np.pi)) ** (1.0 / 3.0)
        x_nS_grid = np.linspace(X_G[-2] + eps, X_G[-1] - eps, n_x_grid)

        for scale in range(1, max_scale + 1):
            for x_nS in x_nS_grid:
                x_min = X_G[:-1].copy() + eps
                x_max = X_G[1:].copy() - eps
                x_min[-1] = x_nS
                x_max[-1] = x_nS
                K_minus = scale * phi * f_mass(x_nS) / f_mass(x_min)
                K_plus = scale * phi * f_mass(x_nS) / f_mass(x_max)
                lo = np.ceil(K_plus)
                hi = np.floor(K_minus)
                if np.all(lo <= hi):
                    Q_SI = lo.astype(int)
                    X_SI = f_inv(scale * phi * f_mass(x_nS) / Q_SI)
                    return {
                        "success": True,
                        "scale": scale,
                        "x_nS": float(x_nS),
                        "X_SI": X_SI,
                        "Q_SI": Q_SI,
                        "K_minus": K_minus,
                        "K_plus": K_plus,
                        "phi": phi,
                        "N": int(Q_SI.sum()),
                    }
        return {"success": False, "reason": "no spanned integers within max_scale"}

    si_result = si_algorithm(SIEVES_ACTIVE, M_G_ACTIVE)
    return (si_result,)


@app.cell
def _si_plot(SIEVES_ACTIVE, mo, plt, si_result):
    if not si_result["success"]:
        _out = mo.md(
            f"**SI algorithm did not converge:** {si_result.get('reason', 'unknown')}. "
            "Adjust the GSD sliders so $m_{n_G-1} > 0$ (i.e., put some mass near the largest sieve)."
        )
    else:
        _Km = si_result["K_minus"]
        _Kp = si_result["K_plus"]
        _Q = si_result["Q_SI"]
        _Xs = si_result["X_SI"]
        _nS = len(_Km)
        _S = SIEVES_ACTIVE  # interval boundaries used by the algorithm

        _fig, (_ax1, _ax2) = plt.subplots(1, 2, figsize=(10, 3.8))

        for _i in range(_nS):
            _ax1.plot([_i, _i], [_Kp[_i], _Km[_i]], "-", color="0.4", lw=6, alpha=0.6)
            _ax1.plot(_i, _Q[_i], "o", color="C3", ms=9, zorder=5)
        _ax1.set_xticks(range(_nS))
        _ax1.set_xticklabels(
            [f"({_S[i]:g}, {_S[i+1]:g}]" for i in range(_nS)],
            rotation=35, ha="right",
        )
        _ax1.set_yscale("log")
        _ax1.set_ylabel(r"Quantity ratio $K$")
        _ax1.set_xlabel("Sieve interval (mm)")
        _ax1.set_title(
            f"Spanned integers (scale = {si_result['scale']}, "
            f"$x_{{nS}}$ = {si_result['x_nS']:.3g} mm)"
        )
        _ax1.grid(True, axis="y", alpha=0.3)

        _ml, _sl, _bl = _ax2.stem(_Xs, _Q, basefmt=" ")
        plt.setp(_ml, "color", "C3")
        plt.setp(_sl, "color", "C3")
        _ax2.set_xscale("log")
        _ax2.set_yscale("log")
        _ax2.set_xlabel("Particle size (mm)")
        _ax2.set_ylabel(r"Quantity $q_i$")
        _ax2.set_title(f"SI sample (MDM): $N$ = {si_result['N']:,}")
        _ax2.grid(True, which="both", alpha=0.3)

        _fig.tight_layout()
        _out = _fig
    _out
    return


@app.cell(hide_code=True)
def _summary(fs_result, mo, si_result):
    _fs_final = fs_result["history"][-1]
    _si_ok = si_result["success"]
    _si_n = f"{si_result['N']:,}" if _si_ok else "—"
    _si_scale = si_result["scale"] if _si_ok else "—"
    mo.md(
        f"""
        ## Summary

        | Algorithm | $N_\\mathrm{{MDM}}$ | Match error | Iterations / scale |
        |---|---:|---:|---:|
        | **FS** (terminal iteration) | {_fs_final['N']:,} | {_fs_final['err']:.2e} | {_fs_final['i'] + 1} |
        | **SI** | {_si_n} | $\\approx 0$ | scale {_si_scale} |

        For most realistic GSDs the SI algorithm reaches an exact match with one to two orders of
        magnitude fewer particles than the terminal FS iteration. Try widening the GSD (large
        $D_{{95}} / D_5$ ratio) and watch $N_\\mathrm{{MDM}}$ climb &mdash; this is the headline result
        of Section 5.2 in the paper.
        """
    )
    return


if __name__ == "__main__":
    app.run()
