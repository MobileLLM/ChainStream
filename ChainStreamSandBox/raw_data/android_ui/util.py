import os
import csv
import tqdm
import json


def select_id_by_app(app_num=50, screenshot_pre_app=10):
    details_path = os.path.join(os.path.dirname(__file__), 'ui_details.csv')

    selected_ids = []
    app_count = {}
    app_finished = 0
    with open(details_path, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # skip header
        for row in reader:
            app_name = row[1]
            ui_id = row[0]
            if app_name not in app_count:
                app_count[app_name] = 1
                selected_ids.append(ui_id)
            else:
                if app_count[app_name] < screenshot_pre_app:
                    app_count[app_name] += 1
                    selected_ids.append(ui_id)
                else:
                    app_finished += 1
                    if app_finished == app_num:
                        break

    print(app_count)

    return selected_ids


def make_data(app_num=50, screenshot_pre_app=10):
    raw_data_path = "/Users/liou/dataset/rico/combined"
    output_path = os.path.join(os.path.dirname(__file__), 'screenshot_data')
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    selected_ids = select_id_by_app(app_num, screenshot_pre_app)


    for ui_id in tqdm.tqdm(selected_ids):
        # copy screenshot to output path
        file_type = ''
        if os.path.exists(os.path.join(raw_data_path, ui_id + '.png')):
            file_type = 'png'
        elif os.path.exists(os.path.join(raw_data_path, ui_id + '.jpg')):
            file_type = 'jpg'
        else:
            print("No screenshot found for ui_id: {}".format(ui_id))
        src_path_img = os.path.join(raw_data_path, ui_id + '.' + file_type)
        dst_path_img = os.path.join(output_path, ui_id + '.' + file_type)
        src_path_json = os.path.join(raw_data_path, ui_id + '.json')
        dst_path_json = os.path.join(output_path, ui_id + '.json')
        os.system("cp {} {}".format(src_path_img, dst_path_img))
        os.system("cp {} {}".format(src_path_json, dst_path_json))


if __name__ == '__main__':
    make_data(app_num=50, screenshot_pre_app=10)