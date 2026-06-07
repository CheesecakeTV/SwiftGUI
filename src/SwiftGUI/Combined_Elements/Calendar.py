from typing import Callable, Iterable, Hashable, Any
import SwiftGUI as sg
from SwiftGUI.Compat import Self
from datetime import datetime as dt
from datetime import date as dt_date
import calendar


class Calendar(sg.BaseCombinedElement):
    defaults = sg.GlobalOptions.Calendar

    def __init__(
            self,
            default_value: dt_date = None,
            *,
            key: Hashable = None,
            key_function: Callable | Iterable[Callable] = None,
            default_event: bool = False,

            default_month: int = None,
            default_year: int = None,

            disabled: bool = None,
            allow_month_selection: bool = None,
            today_selects: bool = None,

            monthnames: Iterable[str] = None,
            daynames: Iterable[str] = None,
            week_starts_on_sunday: bool = None,

            today_background_color: sg.Color | str = None,
            background_color_active: sg.Color | str = None,
            text_color_active: sg.Color | str = None,
    ):
        """
        Lets the user select a certain day on a graphical calendar

        :param default_value: The date selected from the start
        :param key:
        :param key_function:
        :param default_event: Causes an event when the selected date CHANGES. Clicking the selected date again does nothing.
        :param default_month: Month to be visible from the start
        :param default_year: Year to be visible from the start
        :param disabled: True to ignore all day-selections
        :param allow_month_selection: False, to disable all elements the user could use to change the month
        :param monthnames: A list of all month-names. Has to include all 12 month.
        :param daynames: The names of weekdays written above the day-buttons. FIRST DAY MUST BE MONDAY.
        :param week_starts_on_sunday: True, if the week should start at sunday instead of monday
        :param today_background_color: Background-color of the day-button corresponding to the current day
        :param background_color_active: Background-color of the selected day-button
        :param text_color_active: Text-color of the selected day-button
        :param today_selects: True, if the "today"-button should also select "today"
        """
        today = dt_date.today()

        self._weekButtons: list[list[sg.Button]] = list()
        self._weekTexts: list[sg.Text] = list()

        monthnames = list(self.defaults.single("monthnames", monthnames))
        self._monthnames = monthnames

        self._today_button_color = None
        self._active_button_color = None
        self._active_text_color = None

        week_starts_on_sunday = self.defaults.single("week_starts_on_sunday", week_starts_on_sunday)
        self._start_on_sunday = week_starts_on_sunday
        today_selects = self.defaults.single("today_selects", today_selects)

        calendar.setfirstweekday(6 if week_starts_on_sunday else 0)  # 6 Sunday, 0 Monday

        layout = [
            [
                month_combo := sg.ComboboxMapping(
                    dict(zip(monthnames, range(1, 13))),
                    key_function= lambda val: self.see_month(val),
                    default_event=True,
                    expand=True,
                    justify= "center",
                ),
            ],[
                year_spinbox := sg.Spinbox(
                    default_value= 0,
                    increment=1,
                    value_type= int,
                    number_min=0,
                    number_max=10000,
                    default_event=True,
                    key_function= lambda val: self.see_month(year=val),
                    expand=True,
                    justify= "center",
                )
            ], today_list := [
                sg.Button(
                    "◄",
                    key_function= self.see_prior_month,
                    width=2,
                ),
                sg.Button(
                    "Today",
                    key_function= self.select_today if today_selects else self.see_today,
                    expand=True,
                ),
                sg.Button(
                    "►",
                    key_function=self.see_next_month,
                    width=2,
                ),
            ], [
                sg.Spacer(height=5),
            ], [
                sg.GridFrame([
                    [
                            sg.T(),
                            *self._getDayHeaders(week_starts_on_sunday, texts=tuple(self.defaults.single("daynames", daynames))),
                        ],
                        *[self._getButtonRow() for _ in range(6)],
                    ]
                )
            ]
        ]

        # All elements that should be disabled when allow_month_selection = false
        self._month_selection_buttons = today_list

        self._month_selection_combobox = month_combo
        self._year_selection_spinbox = year_spinbox

        self._disabled = None   # If the selection of days is allowed

        super().__init__(
            layout,
            default_event=default_event,
            key=key,
            key_function=key_function,
        )

        self._update_initial(
            allow_month_selection = allow_month_selection,
            disabled = disabled,
            today_background_color = today_background_color,
            background_color_active = background_color_active,
            text_color_active = text_color_active,
        )

        self._selected_month: dt_date = today
        self._selected_day: dt_date | None = None

        self.set_value(default_value)

        if default_month:
            self.see_month(default_month, default_year)
        elif default_year:
            self.see_month(year=default_year)
        else:
            self.see_month(self._selected_month.month)

    def _update_special_key(self,key:str,new_val:Any) -> bool|None:
        match key:
            case "allow_month_selection":
                for elem in self._month_selection_buttons:
                    elem.update_after_window_creation(disabled = not new_val)
                self._month_selection_combobox.update_after_window_creation(disabled = not new_val)
                self._year_selection_spinbox.update_after_window_creation(state = "normal" if new_val else "disabled")

            case "disabled":
                self._disabled = new_val

            case "today_background_color":
                self._today_button_color = new_val
            case "background_color_active":
                self._active_button_color = new_val
            case "text_color_active":
                self._active_text_color = new_val

            case _:
                return super()._update_special_key(key, new_val)

        return True

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
            texts: tuple[str, ...] = ("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"),
    ) -> list[sg.Text]:
        """
        Return the texts on top of the calendar.
        :param startAtSunday: True, if the last element of the passed texts should actually be the first one
        :return:
        """

        if startAtSunday:
            texts = [texts[-1]] + list(texts[:-1])

        return [
            sg.T(text) for text in texts
        ]

    @staticmethod
    def _apply_day_to_button(day: int, button: sg.Button, mark_background: sg.Color = None, mark_text: sg.Color = None, out_of_month: bool = False):
        """
        Write a day-number onto a button.

        :param day: If day is 0, this method does nothing
        :param button:
        :param out_of_month: True, if the button is not in the current month
        :param mark_background: Pass this to change the background-color of the button (if part of the month). Otherwise, it is reset
        :param mark_text: Pass this to change the text-color. Otherwise, it's reset
        :return:
        """
        if not day:
            return

        button.value = day

        if mark_background is None:
            button.update_to_default_value("background_color")
        elif not out_of_month:
            button.update(background_color = mark_background)

        if mark_text is None:
            button.update_to_default_value("text_color")
        else:
            button.update(text_color = mark_text)

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
        date = dt_date(year, month, day)

        if self._start_on_sunday:
            num = int(date.strftime("%U")) + 1   # If you have a problem with this line, feel free to consult your diary about it. If your week starts on Sunday, you deserve performance disadvantages
        else:
            num = date.isocalendar().week

        return num

    visible_month: int
    @property
    def visible_month(self) -> int:
        """Which month is currently visible"""
        return self._selected_month.month

    @visible_month.setter
    def visible_month(self, new_val: int):
        self.see_month(new_val)

    visible_year: int
    @property
    def visible_year(self) -> int:
        """Which year is currently visible"""
        return self._selected_month.year

    @visible_year.setter
    def visible_year(self, new_val: int):
        """Which year is currently visible"""
        self.see_month(year= new_val)

    @sg.BaseCombinedElement._run_after_window_creation
    def see_day(self, day: dt_date) -> Self:
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
        # But yeah, I am going to improve it eventually.

        # Todo: Clean this mess up

        if not month:
            month = self._selected_month.month

        if year is None or year > 10000:
            year = self._selected_month.year

        if year == 0:
            return self

        # if month == self._selected_month.month and year == self._selected_month.year:
        #     return self

        self._month_selection_combobox.value = self._monthnames[month - 1]
        self._year_selection_spinbox.value = year

        self._selected_month = dt_date(year, month, 1)

        today = dt_date.today()
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
                    bg_color = None
                    text_color = None

                    if today_in_month and day == today.day: # Test if the button is today
                        bg_color = self._today_button_color

                    if selection_in_month and day == self._selected_day.day: # Test if the button is selected
                        bg_color = self._active_button_color
                        text_color = self._active_text_color

                    self._apply_day_to_button(day, button, mark_background=bg_color, mark_text=text_color)
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

    def see_next_month(self) -> Self:
        """
        Quick way to view (see) the next month instead of manually incrementing it by 1.
        :return:
        """
        next_month = self.visible_month + 1

        if next_month < 13:
            self.see_month(next_month)
        else:
            self.see_month(1, self.visible_year + 1)

        return self

    def see_prior_month(self) -> Self:
        """
        Quick way to view (see) the previous month instead of manually decrementing it by 1.
        :return:
        """
        prior_month = self.visible_month - 1

        if prior_month > 0:
            self.see_month(prior_month)
        else:
            self.see_month(12, self.visible_year - 1)

        return self

    def select_today(self, see_today: bool = True) -> Self:
        today = dt_date.today()
        self.set_value(today)

        if see_today:
            self.see_today()

        self.done(today)
        return self

    def see_today(self) -> Self:
        """
        View the current month
        :return:
        """
        self.see_day(dt_date.today())
        return self

    def see_selected_day(self) -> Self:
        """
        View the selected month
        :return:
        """
        if self._selected_day is not None:
            self.see_day(self._selected_day)
        return self

    value: dt_date | None
    def _get_value(self) -> dt_date | None:
        return self._selected_day

    def set_value(self, val: dt_date | None) -> Self:

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
            self.set_value(dt.strptime(val, self._json_string_format).date())
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
        if self._disabled:
            return

        val = int(val)

        new_dt = self._selected_month.replace(day=val)

        if new_dt != self.value:
            self.value = new_dt
            self.throw_default_event()

        self.done(self.value)

    def popup(self, **window_kwargs) -> dt_date | None:
        return super().popup(**window_kwargs)

