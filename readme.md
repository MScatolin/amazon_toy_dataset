
# Project Pythia: Estimating Q&A Role on Sales in Online Retail

In online shopping, customers may seek information before deciding the purchase from different sources, such as product descriptions, reviews, and questions. Therefore, it is important to provide essential ve helpful information about the product. Providing the information the customer is looking for can reduce customer barriers to shopping with OnlineRetail. Therefore, the company can increase sales and be apart from our competitors.

The main objective of Project Pythia is: 
* to gain insight about customer questions,
* to determine how Q&A section of a product affects its position on best sellers rank.

**Data:**

A small-scaled data, which is scraped from OnlineRetail.co.uk, was used for this project. There are 10K products offered by 2651 manufacturers and 4136 different online sellers are in dataset. The dataset has both continuous and categorical data, a total of 17. 

**Modelling** 

In this project, we aimed to build a model that predicts the best sellers rank of products which is a proxy for sales.

For this aim, we tried multiple methods with different feature sets. 
* Regression: Prediction of best seller rank with XGBoost Regressor
* Classification: Predict which in bucket the best seller rank is with XGBoost Classifier. 
* Mixed Method:Predict best seller rank with XGBoost Regressor, assign the predictions to the buckets, and use classification metrics to evaluate the performance.
* Ordinal Regression: Predict which in bucket the best seller rank is with mord.OrdinalRidge.

According to the model performances, we decided to use the XGBoost regression model, which is a powerful and highly accurate implementation of gradient boosting.

**Output:**

Based on this model, we created an interactive dash app that shows the estimated best sellers rank of products with different feature inputs such as the product description.  With the help of this tool, sellers can see the products which have opportunities to improve revenue.






File structure
--------------

*Notebooks*: All steps of the Data Science Method was conducted in seperate notebooks.

* Data wrangling: Cleaning, structuring and enriching raw data
* Competitors analysis: The analysis of third-party sellers
* Text processing: Using NLP techniques the process textual data
* Exploratory data analysis: Discover patterns in data
* Modelling: Multiple methods were utilized to build a model predicting best sellers rank. 

*Data*: Different versions of data used in project.

*Presentation* pptx format of presentation


## Authors

- [Marcelo Scatolin Queiroz](https://www.github.com/MScatolin)
- [Hande Gulbagci Dede](https://github.com/hangulde)

