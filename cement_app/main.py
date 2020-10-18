from cement import App
from .controllers.base_controller import BaseController
from .controllers.exercises_controller import ExercisesController
from .controllers.charts_controller import ChartsController


class CementApp(App):
    class Meta:
        label = 'cement_app'

        # Use views directory for output templates
        # https://docs.builtoncement.com/extensions/jinja2#application-meta-options
        extensions = ['jinja2']
        output_handler = 'jinja2'
        template_dir = './cement_app/views'

        handlers = [BaseController, ExercisesController, ChartsController]
