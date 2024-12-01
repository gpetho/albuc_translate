import ollama
import krippendorff
import numpy as np

num_raters = 4
max_items = 500  
model = "qwen2.5:32b"

with open("prompts/mt_analysis.txt") as f:
    prompt_analysis = f.read()

with open("prompts/mt_score.txt") as f:
    prompt_score = f.read()

with open("aligned_sl_lat/spink_lewis.ref.txt") as f:
    refs = f.read().splitlines()

with open("aligned_sl_lat/translations/aya/aya_0.txt") as f:
    hyps = f.read().splitlines()

fluency_ratings = []
accuracy_ratings = []

for i, (ref, hyp) in enumerate(zip(refs, hyps), start=1):
    print(f"Processing pair {i}")
    
    prompt_analysis_formatted = prompt_analysis.format(ref=ref, hyp=hyp)
    print("Analysis Prompt:")
    print(prompt_analysis_formatted)

    analysis_good = False
    while not analysis_good:
        response_analysis = ollama.generate(model=model, prompt=prompt_analysis_formatted)
        try:
            analysis = response_analysis['response'].strip()
            print(f"Analysis: {analysis}")
            analysis_good = True
        except:
            continue  

    prompt_score_formatted = prompt_score.format(ref=ref, hyp=hyp, analysis=analysis)
    print("Score Prompt:")
    print(prompt_score_formatted)

    fluency_ratings_item = []
    accuracy_ratings_item = []

    for rater in range(num_raters):
        good = False
        while not good:
            response_score = ollama.generate(model=model, prompt=prompt_score_formatted)
            
            try:
                response_text = response_score['response'].strip()
                print(f"Rater {rater + 1} response:\n {response_text}")
                
                fluency_line = next(line for line in response_text.split("\n") if line.strip().startswith("Fluency:"))
                accuracy_line = next(line for line in response_text.split("\n") if line.strip().startswith("Accuracy:"))
                
                fluency = int(fluency_line.split(":")[1].strip().lstrip('-').strip())
                accuracy = int(accuracy_line.split(":")[1].strip().lstrip('-').strip())
                
                assert fluency in range(1, 6)
                assert accuracy in range(1, 6)
                
                print(f"Fluency={fluency}, Accuracy={accuracy}")
                good = True
            except Exception as e:
                print(f"Error parsing the scores: {e}")
                continue

        fluency_ratings_item.append(fluency)
        accuracy_ratings_item.append(accuracy)

    fluency_ratings.append(fluency_ratings_item)
    accuracy_ratings.append(accuracy_ratings_item)

    if i >= max_items:
        break  

fluency_ratings_array = np.array(fluency_ratings)
accuracy_ratings_array = np.array(accuracy_ratings)

alpha_fluency = krippendorff.alpha(
    reliability_data=fluency_ratings_array.T,  
    level_of_measurement='ordinal'
)

alpha_accuracy = krippendorff.alpha(
    reliability_data=accuracy_ratings_array.T,  
    level_of_measurement='ordinal'
)

print(f"Krippendorff's alpha for fluency ratings: {alpha_fluency:.4f}")
print(f"Krippendorff's alpha for accuracy ratings: {alpha_accuracy:.4f}")
