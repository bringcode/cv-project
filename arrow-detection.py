from roboflow import Roboflow
rf = Roboflow(api_key="7sg8pwBao1WlyoAmuk3W")
project = rf.workspace().project("direction_detect")
model = project.version(1).model

# infer on a local image
print(model.predict("imgs/arrow.png", confidence=5, overlap=30).json())

# visualize your prediction
# model.predict("imgs/arrow.png", confidence=5, overlap=30).save("prediction.jpg")