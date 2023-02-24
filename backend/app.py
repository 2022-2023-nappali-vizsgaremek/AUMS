import imports_app as imp
from create import api, app

from controllers.index_controller import Index
from controllers.user_controller import Register

api.add_resource(Index, '/')
api.add_resource(Register, '/register')

docs = imp.FlaskApiSpec(app)
docs.register(Index)
docs.register(Register)

if __name__ == '__main__':
    #imp.serve(app, host='0.0.0.0', port=5000)
    app.run(debug=True, port=5000, host="0.0.0.0")