import os

import tensorflow as tf

from tensorflow.keras import (
    layers,
    models
)

from tensorflow.keras.applications import (
    MobileNetV2
)


# -----------------------------
# SETTINGS
# -----------------------------

IMG_SIZE = (224, 224)

BATCH_SIZE = 32

EPOCHS = 10


# -----------------------------
# PROJECT PATH
# -----------------------------

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)


TRAIN_DIR = os.path.join(
    BASE_DIR,
    "dataset",
    "train"
)


VAL_DIR = os.path.join(
    BASE_DIR,
    "dataset",
    "validation"
)


MODEL_DIR = os.path.join(
    BASE_DIR,
    "model"
)


os.makedirs(
    MODEL_DIR,
    exist_ok=True
)


# -----------------------------
# LOAD DATASET
# -----------------------------

train_data = (

    tf.keras.utils
    .image_dataset_from_directory(

        TRAIN_DIR,

        image_size=IMG_SIZE,

        batch_size=BATCH_SIZE,

        shuffle=True

    )

)


validation_data = (

    tf.keras.utils
    .image_dataset_from_directory(

        VAL_DIR,

        image_size=IMG_SIZE,

        batch_size=BATCH_SIZE,

        shuffle=False

    )

)


class_names = train_data.class_names


print(
    "Classes:",
    class_names
)


# -----------------------------
# DATA AUGMENTATION
# -----------------------------

data_augmentation = (

    tf.keras.Sequential([

        layers.RandomFlip(
            "horizontal"
        ),

        layers.RandomRotation(
            0.1
        ),

        layers.RandomZoom(
            0.1
        )

    ])

)


# -----------------------------
# MOBILE NET V2
# -----------------------------

base_model = MobileNetV2(

    input_shape=(
        224,
        224,
        3
    ),

    include_top=False,

    weights="imagenet"

)


base_model.trainable = False


# -----------------------------
# MODEL
# -----------------------------

model = models.Sequential([

    layers.Input(
        shape=(
            224,
            224,
            3
        )
    ),

    data_augmentation,

    layers.Rescaling(
        1.0 / 127.5,
        offset=-1
    ),

    base_model,

    layers.GlobalAveragePooling2D(),

    layers.Dropout(0.3),

    layers.Dense(
        len(class_names),
        activation="softmax"
    )

])


# -----------------------------
# COMPILE
# -----------------------------

model.compile(

    optimizer="adam",

    loss=
    "sparse_categorical_crossentropy",

    metrics=["accuracy"]

)


model.summary()


# -----------------------------
# TRAIN
# -----------------------------

history = model.fit(

    train_data,

    validation_data=
    validation_data,

    epochs=EPOCHS

)


# -----------------------------
# SAVE MODEL
# -----------------------------

model_path = os.path.join(

    MODEL_DIR,

    "agriguard_model.keras"

)


model.save(model_path)


# -----------------------------
# SAVE CLASS NAMES
# -----------------------------

class_path = os.path.join(

    MODEL_DIR,

    "class_names.txt"

)


with open(
    class_path,
    "w"
) as file:

    for name in class_names:

        file.write(
            name + "\n"
        )


print(
    "\nTraining completed!"
)

print(
    "Model saved at:",
    model_path
)

print(
    "Classes saved at:",
    class_path
)