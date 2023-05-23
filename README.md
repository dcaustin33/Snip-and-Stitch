# Stich_gallery
## Training
train_snip_and_stich.py is what is used to train each of our models. It has an associated train_example.sh
which sets all arguments needed to train a full model. The python file provides a descripition of 
each argument as well for clarity.
train_text_inversion.py is what is used to train normal text inversion. The files are virtually 
identical however we separate them for clarity THe only difference between the two are the 
prompts used to train the models.

# Generation
generating_inpainting.py is a script used to generate inpainting pictures. Users need to provide
pictures as well as masks over which to generate. generate_example.sh has an example bash script
needed to generate pictures.

# Evaluation
clip_ranking.py is a script used to rank many inpainting photos providing the top 20, 40, 60, 80, 100
scores per directory as well as the average ranking per directory. The thought is that files for a given
model will be in a single directory. It also saves the images in ranked order to the output_path
provided. clip_text_ranking.sh provides an example bash script to run evaluation.