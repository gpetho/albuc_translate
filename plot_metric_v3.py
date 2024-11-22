import matplotlib.pyplot as plt
import os
import sys
from pathlib import Path
import numpy as np
import json

if len(sys.argv) < 2:
    language = "eng"
else:
    language = sys.argv[1]

metrics = ['BLEU', 'NIST', 'METEOR', 'rouge2',  
#           'chrF2++', 'TER', 'rouge1', 'rougeL',
           'BLEURT', 'BERTScore']

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

def plot_scores(all_scores_occ, all_scores_ofr, all_scores_ara, all_scores_lat, model_order_by_size):
    n_metrics = len(metrics)
    n_rows = n_metrics  # Set to one row per plot
    n_cols = 1  # Set to 1 column
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(18, 5 * n_rows))  # Adjust rows and columns
    axes = axes.flatten() if n_metrics > 1 else [axes]  # Flatten axes array if more than one plot
    
    bar_width = 0.2
    opacity = 0.8
    
    # Ensure the order of subdirs according to model_order_by_size
    ordered_subdirs = [subdir for subdir in model_order_by_size if subdir in all_scores_occ and subdir in all_scores_ofr and subdir in all_scores_ara and subdir in all_scores_lat]
    
    for i, metric in enumerate(metrics):
        means_occ, variances_occ = [], []
        means_ofr, variances_ofr = [], []
        means_ara, variances_ara = [], []
        means_lat, variances_lat = [], []
        
        for subdir in ordered_subdirs:
#            print(subdir)
            try:
                if subdir in all_scores_occ and metric in all_scores_occ[subdir] and all_scores_occ[subdir][metric]:
                    means_occ.append(np.mean(all_scores_occ[subdir][metric]))
                    variances_occ.append(np.var(all_scores_occ[subdir][metric]))
                else:
                    means_occ.append(np.nan)
                    variances_occ.append(np.nan)

                if subdir in all_scores_ofr and metric in all_scores_ofr[subdir] and all_scores_ofr[subdir][metric]:
                    means_ofr.append(np.mean(all_scores_ofr[subdir][metric]))
                    variances_ofr.append(np.var(all_scores_ofr[subdir][metric]))
                else:
                    means_ofr.append(np.nan)
                    variances_ofr.append(np.nan)
                
                if subdir in all_scores_ara and metric in all_scores_ara[subdir] and all_scores_ara[subdir][metric]:
                    means_ara.append(np.mean(all_scores_ara[subdir][metric]))
                    variances_ara.append(np.var(all_scores_ara[subdir][metric]))
                else:
                    means_ara.append(np.nan)
                    variances_ara.append(np.nan)
                
                if subdir in all_scores_lat and metric in all_scores_lat[subdir] and all_scores_lat[subdir][metric]:
                    means_lat.append(np.mean(all_scores_lat[subdir][metric]))
                    variances_lat.append(np.var(all_scores_lat[subdir][metric]))
                else:
                    means_lat.append(np.nan)
                    variances_lat.append(np.nan)
            except IndexError:
                means_occ.append(np.nan)
                variances_occ.append(np.nan)
                means_ofr.append(np.nan)
                variances_ofr.append(np.nan)
                means_ara.append(np.nan)
                variances_ara.append(np.nan)
                means_lat.append(np.nan)
                variances_lat.append(np.nan)
        
        index = np.arange(len(ordered_subdirs))
        
        axes[i].bar(index - 1.5 * bar_width, means_occ, bar_width, alpha=opacity, label=lang_labels[language]['occ'], yerr=variances_occ, capsize=5, color='blue')
        axes[i].bar(index - 0.5 * bar_width, means_ofr, bar_width, alpha=opacity, label=lang_labels[language]['ofr'], yerr=variances_ofr, capsize=5, color='red')
        axes[i].bar(index + 0.5 * bar_width, means_ara, bar_width, alpha=opacity, label=lang_labels[language]['ara'], yerr=variances_ara, capsize=5, color='green')
        axes[i].bar(index + 1.5 * bar_width, means_lat, bar_width, alpha=opacity, label=lang_labels[language]['lat'], yerr=variances_lat, capsize=5, color='orange')
        
        axes[i].set_xlabel(legend_labels[language]['model'])
        axes[i].set_ylabel(legend_labels[language]['score'])
        if metric == 'rouge2':
            metric = 'ROUGE-2'
        axes[i].set_title(legend_labels[language]['score_by_model'].format(metric))
        axes[i].set_xticks(index)
        display_names = [model_display_name[subdir]
                         for subdir in ordered_subdirs]
        axes[i].set_xticklabels(display_names, rotation=90, fontsize='small')

    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc='upper left', ncol=4, fontsize='large')
        
    plt.tight_layout()
    plt.savefig('plot_scores_v3.png', dpi=300, bbox_inches='tight')
    plt.show()

occ_dir = Path('sacrebleu_output_occ')
ofr_dir = Path('sacrebleu_output_ofr')
ara_dir = Path('sacrebleu_output_ara')
lat_dir = Path('sacrebleu_output_lat')

all_scores_occ = {}
all_scores_ofr = {}
all_scores_ara = {}
all_scores_lat = {}

all_scores_occ['chatGPT_GPT4o'] = extract_scores(occ_dir, 'chatgpt')
all_scores_ofr['chatGPT_GPT4o'] = extract_scores(ofr_dir, 'chatgpt')
all_scores_ara['chatGPT_GPT4o'] = extract_scores(ara_dir, 'chatgpt')
all_scores_lat['chatGPT_GPT4o'] = extract_scores(lat_dir, 'chatgpt')

all_scores_occ['claude_3.5_sonnet'] = extract_scores(occ_dir, 'claude')
all_scores_ofr['claude_3.5_sonnet'] = extract_scores(ofr_dir, 'claude')
all_scores_ara['claude_3.5_sonnet'] = extract_scores(ara_dir, 'claude')
all_scores_lat['claude_3.5_sonnet'] = extract_scores(lat_dir, 'claude')


subdirs = [
    'aya', 'aya_35b', 'aya-expanse', 'command-r',
    'gemini-1.5-flash-002', 'gemini-1.5-flash-8b', 'gemini-1.5-pro-002',
    'gemma', 'gemma2', 'gemma2_27b', 'granite3-dense', 'granite3-dense_8b',
    'llama3', 'llama3_70b-instruct-q2_K', 'llama3.1', 'llama3.2', 'mistral',
    'mistral-nemo', 'mistral-small', 'mixtral', 'nemotron-mini', 'phi3',
    'phi3_14b', 'phi3.5', 'qwen2', 'qwen2.5', 'qwen2.5_14b', 'qwen2.5_32b']

for subdir in subdirs:
    scores_dir_occ = occ_dir / 'translations' / subdir
    scores_dir_ofr = ofr_dir / 'translations' / subdir
    scores_dir_ara = ara_dir / 'translations' / subdir
    scores_dir_lat = lat_dir / 'translations' / subdir
    if subdir == 'aya':
        all_scores_occ['aya'] = extract_scores(scores_dir_occ) or {}
        all_scores_ofr['aya'] = extract_scores(scores_dir_ofr) or {}
        all_scores_ara['aya'] = extract_scores(scores_dir_ara) or {}
        all_scores_lat['aya'] = extract_scores(scores_dir_lat) or {}
    elif subdir == 'aya_35b':
        all_scores_occ['aya_35b'] = extract_scores(scores_dir_occ) or {}
        all_scores_ofr['aya_35b'] = extract_scores(scores_dir_ofr) or {}
        all_scores_ara['aya_35b'] = extract_scores(scores_dir_ara) or {}
        all_scores_lat['aya_35b'] = extract_scores(scores_dir_lat) or {}
    elif subdir == 'aya-expanse':
        all_scores_occ['aya-expanse'] = extract_scores(scores_dir_occ) or {}
        all_scores_ofr['aya-expanse'] = extract_scores(scores_dir_ofr) or {}
        all_scores_ara['aya-expanse'] = extract_scores(scores_dir_ara) or {}
        all_scores_lat['aya-expanse'] = extract_scores(scores_dir_lat) or {}
    elif subdir == 'command-r':
        all_scores_occ['command-r'] = extract_scores(scores_dir_occ) or {}
        all_scores_ofr['command-r'] = extract_scores(scores_dir_ofr) or {}
        all_scores_ara['command-r'] = extract_scores(scores_dir_ara) or {}
        all_scores_lat['command-r'] = extract_scores(scores_dir_lat) or {}
    elif subdir == 'gemini-1.5-flash-002':
        all_scores_occ['gemini-1.5-flash-002'] = extract_scores(scores_dir_occ) or {}
        all_scores_ofr['gemini-1.5-flash-002'] = extract_scores(scores_dir_ofr) or {}
        all_scores_ara['gemini-1.5-flash-002'] = extract_scores(scores_dir_ara) or {}
        all_scores_lat['gemini-1.5-flash-002'] = extract_scores(scores_dir_lat) or {}
    elif subdir == 'gemini-1.5-flash-8b':
        all_scores_occ['gemini-1.5-flash-8b'] = extract_scores(scores_dir_occ) or {}
        all_scores_ofr['gemini-1.5-flash-8b'] = extract_scores(scores_dir_ofr) or {}
        all_scores_ara['gemini-1.5-flash-8b'] = extract_scores(scores_dir_ara) or {}
        all_scores_lat['gemini-1.5-flash-8b'] = extract_scores(scores_dir_lat) or {}
    elif subdir == 'gemini-1.5-pro-002':
        all_scores_occ['gemini-1.5-pro-002'] = extract_scores(scores_dir_occ) or {}
        all_scores_ofr['gemini-1.5-pro-002'] = extract_scores(scores_dir_ofr) or {}
        all_scores_ara['gemini-1.5-pro-002'] = extract_scores(scores_dir_ara) or {}
        all_scores_lat['gemini-1.5-pro-002'] = extract_scores(scores_dir_lat) or {}
    elif subdir == 'gemma':
        all_scores_occ['gemma'] = extract_scores(scores_dir_occ) or {}
        all_scores_ofr['gemma'] = extract_scores(scores_dir_ofr) or {}
        all_scores_ara['gemma'] = extract_scores(scores_dir_ara) or {}
        all_scores_lat['gemma'] = extract_scores(scores_dir_lat) or {}
    elif subdir == 'gemma2':
        all_scores_occ['gemma2'] = extract_scores(scores_dir_occ) or {}
        all_scores_ofr['gemma2'] = extract_scores(scores_dir_ofr) or {}
        all_scores_ara['gemma2'] = extract_scores(scores_dir_ara) or {}
        all_scores_lat['gemma2'] = extract_scores(scores_dir_lat) or {}
    elif subdir == 'gemma2_27b':
        all_scores_occ['gemma2_27b'] = extract_scores(scores_dir_occ) or {}
        all_scores_ofr['gemma2_27b'] = extract_scores(scores_dir_ofr) or {}
        all_scores_ara['gemma2_27b'] = extract_scores(scores_dir_ara) or {}
        all_scores_lat['gemma2_27b'] = extract_scores(scores_dir_lat) or {}
    elif subdir == 'granite3-dense':
        all_scores_occ['granite3-dense'] = extract_scores(scores_dir_occ) or {}
        all_scores_ofr['granite3-dense'] = extract_scores(scores_dir_ofr) or {}
        all_scores_ara['granite3-dense'] = extract_scores(scores_dir_ara) or {}
        all_scores_lat['granite3-dense'] = extract_scores(scores_dir_lat) or {}
    elif subdir == 'granite3-dense_8b':
        all_scores_occ['granite3-dense_8b'] = extract_scores(scores_dir_occ) or {}
        all_scores_ofr['granite3-dense_8b'] = extract_scores(scores_dir_ofr) or {}
        all_scores_ara['granite3-dense_8b'] = extract_scores(scores_dir_ara) or {}
        all_scores_lat['granite3-dense_8b'] = extract_scores(scores_dir_lat) or {}
    elif subdir == 'llama3':
        all_scores_occ['llama3'] = extract_scores(scores_dir_occ) or {}
        all_scores_ofr['llama3'] = extract_scores(scores_dir_ofr) or {}
        all_scores_ara['llama3'] = extract_scores(scores_dir_ara) or {}
        all_scores_lat['llama3'] = extract_scores(scores_dir_lat) or {}
    elif subdir == 'llama3_70b-instruct-q2_K':
        all_scores_occ['llama3_70b-instruct-q2_K'] = extract_scores(scores_dir_occ) or {}
        all_scores_ofr['llama3_70b-instruct-q2_K'] = extract_scores(scores_dir_ofr) or {}
        all_scores_ara['llama3_70b-instruct-q2_K'] = extract_scores(scores_dir_ara) or {}
        all_scores_lat['llama3_70b-instruct-q2_K'] = extract_scores(scores_dir_lat) or {}
    elif subdir == 'llama3.1':
        all_scores_occ['llama3.1'] = extract_scores(scores_dir_occ) or {}
        all_scores_ofr['llama3.1'] = extract_scores(scores_dir_ofr) or {}
        all_scores_ara['llama3.1'] = extract_scores(scores_dir_ara) or {}
        all_scores_lat['llama3.1'] = extract_scores(scores_dir_lat) or {}
    elif subdir == 'llama3.2':
        all_scores_occ['llama3.2'] = extract_scores(scores_dir_occ) or {}
        all_scores_ofr['llama3.2'] = extract_scores(scores_dir_ofr) or {}
        all_scores_ara['llama3.2'] = extract_scores(scores_dir_ara) or {}
        all_scores_lat['llama3.2'] = extract_scores(scores_dir_lat) or {}
    elif subdir == 'mistral':
        all_scores_occ['mistral'] = extract_scores(scores_dir_occ) or {}
        all_scores_ofr['mistral'] = extract_scores(scores_dir_ofr) or {}
        all_scores_ara['mistral'] = extract_scores(scores_dir_ara) or {}
        all_scores_lat['mistral'] = extract_scores(scores_dir_lat) or {}
    elif subdir == 'mistral-nemo':
        all_scores_occ['mistral-nemo'] = extract_scores(scores_dir_occ) or {}
        all_scores_ofr['mistral-nemo'] = extract_scores(scores_dir_ofr) or {}
        all_scores_ara['mistral-nemo'] = extract_scores(scores_dir_ara) or {}
        all_scores_lat['mistral-nemo'] = extract_scores(scores_dir_lat) or {}
    elif subdir == 'mistral-small':
        all_scores_occ['mistral-small'] = extract_scores(scores_dir_occ) or {}
        all_scores_ofr['mistral-small'] = extract_scores(scores_dir_ofr) or {}
        all_scores_ara['mistral-small'] = extract_scores(scores_dir_ara) or {}
        all_scores_lat['mistral-small'] = extract_scores(scores_dir_lat) or {}
    elif subdir == 'mixtral':
        all_scores_occ['mixtral'] = extract_scores(scores_dir_occ) or {}
        all_scores_ofr['mixtral'] = extract_scores(scores_dir_ofr) or {}
        all_scores_ara['mixtral'] = extract_scores(scores_dir_ara) or {}
        all_scores_lat['mixtral'] = extract_scores(scores_dir_lat) or {}
    elif subdir == 'nemotron-mini':
        all_scores_occ['nemotron-mini'] = extract_scores(scores_dir_occ) or {}
        all_scores_ofr['nemotron-mini'] = extract_scores(scores_dir_ofr) or {}
        all_scores_ara['nemotron-mini'] = extract_scores(scores_dir_ara) or {}
        all_scores_lat['nemotron-mini'] = extract_scores(scores_dir_lat) or {}
    elif subdir == 'phi3':
        all_scores_occ['phi3'] = extract_scores(scores_dir_occ) or {}
        all_scores_ofr['phi3'] = extract_scores(scores_dir_ofr) or {}
        all_scores_ara['phi3'] = extract_scores(scores_dir_ara) or {}
        all_scores_lat['phi3'] = extract_scores(scores_dir_lat) or {}
    elif subdir == 'phi3_14b':
        all_scores_occ['phi3_14b'] = extract_scores(scores_dir_occ) or {}
        all_scores_ofr['phi3_14b'] = extract_scores(scores_dir_ofr) or {}
        all_scores_ara['phi3_14b'] = extract_scores(scores_dir_ara) or {}
        all_scores_lat['phi3_14b'] = extract_scores(scores_dir_lat) or {}
    elif subdir == 'phi3.5':
        all_scores_occ['phi3.5'] = extract_scores(scores_dir_occ) or {}
        all_scores_ofr['phi3.5'] = extract_scores(scores_dir_ofr) or {}
        all_scores_ara['phi3.5'] = extract_scores(scores_dir_ara) or {}
        all_scores_lat['phi3.5'] = extract_scores(scores_dir_lat) or {}
    elif subdir == 'qwen2':
        all_scores_occ['qwen2'] = extract_scores(scores_dir_occ) or {}
        all_scores_ofr['qwen2'] = extract_scores(scores_dir_ofr) or {}
        all_scores_ara['qwen2'] = extract_scores(scores_dir_ara) or {}
        all_scores_lat['qwen2'] = extract_scores(scores_dir_lat) or {}
    elif subdir == 'qwen2.5':
        all_scores_occ['qwen2.5'] = extract_scores(scores_dir_occ) or {}
        all_scores_ofr['qwen2.5'] = extract_scores(scores_dir_ofr) or {}
        all_scores_ara['qwen2.5'] = extract_scores(scores_dir_ara) or {}
        all_scores_lat['qwen2.5'] = extract_scores(scores_dir_lat) or {}
    elif subdir == 'qwen2.5_14b':
        all_scores_occ['qwen2.5_14b'] = extract_scores(scores_dir_occ) or {}
        all_scores_ofr['qwen2.5_14b'] = extract_scores(scores_dir_ofr) or {}
        all_scores_ara['qwen2.5_14b'] = extract_scores(scores_dir_ara) or {}
        all_scores_lat['qwen2.5_14b'] = extract_scores(scores_dir_lat) or {}
    elif subdir == 'qwen2.5_32b':
        all_scores_occ['qwen2.5_32b'] = extract_scores(scores_dir_occ) or {}
        all_scores_ofr['qwen2.5_32b'] = extract_scores(scores_dir_ofr) or {}
        all_scores_ara['qwen2.5_32b'] = extract_scores(scores_dir_ara) or {}
        all_scores_lat['qwen2.5_32b'] = extract_scores(scores_dir_lat) or {}

plot_scores(all_scores_occ, all_scores_ofr, all_scores_ara, all_scores_lat, model_order_by_size)
