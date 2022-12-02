# three-layer-atmosphere

This is an object-oriented model to simulate the radiation budget in the atmosphere across three layers and associated temperature effects. This model was created by Dr. John R. Christy and M.P. Singh of the University of Alabama Huntsville. 

| Script         | Purpose     |
| ---------------| ------------|
| [Model Class](https://github.com/Corey4005/three-layer-atmosphere/blob/main/model/modelEquations.py) | A class to model atmospheric attributes with methods that opperate on them. |
| [Simulate Cloud Cover](https://github.com/Corey4005/three-layer-atmosphere/blob/main/model/model_cirrus_clouds.py) | This module demonstrates how the model can be iterated upon to simulate temperature changes in the upper atmosphere with increasing cirrus cloud cover. Returns a plot of temperature changes at each layer over small changes with reflectivity |
| [Calculate Layer Temps](https://github.com/Corey4005/three-layer-atmosphere/blob/main/model/model_temps_with_input.py) | This is a module to show how a text file containing solar and infrared values for each layer can be read in and processed to model temperatures. Returns a print statement containing the calculated temperatures from radiation inputs. |
| [Model Greenhouse Effect](https://github.com/Corey4005/three-layer-atmosphere/blob/main/model/model_varying_CO2.py) | 
This is a module to simulate changing CO2 and its effect on the layer temperatures. Injection of CO2 into the troposphere causes increased reflectance of infrared and decresed absorption. Returns a plot of layer temperatures with changing infrared reflectance |
| [Model Aerosols Upper Atmosphere](https://github.com/Corey4005/three-layer-atmosphere/blob/main/model/model_varying_L1_reflectance.py) | This is a module to demonstrate the effect of small changes in solar reflectivity in the stratosphere and absorption on the surface temperature. This would occur with the stratosphere being injected with aerosols that increase solar reflection and decrease solar transmission. Returns a plot of varying solar reflectance with temperature. | 
| [Model Aerosols in Lower Atmosphere](https://github.com/Corey4005/three-layer-atmosphere/blob/main/model/model_varying_L2_reflectance.py) | This is a module to demonstrate the effect of small changes in solar reflectivity in the troposphere and absorption on the surface temperature. This is to simulate the effect of aerosols on the troposphere. Returns a plot after increasing solar reflectance and decreasing solar absorption. 


# Model Equations 

The model uses the functions in the [Model Class](https://github.com/Corey4005/three-layer-atmosphere/blob/main/model/modelEquations.py) module to derive new temperatures. `calculateRadiationBudget()` takes in the coeficients of absorption, transmission and reflection from a textfile and calculates net short and longwave radiation. These calculations are then used by `getTemperatures()` to solve a linear algebra matrix for coeficients used for temperature calculations. Reading the module from top to bottom should provide some idea of how the calculations are perfomred. 

