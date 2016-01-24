p = [0.01, 0.02, 0.05, 0.1, 0.2, 0.3, 0.5, 0.7, 0.9]
median = [34.133907371, 34.1327252224, 34.13226688, 34.1194349104, 34.0824079148, 34.046155306, 33.9054977062, 33.510836225, 30.3595637521]
mean = [33.0049614358, 32.763636743, 32.0363070177, 30.7919720571, 29.3613771908, 28.710292168, 28.212216381, 28.0186615155, 27.9379977358]

import matplotlib.pyplot as plt
medianplt, = plt.plot(p,median,'ro-',label='Median Filtering')
meanplt, = plt.plot(p,mean,'bo-',label='Mean Filtering')
plt.legend(handles=[medianplt,meanplt])

plt.savefig("plot.png")
plt.show()