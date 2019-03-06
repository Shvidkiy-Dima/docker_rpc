
var server = "ws://localhost:8000/ws/"



const StopContainer = '<div class="card"><div class="card-body px-0 py-1"><table class="table"><thead class="thead-dark"><tr>' +
'<th scope="col">Id</th><th scope="col">Image</th><th scope="col">Created</th><th scope="col">Names</th>' +
'</tr></thead><tbody><tr><td>{{ id }}</td><td>{{ image }}</td><td>{{ created }}</td><td>{{ name }}</td></tr></tbody></table>'+
'<div class="row"><div class="col"><a  class="badge badge-secondary text-white ml-3" style="font-size:20px">{{ status }}</a>'+
'</div><div class="col"><strong>Ports: </strong>{{ ports }}</div></div>'+
' <div v-show=load class="spinner-border float-right" role="status"><span class="sr-only">Loading...</span></div>' +
'<button :id=id  v-show=!load :data-action=index @click="delete_container" '+
'class="btn btn-sm btn-danger float-right mr-2"> Delete</button>' +
'<button v-show=!load :id=id  :data-action=index @click="start_container" class="btn btn-sm btn-danger float-right mr-2"> Start</button></div></div></div></div>'

const RunningContainer = '<div class="card"><div class="card-body px-0 py-1"><table class="table"><thead class="thead-dark"><tr>' +
'<th scope="col">Id</th><th scope="col">Image</th><th scope="col">Created</th><th scope="col">Names</th>' +
'</tr></thead><tbody><tr><td>{{ id }}</td><td>{{ image }}</td><td>{{ created }}</td><td>{{ name }}</td></tr></tbody></table>'+
'<div class="row"><div class="col"><a  class="badge badge-primary text-white ml-3" style="font-size:20px">{{ status }}</a>'+
'</div><div class="col"><strong>Ports: </strong>{{ ports }}</div></div>'+
' <div v-show=load class="spinner-border float-right" role="status"><span class="sr-only">Loading...</span></div>' +
'<button :id=id v-show=!load :data-action=index @click="handler" '+
'class="btn btn-sm btn-danger float-right mr-2">  Stop</button></div></div>'

const PausedContainer = '<div class="card"><div class="card-body px-0 py-1"><table class="table"><thead class="thead-dark"><tr>' +
'<th scope="col">Id</th><th scope="col">Image</th><th scope="col">Created</th><th scope="col">Names</th>' +
'</tr></thead><tbody><tr><td>{{ id }}</td><td>{{ image }}</td><td>{{ created }}</td><td>{{ name }}</td></tr></tbody></table>'+
'<div class="row"><div class="col"><a  class="badge badge-secondary text-white ml-3" style="font-size:20px">{{ status }}</a>'+
'</div><div class="col"><strong>Ports: </strong>{{ ports }}</div></div> </div></div>'


const Image =  '<div class="card"><div class="card-body px-0  py-1"><table class="table"><thead class="thead-dark">' +
'<tr><th scope="col">REPOSITORY</th><th scope="col">TAG</th><th scope="col">ID</th><th scope="col">CREATED</th></tr>'+
'</thead><tbody><tr><td>{{ repo }}</td><td>{{ tags }}</td><td> {{ id }}</td><td>{{ created }}</td>'+
'</tr></tbody></table><strong class="px-2 ">SIZE</strong>{{ size }} MB ' +
' <div v-show=load class="spinner-border float-right" role="status"><span class="sr-only">Loading...</span></div>' +
' <button   v-show=!load :id=id  :data-action=index @click="handler" class="btn btn-sm btn-danger float-right mr-2"> Run</button></div></div>' +
'<transition name="fade"> <p v-if="!load">привет</p> </transition>'

const EmptyTemplate =  '<h1>Nothing found</h1>'

const FilterContainers =  '<form @submit.prevent="onSubmit"> <p> <label for="name">Name:</label> <input id="name" v-model="name" placeholder="name">' +
    '</p> <p> <label for="review">Ancestor:</label> <input id="ancestor" v-model="ancestor" placeholder="ancestor">' +
    '</p> <p> <label for="status">Status:</label> <select id="status" v-model="status"> <option></option>' +
      '<option>running</option> <option>exited</option> <option>created</option> <option>restarting</option>' +
      '<option>paused</option> </select>  </p> <input type="checkbox" id="all-containers" v-model="all" true-value=true false-value=false>' +
     '<label for="all-containers">all</label> <p> <input type="submit" value="Submit" value="Go"> </p> </form>'

const FilterImages = '<form  @submit.prevent="onSubmit"> <p> <label for="label">label:</label>' +
        '<input id="label" v-model="label" placeholder="label"> </p> <input id="all-images" type="checkbox" v-model="all" true-value=true false-value=false>' +
    '<label for="all-images">all</label> <br> <label for="dangling-images">dangling</label><br>' +
    '<input type="radio" value="true" v-model="dangling"> True <input type="radio" value="false" v-model="dangling">False' +
    '<input type="radio" value="null" v-model="dangling"> Null <p> <input type="submit" value="Submit" value="Go">'+
    '</p> </form>'

Vue.component('filter_containers', {
     template: FilterContainers,
     data() {
      return {
        name: null,
        ancestor: null,
        status: null,
        all: 'false',
      }
    },
     methods: {
            onSubmit: function(e) {
                var data = {'all': JSON.parse(this.all)}
                if (this.name) { data['name'] = this.name }
                if (this.status) { data['status'] = this.status }
                if (this.ancestor) { data['ancestor'] = this.ancestor }
                app.send_filter(data, 'container')
                }
            }
    })

Vue.component('filter_images', {
     template: FilterImages,
     data() {
      return {
        label: null,
        dangling: null,
        all: 'false',
      }
    },
     methods: {
            onSubmit: function(e) {
                console.log(this.all, this.dangling)
                var data = {'all': JSON.parse(this.all)}
                if (this.label) { data['label'] = this.label }
                if (this.dangling == 'false' || this.dangling == 'true') { data['dangling'] = JSON.parse(this.dangling) }
                app.send_filter(data, 'image')

            }
         }
    })


Vue.component('created', {
  template: StopContainer,
  props: ['id', 'command', 'image', 'created', 'name', 'ports', 'status', 'index', 'load'],
  methods: {
    delete_container: function(e) {
        index = e.target.getAttribute('data-action')
        id = e.target.getAttribute('id')
         Vue.set(app.containers[index], 'load', true)
        app.remove(index, id)
    },
    start_container: function(e) {
                    index = e.target.getAttribute('data-action')
        id = e.target.getAttribute('id')
         Vue.set(app.containers[index], 'load', true)
        app.start(index, id)
    },

    },

})


Vue.component('restarting', {
  template: PausedContainer,
  props: ['id', 'command', 'image', 'created', 'name', 'ports', 'status', 'index', 'load'],
})

Vue.component('paused', {
  template: PausedContainer,
  props: ['id', 'command', 'image', 'created', 'name', 'ports', 'status', 'index', 'load'],
})

Vue.component('running', {
  template: RunningContainer,
  props: ['id', 'command', 'image', 'created', 'name', 'ports', 'status', 'index', 'load'],
  methods: {
    handler: function(e) {
        index = e.target.getAttribute('data-action')
        id = e.target.getAttribute('id')
        Vue.set(app.containers[index], 'load', true)
        app.stop(index, id)
    }
  }
})

Vue.component('exited', {
  template: StopContainer,
  props: ['id', 'command', 'image', 'created', 'name', 'ports', 'status', 'index' , 'load'],

    methods: {
        delete_container: function(e) {
            index = e.target.getAttribute('data-action')
            id = e.target.getAttribute('id')
             Vue.set(app.containers[index], 'load', true)
            app.remove(index, id)
        },
        start_container: function(e) {
            index = e.target.getAttribute('data-action')
            id = e.target.getAttribute('id')
            Vue.set(app.containers[index], 'load', true)
            app.start(index, id)
        },

    },
})

Vue.component('docker_image', {
  template: Image,
  props: ['id','created', 'repo', 'tags', 'size', 'index', 'load'],
      methods: {
        handler: function(e) {
            index = e.target.getAttribute('data-action')
            id = e.target.getAttribute('id')
            Vue.set(app.images[index], 'load', true)
            app.run(index, id)
            }
        }
})

Vue.component('error-modal', { template: '#modal-template'})

var app = new Vue({
  el: '#app',
  data() {
    return {
          containers: [],
          images: [],
          info_images: '',
          info_containers: '',
          showModal: false,
          error_msg: '',
          error_name: '',
        }
    },
  created: function () {
        this.ws = new WebSocket(server);
        var ws = this.ws
        this.store = {}
        this.id = 0
        this.count_containers = 0
        this.count_images = 0

        ws.onopen = function() {
            var init_images = function(data) {
            if (data.length > 0) {
                  app.set_images(data)
             }
            else {
                 app.set_empty('image')
                }
            }
            app.id += 1
            app.store[String(app.id)] = init_images

            data = JSON.stringify({'method': 'get_images', 'params':null, 'version': '1.0', 'id': app.id})
            ws.send(data);

            var init_containers = function(data) {
                if (data.length > 0) {
                    app.set_containers(data, 'running_container')
                }
                else {
                     app.set_empty('container')
                }
            }
            app.id += 1
            app.store[String(app.id)] = init_containers

            data = JSON.stringify({'method': 'get_containers', 'params': {'status': 'running'}, 'version': '1.0', 'id': app.id})
            ws.send(data)
        },

        ws.onmessage = function (response) {
            var data = JSON.parse(response.data)
            if (data['type'] != 'error') {
                app.dispatcher(data)
             }
             if (data['type'] == 'error') {
                app.check_error(data['result'])
             }
        }
        ws.close = function() {
            console.log('Close!')
        }



   },
  methods: {


            dispatcher: function(data) {
                console.log(data, 'recived')
                var id = data['id']
                var result = data['result']
                var callback = this.store[id]
                console.log(callback)
                callback(result)
                delete this.store[id]

            },
            send_filter: function(params, type) {
                this.id += 1

                if (type == 'container') {
                    data = JSON.stringify({'method': 'get_containers', 'params': params, 'version': '1.0', 'id': this.id})
                    this.ws.send(data)
                    callback = function(containers) {
                                    app.containers = []
                                    if (containers.length > 0) {
                                        app.info_containers = ''
                                        app.set_containers(containers)
                                        }
                                    else {
                                        app.set_empty('container')
                                        }
                                    }
                    }
                if (type == 'image') {
                    data = JSON.stringify({'method': 'get_images', 'params': params, 'version': '1.0', 'id': this.id})
                    this.ws.send(data)
                    callback = function(images) {
                                    app.images = []
                                     if (images.length > 0) {
                                        app.set_images(images)
                                        }
                                    else {
                                        app.set_empty('image')
                                        }

                                     }
                        }
                this.store[String(this.id)] = callback
            },

           info: function(){
            this.id += 1
             data = JSON.stringify({'method': 'info', 'params': null , 'version': '1.0', 'id': this.id})
             callback = function(data){
                        console.log(data)
                        return data
                    }
             this.store[String(this.id)] = callback
             this.ws.send(data)
            },

            check_error: function(error){
                    this.showModal = true
                    this.error_msg = error['msg']
                    this.error_name = error['name']
                    app.containers.forEach(function(a) {a.load = false})
                    app.images.forEach(function(a) {a.load = false})
            },

            set_images:  function (data) {
                data.forEach(function push(item) {
                    app.count_images += 1
                    app.images.push({'docker_image': {
                               'id': item['image_id'],
                               'created': item['created'],
                               'tags': item['tags'],
                               'repo': item['repo'],
                               'size': Math.floor(Number(item['size']) / 1000000),
                               },
                               'load': false,
                               'type': 'docker_image'})
                    });

            },

            set_containers:function (data, type) {
                    data.forEach(function push(item, index) {
                    index = app.containers.push({'container': {
                           'id': item['container_id'],
                           'created': item['created'],
                           'name': item['name'],
                           'ports': app.parse_ports(item['ports']),
                            'status': item['status'],
                             'image': item['image'],
                           },
                            'load': false,
                           'type': item['status']})
                          })
           },
           change_container: function (type, index){
                var container = app.containers[index]['container']

                var data = {'container':
                                 {'id': id,
                                'created': container['created'],
                                 'name' :  container['name'],
                                  'ports': container['ports'],
                                  'image': container['image'],
                                  'status': type},
                                  'load': false,
                                    'type': type}
                app.containers.splice(index,1, data);
            },


          set_empty: function(type) {
                if (type == 'container') {
                    this.info_containers = EmptyTemplate
                }
                if (type == 'images') {
                    this.info_images = EmptyTemplate
                }


          },

          parse_ports: function(data) {
                    var ports = ''
                    for (key in data) {
                        if (data[key].length > 0) {
                                ports += data[key] + ' -> ' + key + ', '
                            }
                        else {
                            ports += key + ', '
                        }
                    }
                    return ports

          },

          start: function(index, id) {
                   this.id += 1
                   callback = function(data) {
                           app.change_container('running', index)
                            }
                   this.store[String(this.id)] = callback
                   data = JSON.stringify({'method': 'start_container', 'params': {'id': id} , 'version': '1.0', 'id': this.id})
                   this.ws.send(data)
            },


          run: function(index, id) {
                this.id += 1
                callback = function(data) {
                                console.log(app.containers.length)
                              if (app.containers.length == 0) {
                                    app.info_containers = ''
                              }
                              app.set_containers([data], 'running_container')
                              Vue.set(app.images[index], 'load', false)
                            }
                this.store[String(this.id)] = callback
                data = JSON.stringify({'method': 'run_container', 'params': {'id': id} , 'version': '1.0', 'id': this.id})
                this.ws.send(data)
            },

          stop: function(index, id) {
               this.id += 1
               callback = function(data) {
                            app.change_container('exited', index)
                                        }
                this.store[String(this.id)] = callback
                data = JSON.stringify({'method': 'stop_container', 'params': {'id': id} , 'version': '1.0', 'id': this.id})
                console.log(data, 'Send')
                this.ws.send(data)

           },

          remove: function(index, id){
               this.id += 1
               callback = function(data) {
                    app.containers.splice(index,1);
                    }
               this.store[String(this.id)] = callback
               data = JSON.stringify({'method': 'delete_container', 'params': {'id': id} , 'version': '1.0', 'id': this.id})
               this.ws.send(data)
               this.count_containers -= 1

            },
   },

})
