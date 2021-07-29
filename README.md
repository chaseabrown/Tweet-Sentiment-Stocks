# The Effect of Trending on the Stock Market
Capstone Project. All Python code shown was written by me. My group worked in R.

**Disclaimer-I am sure there are "credentials" in these files, they aren't for anything still in use and they never contained sensitive information. If either were the case, I would have scrubbed them from the file. I understand the security concerns in other situations**

## Introduction
The birth of technologies such as machine learning and neural networks has with it created new opportunities for massive data sets to predict future events, categorize groups, and just gain insight in general. A commonly used data set for this kind of analysis is Twitter because of its ability to offer up-to-date public opinion across the world. One use case for this kind of analysis is predicting stock market changes before they happen. There have been numerous papers published about the success of this strategy. One such example [1] dates back to 2010 and found that they were able to make predictions at an accuracy of 86.7 percent. 11 years later, the advancements in not only twitter usage, but also algorithm strength and integrity gives us the idea that we can potentially do better.

In the first leg of our project, we focused on getting our datasets complete enough to answer the set of exploratory questions we brought up in our proposal. Through this effort, there were roadblocks that necessitated a slight shift in our exploratory research. These roadblocks affected a few details of our original expected dataset which will be explained in more detail in the next section. These dataset changes, also in turn changed our exploratory analysis plans. Because of this some of our initial exploratory questions were deemed out of scope.

After seeing promising results in a select group of stocks, and working to reducing the limiting factors of our dataset, we expanded our exploratory research to include any $TICKER or #TICKER mentions in our 1% sample of twitter. This resulted to just shy of 400,000 tweets including 2967 different stocks for sentiment analysis. The results of this were much more telling than the previous dataset, but it is not without its limitations.

We tested this data across different models and set up our final dataset to be usable for trading in the future. These changes, as explained below, allow the model to collect more data over time.

## Our Dataset

### Exploratory Analysis

Our dataset for exploratory analysis consists of 393,928 tweets that we ran through 2 separate sentiment analysis packages. One that only offers positive and negative and another that offers “Happy”,“Angry”, “Sad”, “Surprise”, “Fear”. These tweets were pulled from the dates we were able to download. The tweet was pull if the stock ticker was mentioned with a # or a $. The point of this was to ensure as best as possible that the dataset was free of irrelevant tweets. In situations where the stock ticker was a word, such as $CAKE, there was too much noise to filter out, so those were removed from the dataset.

As far as stock data goes, while we are using the Yahoo Finance API for stock data, we have slightly altered how we picked our stocks. We pulled tweets for every stock listed in the Nasdaq, then eliminated any stock with less than 100 days of data in our twitter set.


### Our Model

For our Model, we further reduced our dataset to stocks that were showing a higher correlation between their stock and tweet data than the others. This consisted of stocks one might expect, such as AAPL, TSLA, AMZN, and about 10 others. We also switched to live hourly data for our model as that is a much more reliable data source, and it is the only practical option for the model in the real world. This consisted of roughly 300,000 tweets over the course of 2 weeks.

![Data Collected](https://github.com/chaseabrown/Python-Tweet-Sentiment-Stocks-/blob/main/dataCollected.PNG "Data Collected")

## Exploratory Analysis

### Initial Analysis

A majority of these past few weeks have been spent solving data preprocessing issues and downloading data. So far we have been able to download and analyze most of 2020, as shown above.
To start our analysis, we used the data we had collected and created a data frame with the following features:

* Date
* Opening price of stock
* Highest price of stock that day
* Lowest price of stock that day
* Closing price of stock that day
* Volume of stock traded that day
* Volume of tweets collected for that stock that day
* Daily average happy score
* Daily average angry score
* Daily average surprise score
* Daily average sad score
* Daily average fear score
* Daily average sentiment score (number between 0.5 and 1; 0.5 is neutral and 1 is very confident in either direction)
* Whether the stock price increased that day
* Whether the stock price increased by 5 percent that day Yesterday’s average happy score
* Yesterday’s average angry score
* Yesterday’s average sad score
* Yesterday’s average fear score
* Yesterday’s average surprise score
* Yesterday’s volume of tweets collected for that stock Yesterday’s volume of stock traded

Below we have included a correlation matrix showing the magnitude of the correlation between some of the variables from the data set. This will be useful as we move forward through the analysis:

![Correlation Chart](https://github.com/chaseabrown/Python-Tweet-Sentiment-Stocks-/blob/main/correlationChart.png "Correlation")


One interesting thing that caught our attention in Figure 2 is that the correlations between emotion scores from yesterday and whether or not the stock price increased that day are extremely similar as the correlations between emotion scores from the same day and whether or not the stock price increased that day. Our initial belief would’ve been that the emotion scores from yesterday would have had a higher correlation since people’s emotions change and then the stock price reacts. Determining whether the emotion scores are predictive, reactive, both, or neither will be something that we will be focusing on a lot as our analysis continues.
Next, I want a quick glance at the distributions of the daily averages of the emotion scores. This will also be useful, so we can determine how strongly an emotion is for a tweet compared to other tweets.

![Averages](https://github.com/chaseabrown/Python-Tweet-Sentiment-Stocks-/blob/main/averageCount.jpg "Averages")


![Volume](https://github.com/chaseabrown/Python-Tweet-Sentiment-Stocks-/blob/main/volume.jpeg "Volume")


Next, we have a graph that shows the relationship between the volume of tweets collected for said stock during that day and the daily average sentiment score with it conditioned on whether the stock price increased that day. At first glance, it appears interesting that there is a steeper slope for when the price did increase than when price did not increase. Following that, we have a graph that shows the relationship between the volume of stock traded that day and the tweet volume conditioned on whether the stock price increased that day. At initial glance, it appears that both relationships look similar, but further analysis should be done.

![Autozone](https://github.com/chaseabrown/Python-Tweet-Sentiment-Stocks-/blob/main/autozone.jpg "Autozone")

When looked at across all of our stocks, it is clear that there is no general rule of a relationship between our twitter sentiment variables and stock price. This is not the case when you look at the stocks individually, as shown in Figure 5. We will look into more stocks in our next batch of analysis and find more consistent trends.

### Narrowed Analysis

After gathering our dataset, we looped through each stock and ran correlation tests on 3 versions of the dataset. We made changes to our dataset that let us see how well our twitter data correlated with the previous days stock data and the day after. The goal of this is to test whether or not twitter is tracking the stock market live, or whether there are predictive or reactive elements to it. In short, after we eliminated any correlation test that had less than 100 data points, leaving us with 3627 features to test, we found that 44 features had medium and 2 had strong correlation between stock elements tweet elements. Every single time it was a connection between stock price and daily stock volume being compared to tweet volume. Here are some of those findings more close up:

![Pearson AAPL](https://github.com/chaseabrown/Python-Tweet-Sentiment-Stocks-/blob/main/p1.png "Pearson AAPL")
![Spearman AAPL](https://github.com/chaseabrown/Python-Tweet-Sentiment-Stocks-/blob/main/s1.png "Spearman AAPL")
![Pearson NVDA](https://github.com/chaseabrown/Python-Tweet-Sentiment-Stocks-/blob/main/p2.png "Pearson NVDA")
![Spearman NVDA](https://github.com/chaseabrown/Python-Tweet-Sentiment-Stocks-/blob/main/s2.png "Spearman NVDA")
![Pearson NFLX](https://github.com/chaseabrown/Python-Tweet-Sentiment-Stocks-/blob/main/p3.png "Pearson NFLX")
![Spearman NFLX](https://github.com/chaseabrown/Python-Tweet-Sentiment-Stocks-/blob/main/s3.png "Spearman NFLX")
![Pearson TSLA](https://github.com/chaseabrown/Python-Tweet-Sentiment-Stocks-/blob/main/p4.png "Pearson TSLA")
![Spearman TSLA](https://github.com/chaseabrown/Python-Tweet-Sentiment-Stocks-/blob/main/s4.png "Spearman TSLA")
![Pearson FB](https://github.com/chaseabrown/Python-Tweet-Sentiment-Stocks-/blob/main/p5.png "Pearson FB")
![Spearman FB](https://github.com/chaseabrown/Python-Tweet-Sentiment-Stocks-/blob/main/s5.png "Spearman FB")

The number of medium or strong correlated features for the day before and after dropped from 9 each. This pretty conclusively shows that that is little to no correlation between our twitter data and the market moving the day before or after. The main interpretation at this point is there is a partial correlation between stock volume and tweet volume in reference to that stock and this happens live. While we did not find any correlation between our sentiment analysis and the market, there is a lot of potential error to keep in mind. First off, the data set is sampled based on all of twitter, not just stock tweets, so there is not a consistent proportion of stock tweets at any given time. Another issue is the limitation in sentiment analysis technology. Given the size of our dataset, it is possible errors were overlooked.

## Our Model

In order to build out a model, we first needed to clean and prepare our data significantly. A huge thing that we learned from the project was that cleaning and preparing the data might be the most important aspect of building a successful machine learning model. We will explain the steps in chronological order below.

### Steps
Step 1: We chose 21 stocks that we found to have the strongest correlations with twitter sentiment than the other stocks did. These are more popular stocks that are talked about on the news and on social media. The stocks are American Airlines, Apple, Amarin, Amazon, Dynamic Materials Corporation, ENGlobal Corporation, Facebook, Gilead Sciences, Heat Biologics, Inovio Pharmaceuticals Inc, Intel, JOST Werke, Marathon Digital Holdings, Netflix, Novavax, Nvidia, Penn National Gaming, Plug Power, Sorrento Therapeutics, Trillium Therapeutics, and Tesla. Intuitively, it makes sense that bigger and more well known stocks are more correlated with twitter than others. A lot of these stocks such as Apple, Amazon, Facebook, Netflix, and Tesla, we were able to collect a significant amount of tweets associated with them. The more data that we could collect, the better our model would perform in theory.

Step 2: We collected hourly data for each weekday for each stock. We did this using the Twitter API. Since the Twitter API only allows you to retrieve tweets going back 7 days, we collected this data over the course of the month of April. At the beginning of our data collection process, we were collecting a maximum of 500 tweets per stock each day. This was due to data retrieval timing. As we collected data throughout the month, we tried a different number of max tweets to pull in order to find the most efficient and effective number of tweets to pull. At the end of our data collection, we were pulling a maximum of 10,000 tweets per stock each day. While 10,000 was the maximum, none of the stocks ever had 10,000 tweets associated with it. The tweet sentiments were averaged for thehour from all the tweets collected for that hour. The figure below shows a subset of the hourly data. It shows Tesla’s hourly data for April 7th, 2021. As you can see from the figure, we have open price for the hour, closing price for the hour, mean happy score, mean angry score, mean surprise score, mean sad score, mean fear score, mean sentiment score, volume of stock traded that hour, and volume of tweets collected that hour.

![Data](https://github.com/chaseabrown/Python-Tweet-Sentiment-Stocks-/blob/main/figureA.png "Data")

Step 3: We took the daily mean, maximum, minimum, and standard deviation of the hourly emotion sentiment scores for each stock. A subset of this data is shown below. It represents the data collected from the week of April 6th to April 9th for Tesla’s stock. From the figure, you can see that we have the starting open price of the stock that day, the ending close price of the stock that day, the mean happy score, the maximum happy score, minimum happy score, and standard deviation happy score. While the figure only shows happy, we also have those features for angry, surprise, sad, and fear as well.

![Subset](https://github.com/chaseabrown/Python-Tweet-Sentiment-Stocks-/blob/main/figureB.png "Subset")

Step 4: We created a new column called “increase.” This column is TRUE if the stock price closes higher on the next workday than it did today. It is FALSE otherwise. This is our target variable. It is worthy to note that the breakdown of the increase column was 55% FALSE and 45

Step 5: We omitted rows with NAs.

Step 6: Using correlations (albeit very weak), we tried multiple machine learning models to try to predict the increase column. When trying these machine learning models, we tried a large number of different combinations of the features to find the best performing model that we could. We ended up trying 4 different types of models.
1. The XGBoost was by far the worst performing model that we tried. This was somewhat surprising, but this model was no better than a random guess and had an ROC of around 0.52
2. The ridge regression model was the best performing model of the bunch. We will get into the metrics and how it performed below.
3. The lasso regression model performed decently well, but not as well as ridge. 4. The neural network model performed pretty similarly to the lasso model. We did consider using this model as our final model, but opted for ridge since the ridge regression model is significantly more interpretable than a neural network. The ridge regression model also ran instantaneously, while the neural network model took anywhere from a few seconds to a few minutes to run depending on the parameters we inputted.

### Ridge Regression Model Coefficients

* Lambda = 0.1172175 
* min_angry = -215.906087 
* sd_surprise = 1.576678 
* mean_sad = -3.575914
* sd_sad = -1.059764
* mean_fear = 1.914781

### ROC Curve

The ROC curve for our model is labeled below. The ROC curve plots the false positive rate against the sensitivity, which is the true positive rate for different values as the cutoff point. Our area under the curve is 0.58. While this may seem like not a great value, it seems decent given the context of the problem. We are trying to predict the stock market. This is something that experts have been trying to predict for 100s of years. If we were able to predict the stock market with a very high AUC, we’d be millionaires. Given that we are trying to predict a money making environment, an AUC of 0.58 looks promising in our opinion.

![ROC Curve](https://github.com/chaseabrown/Python-Tweet-Sentiment-Stocks-/blob/main/figureC.png "ROC Curve")

### Confusion Matrix

Confusion Matrix: Using the optimal cutoff point that maximizes the accuracy of the model, we created a confusion matrix that is denoted below. It is worthy to note that since the majority class is FALSE, the confusion matrix labels FALSE as the positive class. To clarify on some terminology, the no information rate is the percentage of the target variable that is the majority class.

A model that predicted the FALSE class every single time would be correct 55.38% of the time. At a minimum, a model that we build should be better than that.
Accuracy: 63.85%
95% Confidence Interval for accuracy: (54.96%, 72.09%)
P-Value = p(Accuracy > No Information Rate) = 0.03

|               | True          | False | Total |
| ------------- |:-------------:| -----:| -----:|
| Is True       | 58            | 33    | 91    |
| Is False      | 14            | 25    | 39    |
| Total         | 72            | 58    |       |

### Machine Learning Metrics

The figure below shows the observed value of increase given the predicted value. When our model predicts FALSE, it is correct 64.10% of the time. When our model predicts TRUE, it is correct 63.74% of the time. Keep in mind that this model is just another tool to help you in the stock market. It is not an end all be all to investment strategies. Additionally, our model does not detect the magnitude of rises and falls. It just detects whether or not a stock price goes up or down. It is possible that 36% of wrong predictions could equal the same magnitude as 64% of correct predictions. While further exploration could be done using linear regression to detect magnitude of increases or decreases, we focused on classification models.

![Ratio Correct](https://github.com/chaseabrown/Python-Tweet-Sentiment-Stocks-/blob/main/figureF.png "Ratio Correct")

## Conclusion

The big takeaway from this project is the data limitations when dealing with historical tweets. It is either expensive or needs to be planned years ahead of time for data collection. While that is the case, we found traces of a connection in our exploratory analysis and our model looked even better. It is safe to say that there is a connection between certain stocks and what is being talked about on twitter.

## Short Descriptions of Files:
**getSentiment.py** - Used multithreading to run sentiment analysis on tweets as fast as possible. Our dataset was huge for a personal computer, so it still took awhile. Without the multithreading aspect, the project most likely would have failed.

**auditTweetData.py** - Scanned the file structure to determine which tweet files were currently available and which ones were missing.

**buildBranches.py** - Built the directory structure for the tweet data

**buildDailyAverages.py** - Reads in database of tweets with sentiment analysis and returns daily averages of that data

**buildDB.py** - Used to convert csv data into database data. (I didn't start using a database until I was well into the project)

**buildHourlyData.py** - Reads in database of tweets with sentiment analysis and returns hourly averages of that data

**buildShare.py** - Converts database tables into csv files (My groupmates weren't as well versed in mySQL so I did this to make it easier for them)

**buildStockDaily.py** - Combined tweet sentiment data with daily stock data so they could be compared

**convertFilesToDatabase.py** - Converted tweet files to a database table. Didn't end up being used because I didn't have any interest in waiting 4 days for the 100gbs of tweets on my personal computer

**decompressFiles.py** - Goes through all of the tweet files, decompresses them and saves the decompressed in the same directory

**findCorrelations.py** - Compares each stock feature with each tweet sentiment feature for every stock to find where the correlation is. Used Spearman and Pearson Correlation

**plotDatabaseAudit.py** - Makes a graph to visualize the data audit from auditTeetData.py

**printToFiles.py** - Converts database tables into csv files (My groupmates weren't as well versed in mySQL so I did this to make it easier for them)

**unpackJsons.py** - Me trying different ways to get tweet information from compressed files to find something fast enough 

