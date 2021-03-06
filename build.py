from pybuilder.core import init, use_plugin

use_plugin("python.core")
use_plugin("python.unittest")
use_plugin("python.install_dependencies")
use_plugin("python.flake8")
use_plugin("python.coverage")
use_plugin("python.distutils")
use_plugin("python.pycharm")

name = "grapple"
version = "0.0.1"
default_task = ["clean", "analyze", "publish"]


@init
def set_properties(project):
    project.set_property("flake8_break_build", True)  # default is False
    project.set_property("flake8_verbose_output", True)  # default is False
    project.set_property("flake8_radon_max", 10)  # default is None
    project.set_property_if_unset("flake8_max_complexity", 10)  # default is None
    # Complexity: <= 10 is easy, <= 20 is complex, <= 50 great difficulty, > 50 unmaintainable

    project.set_property("coverage_break_build", True)  # default is False
    project.set_property("coverage_allow_non_imported_modules", False)  # default is True
    project.set_property("coverage_exceptions", [
        '__init__', 'temple',
        'grapple.parsing.temp', 'grapple.parsing.temp.grammar',
        'grapple.parsing.temp.support2', 'grapple.parsing.temp.support',
        'grapple.parsing.temp.visitors', 'grapple.parsing.temp.peg_peg',
        'temple.return_body', 'temple.where'])

    project.set_property("dir_source_unittest_python", "src/test/python")

    project.depends_on("assertpy")
    project.depends_on("overloading")
    project.depends_on("coloredlogs")
    project.depends_on("verboselogs")
    project.depends_on_requirements("requirements.txt")
