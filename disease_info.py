DISEASE_INFO = {

    "Tomato_Early_Blight": {

        "disease": "Tomato Early Blight",

        "severity": "Medium",

        "cause": "Fungal infection",

        "solution":
        "Remove infected leaves, maintain proper spacing, "
        "avoid excess moisture and use recommended fungicide."
    },


    "Tomato_Late_Blight": {

        "disease": "Tomato Late Blight",

        "severity": "High",

        "cause": "Phytophthora-like pathogen",

        "solution":
        "Remove severely affected leaves and plants. "
        "Improve air circulation and use recommended treatment."
    },


    "Tomato_Healthy": {

        "disease": "Healthy Tomato Leaf",

        "severity": "Low",

        "cause": "No visible disease detected",

        "solution":
        "Continue regular monitoring, proper irrigation "
        "and balanced plant nutrition."
    }

}


def get_disease_info(class_name):

    return DISEASE_INFO.get(

        class_name,

        {

            "disease": class_name,

            "severity": "Unknown",

            "cause": "Information unavailable",

            "solution":
            "Please consult an agricultural expert."

        }

    )