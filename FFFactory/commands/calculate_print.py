import click
from click_option_group import optgroup, RequiredMutuallyExclusiveOptionGroup

from FFFactory.processes.calculate_print import CalculatePrint


@click.group(
    name='calculate_print',
    help='Commands to calculate print'
)
def cli():
    pass


@cli.command()
@optgroup.group(
    'Input data source',
    cls=RequiredMutuallyExclusiveOptionGroup,
    help='The sources of input data'
)
@optgroup.option(
    '-i',
    '--input',
    type=click.Path(exists=True, dir_okay=True),
    help='Input directory with files to calculate print'
)
@optgroup.option(
    '-o',
    '--output',
    type=click.Path(),
    help='Output directory for results'
)
@optgroup.group(
    'Slicer options',
    cls=RequiredMutuallyExclusiveOptionGroup,
    help='The slicer options'
)
@optgroup.option(
    '-c',
    '--slicer-config',
    type=click.Path(exists=True, dir_okay=False),
    help='Slicer configuration file'
)
@optgroup.option(
    '-s',
    '--scale',
    flag=True,
    default=False,
    help='Scale the print of the 10-120cm',
)
def calculate_print() -> None:
    calculator = CalculatePrint(self.input_dir, self.output_dir, self.writer)

