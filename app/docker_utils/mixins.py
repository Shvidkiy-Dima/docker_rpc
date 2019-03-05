from datetime import datetime
import json

class SerializeDockerMixin:
    date_format = '%H:%M %d-%m-%Y'

    def get_date(self, date):
        try:
            datetime_ = datetime.strptime(date.split('.')[0], '%Y-%m-%dT%H:%M:%S')
            strtime = datetime_.strftime(self.date_format)
        except Exception:
            strtime = 'None'
        return strtime

    def get_repo(self, repotags):
        repo, tags = repotags[0].split(':') if repotags else ('None', 'None')
        return {'repo': repo, 'tags': tags}

    def get_ports(self, container):
        p = container.attrs['NetworkSettings']['Ports']
        p = {k: (':'.join([j for j in v[0].values()]) if v is not None else [])
               for k, v in p.items()}
        return (p or container.attrs['Config'].get('ExposedPorts')) or {}


    def pars_params(self, params):
        if isinstance(params, str):
            params = json.loads(params)
        filters = {}
        if 'all' in params:
            filters['all'] = params.pop('all')
        if params:
            filters['filters'] = params
        return filters


    def get_image_name(self, name):
        if name.startswith('sha256'):
            name = name.split(':')[1][:10]
        return name