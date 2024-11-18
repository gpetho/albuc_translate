import matplotlib.pyplot as plt
import os
from pathlib import Path
import numpy as np
import json

metrics = ['BLEU', 'chrF2++', 'TER', 'NIST', 'METEOR',
           'rouge1', 'rouge2',
#           'rougeL',
           'BLEURT', 'BERTScore']

model_order_by_size = ['phi3_3.8b', 'mistral_7b', 'qwen2_7b', 'aya_8b',
                       'llama3_8b', 'llama3_1_8b', 'gemma_7b', 'gemma2_9b',
                       'mistral_nemo_12b', 'phi3_14b', 'aya_35b',
                        'mixtral_8x7b', 'llama3_70b',
                       'claude_sonnet_3.5', 'chatGPT_GPT4o']


def extract_scores(directory, filter=None):
    # filter for file names that contain the substring "filter"
    scores = {metric_name: [] for metric_name in metrics}
    for filename in os.listdir(directory):
        if filename.endswith('.json') and (filter is None
                                           or filter in filename):
            with open(directory / filename, 'r') as file:
                data = json.load(file)
                for item in data:
                    if item['name'] in scores:
                        scores[item['name']].append(item['score'])
    return scores

def plot_scores(all_scores_occ, all_scores_ofr, model_order_by_size):
    n_metrics = len(metrics)
    fig, axes = plt.subplots(3, 3, figsize=(18, 18))  # 3 rows, 3 columns for a 3x3 grid
    
    bar_width = 0.35
    opacity = 0.8
    
    # Ensure the order of subdirs according to model_order_by_size
    ordered_subdirs = [subdir for subdir in model_order_by_size if subdir in all_scores_occ and subdir in all_scores_ofr]
    
    for i, metric in enumerate(metrics):
        row, col = divmod(i, 3)  # Determine the subplot's row and column
        means_occ = []
        variances_occ = []
        means_ofr = []
        variances_ofr = []
        for subdir in ordered_subdirs:
            try:
                means_occ.append(np.mean(all_scores_occ[subdir][metric]))
                variances_occ.append(np.var(all_scores_occ[subdir][metric]))
            except IndexError:
                means_occ.append(0)
                variances_occ.append(0)

            try:
                means_ofr.append(np.mean(all_scores_ofr[subdir][metric]))
                variances_ofr.append(np.var(all_scores_ofr[subdir][metric]))
            except IndexError:
                means_ofr.append(0)
                variances_ofr.append(0)
        
        index = np.arange(len(ordered_subdirs))
        
        try:
            axes[row, col].bar(index - bar_width/2, means_occ, bar_width, alpha=opacity, label='Occitan', yerr=variances_occ, capsize=5, color='blue')
        except ValueError:
            print(f"{means_occ=}")
            print(f"{variances_occ=}")
        
        axes[row, col].bar(index + bar_width/2, means_ofr, bar_width, alpha=opacity, label='French', yerr=variances_ofr, capsize=5, color='red')
        axes[row, col].set_xlabel('Model')
        axes[row, col].set_ylabel('Scores')
        axes[row, col].set_title(f'{metric} Scores by Model')
        axes[row, col].set_xticks(index)
        axes[row, col].set_xticklabels(ordered_subdirs, rotation=90, fontsize='small')
        axes[row, col].legend()
    
    plt.tight_layout()
    plt.savefig('plot_scores_v2.png', dpi=300, bbox_inches='tight')
    plt.show()

# Example usage
occ_dir = Path('sacrebleu_output_occ')
ofr_dir = Path('sacrebleu_output_ofr')

all_scores_occ = {}
all_scores_occ['chatGPT_GPT4o'] = extract_scores(occ_dir, 'chatgpt')
all_scores_occ['claude_sonnet_3.5'] = extract_scores(occ_dir, 'claude')

all_scores_ofr = {}
all_scores_ofr['chatGPT_GPT4o'] = extract_scores(ofr_dir, 'chatgpt')
all_scores_ofr['claude_sonnet_3.5'] = extract_scores(ofr_dir, 'claude')

subdirs = ['aya', 'phi3', 'gemma', 'gemma2', 'llama3', 'llama3_1', 'mistral', 'mistral_nemo', 'mixtral', 'qwen2']

for subdir in subdirs:
    scores_dir_occ = occ_dir / 'translations' / subdir
    scores_dir_ofr = ofr_dir / 'ofr_translations' / subdir
    if subdir == 'aya':
        all_scores_occ['aya_8b'] = extract_scores(scores_dir_occ, '8b')
        all_scores_ofr['aya_8b'] = extract_scores(scores_dir_ofr, '8b')
        all_scores_occ['aya_35b'] = extract_scores(scores_dir_occ, '35b')
        all_scores_ofr['aya_35b'] = extract_scores(scores_dir_ofr, '35b')
    if subdir == 'phi3':
        all_scores_occ['phi3_3.8b'] = extract_scores(scores_dir_occ, '3.8b')
        all_scores_ofr['phi3_3.8b'] = extract_scores(scores_dir_ofr, '3.8b')
        all_scores_occ['phi3_14b'] = extract_scores(scores_dir_occ, '14b')
        all_scores_ofr['phi3_14b'] = extract_scores(scores_dir_ofr, '14b')
    elif subdir == 'gemma':
        all_scores_occ['gemma_7b'] = extract_scores(scores_dir_occ)
        all_scores_ofr['gemma_7b'] = extract_scores(scores_dir_ofr)
    elif subdir == 'gemma2':
        all_scores_occ['gemma2_9b'] = extract_scores(scores_dir_occ, '9b')
        all_scores_ofr['gemma2_9b'] = extract_scores(scores_dir_ofr, '9b')
    elif subdir == 'llama3':
        all_scores_occ['llama3_8b'] = extract_scores(scores_dir_occ, '8b')
        all_scores_ofr['llama3_8b'] = extract_scores(scores_dir_ofr, '8b')
        all_scores_occ['llama3_70b'] = extract_scores(scores_dir_occ, '70b')
        all_scores_ofr['llama3_70b'] = extract_scores(scores_dir_ofr, '70b')
    elif subdir == 'llama3_1':
        all_scores_occ['llama3_1_8b'] = extract_scores(scores_dir_occ)
        all_scores_ofr['llama3_1_8b'] = extract_scores(scores_dir_ofr)
    elif subdir == 'mistral':
        all_scores_occ['mistral_7b'] = extract_scores(scores_dir_occ)
        all_scores_ofr['mistral_7b'] = extract_scores(scores_dir_ofr)
    elif subdir == 'mistral_nemo':
        all_scores_occ['mistral_nemo_12b'] = extract_scores(scores_dir_occ)
        all_scores_ofr['mistral_nemo_12b'] = extract_scores(scores_dir_ofr)
    elif subdir == 'mixtral':
        all_scores_occ['mixtral_8x7b'] = extract_scores(scores_dir_occ)
        all_scores_ofr['mixtral_8x7b'] = extract_scores(scores_dir_ofr)
    elif subdir == 'qwen2':
        all_scores_occ['qwen2_7b'] = extract_scores(scores_dir_occ)
        all_scores_ofr['qwen2_7b'] = extract_scores(scores_dir_ofr)

print(all_scores_ofr)

plot_scores(all_scores_occ, all_scores_ofr, model_order_by_size)