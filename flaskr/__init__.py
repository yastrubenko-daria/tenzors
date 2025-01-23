import os
from flask import Flask


app = Flask(__name__, instance_relative_config=True)# папка экземпляра
app.config.from_mapping(
    SECRET_KEY='hello world',
    DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
)

try:
    os.makedirs(app.instance_path)
except OSError:
    pass

from . import db
db.init_app(app)

from . import user
app.register_blueprint(user.bp)

from . import models
from . import tensor
app.register_blueprint(tensor.bp)

#app.add_url_rule('/', endpoint='index')
