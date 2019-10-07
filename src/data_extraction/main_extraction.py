from media_item import MediaItem
import numpy as np
import configparser

if __name__ == '__main__':
    # Reading the password in
    config = configparser.ConfigParser()
    config.read('password.ini')
    apikey = (config['key']['apikey'])
    media_item = MediaItem()

    # Make requests to get pages
    counter = 0
    while counter < 100000:
        print('Call: {}'.format(counter))

        # making a get request
        response = media_item.make_get_request(apikey)
        json_response = media_item.get_json_response()
        qt = json_response['id']

        # all the articles in the json response
        items = media_item.get_items()
        article_count = media_item.get_item_count()

        # if there are no articles left we break
        if items is None or len(items) == 0:
            print('no articles left')
            break

        # if there are articles
        print('{} articles found'.format(article_count))

        # looping through all the articles
        for art in range(article_count):
            print('Article {} of {}'.format(art, article_count))
            # save full json response
            article_item = media_item.get_specific_item(art)
            article_item.save_full_json_response(apikey)

            # getting all the associations (images)
            images = article_item.get_associations()

            # if there are no images we do nothing
            if images is None:
                continue

            # getting all the images
            image_count = article_item.get_association_count()
            print('{} images found in article {}'.format(image_count, art))

            # looping through all the images
            # count goes from 1 to n here
            for img in images.keys():
                print('Image {} of {}'.format(img, image_count))
                # save full json response
                image_item = article_item.get_specific_association(img)
                image_item.save_full_json_response(apikey)

        # going to the next page
        media_item = MediaApi(qt=qt)
        counter = counter + 1
