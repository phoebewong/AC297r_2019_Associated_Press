from media_api import MediaApi
import numpy as np
import configparser

if __name__ == '__main__':
    # Checking to see if things work

    config = configparser.ConfigParser()
    config.read('password.ini')
    apikey = (config['key']['apikey'])

    counter = 0
    while counter < 1000:
        media_item = MediaApi(apikey)
        print('Call: {}'.format(counter))

        # If you don't have any data files and want to make a request, do this
        response = media_item.make_get_request()
        json_response = media_item.get_json_response()
        qt = json_response['id']
        print('Used: {}'.format(response.headers['x-mediaapi-Q-used']))

        # If you want to read from a data file do this
        # file_name = '../../data/old/media_1569609607.json'
        # json_response = media_api.get_json_response_from_file(file_name)

        items = media_item.get_items()
        article_count = media_item.get_item_count()
        if items is None:
            print('no articles left')
            break

        print('{} articles found'.format(article_count))
        for art in range(article_count):
            print('Article {} of {}'.format(art, article_count))
            article_item = media_item.get_specific_item(art)

            images = article_item.get_associations()
            if images is None:
                continue
            image_count = article_item.get_association_count()

            print('{} images found in article {}'.format(image_count, art))
            # count goes from 1 to n here
            for img in images.keys():
                print('Image {} of {}'.format(img, image_count))
                image_item = article_item.get_specific_association(img)

        media_item = MediaApi(apikey, qt)
        counter = counter + 1

    # getting specific things from the item
    # print(article_item.get_headline())
    # print(article_item.get_uri())
    # print(article_item.get_full_json_response())
    # print(article_item.get_entities())
