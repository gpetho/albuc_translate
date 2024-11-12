mkdir aligned_sl_lat

# Extract aligned reference sentences from Spink & Lewis
cat eng/all_text.txt | python aligned_path_to_text.py 1 lat > aligned_sl_lat/spink_lewis.ref.txt

# Extract corresponding MT sentences from ChatGPT and Claude
cat chatgpt_lat/combined.txt | cut -f2 | python aligned_path_to_text.py 0 lat  > aligned_sl_lat/chatgpt.mt.txt
cat claude_lat/sonnet_converted.txt | cut -f2 | python aligned_path_to_text.py 0 lat > aligned_sl_lat/claude.mt.txt

mkdir aligned_sl_lat/translations
# for all other MT systems
for subdir in `ls lat_translations`; do mkdir aligned_sl_lat/translations/$subdir; done
mkdir sacrebleu_output_lat
mkdir sacrebleu_output_lat/translations
for subdir in `ls lat_translations`; do mkdir sacrebleu_output_lat/translations/$subdir; done

for subdir in `ls lat_translations`; do
for mt_file in `ls lat_translations/$subdir`; do
    cat lat_translations/$subdir/$mt_file | cut -f2 | python aligned_path_to_text.py 0 lat > aligned_sl_lat/translations/$subdir/$mt_file
done
done

cat aligned_sl_lat/chatgpt.mt.txt | sacrebleu aligned_sl_lat/spink_lewis.ref.txt -m bleu chrf ter --chrf-word-order 2 > sacrebleu_output_lat/chatgpt.mt.txt.json
cat aligned_sl_lat/chatgpt.mt.txt | python calculate_parallel_metrics.py aligned_sl_lat/spink_lewis.ref.txt sacrebleu_output_lat/chatgpt.mt.txt.json
cat aligned_sl_lat/chatgpt.mt.txt | python calculate_gpu_metrics.py aligned_sl_lat/spink_lewis.ref.txt sacrebleu_output_lat/chatgpt.mt.txt.json

cat aligned_sl_lat/claude.mt.txt | sacrebleu aligned_sl_lat/spink_lewis.ref.txt -m bleu chrf ter --chrf-word-order 2 > sacrebleu_output_lat/claude.mt.txt.json
cat aligned_sl_lat/claude.mt.txt | python calculate_parallel_metrics.py aligned_sl_lat/spink_lewis.ref.txt sacrebleu_output_lat/claude.mt.txt.json
cat aligned_sl_lat/claude.mt.txt | python calculate_gpu_metrics.py aligned_sl_lat/spink_lewis.ref.txt sacrebleu_output_lat/claude.mt.txt.json


find lat_translations -name '*.txt' | sed 's/^lat_//' | parallel -j+0 --bar '
    cat aligned_sl_lat/{} | sacrebleu aligned_sl_lat/spink_lewis.ref.txt -m bleu chrf ter --chrf-word-order 2 > sacrebleu_output_lat/{}.json
'

find lat_translations -name '*.txt' | sed 's/^lat_//' | parallel -j+0 --bar '
    cat aligned_sl_lat/{} | python calculate_parallel_metrics.py aligned_sl_lat/spink_lewis.ref.txt sacrebleu_output_lat/{}.json
'

for subdir in `ls lat_translations` ; do
for mt_file in `ls lat_translations/$subdir`; do
    cat aligned_sl_lat/translations/$subdir/$mt_file | python calculate_gpu_metrics.py aligned_sl_lat/spink_lewis.ref.txt sacrebleu_output_lat/translations/$subdir/$mt_file.json
done
done
