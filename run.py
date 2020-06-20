import os.path
from setup import connex_app
from setup import base_dir

connex_app.add_api(os.path.join(base_dir, 'payments', 'payments_spec.yaml'))
connex_app.add_api(os.path.join(base_dir, 'notes', 'notes_spec.yaml'))

if __name__ == '__main__':
    connex_app.run(debug=True, port=3700)

