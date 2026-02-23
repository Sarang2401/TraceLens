from mangum import Mangum
from tracelens.api.main import app

handler = Mangum(app)
