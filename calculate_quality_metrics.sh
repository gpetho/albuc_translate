# Extract aligned reference sentences from Spink & Lewis
cat eng/all_text.txt | python aligned_path_to_text.py 1 > aligned_sl_mt/spink_lewis.ref.txt

# Extract corresponding MT sentences from ChatGPT and Claude
cat chatgpt_occ/converted_all.txt | cut -f2 | python aligned_path_to_text.py  > aligned_sl_mt/chatgpt.mt.txt
cat claude_occ/sonnet_converted.txt | cut -f2 | python aligned_path_to_text.py  > aligned_sl_mt/claude.mt.txt

# for all other MT systems
for subdir in `ls translations`; do mkdir aligned_sl_mt/translations/$subdir; done
mkdir sacrebleu_output/translations
for subdir in `ls translations`; do mkdir sacrebleu_output/translations/$subdir; done

for subdir in `ls translations`; do
for mt_file in `ls translations/$subdir`; do
    cat translations/$subdir/$mt_file | cut -f2 | python aligned_path_to_text.py > aligned_sl_mt/translations/$subdir/$mt_file
done
done

cat aligned_sl_mt/chatgpt.mt.txt | sacrebleu aligned_sl_mt/spink_lewis.ref.txt -m bleu chrf ter --chrf-word-order 2 > sacrebleu_output/chatgpt.mt.txt.json
cat aligned_sl_mt/chatgpt.mt.txt | python calculate_parallel_metrics.py aligned_sl_mt/spink_lewis.ref.txt sacrebleu_output/chatgpt.mt.txt.json
cat aligned_sl_mt/chatgpt.mt.txt | python calculate_gpu_metrics.py aligned_sl_mt/spink_lewis.ref.txt sacrebleu_output/chatgpt.mt.txt.json

cat aligned_sl_mt/claude.mt.txt | sacrebleu aligned_sl_mt/spink_lewis.ref.txt -m bleu chrf ter --chrf-word-order 2 > sacrebleu_output/claude.mt.txt.json
cat aligned_sl_mt/claude.mt.txt | python calculate_parallel_metrics.py aligned_sl_mt/spink_lewis.ref.txt sacrebleu_output/claude.mt.txt.json
cat aligned_sl_mt/claude.mt.txt | python calculate_gpu_metrics.py aligned_sl_mt/spink_lewis.ref.txt sacrebleu_output/claude.mt.txt.json


find translations -name '*.txt' | parallel -j+0 --bar '
    cat aligned_sl_mt/{} | sacrebleu aligned_sl_mt/spink_lewis.ref.txt -m bleu chrf ter --chrf-word-order 2 > sacrebleu_output/{}.json
'

find translations -name '*.txt' | parallel -j+0 --bar '
    cat aligned_sl_mt/{} | python calculate_parallel_metrics.py aligned_sl_mt/spink_lewis.ref.txt sacrebleu_output/{}.json
'

for subdir in `ls translations` ; do
for mt_file in `ls translations/$subdir`; do
    cat aligned_sl_mt/translations/$subdir/$mt_file | python calculate_gpu_metrics.py aligned_sl_mt/spink_lewis.ref.txt sacrebleu_output/translations/$subdir/$mt_file.json
done
done
