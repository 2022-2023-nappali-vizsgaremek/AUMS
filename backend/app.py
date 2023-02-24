import imports_app as imp
from create import api, app

from controllers.index_controller import Index
from controllers.user_controller import Register

#app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:@localhost:3306/aums"
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:root@mysql_aums:3306/aums"

api.add_resource(Index, '/')
api.add_resource(Register, '/register')

docs = imp.FlaskApiSpec(app)
docs.register(Register)
docs.register(Index)

if __name__ == '__main__':
    #imp.serve(app, host='0.0.0.0', port=5000)
    app.run(debug=True, port=5000, host="0.0.0.0")