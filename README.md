# Stich_gallery
## Training
The train_snip_and_stich.py script is used for training each of our models. It is accompanied by the train_example.sh script, which sets all the necessary arguments for training a complete model. The train_snip_and_stich.py file provides descriptions for each argument to ensure clarity.

Similarly, we use the train_text_inversion.py script for training normal text inversion. Although the files are almost identical, we separate them for better organization. The only distinction between the two is the prompts used to train the models.

# Generation
To generate inpainting pictures, we utilize the generating_inpainting.py script. Users are required to provide pictures and corresponding masks for the generation process. The generate_example.sh script includes a sample bash script that demonstrates how to generate pictures.

# Evaluation
For ranking inpainting photos, we employ the clip_ranking.py script. It calculates the top 20, 40, 60, 80, and 100 scores based on CLIP text similarity for each directory. Additionally, it provides the average ranking per directory and saves the images in ranked order to the specified output_path. An example bash script, clip_text_ranking.sh, is provided for running the evaluation.