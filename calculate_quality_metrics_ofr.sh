# Extract aligned reference sentences from Spink & Lewis
cat eng_to_ofr/all_text.txt | python aligned_path_to_text.py 1 > aligned_sl_ofr/spink_lewis.ref.txt

# Extract corresponding MT sentences from ChatGPT and Claude
cat chatgpt_ofr/converted_all.txt | cut -f2 | python aligned_path_to_text.py 0 ofr > aligned_sl_ofr/chatgpt.mt.txt
cat claude_occ/sonnet_converted.txt | cut -f2 | python aligned_path_to_text.py 0 ofr > aligned_sl_ofr/claude.mt.txt

mkdir sacrebleu_output_ofr
mkdir aligned_sl_ofr/translations
# for all other MT systems
for subdir in `ls ofr_translations`; do mkdir aligned_sl_ofr/translations/$subdir; done
mkdir sacrebleu_output_ofr/translations
for subdir in `ls ofr_translations`; do mkdir sacrebleu_output_ofr/translations/$subdir; done

for subdir in `ls ofr_translations`; do
for mt_file in `ls ofr_translations/$subdir`; do
    cat ofr_translations/$subdir/$mt_file | cut -f2 | python aligned_path_to_text.py 0 ofr > aligned_sl_ofr/translations/$subdir/$mt_file
done
done

cat aligned_sl_ofr/chatgpt.mt.txt | sacrebleu aligned_sl_ofr/spink_lewis.ref.txt -m bleu chrf ter --chrf-word-order 2 > sacrebleu_output_ofr/chatgpt.mt.txt.json
cat aligned_sl_ofr/chatgpt.mt.txt | python calculate_parallel_metrics.py aligned_sl_ofr/spink_lewis.ref.txt sacrebleu_output_ofr/chatgpt.mt.txt.json
cat aligned_sl_ofr/chatgpt.mt.txt | python calculate_gpu_metrics.py aligned_sl_ofr/spink_lewis.ref.txt sacrebleu_output_ofr/chatgpt.mt.txt.json

cat aligned_sl_ofr/claude.mt.txt | sacrebleu aligned_sl_ofr/spink_lewis.ref.txt -m bleu chrf ter --chrf-word-order 2 > sacrebleu_output_ofr/claude.mt.txt.json
cat aligned_sl_ofr/claude.mt.txt | python calculate_parallel_metrics.py aligned_sl_ofr/spink_lewis.ref.txt sacrebleu_output_ofr/claude.mt.txt.json
cat aligned_sl_ofr/claude.mt.txt | python calculate_gpu_metrics.py aligned_sl_ofr/spink_lewis.ref.txt sacrebleu_output_ofr/claude.mt.txt.json


find ofr_translations -name '*.txt' | parallel -j+0 --bar '
    cat aligned_sl_ofr/{} | sacrebleu aligned_sl_ofr/spink_lewis.ref.txt -m bleu chrf ter --chrf-word-order 2 > sacrebleu_output_ofr/{}.json
'

find ofr_translations -name '*.txt' | parallel -j+0 --bar '
    cat aligned_sl_ofr/{} | python calculate_parallel_metrics.py aligned_sl_ofr/spink_lewis.ref.txt sacrebleu_output_ofr/{}.json
'

for subdir in `ls ofr_translations` ; do
for mt_file in `ls ofr_translations/$subdir`; do
    cat aligned_sl_ofr/ofr_translations/$subdir/$mt_file | python calculate_gpu_metrics.py aligned_sl_ofr/spink_lewis.ref.txt sacrebleu_output_ofr/ofr_translations/$subdir/$mt_file.json
done
done


ls ofr_translations/mistral_nemo | parallel -j+0 --bar '
    cat aligned_sl_ofr/ofr_translations/mistral_nemo/{} | python calculate_parallel_metrics.py aligned_sl_ofr/spink_lewis.ref.txt sacrebleu_output_ofr/ofr_translations/mistral_nemo/{}.json
'
for subdir in `ls ofr_translations` ; do
for mt_file in `ls ofr_translations/$subdir`; do
    cat aligned_sl_ofr/ofr_translations/$subdir/$mt_file | python calculate_gpu_metrics.py aligned_sl_ofr/spink_lewis.ref.txt sacrebleu_output_ofr/ofr_translations/$subdir/$mt_file.json
done
done


for subdir in llama3 llama3_1 mistral ; do
for mt_file in `ls ofr_translations/$subdir`; do
    cat aligned_sl_ofr/ofr_translations/$subdir/$mt_file | python calculate_gpu_metrics.py aligned_sl_ofr/spink_lewis.ref.txt sacrebleu_output_ofr/ofr_translations/$subdir/$mt_file.json
done
done
