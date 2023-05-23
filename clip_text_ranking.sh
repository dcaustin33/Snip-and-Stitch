
python3 clip_ranking.py \
    --generated_image_paths \
        './individual_token_per_image/coral/all_generations/ml_people/' \
        './individual_token_per_image/coral/all_generations/all_people/' \
    --prompt 'A man with a beard made of coral' \
    --output_path './individual_token_per_image/coral/all_generations/ranked_people';