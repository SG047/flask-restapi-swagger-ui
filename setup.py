from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from flask import Flask, jsonify, render_template, send_from_directory
from marshmallow import Schema, fields
#import ruamel.yaml

app = Flask(__name__, template_folder='swagger/templates')


@app.route('/')
def hello_world():
    return 'Hello, World'


spec = APISpec(
    title='flask-restapi',
    version='1.0.0',
    openapi_version='3.0.2',
    plugins=[FlaskPlugin(), MarshmallowPlugin()]
)


@app.route('/api/swagger.json')
def create_swagger_spec():
    return jsonify(spec.to_dict())


class TodoResponseSchema(Schema):
    id = fields.Int()
    title = fields.Str()
    status = fields.Boolean()


class TodoListResponseSchema(Schema):
    todo_list = fields.List(fields.Nested(TodoResponseSchema))

class VolumesResponseSchema(Schema):
    name = fields.Str()
    region = fields.Str() #attirbutes in class using marshmallow fileds
    creationToken = fields.Str()
    status = fields.Boolean()

class VolumesListResponseSchema(Schema):
    volumes_list = fields.List(fields.Nested(VolumesResponseSchema)) #nested todo response   



@app.route('/todo')
def todo():
    """Get List of Todo
    ---
    get:
        description: Get List of Todos
        responses:
            200:
                description: Return a todo list
                content:
                    application/json:
                        schema: TodoListResponseSchema
    """

    dummy_data = [{
        'id': 1,
        'title': 'Finish this task',
        'status': False
    }, {
        'id': 2,
        'title': 'Finish that task',
        'status': True
    }]

    return TodoListResponseSchema().dump({'todo_list': dummy_data})


with app.test_request_context():
    spec.path(view=todo)

@app.route('/volumes')
def volumes():
    """Get List of Volumes
    ---
    get:
        description: Get List of Volumes
        tags:
            - volumes
        
        responses:
            200:
                description: Return a Volumes list
                content:
                    application/json:
                        schema: VolumesListResponseSchema
    """

    

    dummy_data = [{
        'region': 'eu-west1',
        'creationtoken': 'test1',
        'status': False,
        'name': 'test'
    
    }]


    def post(self, **kwargs):
        '''
        Get method represents a GET API method
        '''
        return {'message': 'My First Awesome API'}

        
    return VolumesListResponseSchema().dump({'volumes_list': dummy_data})


with app.test_request_context():
    spec.path(view=volumes)



@app.route('/docs')
@app.route('/docs/<path:path>')
def swagger_docs(path=None):
    if not path or path == 'index.html':
        return render_template('index.html', base_url='/docs')
    else:
        return send_from_directory('./swagger/static', path)


#if __name__ == '__main__':
    #app.run(debug=True)
    
    
if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)
    #const port = Process.env.PORT || 5000 
    app.listen(process.env.PORT || 5000)
