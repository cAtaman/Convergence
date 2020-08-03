import os.path
from setup import connex_app
from setup import base_dir

connex_app.add_api(os.path.join(base_dir, 'payments', 'payments_spec.yaml'))
connex_app.add_api(os.path.join(base_dir, 'notes', 'notes_spec.yaml'))

if not os.path.exists(os.path.join(os.path.expanduser('~'), 's3backups')):
    os.makedirs(os.path.join(os.path.expanduser('~'), 's3backups'))
with open(os.path.join(os.path.expanduser('~'), 's3backups', 'working_dir'), 'w') as ff:
    ff.write(os.getcwd())

application = connex_app.app


if __name__ == '__main__':
    application.run(debug=True, port=3700)
