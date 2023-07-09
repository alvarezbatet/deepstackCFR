# -*- coding: utf-8 -*-
"""
Created on Mon May 11 17:37:53 2020

@author: Roger
"""
import pandas as pd
import pickle
import numpy as np

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers


path = r'C:\Users\Roger\Desktop\Computer vision online game\DeepStack\models\3\raw'
inputs = []
for i in range(10):
    print("loading inputs file: ", i, "/10")
    with open(path+"\inputs"+str(i)+".txt", "rb") as f:
        inputs += pickle.load(f)
outputs = []
for i in range(10):
    for j in range(20):
        print("loading outputs file: "+str(i)+"_"+str(j)+"/10")
        with open(path+"\outputs_"+str(i)+"_"+str(j)+".txt", "rb") as f:
            outputs += pickle.load(f)

for i in range(len(inputs)):
    if i % 1000 == 0:
        print("building input and output list ", i,"/", len(inputs))
    inputs[i] = np.concatenate((np.array([val/51 for val in inputs[i][0]]), np.array([inputs[i][1], inputs[i][2]]), inputs[i][3], inputs[i][4]), axis=None)
    outputs[i] = np.concatenate((outputs[i][0], outputs[i][1]), axis=None)

train_inputs, train_outputs = np.array(inputs[:int(len(inputs)*0.8)]), np.array(outputs[:int(len(inputs)*0.8)])
test_inputs, test_outputs = inputs[int(len(inputs)*0.8):], outputs[int(len(inputs)*0.8):]

lrelu = tf.keras.layers.LeakyReLU(alpha=0.1)

def build_model():
  model = keras.Sequential([
    layers.Dense(500, activation=lrelu, input_shape=[len(inputs[0])]),
    layers.Dense(500, activation=lrelu),
    layers.Dense(len(outputs[0]))
  ])

  optimizer = tf.keras.optimizers.RMSprop(0.001)  #TODO investigate other optimizers(Adam,...

  model.compile(loss='mse',
                optimizer=optimizer,
                metrics=['mae', 'mse'])
  return model

model = build_model()

print(model.summary())
example_batch = np.array([train_inputs[0]])
print(len(model.predict(example_batch)[0]))

EPOCHS = 45

history = model.fit(
  train_inputs, train_outputs,
  epochs=EPOCHS, validation_split = 0.2, verbose=1,
  callbacks=[tf.keras.callbacks.TensorBoard()])

