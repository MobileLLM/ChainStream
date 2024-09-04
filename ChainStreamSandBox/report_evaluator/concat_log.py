import json
import os.path
import datetime


def _load_sandbox_logs(log_paths: list):
    log_data = []
    for log_path in log_paths:
        with open(log_path, 'r', encoding='utf-8') as file:
            tmp_log = json.load(file)
        log_data.append(tmp_log)
    return log_data


def concat_logs(log_path_list, new_base_path):
    log_data_list = _load_sandbox_logs(log_path_list)

    first_repeat_time = log_data_list[0]['repeat_time']
    first_task_list = log_data_list[0]['task_list']
    first_generator_name = log_data_list[0]['generator']['generator_class_name']

    for i in range(1, len(log_data_list)):
        if log_data_list[i]['repeat_time']!= first_repeat_time:
            raise ValueError('Repeat time of different logs is not equal.')
        if log_data_list[i]['generator']['generator_class_name'] != first_generator_name:
            raise ValueError('Generator name of different logs is not equal.')
        if log_data_list[i]['task_list']!= first_task_list:
            raise ValueError('Task list of different logs is not equal.')

    all_task_reports = log_data_list[0]['task_reports']
    for task_name, task_report_list in all_task_reports.items():
        for task_report in task_report_list:
            if task_report['report_path'][0] == 'C':
                tmp_report_path = task_report['report_path'].replace('\\', '/')
            else:
                tmp_report_path = task_report['report_path']
            tmp_report_path = tmp_report_path.split("/result/")[-1]
            task_report['report_path'] = os.path.join(new_base_path, tmp_report_path)

    for i in range(1, len(log_data_list)):
        tmp_task_report = log_data_list[i]['task_reports']
        print(f"{i}th log has {len(tmp_task_report)} task reports.")
        for task_name, task_report_list in tmp_task_report.items():
            # print(f"{i}th log has {len(task_report_list)} task reports.")

            for task_report in task_report_list:
                if task_report['report_path'][0] == 'C':
                    tmp_report_path = task_report['report_path'].replace('\\', '/')
                else:
                    tmp_report_path = task_report['report_path']
                tmp_report_path = tmp_report_path.split("/result/")[-1]
                task_report['report_path'] = os.path.join(new_base_path, tmp_report_path)

            if task_name in all_task_reports:
                all_task_reports[task_name].extend(task_report_list)
            else:
                print(f"Task {task_name} is not in the first log.")
                all_task_reports[task_name] = task_report_list

    log_data_list[0]['task_reports'] = all_task_reports

    log_data_list[0]['concat_log_from'] = log_path_list

    with open(log_path_list[0].replace('.json', f'_{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}_concat_log.json'), 'w', encoding='utf-8') as file:
        json.dump(log_data_list[0], file, ensure_ascii=False, indent=4)
        print('Concatenate logs successful.')


if __name__ == '__main__':
    new_base_path = "/Users/liou/Desktop/2024-09-03_19-36-37_chainstream-0-shot-0-example"
    log_path_list = [
        '/Users/liou/Desktop/2024-09-03_19-36-37_chainstream-0-shot-0-example/2024-09-03_19-27-33_chainstream-0-shot-0-example/test_log.json',
        '/Users/liou/Desktop/2024-09-03_19-36-37_chainstream-0-shot-0-example/2024-09-03_19-36-37_chainstream-0-shot-0-example-1/test_log.json',
        '/Users/liou/Desktop/2024-09-03_19-36-37_chainstream-0-shot-0-example/2024-09-03_19-37-51_chainstream-0-shot-0-example-2/test_log.json',
        '/Users/liou/Desktop/2024-09-03_19-36-37_chainstream-0-shot-0-example/2024-09-03_19-38-58_chainstream-0-shot-0-example-3/test_log.json',
        '/Users/liou/Desktop/2024-09-03_19-36-37_chainstream-0-shot-0-example/2024-09-03_19-40-03_chainstream-0-shot-0-example-4/test_log.json',
    ]
    concat_logs(log_path_list, new_base_path)


