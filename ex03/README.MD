python3 logreg_train.py <datenbank> - this step is used to train and give weights as result.
For example:
python3 logreg_train.py dataset_train.csv

python3 logreg_predict.py <dataset test> <weights json> - this step is using the file that i trained to predict new result
For example:
python3 logreg_predict.py dataset_test.csv weights

Value returned is 99% correct.
Error handling: Only number of arguments. In this project, it's about training, so, i don't handle error handling