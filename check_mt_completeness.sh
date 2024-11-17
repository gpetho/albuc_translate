error_found=false; while IFS= read -r file; do [ "$(wc -l < "$file")" -ne 3096 ] && echo "File $file does not have exactly 3096 lines. It has $(wc -l < "$file") lines." && error_found=true; done < <(find occ_translations -type f); [ "$error_found" = false ] && echo "All files in the occ_translations directory and its subdirectories have exactly 3096 lines."

error_found=false; while IFS= read -r file; do [ "$(wc -l < "$file")" -ne 2343 ] && echo "File $file does not have exactly 2343 lines. It has $(wc -l < "$file") lines." && error_found=true; done < <(find ara_translations -type f); [ "$error_found" = false ] && echo "All files in the ara_translations directory and its subdirectories have exactly 2343 lines."

error_found=false; while IFS= read -r file; do [ "$(wc -l < "$file")" -ne 4055 ] && echo "File $file does not have exactly 4055 lines. It has $(wc -l < "$file") lines." && error_found=true; done < <(find lat_translations -type f); [ "$error_found" = false ] && echo "All files in the lat_translations directory and its subdirectories have exactly 4055 lines."

error_found=false; while IFS= read -r file; do [ "$(wc -l < "$file")" -ne 3621 ] && echo "File $file does not have exactly 3621 lines. It has $(wc -l < "$file") lines." && error_found=true; done < <(find ofr_translations -type f); [ "$error_found" = false ] && echo "All files in the ofr_translations directory and its subdirectories have exactly 3621 lines."

