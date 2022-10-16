import one_name_shortener

import random
import csv


class NameShortenerCSV:
    """Class that generates the complete, short and very short name of localities contained in a csv file.

    :param input_file_path: Path to the input file
    :type input_file_path: str
    :param output_file_path: Path to the output file
    :type output_file_path: str
    :param column_insee: Index of the INSEE column
    :type column_insee: int
    :param column_original_name: Index of the original_name column
    :type column_original_name: int
    """

    def __init__(self, input_file_path, output_file_path):
        """Constructor method"""
        self.input_file = input_file_path
        self.output_file = output_file_path
        self.column_insee = 0
        self.column_original_name = 3

    def run(self):
        """Reads the input file and writes in the output files.

        This method reads the original_name in the input file and uses the OneProcessor class
        to generate the complete_name, the short_name and the very_short_name. Then it writes
        the results in the output file.
        It also print sample of the results in the console.
        """
        # Reads the input file and writes in the output file
        with open(self.input_file, "r", encoding="utf-8", newline="") as input_csv_file:
            with open(
                self.output_file, "w", encoding="utf-8", newline=""
            ) as output_csv_file:

                csv_reader = csv.reader(input_csv_file)
                csv_writer = csv.writer(output_csv_file)

                num_line = 0

                for row in csv_reader:

                    if num_line == 0:  # Writing column names
                        csv_writer.writerow(
                            ["COM", "NOM_COMPLET", "NOM_COURT", "NOM_TRES_COURT"]
                        )

                        num_line += 1

                    else:  # Writing all the locality names
                        # Recover the original name in the input file
                        original_name = row[self.column_original_name]
                        insee_code = row[self.column_insee]

                        # Generate complete, short and very short names
                        complete_name = one_name_shortener.NameProcessor(
                            original_name
                        ).preprocess_name()

                        short_name = one_name_shortener.NameProcessor(
                            original_name
                        ).get_short_name()

                        very_short_name = one_name_shortener.NameProcessor(
                            original_name
                        ).get_very_short_name()

                        # Write the row
                        csv_writer.writerow(
                            [
                                insee_code,
                                complete_name,
                                short_name,
                                very_short_name,
                            ]
                        )

                        num_line += 1

                    # Print 1 line out of 700
                    if random.randint(1, 700) == 1:
                        print(
                            complete_name.ljust(38),
                            short_name.ljust(23),
                            very_short_name.ljust(15),
                        )
