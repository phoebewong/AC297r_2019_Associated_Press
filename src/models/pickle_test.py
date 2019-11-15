import dill

if __name__ == '__main__':
    # replace this with the model you want to test
    with open('knn_model.pkl', 'rb') as f:
        model = dill.load(f)

    # replace this with an example of data input
    data = (['general news', 'police', 'law enforcement agencies', 'government and politics', 'robbery', 'theft', 'crime', 'automotive accidents', 'transportation accidents', 'accidents', 'accidents and disasters', 'transportation'])
    predictions = model.predict(data)

    # print predictions. if this works, the model will run on the UI
    print(predictions)

    # try again
    # replace this with an example of data input
    data = (['general news', 'police', 'law enforcement agencies', 'government and politics', 'robbery', 'theft', 'crime', 'automotive accidents', 'transportation accidents', 'accidents', 'accidents and disasters', 'transportation'])
    predictions = model.predict(data)

    # print predictions. if this works, the model will run on the UI
    print(predictions)
