from ..core import chainstream_core
from flask import jsonify, Blueprint, request

devices_blueprint = Blueprint('devices_blueprint', __name__)


@devices_blueprint.route('/api/devices/deviceCards', methods=['GET'])
def get_all_device_cards():
    # data = chainstream_core.get_all_device_cards()
    data = [{"model_name": "ll", "content": 'Content of card'},
            {"model_name": "hh", "content": 'Content of card'},
            {"model_name": "Edge xx", "content": 'Content of card'}]
    return jsonify(data)


@devices_blueprint.route('/api/devices/agentList', methods=['GET'])
def get_agent_list():
    # data = chainstream_core.get_agent_list()
    data = [
        {
            "value": 'hjh',
            "label": 'Agent 2', },
        {
            "value": 'sdf',
            "label": 'Agent 5', },
        {
            "value": 'dsf',
            "label": 'Agent 6', },
    ]
    return jsonify(data)


@devices_blueprint.route('/api/devices/checkDevice', methods=['POST'])
def check_device():
    try:
        # 从请求中获取 JSON 数据
        device_form = request.get_json()

        if not device_form:
            return jsonify({'error': 'No data provided'}), 400

        # 假设有一个函数检查设备信息是否有效
        sensor_info = ...

        if sensor_info:
            return jsonify({'status': 'success', 'message': sensor_info}), 200
        else:
            return jsonify({'status': 'failure', 'message': sensor_info}), 404

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@devices_blueprint.route('/api/devices/addDevice', methods=['POST'])
def add_device():
    try:
        # 从请求中获取 JSON 数据
        device_form = request.get_json()

        if not device_form:
            return jsonify({'error': 'No data provided'}), 400

        # 假设有一个函数添加设备信息
        device_id = ...

        if device_id:
            return jsonify({'status': 'success', 'message': 'Device added successfully'}), 200
        else:
            return jsonify({'status': 'failure', 'message': 'Failed to add device'}), 404

    except Exception as e:
        return jsonify({'error': str(e)}), 500
