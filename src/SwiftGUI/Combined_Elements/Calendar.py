from typing import Callable, Iterable, Hashable
import SwiftGUI as sg
from SwiftGUI.Compat import Self
from datetime import datetime as dt
import calendar


class Calendar(sg.BaseCombinedElement):

    def __init__(
            self,
            *,
            key: Hashable = None,
            key_function: Callable | Iterable[Callable] = None,
            default_event: bool = False,

            week_starts_on_sunday: bool = False,
            today_button_color: sg.Color | str = "darkblue",
            active_button_color: sg.Color | str = "darkred",
    ):
        self._weekButtons: list[list[sg.Button]] = list()
        self._weekTexts: list[sg.Text] = list()

        self._today_button_color = today_button_color
        self._active_button_color = active_button_color

        self._start_on_sunday = week_starts_on_sunday

        self._selected_day: dt | None = None
        self._selected_month: dt = dt.now()

        calendar.setfirstweekday(6 if week_starts_on_sunday else 0)  # 6 Sunday, 0 Monday

        layout = [
            [
                sg.T(),
                *self._getDayHeaders(week_starts_on_sunday),
            ],
            *[self._getButtonRow() for _ in range(6)],
        ]

        super().__init__(
            sg.GridFrame(layout),
            default_event=default_event,
            key=key,
            key_function=key_function,
        )

        self.see_month(self._selected_month.month)

    def _getButtonRow(self) -> list[sg.BaseElement]:
        """
        Make and return a whole row of buttons.
        :return:
        """
        text = sg.Text(width=3, anchor="center")
        self._weekTexts.append(text)
        row = []

        for i in range(7):
            button = sg.Button(
                width=3,
                key_function= self._dayClicked,
            )
            row.append(button)

        self._weekButtons.append(row)

        return [text] + row

    @staticmethod
    def _getDayHeaders(
            startAtSunday: bool = False,
            texts: tuple[str] = ("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"),
    ) -> list[sg.Text]:
        """
        Return the texts on top of the calendar.
        :param startAtSunday: True, if the last element of
        :return:
        """

        if startAtSunday:
            texts = [texts[-1]] + list(texts[:-1])

        return [
            sg.T(text) for text in texts
        ]

    def _apply_day_to_button(self, day: int, button: sg.Button, mark_background: sg.Color = None, out_of_month: bool = False):
        """
        Write a day-number onto a button.

        :param day: If day is 0, this method does nothing
        :param button:
        :param out_of_month: True, if the button is not in the current month
        :param mark_background: Pass this to change the background-color of the button (if part of the month). Otherwise, it is reset
        :return:
        """
        if not day:
            return

        button.value = day

        if mark_background is None:
            button.update_to_default_value("background_color")
        else:
            if not out_of_month:
                button.update(background_color = mark_background)

        button.update(disabled= out_of_month)

    @staticmethod
    def _get_prev_month_calendar(year: int, month: int) -> list[list[int]]:
        """

        :param year:
        :param month:
        :return:
        """
        if month > 1:
            prev_month = calendar.monthcalendar(year, month - 1)
        else:
            prev_month = calendar.monthcalendar(year - 1, month=12)

        return prev_month

    def get_weeknumber(self, day: int, month: int, year: int) -> int:
        """
        Returns the weeknumber of the specified day
        :param day:
        :param month:
        :param year:
        :return:
        """
        date = dt(year, month, day)

        if self._start_on_sunday:
            num = int(date.strftime("%U")) + 1   # If you have a problem with this line, feel free to consult your diary about it. If your week starts on Sunday, you deserve performance disadvantages
        else:
            num = date.isocalendar().week

        return num

    @property
    def visible_month(self) -> int:
        """Which month is currently visible"""
        return self._selected_month.month

    @property
    def visible_year(self) -> int:
        """Which month is currently visible"""
        return self._selected_month.year

    @sg.BaseCombinedElement._run_after_window_creation
    def see_day(self, day: dt) -> Self:
        """
        See the month containing this day
        :param day:
        :return:
        """
        self.see_month(day.month, day.year)
        return self

    @sg.BaseCombinedElement._run_after_window_creation
    def see_month(self, month: int = None, year: int = None) -> Self:
        """
        Show a certain month in the calendar

        :param month: Leave empty to re-open the current month
        :param year: Year that month is in. Leave empty for current year
        :return:
        """
        # I know this function looks HORRIBLE.
        # That's because working with dates is horrible.
        # Critique it all you want but it works quite reliable.

        if year is None:
            year = self._selected_month.year

        self._selected_month = dt(year, month, 1)

        today = dt.now()
        today_in_month = today.month == month and today.year == year

        selection_in_month = self._selected_day is not None and self._selected_day.month == month and self._selected_day.year == year

        prev_week = self._get_prev_month_calendar(year, month)[-1]
        current_month = calendar.monthcalendar(year, month)

        for day, button in zip(prev_week, self._weekButtons[0]):
            if not day:
                break

            self._apply_day_to_button(day, button, out_of_month=True)
        else:
            # If the first row is already full, make sure to push the other days
            current_month = [[]] + current_month
            self._weekTexts[0].value = ""

        self._weekTexts[-1].value = ""  # This might be overwritten later

        future_day = 0
        reached_start_of_month = False
        for n, row in enumerate(self._weekButtons):
            refreshed_weeknumber = False

            if n < len(current_month):
                days = current_month[n]
            else:
                days = [0] * 7

            for day, button in zip(days, row):
                if day:
                    color = None

                    if today_in_month and day == today.day: # Test if the button is today
                        color = self._today_button_color

                    if selection_in_month and day == self._selected_day.day: # Test if the button is selected
                        color = self._active_button_color

                    self._apply_day_to_button(day, button, mark_background=color)
                    reached_start_of_month = True

                    if not refreshed_weeknumber:
                        refreshed_weeknumber = True
                        self._weekTexts[n].value = self.get_weeknumber(day, month, year)

                elif reached_start_of_month:
                    # If this month has no more days
                    future_day += 1
                    self._apply_day_to_button(future_day, button, out_of_month=True)

        # Datetime immer um 1d erhöhen

        return self

    def see_next_month(self):
        """
        Quick way to view (see) the next month instead of manually incrementing it by 1.
        :return:
        """
        next_month = self.visible_month + 1

        if next_month < 13:
            self.see_month(next_month)
        else:
            self.see_month(1, self.visible_year + 1)

    def see_prior_month(self):
        """
        Quick way to view (see) the previous month instead of manually decrementing it by 1.
        :return:
        """
        prior_month = self.visible_month - 1

        if prior_month > 0:
            self.see_month(prior_month)
        else:
            self.see_month(12, self.visible_year - 1)

    def _get_value(self) -> dt | None:
        return self._selected_day

    def set_value(self, val: dt | None) -> Self:

        update_necessary = self._selected_day and self._selected_month.month == self._selected_day.month

        if val is None:
            self._selected_day = val
        else:
            self._selected_day = val
            self._selected_month = val
            update_necessary = True

        if update_necessary:
            self.see_month(self._selected_month.month)

        return self

    _json_string_format = "%Y-%m-%d"
    def to_json(self) -> str | None:
        if self._selected_day is None:
            return None

        return self._selected_day.strftime(self._json_string_format)

    def from_json(self, val: str | None) -> Self:
        if val:
            self.set_value(dt.strptime(val, self._json_string_format))
        else:
            self.set_value(None)

        return self

    def _dayClicked(self, val: str | int):
        """
        Key-function.
        When one of the buttons is clicked, its val (the day-number) is passed to this function
        :param val:
        :return:
        """
        val = int(val)

        new_dt = self._selected_month.replace(day=val)

        if new_dt != self.value:
            self.value = new_dt
            self.throw_default_event()
