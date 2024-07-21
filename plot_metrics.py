import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import os
import json

model_order_by_size = ['phi3_3.8b', 'gemma_7b', 'mistral_7b', 'qwen2_7b',
                       'aya_8b', 'llama3_8b',  'gemma_9b', 'phi3_14b',
                       'mixtral_8x7b', 'aya_35b',
                       'claude_sonnet_3.5', 'chatGPT_GPT4o']


def extract_scores(directory, filter=None):
    # filter for file names that contain the substring "filter"
    scores = {'BLEU': [], 'chrF2++': [], 'TER': []}
    for filename in os.listdir(directory):
        if filename.endswith('.json') and (filter is None
                                           or filter in filename):
            with open(directory / filename, 'r') as file:
                data = json.load(file)
                for item in data:
                    if item['name'] == 'BLEU':
                        scores['BLEU'].append(item['score'])
                    elif item['name'] == 'chrF2++':
                        scores['chrF2++'].append(item['score'])
                    elif item['name'] == 'TER':
                        scores['TER'].append(item['score'])
    return scores


def plot_scores(all_scores, model_order_by_size):
    metrics = ['BLEU', 'chrF2++', 'TER']
    n_metrics = len(metrics)
    fig, axes = plt.subplots(1, n_metrics, figsize=(15, 5))  # 1 row, n_metrics columns
    
    bar_width = 0.35
    opacity = 0.8
    
    # Ensure the order of subdirs according to model_order_by_size
    ordered_subdirs = [subdir for subdir in model_order_by_size if subdir in all_scores]
    
    for i, metric in enumerate(metrics):
        means = [np.mean(all_scores[subdir][metric]) for subdir in ordered_subdirs]
        variances = [np.var(all_scores[subdir][metric]) for subdir in ordered_subdirs]
        index = np.arange(len(ordered_subdirs))
        
        axes[i].bar(index, means, bar_width, alpha=opacity, label=metric, yerr=variances, capsize=5)
        axes[i].set_xlabel('Subdirectory')
        axes[i].set_ylabel('Scores')
        axes[i].set_title(f'{metric} Scores by Subdirectory')
        axes[i].set_xticks(index)
        axes[i].set_xticklabels(ordered_subdirs, rotation=90, fontsize='small')
        axes[i].legend()
    
    plt.tight_layout()
    plt.savefig('plot_scores.png', dpi=300, bbox_inches='tight')
    plt.show()


def main():
    base_dir = Path('translations')
    outputs_dir = Path('sacrebleu_output')
    all_scores = {}
    all_scores['chatGPT_GPT4o'] = extract_scores(outputs_dir, 'chatgpt')
    all_scores['claude_sonnet_3.5'] = extract_scores(outputs_dir, 'claude')
    for subdir in os.listdir(base_dir):
        scores_dir = outputs_dir / base_dir / subdir
        if subdir == 'aya':
            all_scores['aya_8b'] = extract_scores(scores_dir, '8b')
            all_scores['aya_35b'] = extract_scores(scores_dir, '35b')
        elif subdir == 'phi3':
            all_scores['phi3_3.8b'] = extract_scores(scores_dir, '3.8b')
            all_scores['phi3_14b'] = extract_scores(scores_dir, '14b')
        elif subdir == 'gemma':
            all_scores['gemma_7b'] = extract_scores(scores_dir)
        elif subdir == 'gemma2':
            all_scores['gemma_9b'] = extract_scores(scores_dir)
        elif subdir == 'llama3':
            all_scores['llama3_8b'] = extract_scores(scores_dir, '8b')
#            all_scores['phi3_14b'] = extract_scores(scores_dir, '14b')
        elif subdir == 'mistral':
            all_scores['mistral_7b'] = extract_scores(scores_dir)
        elif subdir == 'mixtral':
            all_scores['mixtral_8x7b'] = extract_scores(scores_dir)
        elif subdir == 'qwen2':
            all_scores['qwen2_7b'] = extract_scores(scores_dir)
        # else:
        #     all_scores[subdir] = extract_scores(scores_dir)

    print(len(all_scores))
    plot_scores(all_scores, model_order_by_size)


if __name__ == "__main__":
    main()