#### Instructions
+ This is the simulation for Mechanical Neural Network (MNN) based on Pymunk
+ For the five python files, the HexaLattice.py works as the main part. In this file the main function is executed.
+ beam.py is responsible for the creation of  flexible-stiffness beams, while node.py is reponsible for the creation of the static and float nodes.
+ operations.py contains all the external operations that are implemented in this MNN simulation, such as external force, and drawing arrows that represent the displacement.
+ In settings.py you can set the environment properties of the simulation, for example the screen size.

#### Things to Take Care
+ The file settings.py is not completely global, which means some details of the code uses the global settings while having not import the class Settings. Therefore one must be careful when editing the settings, for that may induce unexpected result.