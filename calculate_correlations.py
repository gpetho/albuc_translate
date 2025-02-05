import json
import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import pearsonr, spearmanr

from plot_metric_v3 import metrics, model_to_size, eval_languages, model_to_date

data = []

models = [m for m in model_to_size if model_to_size[m] not in (0, 70)]

print(models)

for lang in eval_languages:
    for model in models:
        for n in range(10):
            try:
                fname = f"sacrebleu_output_{lang}/translations/{model}/{model}_{n}.txt.json"
#                print(fname)
                with open(fname) as f:
                    bad_score = False
                    json_data = json.load(f)
                    scores = {}
                    for data_dict in json_data:
                        if type(data_dict["score"]) != float:
                            print("Bad score:", data_dict["name"], data_dict["score"], fname)
                            bad_score = True
                        scores[data_dict["name"]] = data_dict["score"]
                    if bad_score:
                        continue
                    metric_values = [scores[metric] for metric in metrics]
                    data.append([math.log(model_to_size[model]), model_to_date[model], lang, *metric_values])
            except FileNotFoundError:
                continue

df = pd.DataFrame(data, columns=["size", "date", "lang", *metrics])

metric = "rouge2"

for lang in eval_languages:
    df_lang = df[df["lang"] == lang]

    # Extract only "size", "date" and metric columns
    df_lang = df_lang[["size", "date", metric]]

    sns.pairplot(df_lang)  # Use seaborn for easy pair plots
    plt.suptitle('Pairwise Scatter Plots', y=1.02) # Adjust title position

    # save plot to file
    plt.savefig(f'pairplot_{lang}.png')

    # plot just metric vs size
    plt.figure()
    sns.scatterplot(data=df_lang, x='size', y=metric)
    plt.title(f"{metric} vs. Size ({lang})")
    plt.xlabel("Size (log scale)")
    plt.ylabel(metric)

    # save plot to file
    plt.savefig(f'size_vs_{metric}_{lang}.png')

    # 2. Correlation Calculations
    pearson_corr = df_lang.corr(method='pearson')
    spearman_corr = df_lang.corr(method='spearman')

    print(f"Pearson Correlation {lang}:")
    print(pearson_corr)

    print(f"\nSpearman Correlation {lang}:")
    print(spearman_corr)

    # 3. Correlation with p-values (optional, but good practice)

    pearson_size_score = pearsonr(df_lang['size'], df_lang[metric])
    pearson_date_score = pearsonr(df_lang['date'], df_lang[metric])
    spearman_size_score = spearmanr(df_lang['size'], df_lang[metric])
    spearman_date_score = spearmanr(df_lang['date'], df_lang[metric])

    print("\nPearson Correlation (with p-values):")
    print(f"Size vs. Score:  Correlation = {pearson_size_score[0]:.3f}, p-value = {pearson_size_score[1]:.3f}")
    print(f"Date vs. Score:  Correlation = {pearson_date_score[0]:.3f}, p-value = {pearson_date_score[1]:.3f}")

    print("\nSpearman Correlation (with p-values):")
    print(f"Size vs. Score:  Correlation = {spearman_size_score[0]:.3f}, p-value = {spearman_size_score[1]:.3f}")
    print(f"Date vs. Score:  Correlation = {spearman_date_score[0]:.3f}, p-value = {spearman_date_score[1]:.3f}")

num_metrics = len(metrics)
num_data_points = len(df_lang)

# extract only the metrics columns
df = df[metrics]

# 1. Calculate Correlation Matrices
pearson_corr = df.corr(method='pearson')
spearman_corr = df.corr(method='spearman')

# 2. Create Heatmaps

plt.figure(figsize=(10, 8))  # Adjust figure size as needed

# Mask the upper triangle for better visualization (optional)
mask = np.triu(np.ones_like(pearson_corr, dtype=bool))  # Create mask
sns.heatmap(pearson_corr, annot=True, cmap="coolwarm", fmt=".2f", mask=mask)  # Use mask
plt.title("Pearson Correlation Heatmap")

# save plot to file
plt.savefig('pearson_corr_heatmap.png')

plt.figure(figsize=(10, 8))
mask = np.triu(np.ones_like(spearman_corr, dtype=bool))
sns.heatmap(spearman_corr, annot=True, cmap="coolwarm", fmt=".2f", mask=mask)
plt.title("Spearman Correlation Heatmap")

# save plot to file
plt.savefig('spearman_corr_heatmap.png')
