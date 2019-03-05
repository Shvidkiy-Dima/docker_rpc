
info = {
        'Main': {
            'request': {'method': '(server func)', 'params': '(json serializable object)', 'version': '1.0', 'id': '(callback id)'},
            'response': {
                'success': {'result': '(json)', 'id': '(callback id)', 'version': '1.0', 'type': 'success'},
                'error': {'result': 'error_info(json)', 'id': '(callback id)', 'version': '1.0', 'type': 'error'}
            }
        },
        'Methods': {
            'info': {},
            'get_containers(filtering options)': {
                'Filters': {
                    'all(bool)': 'Show all containers. Only running containers are shown by default',
                    'exited(int)': 'Only containers with specified exit code',
                    'status(str)': 'restarting, running, paused or exited',
                    'label(str)': 'format either "key" or "key=value"',
                    'id(str)': 'The id of the container',
                    'name(str)': 'The name of the container',
                    'before(str)': 'Only containers created before a particular container. Give the container name or id',
                    'since(str)': 'Only containers created after a particularcontainer. Give container name or id',
                    'ancestor(str)': 'Filter by container ancestor. Format of <image-name>[:tag], <image-id>, or <image@digest>.'
                }
            },
            'get_images(filtering options)': {
                'Filters': {
                    'dangling(bool)': '',
                    'label(str)': 'format either key or key=value'
                }

            },
            'start_container(image id)': {},
            'run_container(container id)': {},
            'stop_container(container id)': {},
            'delete_container(container id)': {},

     }
}

