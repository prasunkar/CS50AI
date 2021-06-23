
# 🚦 Traffic Project

**Objective:** Write an AI to identify which traffic sign appears in a photograph.

## 📺 Demonstration

```
$ python traffic.py gtsrb
Epoch 1/10
500/500 [==============================] - 5s 9ms/step - loss: 3.7139 - accuracy: 0.1545
Epoch 2/10
500/500 [==============================] - 6s 11ms/step - loss: 2.0086 - accuracy: 0.4082
Epoch 3/10
500/500 [==============================] - 6s 12ms/step - loss: 1.3055 - accuracy: 0.5917
Epoch 4/10
500/500 [==============================] - 5s 11ms/step - loss: 0.9181 - accuracy: 0.7171
Epoch 5/10
500/500 [==============================] - 7s 13ms/step - loss: 0.6560 - accuracy: 0.7974
Epoch 6/10
500/500 [==============================] - 9s 18ms/step - loss: 0.5078 - accuracy: 0.8470
Epoch 7/10
500/500 [==============================] - 9s 18ms/step - loss: 0.4216 - accuracy: 0.8754
Epoch 8/10
500/500 [==============================] - 10s 20ms/step - loss: 0.3526 - accuracy: 0.8946
Epoch 9/10
500/500 [==============================] - 10s 21ms/step - loss: 0.3016 - accuracy: 0.9086
Epoch 10/10
500/500 [==============================] - 10s 20ms/step - loss: 0.2497 - accuracy: 0.9256
333/333 - 5s - loss: 0.1616 - accuracy: 0.9535
```

## 🌉 Background

As research continues in the development of self-driving cars, one of the key challenges is  [computer vision](https://en.wikipedia.org/wiki/Computer_vision), allowing these cars to develop an understanding of their environment from digital images. In particular, this involves the ability to recognize and distinguish road signs – stop signs, speed limit signs, yield signs, and more.

In this project, I use  [TensorFlow](https://www.tensorflow.org/)  to build a neural network to classify road signs based on an image of those signs. To do so, I need a labeled dataset: a collection of images that have already been categorized by the road sign represented in them.

Several such data sets exist, but for this project, we’ll use the  [German Traffic Sign Recognition Benchmark](http://benchmark.ini.rub.de/?section=gtsrb&subsection=news)  (GTSRB) dataset, which contains thousands of images of 43 different kinds of road signs.

## 🧐 Understanding

First, take a look at the data set by opening the  `gtsrb`  directory. You’ll notice 43 subdirectories in this dataset, numbered  `0`  through  `42`. Each numbered subdirectory represents a different category (a different type of road sign). Within each traffic sign’s directory is a collection of images of that type of traffic sign.

Next, take a look at  `traffic.py`. In the  `main`  function, we accept as command-line arguments a directory containing the data and (optionally) a filename to which to save the trained model. The data and corresponding labels are then loaded from the data directory (via the  `load_data`  function) and split into training and testing sets. After that, the  `get_model`  function is called to obtain a compiled neural network that is then fitted on the training data. The model is then evaluated on the testing data. Finally, if a model filename was provided, the trained model is saved to disk.

## 🧪 My Experimentation Process

My initial goal was to solely gain the maximum accuracy possible, given the dataset. I started with large amounts of hidden layers and one of both a convolutional and output layer, all with slightly differentiating settings and saw what came out of it. Evidently, this did not work as well as I intended, mainly due to immense training times/ETAs and lackluster results. I gradually removed one hidden layer at a time, further tweaking the settings to what I saw fit. This resulted in massive improvements, with an average accuracy increase of 5-7% per iteration. I repeated this cycle various times until I was content with the outcomes.

In the future, I intend to focus on achieving maximum efficiency instead of accuracy, as this will give more training value to the neural network. Of course, I will continue to improve on the accuracy through more intelligent use of the variety of layers, as long as the neural network maintains exemplary growth in knowledge and speed.

## 🙏 Acknowledgements

Data provided by  [J. Stallkamp, M. Schlipsing, J. Salmen, and C. Igel. The German Traffic Sign Recognition Benchmark: A multi-class classification competition. In Proceedings of the IEEE International Joint Conference on Neural Networks, pages 1453–1460. 2011](http://benchmark.ini.rub.de/index.php?section=gtsrb&subsection=dataset#Acknowledgements)
