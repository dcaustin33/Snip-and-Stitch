from flask import Flask, render_template, request
import random
import uuid
import os

app = Flask(__name__)

features = ['barnacles', 'coral', 'lichen', 'komondor', 'worms', 'ladybugs']

def get_image_paths(category):
    image_paths = []
    randint = random.randint(1, 40)
    directory_of_images = os.listdir(f"static/{category}/composite_style")
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
        with open(f'{uuid.uuid4()}.txt', 'w') as f:
            f.write(f'static/results/{selected_image}, {category}')
        f.close()
    print(category_path)
    return render_template("index.html", 
                           category = category,
                           selected_image=None, 
                           category_path=category_path,
                           image_path_1=image_path1,
                           image_path_2=image_path2,
                           image_path_3=image_path3,
                           image_path_4=image_path4)

if __name__ == "__main__":
    app.run(debug=True, port=7001)