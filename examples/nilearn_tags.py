# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "nilearn[dev]>=0.12.1",
#   "ruff",
#   "python-lsp-server"
# ]
# ///

import marimo

__generated_with = "0.17.0"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""# Tags in sklearn (>1.6.0) and nilearn (>0.11.1)""")
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
    from sklearn import __version__
    return (__version__,)


@app.cell(hide_code=True)
def _(__version__, mo):
    mo.md(
        rf"""
    With sklearn >= 1.6 (currently running {__version__}) tags were made part of the public API.

    - [documentation](https://scikit-learn.org/stable/modules/generated/sklearn.utils.Tags.html)
    - [developper guide](https://scikit-learn.org/stable/developers/develop.html#estimator-tags)
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""All estimators have tags accessible by the `__sklearn_tags__` magic method.""")
    return


@app.cell
def _(print):
    from sklearn.base import BaseEstimator

    estimator = BaseEstimator()

    print(estimator.__sklearn_tags__())
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""Several estimators have an `estimator_type` that can be used by several utility functions to determine some behaviors.""")
    return


@app.cell
def _():
    from sklearn.linear_model import LinearRegression

    lr = LinearRegression()

    lr.__sklearn_tags__().estimator_type
    return (lr,)


@app.cell
def _(lr, print):
    from sklearn.base import is_classifier, is_regressor, is_clusterer

    print(f"{is_classifier(lr)=}")
    print(f"{is_regressor(lr)=}")
    print(f"{is_clusterer(lr)=}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    **Transformer tags** can be used to determine how to handle data types during feature extraction.

    /// warning 
    **TODO** make use of this in nilearn?
    ///
    """
    )
    return


@app.cell
def _(print):
    from sklearn.decomposition import DictionaryLearning

    dl = DictionaryLearning()

    print(dl.__sklearn_tags__().transformer_tags)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""More important for Nilearn are the inputs tags.""")
    return


@app.cell
def _(lr, print):
    from sklearn.utils import InputTags as SkInputTags

    print(SkInputTags())
    print(lr.__sklearn_tags__().input_tags)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Nilearn tags""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""Starting from Nilearn==0.11.1, some extra home-made tags have been added to be able to handle the fact that our estimators can accept nifti or surface image directly.""")
    return


@app.cell
def _(print):
    from nilearn._utils.tags import InputTags

    tags = InputTags()

    print(tags)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    /// warning
    **TODO** `masker`, `multimasker` and `glm` should probably not be part of `input_tags` but maybe should be `estimator_type` instead. 
    ///
    """
    )
    return


@app.cell
def _(print):
    from nilearn.glm.first_level import FirstLevelModel

    flm = FirstLevelModel()

    print(flm.__sklearn_tags__())
    return FirstLevelModel, flm


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""Nilearn also has a few utility function to determine certain characteristic of an estimator.""")
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


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    /// admonition | Heads up.

    Note functions `is_masker`, `is_glm`... will be moved to `nilearn._utils.tags` in Nilearn>=0.13.
    ///
    """
    )
    return


@app.cell
def _(print):
    from nilearn.decoding import Decoder

    dec = Decoder()

    print(dec.__sklearn_tags__())
    return


@app.cell
def _(print):
    from nilearn.decoding import DecoderRegressor

    reg = DecoderRegressor()

    print(reg.__sklearn_tags__())
    return


@app.cell
def _(print):
    from nilearn.maskers import NiftiMasker

    nii_masker = NiftiMasker()

    print(nii_masker.__sklearn_tags__())
    return (NiftiMasker,)


@app.cell
def _(print):
    from nilearn.maskers import SurfaceMasker

    surf_masker = SurfaceMasker()

    print(surf_masker.__sklearn_tags__())
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""### Nilearn tags in practice""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    Nilearn tags are mostly used internally for now in the tests that run a series of checks on our estimators.

    - see in [nilearn/_utils/estimator_checks.py](https://github.com/nilearn/nilearn/blob/4219cb72f749ed0a4dee6e1811627444b05c764f/nilearn/_utils/estimator_checks.py#L567-L590)

    ```python
        if accept_niimg_input(estimator) or accept_surf_img_input(estimator):
            yield (clone(estimator), check_fit_returns_self)
            yield (clone(estimator), check_img_estimator_dict_unchanged)
            yield (clone(estimator), check_img_estimator_dont_overwrite_parameters)
            yield (clone(estimator), check_img_estimator_fit_check_is_fitted)
            yield (clone(estimator), check_img_estimator_fit_idempotent)
            yield (clone(estimator), check_img_estimator_overwrite_params)
            yield (clone(estimator), check_img_estimator_pickle)
            yield (clone(estimator), check_img_estimator_fit_score_takes_y)
            yield (clone(estimator), check_img_estimator_n_elements)
            yield (clone(estimator), check_img_estimator_pipeline_consistency)
            yield (clone(estimator), check_img_estimator_standardization)
            yield (clone(estimator), check_nilearn_methods_sample_order_invariance)

            if requires_y:
                yield (clone(estimator), check_img_estimator_requires_y_none)

            if is_classifier(estimator) or is_regressor(estimator):
                yield (clone(estimator), check_supervised_img_estimator_y_no_nan)
                yield (clone(estimator), check_decoder_empty_data_messages)
                yield (clone(estimator), check_decoder_compatibility_mask_image)
                yield (clone(estimator), check_decoder_with_surface_data)
                yield (clone(estimator), check_decoder_with_arrays)
                if is_regressor(estimator):
                    yield (
                        clone(estimator),
                        check_img_regressor_no_decision_function,
                    )
    ```
    """
    )
    return


@app.cell
def _(FirstLevelModel, NiftiMasker, print):
    from nilearn._utils.estimator_checks import nilearn_check_estimator

    for est, check, name in nilearn_check_estimator([NiftiMasker(), FirstLevelModel()]):
        print(f"{est.__class__.__name__} - {name}")

        # uncomment to actually run the checks
        # check(est)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Making nilearn tags part of the public API""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    Currently we need to support the tag system for both sklearn>=1.4.0;<1.6 and sklearn>=1.6.

    But it would be nice to start slowly bumping sklearn versions to make 1.6 the minimum version supported: by this time we could make the nilearn tags also part of our public API.

    Python SPEC0 has the following schedule suggestion:
    - https://scientific-python.org/specs/spec-0000/#support-window
    - 2026 - Quarter 1: drop sklearn 1.4
    - 2026 - Quarter 2: drop sklearn 1.5

    For us I would suggest: 
    - nilearn 0.14 -  mimimum sklearn bumped to 1.5
    - nilearn 0.15 -  mimimum sklearn bumped to 1.6
    """
    )
    return


if __name__ == "__main__":
    app.run()
