export NUM_IMAGES_TO_GENERATE=50
export DEVICE='cuda:0'

python3 generate_inpainting_for_multiple_pics.py \
    --prompt "A picture of a person with hair in the style of <color>" \
    --model_path path_to_model \
    --image_paths \
        'generation_pics/hair_pics/hair0.png' \
        'generation_pics/hair_pics/hair1.png' \
        'generation_pics/hair_pics/hair2.png' \
        'generation_pics/hair_pics/hair3.png' \
        'generation_pics/hair_pics/hair4.png' \
        'generation_pics/hair_pics/hair5.png' \
        'generation_pics/hair_pics/hair6.png' \
        'generation_pics/hair_pics/hair7.png' \
    --mask_paths \
        'generation_pics/hair_masks/hair_mask0.png' \
        'generation_pics/hair_masks/hair_mask1.png' \
        'generation_pics/hair_masks/hair_mask2.png' \
        'generation_pics/hair_masks/hair_mask3.png' \
        'generation_pics/hair_masks/hair_mask4.png' \
        'generation_pics/hair_masks/hair_mask5.png' \
        'generation_pics/hair_masks/hair_mask6.png' \
        'generation_pics/hair_masks/hair_mask7.png' \
    --output_path komondor/all_generations/model_3_generations/ \
    --num_images_to_generate $NUM_IMAGES_TO_GENERATE \
    --device $DEVICE;