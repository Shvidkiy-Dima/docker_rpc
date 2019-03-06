from .mixins import SerializeDockerMixin

import docker
import json



class BaseDocker:

    def __init__(self):
        self.client = docker.from_env()

    def delete(self, container_id):
        """ delete container """
        c = self.client.containers.get(container_id)
        c.remove()


    def stop(self, container_id):
        """ stop container """
        c = self.client.containers.get(container_id)
        c.stop()


    def start(self, container_id):
        """ start container """
        c = self.client.containers.get(container_id)
        c.start()


    def run(self, image_id):
        """ run container """
        c = self.client.containers.run(image_id, detach=True)
        if c.status == 'created': c.reload()
        return c



class SerializeDocker(SerializeDockerMixin, BaseDocker):

    def __init__(self, date_format='%H:%M %d-%m-%Y', to_json=False):
        self.to_json = to_json
        self.date_format = date_format
        super().__init__()

    def return_data(self, data):
        """ return json or python dict """
        if self.to_json:
            data = json.dumps(data)
        return data

    def run(self, image_id):
        """ run container and return serialize obj """
        i = self.client.images.get(image_id)
        name = self.get_repo(i.tags)['repo']
        container = super().run(name if name != 'None' else image_id)
        return self.return_data(self.make_container(container))


    def get_container_from_id(self, c_id):
        """ serialize obj from container """
        c = self.client.containers.get(c_id)
        return self.return_data(self.make_container(c))


    def get_containers(self, **params):
        """ get containers - filter(**params)"""
        params = self.pars_params(params)
        data = [self.make_container(c) for c in self.client.containers.list(**params)]
        return self.return_data(data)

    def get_images(self, **params):
        """ get images - filter(**params)"""
        params = self.pars_params(params)
        data = [self.make_image(i) for i in self.client.images.list(**params)]
        return self.return_data(data)


    def make_container(self, c):
        container_data = {
            'container_id': c.short_id,
            'full_id': c.id,
            'image': self.get_image_name(c.attrs['Config']['Image']),
            'created': self.get_date(c.attrs['Created']),
            'name': c.attrs['Name'],
            'ports': self.get_ports(c),
            'status': c.status,
        }
        return container_data

    def make_image(self, i):
        image_data = {
            'full_id': i.id,
            'image_id': i.short_id.split(':')[1],
            'created': self.get_date(i.attrs['Created']),
            'size': i.attrs['Size'],
            }
        image_data.update(self.get_repo(i.tags))
        return image_data


