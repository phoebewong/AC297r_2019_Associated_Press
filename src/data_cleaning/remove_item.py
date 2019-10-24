import csv
import constants

#cleaning history output
history_dir = constants.HIST_DIR
hist_content_type_name = constants.media_removal_hist_name
hist_article_name = constants.article_removal_hist_name

#cleaning output directory
output_directory = constants.OUTPUT_DIR

def remove_content_type(img_summary_file, content_type, output_file):
    '''
    remove media files of unwanted content type.

    Params:
    -------
    1) img_summary_file: string, media file summary csv name
    2) content_type: list or array_like, content type to remove
    3) output_file: string, new media file summary csv output name

    Return:
    -------
    write txt file for media file removal
    '''
    #track removal
    remove_list = list()

    with open(img_summary_file, 'r') as image_summary, open(output_file, 'w') as image_summary_new:
        csv_reader = csv.reader(image_summary)
        csv_writer = csv.writer(image_summary_new)
        #get header of csv file
        header = next(csv_reader)
        csv_writer.writerow(header)
        #find image id, article id, content type index
        idx_iid, idx_ct = header.index('id'), header.index('content_type')
        for row in csv_reader:
            #if content type is for removal
            if row[idx_ct] in content_type:
                #record image id
                remove_list.append(row[idx_iid])
            else:
                csv_writer.writerow(row)

    #filename for removal
    img_removal_file = f'{history_dir}/{hist_content_type_name}'
    print(f'{len(remove_list)} media files removed')
    print(f'writing {img_removal_file}')
    with open(img_removal_file, 'w') as removal_hist:
        for idx in remove_list:
            removal_hist.write(f'{idx}\n')

def remove_foreign_article(article_summary_file, target_language, output_file):
    '''
    remove article files in unwanted language.

    Params:
    -------
    1) article_summary_file: string, article summary csv file name
    2) target_language: list or array_like, language type to keep
    3) output_file: string, output file name

    Return:
    -------
    write txt file for article removal
    '''
    #track removal
    remove_list = list()

    with open(article_summary_file, 'r') as article_summary, open(output_file, 'w') as article_summary_new:
        csv_reader = csv.reader(article_summary)
        csv_writer = csv.writer(article_summary_new)
        #get header of csv file
        header = next(csv_reader)
        csv_writer.writerow(header)
        #find article id, language index
        idx_id, idx_lang = header.index('id'), header.index('language')
        for row in csv_reader:
            #if language is not for keep
            if row[idx_lang] not in target_language:
                #record article id
                remove_list.append(row[idx_id])
            else:
                csv_writer.writerow(row)

    #filename for removal
    article_removal_file = f'{history_dir}/{hist_article_name}'
    print(f'{len(remove_list)} articles removed')
    print(f'writing {article_removal_file}')
    with open(article_removal_file, 'w') as removal_hist:
        for idx in remove_list:
            removal_hist.write(f'{idx}\n')

def remove_article_wo_images(new_image_summary_file, new_article_summary_file):
    '''
    identify article files without associated images.

    Params:
    -------
    1) new_image_summary_file: string, new image summary csv file name after calling "remove content type"
    2) new_article_summary_file: string, new article summary csv file name after calling "remove foreign article"

    Return:
    -------
    append to article txt file for article removal
    '''
    #track article ids in article and image summary
    article_id = list()
    article_idx = list()

    #get article id from article summary
    with open(new_article_summary_file, 'r') as article_summary:
        csv_reader = csv.reader(article_summary)
        #get header of csv file
        header = next(csv_reader)
        #find article id
        idx_id = header.index('id')
        for row in csv_reader:
            article_id.append(row[idx_id])

    #get article id from image summary
    with open(new_image_summary_file, 'r') as image_summary:
        csv_reader = csv.reader(image_summary)
        #get header of csv file
        header = next(csv_reader)
        #find article id
        idx_aid = header.index('article_idx')
        for row in csv_reader:
            article_idx.append(row[idx_aid])

    #remove list
    remove_list = list(set(article_id) - set(article_idx))

    #filename for removal
    article_removal_file = f'{history_dir}/{hist_article_name}'
    print(f'{len(remove_list)} articles added to removal list')
    print(f'appending to {article_removal_file}')
    with open(article_removal_file, 'a+') as removal_hist:
        for idx in remove_list:
            removal_hist.write(f'{idx}\n')
