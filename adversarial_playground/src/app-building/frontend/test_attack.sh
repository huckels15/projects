curl \
-X POST \
-H "Authorization: Bearer ya29.c.c0ASRK0GaqQt0Fkz9-ityLJmz7MfzZbu74opiVCR5l4jKRufGIO_KqmA7I75VigyNCnkY61mhm77XWGpvTus0wxbPMq_ruAxKWDY6qY_gMgzV-ld3OOv_UacqAnNP792EXse8MN15QmRb6N2Kz6haNU8NFhXC6A0uyOZLFQ3NVWosokfoAGHaZ47vVhZrU7C8PGsetObllWUUGe1tOVr2NDqACbWhifzz6cUym02g7pX4Kfbem81wR8mQYOP_Gta53AECGb18aQiZCEF7sdt4lkX1bdWYB2NAFUuqY7ZZ5KG0v2TDb0vFjbyNuFxSjRuU1qc2F-BYI6geyT9FsZzBz_hyD-lMJNsOXJW8yYlW0Yl7cZG3u2uwASrT3v0NIGPYjNbpdyfJVTcVTAKgtwB66sCNdx0et9pJ8QXcE428AnOjsSwMy3zigZ8jIpdQ3M8y12zwJn8k4n_yFojMgF3-62Yc40B8jxkqJQ3cgqi8sxzd7l1VBSYlma5YrhV5JX672htdyjpV-dv5aXxM0OzbM1qWerv2tjBgi9zWZdZotgtdqQ2RQgBVtwZ0xIdyesXZhFR7k44U-X1vylXZfvO83__B0uigZwvgdoo8balM4cMW6ox2-W8rvJJ6cbxaVJRsat_W5MmiJyrdsgpd_Bkx8XtlIfvhXWz3kOoVoc8IzpYSa7r9hRfWpudobj7w9JuZF1jU_rnZtj9m1YS1SQVRr-a021F1dV-esv7Z-ek3cbl5OBMnUgnmrM1p6lihff4JsBybvlWvS3goeSt18ayFWx59pScFecrIquBrV4M8wZJ5dB4cz4dB-gh_Vjz9g5yd3eoc-B4SutUJ4pFRqbxgjgMr9B8FIgseXSwkMlm-stWOzQW2pv7WZ0eeyFZyolmoOkIxkp4l541iV48p8_Ugg0Ua-15uUm__-h730pq423Y92yI_67jlMB_op975I08vkJiihQWwvXe_ZtdVOVfvlwsRZsfg8-So1MvQOc38V9hBhtdy1Q_kSQOj" \
-H "Content-Type: application/json" \
https://us-east1-aiplatform.googleapis.com/ui/projects/secret-cipher-399620/locations/us-east1/endpoints/3829946445218185216:predict \
-d '{
  "instances": [
    {
      "model": "resnet",
      "attack": "fgsm",
      "epsilon": 0.2
    }
  ]
}'