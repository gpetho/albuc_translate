mkdir aligned_sl_ara

# Extract aligned reference sentences from Spink & Lewis
cat eng/all_text.txt | python aligned_path_to_text.py 1 lat > aligned_sl_ara/spink_lewis.ref.txt

# Extract corresponding MT sentences from ChatGPT and Claude
cat chatgpt_ara/converted.txt | cut -f2 | python aligned_path_to_text.py 0 ara  > aligned_sl_ara/chatgpt.mt.txt
cat claude_ara/claude_ara.txt | python aligned_path_to_text.py 0 ara > aligned_sl_ara/claude.mt.txt

mkdir aligned_sl_ara/translations
# for all other MT systems
for subdir in `ls ara_translations`; do mkdir aligned_sl_ara/translations/$subdir; done
mkdir sacrebleu_output_ara
mkdir sacrebleu_output_ara/translations
for subdir in `ls ara_translations`; do mkdir sacrebleu_output_ara/translations/$subdir; done

for subdir in `ls ara_translations`; do
for mt_file in `ls ara_translations/$subdir`; do
    cat ara_translations/$subdir/$mt_file | cut -f2 | python aligned_path_to_text.py 0 lat > aligned_sl_ara/translations/$subdir/$mt_file
done
done

cat aligned_sl_ara/chatgpt.mt.txt | sacrebleu aligned_sl_ara/spink_lewis.ref.txt -m bleu chrf ter --chrf-word-order 2 > sacrebleu_output_ara/chatgpt.mt.txt.json
cat aligned_sl_ara/chatgpt.mt.txt | python calculate_parallel_metrics.py aligned_sl_ara/spink_lewis.ref.txt sacrebleu_output_ara/chatgpt.mt.txt.json
cat aligned_sl_ara/chatgpt.mt.txt | python calculate_gpu_metrics.py aligned_sl_ara/spink_lewis.ref.txt sacrebleu_output_ara/chatgpt.mt.txt.json

cat aligned_sl_ara/claude.mt.txt | sacrebleu aligned_sl_ara/spink_lewis.ref.txt -m bleu chrf ter --chrf-word-order 2 > sacrebleu_output_ara/claude.mt.txt.json
cat aligned_sl_ara/claude.mt.txt | python calculate_parallel_metrics.py aligned_sl_ara/spink_lewis.ref.txt sacrebleu_output_ara/claude.mt.txt.json
cat aligned_sl_ara/claude.mt.txt | python calculate_gpu_metrics.py aligned_sl_ara/spink_lewis.ref.txt sacrebleu_output_ara/claude.mt.txt.json


find ara_translations -name '*.txt' | sed 's/^lat_//' | parallel -j+0 --bar '
    cat aligned_sl_ara/{} | sacrebleu aligned_sl_ara/spink_lewis.ref.txt -m bleu chrf ter --chrf-word-order 2 > sacrebleu_output_ara/{}.json
'

find ara_translations -name '*.txt' | sed 's/^lat_//' | parallel -j+0 --bar '
    cat aligned_sl_ara/{} | python calculate_parallel_metrics.py aligned_sl_ara/spink_lewis.ref.txt sacrebleu_output_ara/{}.json
'

for subdir in `ls ara_translations` ; do
for mt_file in `ls ara_translations/$subdir`; do
    cat aligned_sl_ara/translations/$subdir/$mt_file | python calculate_gpu_metrics.py aligned_sl_ara/spink_lewis.ref.txt sacrebleu_output_ara/translations/$subdir/$mt_file.json
done
done
