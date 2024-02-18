import re


class LineMessageParser:
    def parse_breast_milk_record(self, data):
        time = self.extract_timeformat(data)
        cc = self.extract_cc(data)
        return time, cc

    def extract_timeformat(self, data):
        # attempt to match time range
        time_match_range = re.search(
            r'(\d{1,2}:?\d{2})\s*-\s*(\d{1,2}:?\d{2})', data)
        if time_match_range:
            start_time, end_time = time_match_range.group(1, 2)
            # 格式化時間
            start_time_formatted = self.__format_time(start_time)
            end_time_formatted = self.__format_time(end_time)
            return f"{start_time_formatted}-{end_time_formatted}"

        # attempt to match single time
        time_match_single = re.search(r'(\d{1,2}:?\d{2})', data)
        if time_match_single:
            time = time_match_single.group(1)
            return f"{self.__format_time(time)}"

        raise ValueError("The time format is not correct")

    def __format_time(self, time_str):
        """Format the time string to HH:MM format."""
        if ':' in time_str:
            return time_str  # string is HH:MM format
        elif len(time_str) == 4:
            return f"{time_str[:2]}:{time_str[2:]}"
        elif len(time_str) == 3:
            return f"0{time_str[0]}:{time_str[1:]}"
        else:
            raise ValueError("Invalid time format")

    def extract_cc(self, data):
        # Check for correct time range format
        time_range_pattern = re.compile(
            r'^\d{1,2}:?\d{2}\s*-\s*\d{1,2}:?\d{2}\s*$')
        if time_range_pattern.match(data):
            raise ValueError(
                "Time range format is correct, but this method is for extracting cc")

        # Check for simple time format without "cc", raise error as before
        if re.match(r'^\d{1,2}:?\d{2}\s*$', data):
            raise ValueError("The cc format is not correct")

        # check match cc
        cc_pattern = re.compile(r'(\d+)\s*(cc)?\s*$', re.IGNORECASE)
        cc_match = cc_pattern.search(data)
        if cc_match:
            cc_amount = cc_match.group(1)
            return int(cc_amount)

        raise ValueError("The cc format is not correct")
