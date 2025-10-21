# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "nilearn[dev]>=0.12.1",
#   "scitkit-learn==1.5.2",
#   "ruff",
#   "python-lsp-server"
# ]
# ///

import marimo

__generated_with = "0.17.0"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""# Tags in sklearn (1.5.2) and nilearn (>0.11.1)""")
    return


@app.cell
def _():
    import marimo as mo
    from rich import print
    return mo, print


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## sklearn tags""")
    return


@app.cell
def _():
    from sklearn import __version__ as sk_version
    return (sk_version,)


@app.cell(hide_code=True)
def _(mo, sk_version):
    mo.md(
        rf"""With older sklearn < 1.6 (currently running {sk_version}) tags were not part of the public API."""
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""Tags were accessible by the `_more_tags` private method.""")
    return


@app.cell
def _(print):
    from sklearn.base import BaseEstimator

    estimator = BaseEstimator()

    print(estimator._more_tags())
    return


@app.cell
def _():
    from sklearn.linear_model import LinearRegression

    lr = LinearRegression()

    lr._more_tags()
    return (lr,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""Sklearn had a couple of utility functions to determine some behaviors.""")
    return


@app.cell
def _(lr, print):
    from sklearn.base import is_classifier, is_regressor

    print(f"{is_classifier(lr)=}")
    print(f"{is_regressor(lr)=}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Nilearn tags""")
    return


@app.cell
def _():
    from nilearn import __version__ as nil_version
    return (nil_version,)


@app.cell(hide_code=True)
def _(mo, nil_version):
    mo.md(
        rf"""Starting from Nilearn>=0.11.1 (here running {nil_version}), some extra home-made tags have been added to be able to handle the fact that our estimators can accept nifti or surface image directly."""
    )
    return


@app.cell
def _(print):
    from nilearn._utils.tags import tags

    print(tags())

    print(tags(niimg_like=True, surf_img=True, masker=True, multi_masker=True, glm=True))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""Access to the tags of an estimator can be done via the old `_more_tags()` or the `__sklearn_tags__()` magic method to be both compatible with all sklearn versions."""
    )
    return


@app.cell
def _(print):
    from nilearn.glm.first_level import FirstLevelModel

    flm = FirstLevelModel()

    print(flm._more_tags())
    print(flm.__sklearn_tags__())
    return (flm,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""Nilearn also has a few utility function to determine certain characteristic of an estimator."""
    )
    return


@app.cell
def _(flm, print):
    from nilearn._utils.estimator_checks import (
        is_masker,
        is_glm,
        is_multimasker,
        accept_niimg_input,
        accept_surf_img_input,
    )

    print(f"{is_masker(flm)=}")
    print(f"{is_multimasker(flm)=}")
    print(f"{is_glm(flm)=}")
    print(f"{accept_niimg_input(flm)=}")
    print(f"{accept_surf_img_input(flm)=}")
    return


if __name__ == "__main__":
    app.run()
