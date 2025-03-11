# %%
# Comparing results across studies
# --------------------------------
#
# NARPS study comparison
#

# %% Get data fromp neurovault
from pathlib import Path

from nilearn.datasets import fetch_neurovault_ids

# {team : collections_id} dictionary
collection_ids = {
    "0JO0": "4807",
    "6VV2": "4883",
}

# %%
# Uncomment the code below to get images from all teams.
# Note this will take a very long time.
#
# .. code-block:: python
#
#    import requests
#    import pandas as pd
#
#    output_dir = Path.cwd() / "results" / "plot_transparency"
#    output_dir.mkdir(exist_ok=True, parents=True)
#
#    output_file = output_dir / "analysis_pipelines.xlsx"
#
#
#    def download_team_listing(output_file):
#        url = 'https://github.com/poldrack/narps/raw/refs/heads/master/ImageAnalyses/metadata_files/analysis_pipelines_for_analysis.xlsx'
#        response = requests.get(url, stream=True)
#        with open(output_file, "wb") as file:
#            for chunk in response.iter_content(chunk_size=8192):
#                file.write(chunk)
#
#
#    def get_collection_ids(infile=output_file):
#        TEAMS_TO_SKIP = ['1K0E', 'X1Z4', 'L1A8', 'VG39', '5G9K', '16IN']
#        # requires openpyxl
#        teaminfo = pd.read_excel(infile, skiprows=1)
#        collectionID = {}
#        for t in teaminfo.index:
#            teamID = teaminfo.loc[t, 'teamID']
#            if teamID in TEAMS_TO_SKIP:
#                continue
#            public_link = teaminfo.loc[t, 'NV_collection_link']
#            collectionID[teamID] = Path(public_link).stem
#
#        return(collectionID)
#
#    collection_ids = get_collection_ids()
#

nv_data = fetch_neurovault_ids(collection_ids=collection_ids.values())

# %%
# Select the data we want to plot.
#
# Keep only maps for hypothesis 1.
#

hypothesis = "1"

data_to_plot = {k: {"collection_id": v} for k, v in collection_ids.items()}
for x in nv_data["images_meta"]:
    file = Path(x["file"])
    if hypothesis not in file.stem:
        continue

    team = list(collection_ids.keys())[
        list(collection_ids.values()).index(str(x["collection_id"]))
    ]

    if "_unthresh" in file.stem:
        data_to_plot[team]["unthresholded"] = x["absolute_path"]
    if "_thresh" in file.stem:
        data_to_plot[team]["thresholded"] = x["absolute_path"]

# %%
# Compare the thresholded and unthresholded results
#
from matplotlib import pyplot as plt
import numpy as np
from nilearn.plotting import plot_stat_map, show

threshold = 3
figure_width = 9

plotting_config = {
    "display_mode": "x",
    # take a cut through
    # the ventro medial prefrontal cortex
    # to match region of interest for hypothesis 1
    "cut_coords": [1],
    "draw_cross": False,
    "vmax": 5,
}


fig, axes = plt.subplots(
    len(data_to_plot),
    2,
    figsize=(figure_width, len(data_to_plot) * 4),
)
axes = np.atleast_2d(axes)

for i, (team, data) in enumerate(data_to_plot.items()):
    plot_stat_map(
        data["thresholded"],
        title=f"team {team} - thresholded",
        axes=axes[i, 0],
        cmap="inferno",
        **plotting_config,
    )
    plot_stat_map(
        data["unthresholded"],
        title=f"team {team} - unthresholded",
        transparency=data["unthresholded"],
        transparency_range=[0, threshold],
        axes=axes[i, 1],
        cmap="cold_hot",
        **plotting_config,
    )

show()

