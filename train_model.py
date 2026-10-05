# ==========================================
# MOODSENSE EMOTION MODEL TRAINING
# ==========================================

import os
import tensorflow as tf

from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras import layers, models


# ==========================================
# 1. PROJECT PATHS
# ==========================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

TRAIN_DIR = os.path.join(
    BASE_DIR,
    "fer2013",
    "train"
)

TEST_DIR = os.path.join(
    BASE_DIR,
    "fer2013",
    "test"
)

MODEL_DIR = os.path.join(
    BASE_DIR,
    "model"
)

MODEL_PATH = os.path.join(
    MODEL_DIR,
    "emotion_model.h5"
)


# ==========================================
# 2. CREATE MODEL FOLDER
# ==========================================

os.makedirs(
    MODEL_DIR,
    exist_ok=True
)


# ==========================================
# 3. IMAGE SETTINGS
# ==========================================

IMAGE_SIZE = (48, 48)

BATCH_SIZE = 64

EPOCHS = 20


# ==========================================
# 4. TRAINING DATA GENERATOR
# ==========================================

train_datagen = ImageDataGenerator(
    rescale=1.0 / 255.0,
    rotation_range=10,
    width_shift_range=0.1,
    height_shift_range=0.1,
    zoom_range=0.1,
    horizontal_flip=True
)


# ==========================================
# 5. TEST DATA GENERATOR
# ==========================================

test_datagen = ImageDataGenerator(
    rescale=1.0 / 255.0
)


# ==========================================
# 6. LOAD TRAINING DATA
# ==========================================

train_data = train_datagen.flow_from_directory(

    TRAIN_DIR,

    target_size=IMAGE_SIZE,

    color_mode="grayscale",

    batch_size=BATCH_SIZE,

    class_mode="categorical",

    shuffle=True
)


# ==========================================
# 7. LOAD TEST DATA
# ==========================================

test_data = test_datagen.flow_from_directory(

    TEST_DIR,

    target_size=IMAGE_SIZE,

    color_mode="grayscale",

    batch_size=BATCH_SIZE,

    class_mode="categorical",

    shuffle=False
)


# ==========================================
# 8. SHOW CLASS ORDER
# ==========================================

print("\nEmotion Class Mapping:")

print(
    train_data.class_indices
)


# ==========================================
# 9. CREATE CNN MODEL
# ==========================================

model = models.Sequential([

    layers.Input(
        shape=(48, 48, 1)
    ),

    layers.Conv2D(
        32,
        (3, 3),
        activation="relu"
    ),

    layers.BatchNormalization(),

    layers.MaxPooling2D(
        (2, 2)
    ),

    layers.Dropout(0.25),


    layers.Conv2D(
        64,
        (3, 3),
        activation="relu"
    ),

    layers.BatchNormalization(),

    layers.MaxPooling2D(
        (2, 2)
    ),

    layers.Dropout(0.25),


    layers.Conv2D(
        128,
        (3, 3),
        activation="relu"
    ),

    layers.BatchNormalization(),

    layers.MaxPooling2D(
        (2, 2)
    ),

    layers.Dropout(0.25),


    layers.Flatten(),


    layers.Dense(
        128,
        activation="relu"
    ),

    layers.Dropout(0.5),


    layers.Dense(
        7,
        activation="softmax"
    )

])


# ==========================================
# 10. COMPILE MODEL
# ==========================================

model.compile(

    optimizer="adam",

    loss="categorical_crossentropy",

    metrics=["accuracy"]

)


# ==========================================
# 11. DISPLAY MODEL
# ==========================================

model.summary()


# ==========================================
# 12. TRAIN MODEL
# ==========================================

print("\nStarting MoodSense emotion training...\n")


history = model.fit(

    train_data,

    validation_data=test_data,

    epochs=EPOCHS

)


# ==========================================
# 13. SAVE MODEL
# ==========================================

model.save(
    MODEL_PATH
)


print("\n==========================================")
print("MODEL TRAINING COMPLETED")
print("==========================================")

print(
    "\nModel saved at:"
)

print(
    MODEL_PATH
)