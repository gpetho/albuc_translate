error_found=false; while IFS= read -r file; do [ "$(wc -l < "$file")" -ne 2806 ] && echo "File $file does not have exactly 2806 lines. It has $(wc -l < "$file") lines." && error_found=true; done < <(find aligned_sl_mt -type f); [ "$error_found" = false ] && echo "All files in the aligned_sl_mt directory and its subdirectories have exactly 2806 lines."

error_found=false; while IFS= read -r file; do [ "$(wc -l < "$file")" -ne 2173 ] && echo "File $file does not have exactly 2173 lines. It has $(wc -l < "$file") lines." && error_found=true; done < <(find aligned_sl_ara -type f); [ "$error_found" = false ] && echo "All files in the aligned_sl_ara directory and its subdirectories have exactly 2173 lines."

error_found=false; while IFS= read -r file; do [ "$(wc -l < "$file")" -ne 2881 ] && echo "File $file does not have exactly 2881 lines. It has $(wc -l < "$file") lines." && error_found=true; done < <(find aligned_sl_lat -type f); [ "$error_found" = false ] && echo "All files in the aligned_sl_lat directory and its subdirectories have exactly 2881 lines."

error_found=false; while IFS= read -r file; do [ "$(wc -l < "$file")" -ne 2517 ] && echo "File $file does not have exactly 2517 lines. It has $(wc -l < "$file") lines." && error_found=true; done < <(find aligned_sl_ofr -type f); [ "$error_found" = false ] && echo "All files in the aligned_sl_ofr directory and its subdirectories have exactly 2517 lines."

