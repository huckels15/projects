# Testing Methodology:

## Unit Tests:

Tests were implemented to test the functionality of the python functions integral to the app. These included the python modules that are responsible for the following:

- AlexNet attacks
- Robust AlexNet attacks
- ResNet attacks
- Robust ResNet attacks
- Custom attacks
- AlexNet dataset download
- ResNet dataset download
- Custom upload dataset
- Custom upload model 

The app.py files for each of these were excluded, as the endpoints are tested in the integration test, and many of the tests cannot be run locally, as the endpoint functionality introduces the need for model training/evaluation, which is impractical on a non-GPU optimized architecture. The rest of the images do not include any python functionality, except for command line integration, which we did not deem as necessary to test with a testing suite.

## Integration Tests:

The integration tests look at the deployed app and all of the endpoints including the frontpage, information pages, upload page, and model page. The functionality and accessibility by users is tested to ensure that the different containers were sucessfully deployed. 