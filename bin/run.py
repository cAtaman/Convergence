from bin.setup import connex_app

connex_app.add_api('swagger.yaml')

if __name__ == '__main__':
    connex_app.run(debug=True, port=3700)

# todo: rename root folder (app name) to Convergence
#       do so in github too
#       commit everything, move /venv to safe place, rename in github, delete local, mkdir Convergence, git clone
#       copy /venv back
