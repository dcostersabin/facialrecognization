from machineLearning.models import FirstFilter
from user.models import Employees
from sklearn.preprocessing import MinMaxScaler
import numpy as np
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Dropout


def neural_network_predict_hour_work(user=1):
    if Employees.objects.filter(employee_id=user).exists():
        training_data = list()
        all_data = FirstFilter.objects.filter(user_id_id=user).order_by('-entry_date')[:400]
        counter = 0
        for data in all_data:
            if counter < 200:
                training_data.append([data.hours_worked])
            else:
                break
            counter += 1
        training_data.reverse()
        # //feature scaling
        # sc = MinMaxScaler(feature_range=(0, 1))
        # training_set_scaled = sc.fit_transform(training_data)
        training_set_scaled = np.array(training_data)
        # return training_set_scaled
        X_train = []
        y_train = []
        for i in range(60, len(training_set_scaled)):
            X_train.append(training_set_scaled[i - 60:i, 0])
            y_train.append(training_set_scaled[i, 0])

        X_train, y_train = np.array(X_train), np.array(y_train)
        X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))
        regressor = Sequential()
        regressor.add(LSTM(units=50, return_sequences=True, input_shape=(X_train.shape[1], 1)))
        regressor.add(Dropout(0.2))

        regressor.add(LSTM(units=50, return_sequences=True))
        regressor.add(Dropout(0.2))

        regressor.add(LSTM(units=50, return_sequences=True))
        regressor.add(Dropout(0.2))

        regressor.add(LSTM(units=50))
        regressor.add(Dropout(0.2))

        regressor.add(Dense(units=1))
        regressor.compile(optimizer='dadam', loss='mean_squared_logarithmic_error')
        regressor.fit(X_train, y_train, epochs=100, batch_size=32)
        counter = 0
        testing_data = list()
        for data in all_data:
            if counter < 180:
                pass
            else:
                testing_data.append([data.hours_worked])
            counter += 1
        testing_new_data = np.array(testing_data)
        X_test = []
        for i in range(60, 80):
            X_test.append(testing_new_data[i - 60:i, 0])
        X_test = np.array(X_test)
        X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))
        # return X_train.shape
        predicted_hours = regressor.predict(X_test)
        # predicted_hours = sc.inverse_transform(predicted_hours)
        return predicted_hours
