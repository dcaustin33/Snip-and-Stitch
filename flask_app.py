from flask import Flask, render_template, request
import random
import uuid
import os

app = Flask(__name__)

features = ['barnacles', 'coral', 'lichen', 'komondor', 'worms', 'ladybugs']

def get_image_paths(category):
    image_paths = []
    
    directory_of_images = os.listdir(f"static/{category}/composite_style")
    randint = random.randint(0, len(directory_of_images) - 1)
    image_suffix = directory_of_images[randint]
    image_path1 = f"static/{category}/composite_style/{image_suffix}"
    image_path2 = f"static/{category}/seg_style/{image_suffix}"
    image_path3 = f"static/{category}/composite_inversion/{image_suffix}"
    image_path4 = f"static/{category}/seg_inversion/{image_suffix}"
    return image_path1, image_path2, image_path3, image_path4



@app.route("/", methods=["GET", "POST"])
def index():
    category = random.choice(features)
    image_path1, image_path2, image_path3, image_path4 = get_image_paths(category)
    category_path = f'static/category/{category}.png'
    
    
    if request.method == "POST":
        selected_image = request.form.get("image")
        print(f"User selected image: {selected_image}")
        # Here you can save the selection to a database or file
        with open(f'static/results{uuid.uuid4()}.txt', 'w') as f:
            f.write(f'{selected_image}, {category}')
        f.close()
    # shuffle the images
    image_paths = [image_path1, image_path2, image_path3, image_path4]
    types = ['composite_style', 'seg_style', 'composite_inversion', 'seg_inversion']
    image_paths_types = list(zip(image_paths, types))
    random.shuffle(image_paths_types)
    
    return render_template("index.html", 
                           category = category,
                           selected_image=None, 
                           category_path=category_path,
                           image_path_1=image_paths_types[0][0],
                           image_path_2=image_paths_types[1][0],
                           image_path_3=image_paths_types[2][0],
                           image_path_4=image_paths_types[3][0],
                           image_paths_type1=image_paths_types[0][1],
                           image_paths_type2=image_paths_types[1][1],
                           image_paths_type3=image_paths_types[2][1],
                           image_paths_type4=image_paths_types[3][1])

if __name__ == "__main__":
    app.run(debug=True, port=7001)