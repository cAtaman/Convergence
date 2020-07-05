import os.path
import git
from flask import request
from setup import connex_app, app
from setup import base_dir

connex_app.add_api(os.path.join(base_dir, 'payments', 'payments_spec.yaml'))
connex_app.add_api(os.path.join(base_dir, 'notes', 'notes_spec.yaml'))


@app.route('/update_server', methods=['POST'])
def webhook():
    if request.method == 'POST':
        repo = git.Repo('https://github.com/cAtaman/Convergence')
        origin = repo.remotes.origin
        origin.pull()
        return 'Updated PythonAnywhere successfully', 200
    else:
        return 'Wrong event type', 400


if __name__ == '__main__':
    connex_app.run(debug=True, port=3700)

