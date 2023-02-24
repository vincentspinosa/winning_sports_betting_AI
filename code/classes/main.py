from Model import Model
from Layer import Layer

model = Model()

l1 = Layer()
l2 = Layer()
l3 = Layer()

model.add_layer(l1)
model.add_layer([l2, l3])

print(model.fit())


