import csv
import sys
from zipfile import error

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    def month_type(value: str) -> int:
        months = {
            "jan": 0, "feb": 1, "mar": 2, "apr": 3,
            "may": 4, "june": 5, "jul": 6, "aug": 7,
            "sep": 8, "oct": 9, "nov": 10, "dec": 11
        }
        return months[value.strip().lower()]

    def visitor_type(value: str) -> int:
        return 1 if value == "Returning_Visitor" else 0

    def weekend_type(value: str) -> int:
        return 1 if value.strip().lower() == "true" else 0

    col_types = [int, float, int, float, int, float, float, float, float, float,
                 month_type, int, int, int, int, visitor_type, weekend_type]

    evidence = []
    labels = []

    with open('shopping.csv', mode='r') as file:
        reader = csv.reader(file)
        next(reader)

        for row in reader:
            converted = [func(value) for func, value in zip(col_types, row[:-1])]
            evidence.append(converted)
            labels.append(1 if row[-1].strip().lower() == "true" else 0)

    return evidence, labels

def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    model = KNeighborsClassifier(n_neighbors=1)
    model.fit(evidence, labels)
    return model

def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    if len(labels) != len(predictions):
        raise ValueError("labels and predictions must be the same length")

    num = len(labels)
    pos_total = 0
    neg_total = 0
    TP = 0
    TN = 0

    for i in range(num):
        if labels[i] == 1:
            pos_total += 1
            if predictions[i] == 1:
                TP += 1
        else:
            neg_total += 1
            if predictions[i] == 0:
                TN += 1
    sensitivity = TP / pos_total if pos_total > 0 else 0
    specificity = TN / neg_total if neg_total > 0 else 0

    return sensitivity, specificity
if __name__ == "__main__":
    main()
