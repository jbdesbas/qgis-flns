import one_name_shortener
import csv_name_shortener

import click


@click.group()
def csv_file():
    pass


@csv_file.command()
def run_csv():
    """Command that processes a csv file of locality names"""

    click.echo("")
    input = click.prompt(
        "Please enter the input file path", type=click.Path(exists=True)
    )
    output = click.prompt(
        "Please enter the output file path", type=click.Path(exists=False)
    )
    input_file_path = click.format_filename(input, shorten=False)
    output_file_path = click.format_filename(output, shorten=False)

    print("")
    print("--------- Lancement du script ---------")
    print("")

    simplifier = csv_name_shortener.NameShortenerCSV(input_file_path, output_file_path)
    simplifier.run()

    print("")
    print("--------- Script achevé avec succès ---------")
    print("")


@click.group()
def one_name():
    pass


@one_name.command()
def run_one_name():
    """Command that processes only one locality name"""

    original_name = click.prompt("Please enter the locality name", type=str)

    click.echo(f"Original name: {original_name}")
    complete_name = one_name_shortener.NameProcessor(original_name).preprocess_name()
    click.echo(f"Complete name: {complete_name}")
    short_name = one_name_shortener.NameProcessor(original_name).get_short_name()
    click.echo(f"Short name: {short_name}")
    very_short_name = one_name_shortener.NameProcessor(
        original_name
    ).get_very_short_name()
    click.echo(f"Very short name: {very_short_name}")


cli = click.CommandCollection(sources=[csv_file, one_name])


if __name__ == "__main__":
    cli()
