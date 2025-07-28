from app.interfaces.sensitive_data_checker import SensitiveDataChecker, FlaggedSensitiveData
from typing import List
import re
import asyncio

class SensitiveDataCheckerImpl(SensitiveDataChecker):
    """
    Implementation of the SensitiveDataChecker interface.
    This class is responsible for checking if a given text contains sensitive data.
    """

    async def check(self, text: str) -> List[FlaggedSensitiveData]:
        sd:List[FlaggedSensitiveData] = []
        tasks = [
            self._check_for_ssn(text),
            self._check_for_credit_card(text),
            self._check_for_email(text)
        ]
        reports = await asyncio.gather(*tasks)
        for report in reports:
            if report:
                sd.extend(report)

        return sd


    async def _check_for_ssn(self,text:str):


        ssn_validate_pattern = r"\b(?!666|000|9\d{2})\d{3}-(?!00)\d{2}-(?!0{4})\d{4}\b"  # Adjusted to match SSN format with dashes
        matches = re.finditer(ssn_validate_pattern, text)
        fdl = []
        for match in matches:
            fd = FlaggedSensitiveData(
                text_snippet=match.group(),
                data_type="SSN",
                start_index=match.start(),
                end_index=match.end()
            )
            print(f"Flagged SSN: {fd.text_snippet} at indices {fd.start_index}-{fd.end_index}")
            fdl.append(fd)
        return fdl


    async def _check_for_credit_card(self,text:str) -> List[FlaggedSensitiveData]:
        # Regex pattern for credit card numbers (Visa, MasterCard, American Express, Discover)
        fdl= []
        # Visa: 4[0-9]{12}(?:[0-9]{3})?
        credit_card_pattern = r"\b(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14}|3[47][0-9]{13}|6(?:011|5[0-9]{2})[0-9]{12})\b"
        matches_visa = re.finditer(credit_card_pattern, text)

        # MasterCard: 5[1-5][0-9]{14}
        credit_card_pattern = r"\b(?:5[1-5][0-9]{14})\b"
        matches_mc = re.finditer(credit_card_pattern, text)

        # American Express: 3[47][0-9]{13}
        credit_card_pattern = f"\b(?:3[47][0-9]{{13}})\b"
        matches_amex = re.finditer(credit_card_pattern, text)

        # combined matches
        all_matches = list(matches_visa) + list(matches_mc) + list(matches_amex)
        for match in all_matches:
            fd = FlaggedSensitiveData(
                text_snippet=match.group(),
                data_type="credit_card",
                start_index=match.start(),
                end_index=match.end()
            )
            print(f"Flagged credit card: {fd.text_snippet} at indices {fd.start_index}-{fd.end_index}")
            fdl.append(fd)

        # check for word credit card
        pattern_words = ["credit card","credit card number","cc number", "credit card number is"]
        text_arr = text.split()
        for word in pattern_words:
            if word in text_arr:
                index = text_arr.index(word)
                # Assuming the credit card number follows the word "credit card"
                if index + 1 < len(text_arr):
                    cc_number = text_arr[index + 1]
                    cc_number = cc_number.replace("-", "").replace(".", "")
                    # check if numeric

                    if re.match( r"\b\d{12,19}\b", cc_number):
                        fd = FlaggedSensitiveData(
                            text_snippet=cc_number,
                            data_type="credit_card",
                            start_index=text.index(cc_number),
                            end_index=text.index(cc_number) + len(cc_number)
                        )
                        print(f"Flagged credit card from words: {fd.text_snippet} at indices {fd.start_index}-{fd.end_index}")
                    print(f"Flagged credit card from words: {fd.text_snippet} at indices {fd.start_index}-{fd.end_index}")
                    fdl.append(fd)



        return fdl


    async def _check_for_email(self,text:str):
        # blanket on all emails
        email_regex_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
        matches = re.finditer(email_regex_pattern, text)
        fdl = []
        for match in matches:
            fd = FlaggedSensitiveData(
                text_snippet=match.group(),
                data_type="email",
                start_index=match.start(),
                end_index=match.end()
            )
            print(f"Flagged email: {fd.text_snippet} at indices {fd.start_index}-{fd.end_index}")
            fdl.append(fd)
        return fdl

if __name__ == "__main__":
    import asyncio
    text = "Contact us at abc@bcd.com or visit our website. My SSN is 123-46-6789 and my credit card number is 4111-111111111111."
    checker = SensitiveDataCheckerImpl()
    flagged_data = asyncio.run(checker.check(text))
    for data in flagged_data:
         print(f"Flagged Data: {data.text_snippet}, Type: {data.data_type}, Start: {data.start_index}, End: {data.end_index}")
