import os
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd

matplotlib.rcParams["font.family"] = "Times New Roman"
matplotlib.rcParams["font.size"] = 8

cmip5_file = "data/station_climate_anomaly_CMIP5.csv"
cmip6_file = "data/station_climate_anomaly_CMIP6.csv"

cmip5_data = pd.read_csv(cmip5_file)
cmip6_data = pd.read_csv(cmip6_file)

variables = ["tasmin", "tasmax", "rsds", "hurs", "pr", "sfcWind"]

cmip5_scenarios = ["RCP26", "RCP45", "RCP85"]
cmip6_scenarios = ["SSP126", "SSP245", "SSP585"]

colors = ["blue", "green", "red"]

cmip5_labels = [
    "RCP26 - Historical",
    "RCP45 - Historical",
    "RCP85 - Historical"
]

cmip6_labels = [
    "SSP126 - Historical",
    "SSP245 - Historical",
    "SSP585 - Historical"
]

annotations_cmip5 = ["(a)", "(b)", "(c)", "(d)", "(e)", "(f)"]
annotations_cmip6 = ["(g)", "(h)", "(i)", "(j)", "(k)", "(l)"]

fig = plt.figure(figsize=(5.5, 8.0))
gs = fig.add_gridspec(6, 2)

for i, variable in enumerate(variables):

    ax = fig.add_subplot(gs[i, 0])

    for j, scenario in enumerate(cmip5_scenarios):

        mean_column = f"{variable}_{scenario}_mean"
        std_column = f"{variable}_{scenario}_std"

        annual_means = cmip5_data[mean_column].values
        annual_stds = cmip5_data[std_column].values

        ax.plot(
            cmip5_data["Year"],
            annual_means,
            label=cmip5_labels[j],
            color=colors[j],
            linewidth=1,
        )

        ax.fill_between(
            cmip5_data["Year"],
            annual_means - annual_stds,
            annual_means + annual_stds,
            color=colors[j],
            alpha=0.15,
        )

    ax.set_xlabel("Year")

    if variable == "tasmin":
        ax.set_ylabel("Minimum temperature (K)")
    elif variable == "tasmax":
        ax.set_ylabel("Maximum temperature (K)")
    elif variable == "rsds":
        ax.set_ylabel("Solar radiation (W m$^{-2}$)")
    elif variable == "hurs":
        ax.set_ylabel("Relative humidity (%)")
    elif variable == "pr":
        ax.set_ylabel("Precipitation (mm day$^{-1}$)")
    elif variable == "sfcWind":
        ax.set_ylabel("Wind speed (m s$^{-1}$)")

    ax.text(0.02, 0.98, annotations_cmip5[i], transform=ax.transAxes, va="top")

    if i == 0:
        ax.legend(
            loc="upper center",
            ncol=1,
            bbox_to_anchor=(0.35, 1.05),
            frameon=False,
        )

for i, variable in enumerate(variables):

    ax = fig.add_subplot(gs[i, 1])

    for j, scenario in enumerate(cmip6_scenarios):

        mean_column = f"{variable}_{scenario}_mean"
        std_column = f"{variable}_{scenario}_std"

        annual_means = cmip6_data[mean_column].values
        annual_stds = cmip6_data[std_column].values

        ax.plot(
            cmip6_data["Year"],
            annual_means,
            label=cmip6_labels[j],
            color=colors[j],
            linewidth=1,
        )

        ax.fill_between(
            cmip6_data["Year"],
            annual_means - annual_stds,
            annual_means + annual_stds,
            color=colors[j],
            alpha=0.15,
        )

    ax.set_xlabel("Year")
    ax.text(0.02, 0.98, annotations_cmip6[i], transform=ax.transAxes, va="top")

    if i == 0:
        ax.legend(
            loc="upper center",
            ncol=1,
            bbox_to_anchor=(0.35, 1.05),
            frameon=False,
        )

plt.subplots_adjust(
    left=0.1,
    bottom=0.05,
    right=0.95,
    top=0.97,
    wspace=0.18,
    hspace=0.5,
)

os.makedirs("figures", exist_ok=True)

plt.savefig(
    "figures/climate_aver_models.png",
    dpi=600,
    bbox_inches="tight",
)

plt.show()
