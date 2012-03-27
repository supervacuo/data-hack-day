from django import forms

from bootstrap_toolkit.widgets import BootstrapDateInput


class BootstrapSplitDateTimeWidget(forms.MultiWidget):

	def __init__(self, date_attrs=None, time_attrs=None, date_format=None, time_format=None):
		widgets = (
			BootstrapDateInput(attrs=date_attrs),
			forms.TimeInput(attrs=time_attrs),)
		super(BootstrapSplitDateTimeWidget, self).__init__(widgets, None)

	def decompress(self, value):
		if value:
			value = forms.util.to_current_timezone(value)
			return [value.time().replace(microsecond=0), value.date()]
		return [None, None]
