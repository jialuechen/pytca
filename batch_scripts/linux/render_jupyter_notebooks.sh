# Note that on some instances of Linux this may not fetch the required directory (it has been tested with RedHat)
export SCRIPT_FOLDER="$( dirname "$(readlink -f -- "$0")" )"
source $SCRIPT_FOLDER/installation/set_pytca_env_vars.sh

echo 'Batch folder' $SCRIPT_FOLDER
echo 'Cuemacro pytca' $pytca_CUEMACRO

# Set Python environment
source $SCRIPT_FOLDER/installation/activate_python_environment.sh

cd $pytca_CUEMACRO/pytca_notebooks
jupyter nbconvert --to html *.ipynb