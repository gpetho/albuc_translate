# Extract aligned reference sentences from Spink & Lewis
cat eng/all_text.txt | python aligned_path_to_text.py 1 occ > aligned_sl_occ/spink_lewis.ref.txt

# Extract corresponding MT sentences from ChatGPT and Claude
cat chatgpt_occ/converted_all.txt | cut -f2 | python aligned_path_to_text.py 0 occ > aligned_sl_occ/chatgpt.mt.txt
cat claude_occ/sonnet_converted.txt | cut -f2 | python aligned_path_to_text.py 0 occ > aligned_sl_occ/claude.mt.txt

# for all other MT systems
for subdir in `ls occ_translations`; do mkdir aligned_sl_occ/translations/$subdir; done
mkdir sacrebleu_output/translations
for subdir in `ls occ_translations`; do mkdir sacrebleu_output/translations/$subdir; done

for subdir in `ls occ_translations`; do
for mt_file in `ls occ_translations/$subdir`; do
    cat occ_translations/$subdir/$mt_file | cut -f2 | python aligned_path_to_text.py 0 occ > aligned_sl_occ/translations/$subdir/$mt_file
done
done

cat aligned_sl_occ/chatgpt.mt.txt | sacrebleu aligned_sl_occ/spink_lewis.ref.txt -m bleu chrf ter --chrf-word-order 2 > sacrebleu_output/chatgpt.mt.txt.json
cat aligned_sl_occ/chatgpt.mt.txt | python calculate_parallel_metrics.py aligned_sl_occ/spink_lewis.ref.txt sacrebleu_output/chatgpt.mt.txt.json
cat aligned_sl_occ/chatgpt.mt.txt | python calculate_gpu_metrics.py aligned_sl_occ/spink_lewis.ref.txt sacrebleu_output/chatgpt.mt.txt.json

cat aligned_sl_occ/claude.mt.txt | sacrebleu aligned_sl_occ/spink_lewis.ref.txt -m bleu chrf ter --chrf-word-order 2 > sacrebleu_output/claude.mt.txt.json
cat aligned_sl_occ/claude.mt.txt | python calculate_parallel_metrics.py aligned_sl_occ/spink_lewis.ref.txt sacrebleu_output/claude.mt.txt.json
cat aligned_sl_occ/claude.mt.txt | python calculate_gpu_metrics.py aligned_sl_occ/spink_lewis.ref.txt sacrebleu_output/claude.mt.txt.json


find occ_translations -name '*.txt' | sed 's/^occ_//' |  parallel -j+0 --bar '
    if [ ! -f sacrebleu_output_occ/{}.json ]; then
        cat aligned_sl_occ/{} | sacrebleu aligned_sl_occ/spink_lewis.ref.txt -m bleu chrf ter --chrf-word-order 2 > sacrebleu_output_occ/{}.json
    fi
'


find occ_translations -name '*.txt' | sed 's/^occ_//' |  parallel -j+0 --bar '
    cat aligned_sl_occ/{} | python calculate_parallel_metrics.py aligned_sl_occ/spink_lewis.ref.txt sacrebleu_output_occ/{}.json
'

calculate_gpu_metrics_batch.py occ
calculate_bertscore.py occ
