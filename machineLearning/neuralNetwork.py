from machineLearning.models import FirstFilter
from user.models import Employees
import numpy as np
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Dropout
from machineLearning.models import NeuralNetworkPredictedRecord, NeuralNetworkTestRecord, NeuralNetworkTrainingRecord


def neural_network_predict_hour_work():
    NeuralNetworkPredictedRecord.objects.all().delete()
    NeuralNetworkTestRecord.objects.all().delete()
    NeuralNetworkTrainingRecord.objects.all().delete()
    all_users = Employees.objects.all()
    c = 1
    for user in all_users:
        user = user.employee_id
        print("+++++++++__________________FOR USER_________________+++++++++",user)
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
            training_set_scaled = np.array(training_data)
            X_train = []
            y_train = []
            for i in range(60, len(training_set_scaled)):
                training_saved_database = NeuralNetworkTrainingRecord()
                training_saved_database.use_id_id = user
                training_saved_database.data = training_set_scaled[i]
                training_saved_database.save()
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
            regressor.compile(optimizer='adam', loss='mean_squared_logarithmic_error')
            regressor.fit(X_train, y_train, epochs=100, batch_size=32)
            counter = 0
            testing_data = list()
            for data in all_data:
                if counter < 180:
                    pass
                else:
                    testing_save_database = NeuralNetworkTestRecord()
                    testing_save_database.use_id_id = user
                    testing_save_database.data = data.hours_worked
                    testing_save_database.save()
                    testing_data.append([data.hours_worked])
                counter += 1
            testing_new_data = np.array(testing_data)
            X_test = []
            for i in range(60, 80):
                X_test.append(testing_new_data[i - 60:i, 0])
            X_test = np.array(X_test)
            X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))
            predicted_hours = regressor.predict(X_test)
            for hours in predicted_hours:
                new_data = NeuralNetworkPredictedRecord()
                new_data.use_id_id = user
                new_data.data = hours
                new_data.save()

    return True
