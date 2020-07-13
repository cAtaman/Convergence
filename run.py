import os.path
from setup import connex_app
from setup import base_dir

connex_app.add_api(os.path.join(base_dir, 'payments', 'payments_spec.yaml'))
connex_app.add_api(os.path.join(base_dir, 'notes', 'notes_spec.yaml'))
application = connex_app.app

if __name__ == '__main__':
<<<<<<< HEAD
    connex_app.run(debug=True, port=3700)
=======
    application.run(debug=True, port=3700)

>>>>>>> 40d2841371adf9a5f9c6ad81d1b42de48f80b039
