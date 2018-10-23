Whereas linear regression algorithms are used to predict/forecast values but logistic regression is used for classification tasks.

Many classification tasks done routinely by people, e.g. classifying whether an email is a spam or not, classifying whether a tumour is malignant or benign, are typical examples ML algorithms can do.

LR is a classification algorithm that is used to predict the probability of a categorical dependent variable. In logistic regression, the dependent variable is a binary variable (data is 1 or 0).
The independent variables should be independent of each other. That is, the model should have little or no multicollinearity.
Requires quite large sample sizes.

Types include: Binary (Pass/Fail), Multi (Cats, Dogs, Sheep), Ordinal (Low, Medium, High)

The Sigmoid Function: logistic regression algorithm also uses a linear equation with independent predictors to predict a value (which can be between negative infinity and positive infinity). To squash the predicted value between 0 and 1, we use the sigmoid function.

**The Cost Function**

Is used to measure the accuracy of the LR model for a given set of parameters θ.
The math behind this is a little complicated, but you can interpret it as computing an error rate based on a comparison of the predicted probability of an outcome P(1) and the actual outcome y. The closer the predicted probability is to 1 or 100%, the lower the error for the “1” or “positive class”.

Example 1
---------
Say we’re given [data](http://scilab.io/wp-content/uploads/2016/07/data_classification.csv) on student exam results and our goal is to predict whether a student will pass or fail based on number of hours slept and hours spent studying. We have two features (hours slept, hours studied) and two classes: passed (1) and failed (0).

![](../images/logreg3.png)

**Sigmoid activation** Use sigmoid to map predictions to probabilities:

![](../images/logreg2.png)

**Decision boundary** In order to map this to a discrete class, we select a threshold value or tipping point above which we will classify values

![](../images/logreg6.png)

**Making predictions** A prediction function in logistic regression returns the probability of our observation being positive, True, or “Yes”. We call this class 1 and its notation is P(class=1)

![](../images/logreg8.png)

    def predict(features, weights):
        ''' Returns 1D array of probabilities that class label == 1 '''
        z = np.dot(features, weights)
        return sigmoid(z)

**The Cost Function** We cannot use the same cost function MSE (L2) as we did for linear regression, because our prediction function is non-linear (due to sigmoid transform). Instead we use as function known as Log Loss.

    def cost_function(features, labels, weights):
        observations = len(labels)
        predictions = predict(features, weights)

        #Take the error when label=1
        class1_cost = -labels*np.log(predictions)

        #Take the error when label=0
        class2_cost = (1-labels)*np.log(1-predictions)

        #Take the sum of both costs
        cost = class1_cost - class2_cost

        #Take the average cost
        cost = cost.sum()/observations
        return cost

**Gradient Descent** To minimize our cost, we use Gradient Descent just like before in Linear Regression.

    def update_weights(features, labels, weights, lr):
        '''
        Vectorized Gradient Descent

        Features:(200, 3)
        Labels: (200, 1)
        Weights:(3, 1)
        '''
        N = len(features)

        #1 - Get Predictions
        predictions = predict(features, weights)

        #2 Transpose features from (200, 3) to (3, 200)
        # So we can multiply w the (200,1)  cost matrix.
        # Returns a (3,1) matrix holding 3 partial derivatives --
        # one for each feature -- representing the aggregate
        # slope of the cost function across all observations
        gradient = np.dot(features.T,  predictions - labels)

        #3 Take the average cost derivative for each feature
        gradient /= N

        #4 - Multiply the gradient by our learning rate
        gradient *= lr

        #5 - Subtract from our weights to minimize cost
        weights -= gradient

        return weights

**Mapping probabilities to classes and training**

    def decision_boundary(prob):
        return 1 if prob >= .5 else 0

    def classify(preds):
        '''
        >>> def classify([ 0.967, 0.448, 0.015, 0.780, 0.978, 0.004])
        [1, 0, 0, 1, 1, 0]
        '''
        decision_boundary = np.vectorize(decision_boundary)
        return decision_boundary(predictions).flatten()

    def train(features, labels, weights, lr, iters):
        cost_history = []

        for i in range(iters):
            weights = update_weights(features, labels, weights, lr)

            #Calculate error for auditing purposes
            cost = cost_function(features, labels, weights)
            cost_history.append(cost)

            # Log Progress
            if i % 1000 == 0:
                print "iter: "+str(i) + " cost: "+str(cost)

        return weights, cost_history

![](../images/logreg9.png)

**Accuracy** measures how correct our predictions were. In this case we simple compare predicted labels to true labels and divide by the total.

    def accuracy(predicted_labels, actual_labels):
        diff = predicted_labels - actual_labels
        return 1.0 - (float(np.count_nonzero(diff)) / len(diff))

**Decision boundary** Another helpful technique is to plot the decision boundary on top of our predictions to see how our labels compare to the actual labels.

    def plot_decision_boundary(trues, falses):
        fig = plt.figure()
        ax = fig.add_subplot(111)

        no_of_preds = len(trues) + len(falses)

        ax.scatter([i for i in range(len(trues))], trues, s=25, c='b', marker="o", label='Trues')
        ax.scatter([i for i in range(len(falses))], falses, s=25, c='r', marker="s", label='Falses')

        plt.legend(loc='upper right');
        ax.set_title("Decision Boundary")
        ax.set_xlabel('N/2')
        ax.set_ylabel('Predicted Probability')
        plt.axhline(.5, color='black')
        plt.show()

![](../images/logreg10.png)

**More than two discrete outcomes**

Say you are trying to distinguish between 3 outcomes, i.e. fraudulent vs. valid vs. refunded transactions. To solve this multiclass problem, you’d basically create 3 separate logistic regression models: the 1st by separating fraud vs. valid + refunded, the 2nd for valid vs. fraud + refunded, and the 3rd for refunded vs. valid + fraud. Then for each example you want to run a prediction, you simply choose the model with the highest predicted probability.

Example 2
---------
The [dataset](http://archive.ics.uci.edu/ml/index.php) provides the bank customers’ information. It includes 41,188 records and 21 fields:

![](../images/logreg12.png)

**Predict variable (desired target)**

y — has the client subscribed a term deposit? (binary: “1”, means “Yes”, “0” means “No”)

The education column of the dataset has many categories and we need to reduce the categories for a better modelling.

![](../images/logreg13.png)

**Data exploration**

![](../images/logreg14.png)

Our classes are imbalanced, and the ratio of no-subscription to subscription instances is 89:11. Before we go ahead to balance the classes, let’s do some more exploration.

![](../images/logreg15.png)

The average age of customers who bought the term deposit is higher, and the pdays (days since the customer was last contacted) is lower.

![](../images/logreg18.png)

**Create training data**

**Recursive Feature Elimination (RFE)**

Based on the idea to repeatedly construct a model and choose either the best or worst performing feature, setting the feature aside and then repeating the process with the rest of the features. This process is applied until all features in the dataset are exhausted. The goal of RFE is to select features by recursively considering smaller and smaller sets of features.

    data_final_vars=data_final.columns.values.tolist()
    y=['y']
    X=[i for i in data_final_vars if i not in y]

    from sklearn.feature_selection import RFE
    from sklearn.linear_model import LogisticRegression

    logreg = LogisticRegression()

    rfe = RFE(logreg, 20)
    rfe = rfe.fit(os_data_X, os_data_y.values.ravel())
    print(rfe.support_)
    print(rfe.ranking_)


    cols=['euribor3m', 'job_blue-collar', 'job_housemaid', 'marital_unknown', 'education_illiterate', 'default_no', 'default_unknown',
          'contact_cellular', 'contact_telephone', 'month_apr', 'month_aug', 'month_dec', 'month_jul', 'month_jun', 'month_mar',
          'month_may', 'month_nov', 'month_oct', "poutcome_failure", "poutcome_success"]
    X=os_data_X[cols]
    y=os_data_y['y']

**Implementing the model**

    import statsmodels.api as sm
    logit_model=sm.Logit(y,X)
    result=logit_model.fit()
    print(result.summary2())

The p-values for most of the variables are smaller than 0.05, except four variables which we remove:

    X=os_data_X[cols]
    y=os_data_y['y']

    logit_model=sm.Logit(y,X)
    result=logit_model.fit()
    print(result.summary2())



