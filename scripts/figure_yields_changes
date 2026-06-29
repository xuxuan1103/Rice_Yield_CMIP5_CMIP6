import os
import pandas as pd
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import ttest_1samp

matplotlib.rcParams['font.family'] = 'Times New Roman'
matplotlib.rcParams['font.size'] = 8


def read_csv_files(folder_path):
    data_dict = {}
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.csv'):
                file_path = os.path.join(root, file)
                parts = file.split('_')
                if len(parts) >= 3 and (parts[1].startswith('RCP') or parts[1].startswith('SSP')):
                    model = parts[0]
                    scenario = parts[1]
                    if model not in data_dict:
                        data_dict[model] = {}
                    if scenario not in data_dict[model]:
                        data_dict[model][scenario] = []
                    df = pd.read_csv(file_path, header=None)
                    data_dict[model][scenario].append(df)
    return data_dict


def calculate_yearly_yield_per_model(data_dict, scenario):
    model_yearly_yield = {}
    for model, experiments in data_dict.items():
        if scenario in experiments:
            yearly_yield_per_experiment = []
            for exp_df in experiments[scenario]:
                yearly_yield = exp_df.mean(axis=0) / 1000
                yearly_yield_per_experiment.append(yearly_yield)
            combined_yearly_yield = pd.concat(yearly_yield_per_experiment, axis=1)
            model_mean_yearly_yield = combined_yearly_yield.mean(axis=1)
            model_yearly_yield[model] = model_mean_yearly_yield
    return model_yearly_yield


def read_obs_data(file_path):
    obs_df = pd.read_csv(file_path, header=None)
    obs_mean = obs_df.mean().mean() / 1000
    return obs_mean


def calculate_percentage_change(model_yearly_yield, obs_mean):
    percentage_change = {}
    for model, yields in model_yearly_yield.items():
        change = yields - obs_mean
        percentage_change[model] = (change / obs_mean) * 100
    return percentage_change


def perform_significance_test(percentage_changes, scenarios):
    significance_results = {scenario: {} for scenario in scenarios}
    for scenario in scenarios:
        for model, percentage in percentage_changes[scenario].items():
            _, p_value = ttest_1samp(percentage, 0)
            significance_results[scenario][model] = p_value
    return significance_results


def plot_yields_percentage_change(ax, percentage_changes, scenarios, title, letter, models_order, significance_results):
    models = models_order
    values = {model: [] for model in models}
    std_devs = {model: [] for model in models}

    for i, scenario in enumerate(scenarios):
        for model, percentage in percentage_changes[scenario].items():
            values[model].append(np.mean(percentage))
            std_devs[model].append(np.std(percentage))

    index = np.arange(len(models))
    bar_width = 0.25
    colors = ['blue', 'green', 'red']
    legend_lines = []

    for i, scenario in enumerate(scenarios):
        scenario_values = [values[model][i] for model in models]
        scenario_std_devs = [std_devs[model][i] for model in models]

        line, = ax.plot([], [], marker='o', linestyle='', color=colors[i], label=scenario)

        ax.errorbar(
            index + i * bar_width,
            scenario_values,
            yerr=scenario_std_devs,
            fmt='o',
            color=colors[i],
            capsize=5,
            markersize=3,
            elinewidth=1
        )

        for k, model in enumerate(models):
            if significance_results[scenario][model] < 0.05:
                mid_x = index[k] + i * bar_width
                max_height = scenario_values[k] + scenario_std_devs[k]
                ax.annotate('*', xy=(mid_x, max_height), ha='center', va='bottom', fontsize=6)

        legend_lines.append(line)

    ax.axhline(y=0, linestyle='--', color='black', linewidth=0.5)

    if letter == '(a)':
        ax.set_ylabel('Rainfed rice yield change (%)')
    elif letter == '(c)':
        ax.set_ylabel('Irrigated rice yield change (%)')

    ax.set_title(title, loc='left')
    ax.set_xticks(index + bar_width * 1.5)
    ax.set_xticklabels(models, rotation=90)

    ax.text(0.01, 0.98, letter, transform=ax.transAxes, va='top', ha='left')

    if letter in ['(a)', '(b)']:
        ax.legend(
            handles=legend_lines,
            loc='lower right',
            bbox_to_anchor=(1.02, -0.05),
            markerscale=0.6,
            frameon=False,
            handletextpad=0.05
        )


def save_results_to_csv(
    percentage_changes,
    folder_paths,
    obs_file_paths,
    scenarios,
    titles,
    models_orders,
    filename_prefix,
    significance_results
):
    results_list = []

    for i, folder_path in enumerate(folder_paths):
        obs_mean = read_obs_data(obs_file_paths[i])

        for scenario in scenarios:
            for model, percentage in percentage_changes[scenario].items():
                mean_value = np.mean(percentage)
                std_dev = np.std(percentage)
                p_value = significance_results[scenario][model]

                results_list.append(
                    (
                        f"{model}_{scenario}",
                        mean_value,
                        std_dev,
                        p_value
                    )
                )

    results_df = pd.DataFrame(
        results_list,
        columns=[
            'Model_Scenario',
            'Mean_Value',
            'Std_Dev',
            'P_Value'
        ]
    )

    results_df.to_csv(f'{filename_prefix}.csv', index=False)
    if __name__ == "__main__":

        os.makedirs("figures", exist_ok=True)

        cmip5_folder_paths = [
            "data/yields_cmip5/Water_limited_yields_nCO2",
            "data/yields_cmip5/Potential_yields_nCO2"
        ]

        cmip5_obs_file_paths = [
            "data/Obs_Rainfed.csv",
            "data/Obs_Irrigated.csv"
        ]

        cmip5_scenarios = ['RCP26', 'RCP45', 'RCP85']
        cmip5_titles = ['CMIP5', 'CMIP5']

        cmip6_folder_paths = [
            "data/yields_cmip6/Water_limited_yields_nCO2",
            "data/yields_cmip6/Potential_yields_nCO2"
        ]

        cmip6_obs_file_paths = [
            "data/Obs_Rainfed.csv",
            "data/Obs_Irrigated.csv"
        ]

        cmip6_scenarios = ['SSP126', 'SSP245', 'SSP585']
        cmip6_titles = ['CMIP6', 'CMIP6']

        fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(5.5, 5.5))

        models_orders = {
            '(a)': ['MPI-ESM-LR', 'MIROC-ESM', 'HadGEM2-ES', 'IPSL-CM5A-LR', 'CNRM-CM5'],
            '(c)': ['MPI-ESM-LR', 'MIROC-ESM', 'HadGEM2-ES', 'IPSL-CM5A-LR', 'CNRM-CM5'],
            '(b)': ['MPI-ESM1-2-LR', 'MIROC6', 'UKESM1-0-LL', 'IPSL-CM6A-LR', 'CNRM-CM6-1'],
            '(d)': ['MPI-ESM1-2-LR', 'MIROC6', 'UKESM1-0-LL', 'IPSL-CM6A-LR', 'CNRM-CM6-1']
        }

        cmip5_rainfed_data_dict = read_csv_files(cmip5_folder_paths[0])
        cmip5_rainfed_obs_mean = read_obs_data(cmip5_obs_file_paths[0])
        cmip5_rainfed_percentage_changes = {}

        for scenario in cmip5_scenarios:
            model_yearly_yield = calculate_yearly_yield_per_model(cmip5_rainfed_data_dict, scenario)
            percentage_change = calculate_percentage_change(model_yearly_yield, cmip5_rainfed_obs_mean)
            cmip5_rainfed_percentage_changes[scenario] = percentage_change

        cmip5_irrigated_data_dict = read_csv_files(cmip5_folder_paths[1])
        cmip5_irrigated_obs_mean = read_obs_data(cmip5_obs_file_paths[1])
        cmip5_irrigated_percentage_changes = {}

        for scenario in cmip5_scenarios:
            model_yearly_yield = calculate_yearly_yield_per_model(cmip5_irrigated_data_dict, scenario)
            percentage_change = calculate_percentage_change(model_yearly_yield, cmip5_irrigated_obs_mean)
            cmip5_irrigated_percentage_changes[scenario] = percentage_change

        cmip5_significance_rainfed = perform_significance_test(
            cmip5_rainfed_percentage_changes,
            cmip5_scenarios
        )

        cmip5_significance_irrigated = perform_significance_test(
            cmip5_irrigated_percentage_changes,
            cmip5_scenarios
        )

        plot_yields_percentage_change(
            axes[0, 0],
            cmip5_rainfed_percentage_changes,
            cmip5_scenarios,
            cmip5_titles[0],
            '(a)',
            models_orders['(a)'],
            cmip5_significance_rainfed
        )

        axes[0, 0].set_ylim(-50, 15)

        plot_yields_percentage_change(
            axes[1, 0],
            cmip5_irrigated_percentage_changes,
            cmip5_scenarios,
            cmip5_titles[1],
            '(c)',
            models_orders['(c)'],
            cmip5_significance_irrigated
        )

        axes[1, 0].set_ylim(-30, 10)

        cmip6_rainfed_data_dict = read_csv_files(cmip6_folder_paths[0])
        cmip6_rainfed_obs_mean = read_obs_data(cmip6_obs_file_paths[0])
        cmip6_rainfed_percentage_changes = {}

        for scenario in cmip6_scenarios:
            model_yearly_yield = calculate_yearly_yield_per_model(cmip6_rainfed_data_dict, scenario)
            percentage_change = calculate_percentage_change(model_yearly_yield, cmip6_rainfed_obs_mean)
            cmip6_rainfed_percentage_changes[scenario] = percentage_change

        cmip6_irrigated_data_dict = read_csv_files(cmip6_folder_paths[1])
        cmip6_irrigated_obs_mean = read_obs_data(cmip6_obs_file_paths[1])
        cmip6_irrigated_percentage_changes = {}

        for scenario in cmip6_scenarios:
            model_yearly_yield = calculate_yearly_yield_per_model(cmip6_irrigated_data_dict, scenario)
            percentage_change = calculate_percentage_change(model_yearly_yield, cmip6_irrigated_obs_mean)
            cmip6_irrigated_percentage_changes[scenario] = percentage_change

        cmip6_significance_rainfed = perform_significance_test(
            cmip6_rainfed_percentage_changes,
            cmip6_scenarios
        )

        cmip6_significance_irrigated = perform_significance_test(
            cmip6_irrigated_percentage_changes,
            cmip6_scenarios
        )

        plot_yields_percentage_change(
            axes[0, 1],
            cmip6_rainfed_percentage_changes,
            cmip6_scenarios,
            cmip6_titles[0],
            '(b)',
            models_orders['(b)'],
            cmip6_significance_rainfed
        )

        axes[0, 1].set_ylim(-50, 20)

        plot_yields_percentage_change(
            axes[1, 1],
            cmip6_irrigated_percentage_changes,
            cmip6_scenarios,
            cmip6_titles[1],
            '(d)',
            models_orders['(d)'],
            cmip6_significance_irrigated
        )

        axes[1, 1].set_ylim(-40, 5)

        plt.subplots_adjust(
            left=0.1,
            bottom=0.18,
            right=0.95,
            top=0.95,
            wspace=0.2,
            hspace=0.70
        )

        plt.savefig("figures/yields_changes.png", dpi=600)
        plt.show()
