import subprocess

from behave import given, then, when
from behave.runner import Context


@given('maximum number of bus stops driven is {max_driven_bus_stop_count:d}')
def step_impl(context: Context, max_driven_bus_stop_count: int):
    context.max_driven_bus_stop_count = max_driven_bus_stop_count


@given('bus drivers with the following routes and rumors')
def step_impl2(context: Context):
    context.drivers = []

    for driver in context.table:
        bus_route = ','.join(
            bus_stop.strip() for bus_stop in driver['Route'].split(',')
        )

        rumors = ','.join(
            rumor.strip() for rumor in driver['Rumors'].split(',')
        )

        context.drivers.append(f'{bus_route};{rumors}')


@when('bus drivers have completed driving')
def step_impl3(context: Context):
    context.exit_code = subprocess.run(
        [
            'python',
            'main.py',
            str(context.max_driven_bus_stop_count),
            *context.drivers,
        ],
    ).returncode


@then('all rumors are successfully shared')
def step_impl4(context: Context):
    assert context.exit_code == 0


@then('all rumors are not shared')
def step_impl5(context: Context):
    assert context.exit_code != 0
