original subject = file en.subject.pdf
(Project is done)

This project is about

1. visualising data in table (ex00), graphic (ex01) form
2. first maschine learning (ex02)

ex01 (done):
visualize data in a table with certain features: count, mean, std, min, 25%, 50%, 75%, max.

ex02 (done):

ex02.1 => visualize data in histograms to see which course has most homogenous score distribution.
Because there are 2 pretty similar courses:Care of Magical Creatures and Arithmancy, so i need to have a further step to find the winner.
The way i found the winner: The science that has the largest common area among all the courses is the winner. Common area is calculated based on number of blocks. There will be 20 column and scores belong to 1 of them

ex02.2 =>  visualize data in a scatter plot answering: What are the two features that are similar?
Answer: Run it, and we will see Astronomy and Defense Against the Dark Arts are most similar
Why: Because they are inversely proportional (run it, then you will see it)
or 
https://en.wikipedia.org/wiki/Pearson_correlation_coefficient

ex02.3  visualize data in pair_plot - means both histogram and scatter plot in 1 window to ahve overview

ex03: first maschine learning exercise: Train a model with dataset_train.csv and let it predict file dataset_test.csv

ex03:
- Train a model with a databank (such as dataset_train.csv)
- use that model to predict another databank (such as dataset_test.csv) to check the ability to guess a the house.

How to run?

git clone https://github.com/TomTris/dslr
cd dslr
source myenv/bin/active

then, go to the directory, python3 + name of programm, it will show instructions.

At the end. let me clarify:
This project is driven by my personal motivation to explore and learn.
My goal is to become proficient in using Python for my specific needs, focusing on efficiency and deeper understanding. I don't want to rely on one-size-fits-all functions, nor do I want to get stuck on too basic, low-level tasks like in C. Instead, it's about gradually becoming more familiar with Python, learning to use it effectively for my objectives. 