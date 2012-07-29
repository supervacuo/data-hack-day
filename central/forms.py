from django import forms

#from central.widgets import BootstrapSplitDateTimeWidget

from central.models import Event, MediaObject, YouTubeVideo, ResponseObject


class AddEventForm(forms.ModelForm):
	class Meta:
		model = Event
		#widgets = {
		#	'start_datetime': forms.SplitDateTimeWidget(
		#		time_attrs={'placeholder': datetime.today().strftime('%T')},
		#		date_attrs={'placeholder': datetime.today().strftime('%d-%m-%Y')}),
		#	'end_datetime': forms.SplitDateTimeWidget(
		#		time_attrs={'placeholder': datetime.today().strftime('%T')},
		#		date_attrs={'placeholder': datetime.today().strftime('%d-%m-%Y')}),
		#}
		widgets = {'start_datetime':
				forms.SplitDateTimeWidget(date_format='%d-%m-%Y', time_format='%H:%M'),
				'end_datetime': forms.SplitDateTimeWidget}

		def clean_end_datetime(self):
			start_datetime = self.cleaned_data['start_datetime']
			end_datetime = self.cleaned_data['end_datetime']

			if start_datetime > end_datetime:
				raise forms.ValidationError('You\'ve said that the event ends before it starts!')

			if start_datetime == end_datetime:
				raise forms.ValidationError('It looks like you\'ve chosen the same date/time for both event start and finish.')


class AddMediaObjectForm(forms.ModelForm):
	class Meta:
		model = MediaObject


class AddYouTubeVideoForm(forms.ModelForm):
	class Meta:
		model = YouTubeVideo
		exclude = ('media_object', 'event')


class AddYouTubeIDForm(forms.Form):
	youtube_id = forms.CharField()


class AddMediaObjectCSVForm(forms.Form):
	csv_file = forms.FileField(label='CSV file',
		help_text=u'''Select a CSV(comma-separated value) file from your computer to
			upload new media objects.''')

	class AddResponseObjectForm(forms.ModelForm):
		class Meta:
			model = ResponseObject
		exclude = ('event',)


class DateRangeForm(forms.Form):
	start = forms.DateTimeField()
	end = forms.DateTimeField()


class AddMediaObjectRSSForm(forms.Form):
	url = forms.URLField(required=False, label='On the web')
	_file = forms.FileField(required=False, label='On your computer')

	def clean(self):
		if self.cleaned_data.get('url') and self.cleaned_data.get('_file'):
			raise forms.ValidationError('Specify either a link or an RSS file, not both')
		if not self.cleaned_data.get('url') and not self.cleaned_data.get('_file'):
			raise forms.ValidationError('You didn\'t provide an RSS file')
		return self.cleaned_data
