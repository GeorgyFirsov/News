import pickle


def prediction(pickle_path, data):
    """Function converts prepared data
    to a prediction about stocks using serialized
    earlier predictor

    :param pickle_path: full path to serialized predictor object
    :param data: data frame with processed news

    :return: special predicted values in order of companies
    """

    with open(pickle_path, 'rb') as binary:
        predictor = pickle.load(binary)

    data_ready = data.drop(['Company'], axis=1).values

    return predictor.predict(data_ready)
