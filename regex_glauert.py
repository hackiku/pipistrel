    def regex_fortran(output):
        import re

        # Part a) Extracting coefficients
        coefficient_text = """
        KOEFICIJENT UZGONA KRILA            Cz = {cz_regex}
        KOEF. INDUKOVANOG OTPORA KRILA      Cxi = {cxi_regex}
        Popravni faktor indukovanog otpora  delta = {delta_regex}
        GRADIJENT UZGONA KRILA              a =  {a_regex} [1/o]
        aerodinamicki napadni ugao krila    AlfaA =   {alfaa_regex} [o]
        aerodinamicki nap. ugao u korenu    AlfaAs=   {alfaas_regex} [o]
        GEOMETRIJSKI NAPADNI UGAO KRILA     Alfa  =   {alfa_regex} [o]
        UGAO NULTOG UZGONA KRILA            AlfaN =  {alfan_regex} [o]
        """

        # Replace placeholders with regex for number extraction
        regex_template = coefficient_text.format(
            cz_regex=r"(-?\d+\.\d+)",
            cxi_regex=r"(-?\d+\.\d+)",
            delta_regex=r"(-?\d+\.\d+)",
            a_regex=r"(-?\d+\.\d+)",
            alfaa_regex=r"(-?\d+\.\d+)",
            alfaas_regex=r"(-?\d+\.\d+)",
            alfa_regex=r"(-?\d+\.\d+)",
            alfan_regex=r"(-?\d+\.\d+)"
        )
        
        coefficients = {}
        for line in regex_template.strip().split('\n'):
            key, regex = line.strip().split()[:2]
            match = re.search(regex, output)
            if match:
                coefficients[key] = float(match.group(1))
            else:
                print(f"No match found for key: {key}")  # Debugging line

            return coefficients
