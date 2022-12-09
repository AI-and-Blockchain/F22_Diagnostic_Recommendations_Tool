This is the code folder for our project.

Here are some steps for getting started:

- You can install necessary packages to run our code via our requirements.txt file -> pip3 install -r requirements.txt
- We follow a package and module structure here. 
   - So when running files, run it from the diagnosticsreccode directory level and run .py files within each of our sub-component directories. E.g.,
  python MachineLearning_comp/run_model.py -> will execute code in the machine learning part of the diagnosticsreccode package.
- All the functions we support can be browsed by running the main_runner file -> python main_runner.py. The user is prompted with options here to register their hospital node, view statistics and train their model. These functions are made possible due to the blockchain integration.- 
- Note: When starting a new training, make sure that the data/active_hospitals.txt file contains "0\n" only in its contents. If not, hospitals from previous trainings will be stored there.


  
 
