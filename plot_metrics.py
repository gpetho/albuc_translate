import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import os
import json

metrics = ['BLEU', 'chrF2++', 'TER', 'NIST', 'METEOR',
           'rouge1', 'rouge2', 'rougeL', 'BLEURT']

model_order_by_size = ['phi3_3.8b', 'gemma_7b', 'mistral_7b', 'qwen2_7b',
                       'aya_8b', 'llama3_8b',  'gemma2_9b', 'phi3_14b',
                       'mixtral_8x7b', 'aya_35b', 'llama3_70b',
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
                    scores[item['name']].append(item['score'])
    return scores


def plot_scores(all_scores, model_order_by_size):
    fig, axes = plt.subplots(3, 3, figsize=(18, 18))  # 3 rows, 3 columns for a 3x3 grid
    
    bar_width = 0.35
    opacity = 0.8
    
    # Ensure the order of subdirs according to model_order_by_size
    ordered_subdirs = [subdir for subdir in model_order_by_size
                       if subdir in all_scores]
    
    for i, metric in enumerate(metrics):
        row, col = divmod(i, 3)  # Determine the subplot's row and column
        means = [np.mean(all_scores[subdir][metric])
                 for subdir in ordered_subdirs]
        variances = [np.var(all_scores[subdir][metric])
                     for subdir in ordered_subdirs]
        index = np.arange(len(ordered_subdirs))
        
        axes[row, col].bar(index, means, bar_width, alpha=opacity, label=metric, yerr=variances, capsize=5)
        axes[row, col].set_xlabel('Subdirectory')
        axes[row, col].set_ylabel('Scores')
        axes[row, col].set_title(f'{metric} Scores by Subdirectory')
        axes[row, col].set_xticks(index)
        axes[row, col].set_xticklabels(ordered_subdirs, rotation=90, fontsize='small')
        axes[row, col].legend()
    
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
            all_scores['gemma2_9b'] = extract_scores(scores_dir, '9b')
        elif subdir == 'llama3':
            all_scores['llama3_8b'] = extract_scores(scores_dir, '8b')
            all_scores['llama3_70b'] = extract_scores(scores_dir, '70b')
        elif subdir == 'mistral':
            all_scores['mistral_7b'] = extract_scores(scores_dir)
        elif subdir == 'mixtral':
            all_scores['mixtral_8x7b'] = extract_scores(scores_dir)
        elif subdir == 'qwen2':
            all_scores['qwen2_7b'] = extract_scores(scores_dir)
        # else:
        #     all_scores[subdir] = extract_scores(scores_dir)

    plot_scores(all_scores, model_order_by_size)


if __name__ == "__main__":
    main()