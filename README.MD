# Penney Game
Penney's game is a game that involves two players tossing a coin until a sequence appears.  

The two players chose, before tossing the coin, one sequence each of Head and Tails  with lenght 3 (for example: "Head, Head, Tails" chosen by player 1 and "Tails, Head, Tails" chosen by player 2). It is important to know that choices are ordered and that information is complete (player 1 chose a sequence, then player 2, knowing the sequence chosen by player 1, chose another sequence. Player 1 knows that player 2 knows player 1 sequence, player 2 knows that player 1 knows that player 2 knows player 1 sequence etc...).  

The game is intransitive, which means that, even if probability to toss Head or Tails is 50%, player 2 can always chose a sequence that will happen with more probability than the sequence chosen by player 1, it doesn't matter which sequence is chosen by player 1. That means that, if I represent all the possible sequences in a graph, and I know which node is an absorbing trap (sequence chosen by player 1), I can always find another absorbing trap with more probability to happen before the other absorbing trap.  

It is possible to define a number called "intransitiveness", that measures how much the game is "unfair". If intransitiveness is >0 it means that the player 2 has an advantage, if intransitiveness is <0 it means that player 1 has an advantage. Intransitiveness change with loaded coins (probability to toss Tails different from 50%). The goal of the simulation is to find out the intransitiveness function with respect to probability and to find out if there are ways to load the coins in order to have a fair game (intransitiveness=0). The intransitiveness can be written as,
$$\sigma = min_{i=1,...,N}[max_{j=1,...,N}V_{ij}]-\frac{1}{2}$$
where $V_{ij}$ is the victory matrix.  

It is possible to play also a simplified version of Penney's Game, where the sequence has lenght 2 instead of 3. What's interesting is that in this case the game is transitive for a 0.5 probability to toss a T, while for the classic Penney's game the game is intransitive. 
It's also interesting to notice the different shape of the two intransitiveness functions, that is counterintuitive.  

# Structure of the project
This is how I divided my project into blocks:  
- In the file **main** there is the main part of the code, where I have written two functions that represent the victory matrix of Penney's Game and the victory matrix of Penney's Game simplified, and a function where I simulate the game multiple times for each given probability and each given sequences of players, in order to have good statistics. The code also print the value of probability for which the intransitiveness of the game has 0 value. Then the code saves all the probability and intransitiveness values in order to plot them in another file. Here I used ConfigParser library in order to import the configuration file from command line, and passing its parameters to the program.
- In the file **test** I used Unittest library to test the correct functioning of the functions from main file.
- In the file **config** there are all the definitions of the parameters used in the main file and in the plot file, as number of simulations for each game or range of probability. It's a .txt file that is imported in main file and plot file.
- In the file **plot** there are the plottings of the results of Penney's game and Penney's game simplified. Here I used ConfigParser library in order to import the configuration file from command line, and passing its parameters to the program.  

These are the steps in order to start the program and to plot the results:  

1. First, the user has to chose between the different parameters (like title of the graphs, range of probability, random seed...) on config.txt and eventually write a new one with the same name and the same syntax of **config**; if the user wants to do so, he has also to specify the local paths to the folder where graphs must be saved.
2. Then, to start the game the user has to launch the file **main** which imports its parameters from **config** using ConfigParser library. The collected data (values of intransitiveness for Penney Game and Penney Game simplified) are saved automatically using json library. The simulation can take a long time, so, when the file is run, is possible to see the percentage of completion of the simulation thanks to the tqdm library.
3. At the end the user has to launch the **plot** file with the configuration he wants. The data are loaded automatically with json library, and the results are automatically saved in the *images* folder.


