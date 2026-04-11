
FUNCTIONS_CHAINING={
    'find_children':{
        'name':'find_children',
        'description':'查找记忆树某节点下的所有子节点，返回这些子节点的描述信息',
        'parameters':{
            'type': 'object',
            'properties':{
                'node_tag':{
                    'type':'string',
                    'description':'要查询节点的描述信息，为空代表查询根节点'
                }
            },
            'required': ['message'],
        }
    },
    'restruct_children':{
        'name':'restruct_children',
        'description':'将记忆树的一个节点的一个或多个子节点作为目标节点，将目标节点的父节点替换为一个新节点，并且新节点的描述信息能够概括这些目标节点，并使新节点的父节点为该节点',
        'parameters':{
            'type':'object',
            'properties':{
                'children_list':{
                    'type':'array',
                    "items": {
                        "type": "string"
                    },
                    'description':'目标节点列表'
                },
                'node_tag':{
                    'type':'string',
                    'description':'新节点的描述信息'
                }
            },
            'required': ['children_list','node_tag']
        }
    },
    'add_children':{
        'name':'add_children',
        'description':'在记忆树的一个非叶节点下添加子节点',
        'parameters':{
            'type':'object',
            'properties':{
                'father_tag':{
                    'type':'string',
                    'description':'要添加子节点的父节点的描述信息'
                },
                'node_tag':{
                    'type':'string',
                    'description':'要添加的叶节点的描述信息'
                }
            },
            'required': ['father_tag','node_tag']
        }
    },
    'send_message':{
        'name':'send_message',
        'description':'向用户发送信息',
        'parameters':{
            'type':'object',
            'properties':{
                'message':{
                    'type':'string',
                    'description':'发送给用户的信息'
                }
            },
            'required':['message']
        }
    }
}


