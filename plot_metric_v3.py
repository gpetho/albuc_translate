import matplotlib.pyplot as plt
import os
import sys
from pathlib import Path
import numpy as np
import json

if len(sys.argv) < 2:
    legend_language = "eng"
else:
    legend_language = sys.argv[1]

plot_filename = 'plot_scores_ddhum.png'

eval_languages = [
    'occ',
    'ofr',
    # 'ara',
    # 'lat'
]

lang_colour = {
    'occ': 'blue',
    'ofr': 'red',
    'ara': 'green',
    'lat': 'orange'
}

metrics = ['BLEU',
           'NIST', 'METEOR',
#           'chrF2++',
           'TER', 
            'rouge1',
           'rouge2',  
# 'rougeL',
           'BLEURT', 'BERTScore'
           ]

lang_labels = {
    'eng': {
        'occ': 'Old Occitan',
        'ofr': 'Old French',
        'ara': 'Arabic',
        'lat': 'Latin'},
    'hun': {
        'occ': 'Óokcitán',
        'ofr': 'Ófrancia',
        'ara': 'Arab',
        'lat': 'Latin'},
    }

legend_labels = {
    'eng': {
        'score': 'Score',
        'model': 'Model',
        'score_by_model': '{} Score by Model',
    },
    'hun': {
        'score': 'Érték',
        'model': 'Modell',
        'score_by_model': 'Modellek {} értéke',
    }
}
model_to_size = {
    'granite3-dense': 2, 'llama3.2': 3, 'nemotron-mini': 4, 'phi3': 4,
    'phi3.5': 4, 'mistral': 7, 'qwen2': 7, 'qwen2.5': 7, 'aya': 8,
    'aya-expanse': 8, 'granite3-dense_8b': 8, 'llama3': 8, 'llama3.1': 8,
    'gemini-1.5-flash-8b': 8, 'gemma': 9, 'gemma2': 9, 'mistral-nemo': 12,
    'phi3_14b': 14, 'qwen2.5_14b': 14, 'mistral-small': 22, 'gemma2_27b': 27,
    'qwen2.5_32b': 32, 'aya_35b': 35, 'command-r': 35, 'mixtral': 56,
    'llama3_70b-instruct-q2_K': 70, 'gemini-1.5-flash-002': 0,
    'gemini-1.5-pro-002': 0, 'claude_3.5_sonnet': 0, 'chatGPT_GPT4o': 0}

model_display_name = {
    'granite3-dense': 'Granite3 Dense 2b', 'llama3.2': 'Llama3.2 3b',
    'nemotron-mini': 'Nemotron-Mini 4b', 'phi3': 'Phi-3 3.8b',
    'phi3.5': 'Phi-3.5 3.8b', 'mistral': 'Mistral 7b', 'qwen2': 'Qwen2 7b',
    'qwen2.5': 'Qwen2.5 7b', 'aya': 'Aya 8b', 'aya-expanse': 'Aya Expanse 8b',
    'granite3-dense_8b': 'Granite3 Dense 8b', 'llama3': 'Llama 3 8b',
    'llama3.1': 'Llama 3.1 8b', 'gemma': 'Gemma 9b', 'gemma2': 'Gemma 2 9b',
    'gemini-1.5-flash-8b': 'Gemini 1.5 Flash-8b',
    'mistral-nemo': 'Mistral Nemo 12b', 'phi3_14b': 'Phi-3 14b',
    'qwen2.5_14b': 'Qwen2.5 14b', 'mistral-small': 'Mistral-Small 22b',
    'gemma2_27b': 'Gemma 2 27b', 'qwen2.5_32b': 'Qwen2.5 32b',
    'aya_35b': 'Aya 35b', 'command-r': 'Command-R 35b',
    'mixtral': 'Mixtral 8x7b', 'llama3_70b-instruct-q2_K': 'Llama 3 70b',
    'gemini-1.5-flash-002': 'Gemini 1.5 Flash',
    'gemini-1.5-pro-002': 'Gemini 1.5 Pro',
    'claude_3.5_sonnet': 'Claude 3.5 Sonnet', 'chatGPT_GPT4o': 'GPT-4o'}


model_order_by_size = [
    'granite3-dense', 'llama3.2', 'nemotron-mini', 'phi3', 'phi3.5', 
    'mistral', 'qwen2', 'qwen2.5', 'aya', 'aya-expanse',
    'granite3-dense_8b', 'llama3', 'llama3.1', 'gemma', 'gemma2',
    'gemini-1.5-flash-8b', 'mistral-nemo', 'phi3_14b', 'qwen2.5_14b', 
    'mistral-small', 'gemma2_27b', 'qwen2.5_32b', 'aya_35b',
    'command-r', 'mixtral', 'llama3_70b-instruct-q2_K',
    'gemini-1.5-flash-002', 'gemini-1.5-pro-002', 'claude_3.5_sonnet',
    'chatGPT_GPT4o']


def extract_scores(directory, filter=None):
    # filter for file names that contain the substring "filter"
    scores = {metric_name: [] for metric_name in metrics}
    if not os.path.exists(directory):
        return None
    for filename in os.listdir(directory):
        if filename.endswith('.json') and (filter is None
                                           or filter in filename):
            with open(directory / filename, 'r') as file:
                try:
                    data = json.load(file)
                    for item in data:
                        if item['name'] in scores:
                            scores[item['name']].append(item['score'])
                except json.JSONDecodeError:
                    print(f"Warning: Failed to decode JSON from {filename}. Skipping this file.")
                    continue
    return scores

def plot_scores(all_scores_dict, model_order_by_size):
    n_metrics = len(metrics)
    n_cols = 2  # Set to 1 column
    n_rows = int(n_metrics / n_cols) # Set to one row per plot
    fig_width = len(eval_languages) * 10  # Adjust width according to number of languages
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(fig_width, 5 * n_rows))  # Adjust rows and columns
    axes = axes.flatten() if n_metrics > 1 else [axes]  # Flatten axes array if more than one plot
    
    bar_width = 0.2
    opacity = 0.8
    
    # Ensure the order of subdirs according to model_order_by_size
    ordered_subdirs = []
    for subdir in model_order_by_size:
        if all([subdir in lang_subdirs for lang_subdirs in all_scores_dict.values()]):
            ordered_subdirs.append(subdir)
#    ordered_subdirs = [subdir for subdir in model_order_by_size if subdir in all_scores_occ and subdir in all_scores_ofr and subdir in all_scores_ara and subdir in all_scores_lat]
    
    for i, metric in enumerate(metrics):
        means = {lang: [] for lang in eval_languages}
        variances = {lang: [] for lang in eval_languages}

        for subdir in ordered_subdirs:
#            print(subdir)
            for lang in eval_languages:
                try:
                    if (subdir in all_scores_dict[lang]
                        and metric in all_scores_dict[lang][subdir]
                        and all_scores_dict[lang][subdir][metric]):
                        means[lang].append(np.mean(all_scores_dict[lang][subdir][metric]))
                        variances[lang].append(np.var(all_scores_dict[lang][subdir][metric]))
                    else:
                        means[lang].append(np.nan)
                        variances[lang].append(np.nan)

                except IndexError:
                    for lang in eval_languages:
                        means[lang].append(np.nan)
                        variances[lang].append(np.nan)
        
        index = np.arange(len(ordered_subdirs)) * (len(eval_languages) * bar_width + 0.2)

        data_max = max(max(means[lang]) for lang in eval_languages)
        print(data_max)

        if len(eval_languages) == 4:
            offsets = [-1.5, -0.5, 0.5, 1.5]
        else:
            offsets = [-0.5, 0.5]
        
        for offset, lang in zip(offsets, eval_languages):
            axes[i].bar(index + offset * bar_width,
                        means[lang], bar_width, alpha=1,
                        label=lang_labels[legend_language][lang],
                        yerr=variances[lang], capsize=5,
                        color=lang_colour[lang])

        ax = axes[i]
        # Save the original y-axis limits
        y_min, y_max = ax.get_ylim()
        print(y_min, y_max)

        # Add horizontal guides
        y_ticks = ax.get_yticks()
        print(y_ticks)

        for j in range(len(y_ticks) - 1):
            ax.axhspan(y_ticks[j], y_ticks[j + 1], facecolor='lightgrey' if j % 2 == 0 else 'white', alpha=0.5)

        for offset, lang in zip(offsets, eval_languages):
            axes[i].bar(index + offset * bar_width,
                        means[lang], bar_width, alpha=1,
                        yerr=variances[lang], capsize=5,
                        color=lang_colour[lang])

        axes[i].set_xlabel(legend_labels[legend_language]['model'])
        axes[i].set_ylabel(legend_labels[legend_language]['score'])
        if metric == 'rouge2':
            metric = 'ROUGE-2'
        axes[i].set_title(legend_labels[legend_language]['score_by_model'].format(metric))
        axes[i].set_xticks(index)
        display_names = [model_display_name[subdir]
                         for subdir in ordered_subdirs]
        axes[i].set_xticklabels(display_names, rotation=90, fontsize='small')

    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc='upper left', ncol=4, fontsize='large')
        
    plt.tight_layout()
    plt.savefig(plot_filename, dpi=300, bbox_inches='tight')
    plt.show()


lang_dir = {lang: Path(f'sacrebleu_output_{lang}') for lang in eval_languages}

all_scores_dict = {lang: {} for lang in eval_languages}

for lang in eval_languages:
    all_scores_dict[lang]['chatGPT_GPT4o'] = extract_scores(lang_dir[lang], 'chatgpt')
    all_scores_dict[lang]['claude_3.5_sonnet'] = extract_scores(lang_dir[lang], 'claude')

subdirs = [
    'aya', 'aya_35b', 'aya-expanse', 'command-r',
    'gemini-1.5-flash-002', 'gemini-1.5-flash-8b', 'gemini-1.5-pro-002',
    'gemma', 'gemma2', 'gemma2_27b', 'granite3-dense', 'granite3-dense_8b',
    'llama3', 'llama3_70b-instruct-q2_K', 'llama3.1', 'llama3.2', 'mistral',
    'mistral-nemo', 'mistral-small', 'mixtral', 'nemotron-mini', 'phi3',
    'phi3_14b', 'phi3.5', 'qwen2', 'qwen2.5', 'qwen2.5_14b', 'qwen2.5_32b']

for subdir in subdirs:
    scores_dir = {lang: lang_dir[lang] / 'translations' / subdir for lang in eval_languages}
    for lang in eval_languages:
        all_scores_dict[lang][subdir] = extract_scores(scores_dir[lang]) or {}

plot_scores(all_scores_dict, model_order_by_size)
